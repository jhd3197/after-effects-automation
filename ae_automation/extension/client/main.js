/**
 * AE Automation Chat Panel
 * Communicates with Python Flask backend for AI chat + AE control
 */

(function () {
    "use strict";

    // ── State ──────────────────────────────────────────────────
    var csInterface = null;
    var settings = {
        backendUrl: "http://localhost:5001",
        model: "openai/gpt-4o",
    };
    var pendingActions = [];
    var chatHistory = [];
    var isConnected = false;

    // ── Init ───────────────────────────────────────────────────
    function init() {
        // Try to init CSInterface (only works inside AE)
        try {
            csInterface = new CSInterface();
        } catch (e) {
            console.log("CSInterface not available — running outside AE");
            csInterface = null;
        }

        loadSettings();
        bindEvents();
        checkConnection();

        // Poll connection status every 15s
        setInterval(checkConnection, 15000);
    }

    // ── Settings ───────────────────────────────────────────────
    function loadSettings() {
        try {
            var saved = localStorage.getItem("ae_chat_settings");
            if (saved) {
                var parsed = JSON.parse(saved);
                settings.backendUrl = parsed.backendUrl || settings.backendUrl;
                settings.model = parsed.model || settings.model;
            }
        } catch (e) {}

        document.getElementById("backendUrl").value = settings.backendUrl;
        document.getElementById("modelSelect").value = settings.model;
    }

    function saveSettings() {
        settings.backendUrl = document.getElementById("backendUrl").value.replace(/\/+$/, "");
        settings.model = document.getElementById("modelSelect").value;
        localStorage.setItem("ae_chat_settings", JSON.stringify(settings));
        toggleSettings();
        checkConnection();
    }

    function toggleSettings() {
        var panel = document.getElementById("settingsPanel");
        panel.classList.toggle("hidden");
    }

    // ── Connection ─────────────────────────────────────────────
    function checkConnection() {
        var dot = document.getElementById("statusDot");
        dot.className = "status-dot connecting";
        dot.title = "Connecting...";

        fetch(settings.backendUrl + "/api/chat/status", { method: "GET" })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                isConnected = true;
                dot.className = "status-dot online";
                dot.title = "Connected to backend";
            })
            .catch(function () {
                isConnected = false;
                dot.className = "status-dot offline";
                dot.title = "Backend offline — start with: ae-automation chat";
            });
    }

    // ── Events ─────────────────────────────────────────────────
    function bindEvents() {
        document.getElementById("sendBtn").addEventListener("click", sendMessage);
        document.getElementById("settingsBtn").addEventListener("click", toggleSettings);
        document.getElementById("saveSettings").addEventListener("click", saveSettings);
        document.getElementById("executeActions").addEventListener("click", executeAllActions);
        document.getElementById("dismissActions").addEventListener("click", dismissActions);

        var input = document.getElementById("userInput");
        input.addEventListener("keydown", function (e) {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // Auto-resize textarea
        input.addEventListener("input", function () {
            this.style.height = "auto";
            this.style.height = Math.min(this.scrollHeight, 100) + "px";
        });
    }

    // ── Chat ───────────────────────────────────────────────────
    function sendMessage() {
        var input = document.getElementById("userInput");
        var text = input.value.trim();
        if (!text) return;

        // Add user message to UI
        addMessage("user", text);
        chatHistory.push({ role: "user", content: text });

        input.value = "";
        input.style.height = "auto";

        if (!isConnected) {
            addMessage("system", "Backend is offline. Start it with:\nae-automation chat");
            return;
        }

        // Show typing indicator
        var typingEl = showTyping();

        // Gather AE project context if available
        getProjectContext(function (context) {
            var payload = {
                message: text,
                history: chatHistory.slice(-20), // last 20 messages for context
                model: settings.model,
                ae_context: context,
            };

            fetch(settings.backendUrl + "/api/chat/message", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    removeTyping(typingEl);

                    if (data.success) {
                        var msgEl = addMessage("assistant", data.response);
                        chatHistory.push({ role: "assistant", content: data.response });

                        // Handle actions
                        if (data.actions && data.actions.length > 0) {
                            showActionBadges(msgEl, data.actions);
                            pendingActions = pendingActions.concat(data.actions);
                            updateActionsBar();
                        }
                    } else {
                        addMessage("system", "Error: " + (data.error || "Unknown error"));
                    }
                })
                .catch(function (err) {
                    removeTyping(typingEl);
                    addMessage("system", "Connection error: " + err.message);
                    isConnected = false;
                    checkConnection();
                });
        });
    }

    // ── AE Context ─────────────────────────────────────────────
    function getProjectContext(callback) {
        if (!csInterface) {
            callback(null);
            return;
        }

        csInterface.evalScript("getProjectInfo()", function (result) {
            try {
                callback(JSON.parse(result));
            } catch (e) {
                callback(null);
            }
        });
    }

    // ── Execute AE Actions ─────────────────────────────────────
    function executeAction(action, badgeEl) {
        if (!csInterface || action.type === "render") {
            // Fallback: send to backend for execution via command queue
            fetch(settings.backendUrl + "/api/chat/execute", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: action }),
            })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    if (data.success) {
                        if (badgeEl) badgeEl.classList.add("executed");
                        // Start polling render progress for render actions
                        if (action.type === "render") {
                            startRenderProgressPoll();
                        }
                    } else {
                        if (badgeEl) badgeEl.classList.add("failed");
                        addMessage("system", "Action failed: " + (data.error || "Unknown"));
                    }
                })
                .catch(function (err) {
                    if (badgeEl) badgeEl.classList.add("failed");
                });
            return;
        }

        // Execute directly in AE via ExtendScript
        var script = actionToExtendScript(action);
        if (script) {
            csInterface.evalScript(script, function (result) {
                if (result === "EvalScript error.") {
                    if (badgeEl) badgeEl.classList.add("failed");
                    addMessage("system", "ExtendScript error for: " + action.type);
                } else {
                    if (badgeEl) badgeEl.classList.add("executed");
                }
            });
        }
    }

    function executeAllActions() {
        var badges = document.querySelectorAll(".action-badge:not(.executed):not(.failed)");
        for (var i = 0; i < pendingActions.length; i++) {
            executeAction(pendingActions[i], badges[i] || null);
        }
        pendingActions = [];
        updateActionsBar();
    }

    function dismissActions() {
        pendingActions = [];
        updateActionsBar();
    }

    // ── Action → ExtendScript ──────────────────────────────────
    function actionToExtendScript(action) {
        var type = action.type;
        var p = action.params || {};

        switch (type) {
            case "create_comp":
                return 'createComp("' + esc(p.name) + '", ' +
                    (p.width || 1920) + ', ' + (p.height || 1080) + ', ' +
                    (p.duration || 10) + ', ' + (p.fps || 30) + ')';

            case "edit_text":
                return 'editLayerText("' + esc(p.comp_name) + '", "' +
                    esc(p.layer_name) + '", "' + esc(p.value) + '")';

            case "edit_property":
                return 'editLayerProperty("' + esc(p.comp_name) + '", "' +
                    esc(p.layer_name) + '", "' + esc(p.property) + '", "' +
                    esc(p.value) + '")';

            case "set_color":
                return 'setLayerColor("' + esc(p.comp_name) + '", "' +
                    esc(p.layer_name) + '", "' + esc(p.property) + '", "' +
                    esc(p.hex) + '")';

            case "add_marker":
                return 'addMarkerToLayer("' + esc(p.comp_name) + '", "' +
                    esc(p.layer_name) + '", "' + esc(p.name) + '", ' +
                    (p.time || 0) + ')';

            case "save_project":
                return 'saveProject()';

            case "get_project_info":
                return 'getProjectInfo()';

            case "list_comps":
                return 'listCompositions()';

            case "render":
                // Rendering is handled by the backend; no ExtendScript needed
                return null;

            default:
                return null;
        }
    }

    function esc(str) {
        if (!str) return "";
        str = String(str);
        // Sanitize <br> tags to AE carriage returns before escaping
        str = str.replace(/<br\s*\/?>/gi, "\\r");
        // Escape all special characters to prevent ExtendScript injection
        str = str.replace(/\\/g, "\\\\");
        str = str.replace(/"/g, '\\"');
        str = str.replace(/\n/g, "\\n");
        str = str.replace(/\r/g, "\\r");
        str = str.replace(/\t/g, "\\t");
        str = str.replace(/\0/g, "");
        // Remove characters that could break out of string context
        str = str.replace(/[)(\];]/g, "");
        return str;
    }

    // ── UI Helpers ─────────────────────────────────────────────
    function addMessage(role, content) {
        var container = document.getElementById("messages");
        var msgDiv = document.createElement("div");
        msgDiv.className = "message " + role;

        var contentDiv = document.createElement("div");
        contentDiv.className = "message-content";
        contentDiv.innerHTML = formatMessage(content);

        msgDiv.appendChild(contentDiv);
        container.appendChild(msgDiv);
        container.scrollTop = container.scrollHeight;

        return msgDiv;
    }

    function formatMessage(text) {
        // Basic markdown-like formatting
        text = escapeHtml(text);

        // Code blocks
        text = text.replace(/```(\w*)\n([\s\S]*?)```/g, function (m, lang, code) {
            return '<pre><code>' + code + '</code></pre>';
        });

        // Inline code
        text = text.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Bold
        text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

        // Line breaks
        text = text.replace(/\n/g, '<br>');

        return text;
    }

    function escapeHtml(text) {
        var div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }

    function showTyping() {
        var container = document.getElementById("messages");
        var div = document.createElement("div");
        div.className = "message assistant";
        div.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
        container.appendChild(div);
        container.scrollTop = container.scrollHeight;
        return div;
    }

    function removeTyping(el) {
        if (el && el.parentNode) el.parentNode.removeChild(el);
    }

    function showActionBadges(msgEl, actions) {
        var contentDiv = msgEl.querySelector(".message-content");
        var badgesDiv = document.createElement("div");
        badgesDiv.style.marginTop = "6px";

        for (var i = 0; i < actions.length; i++) {
            var badge = document.createElement("span");
            badge.className = "action-badge";
            badge.textContent = actions[i].label || actions[i].type;
            badge.dataset.index = i;
            (function (action, el) {
                el.addEventListener("click", function () {
                    executeAction(action, el);
                });
            })(actions[i], badge);
            badgesDiv.appendChild(badge);
        }

        contentDiv.appendChild(badgesDiv);
    }

    function updateActionsBar() {
        var bar = document.getElementById("actions-bar");
        var label = document.getElementById("actionsLabel");

        if (pendingActions.length > 0) {
            bar.classList.remove("hidden");
            label.textContent = pendingActions.length + " pending action" + (pendingActions.length > 1 ? "s" : "");
        } else {
            bar.classList.add("hidden");
        }
    }

    // ── Render Progress Polling ────────────────────────────────
    var renderPollTimer = null;
    var renderProgressEl = null;

    function startRenderProgressPoll() {
        // Create a progress bar message in the chat
        renderProgressEl = addMessage("system", "");
        var contentDiv = renderProgressEl.querySelector(".message-content");
        contentDiv.innerHTML =
            '<div class="progress-bar">' +
            '  <div class="progress-fill" style="width: 0%"></div>' +
            '  <span class="progress-text">Render starting...</span>' +
            '</div>';

        renderPollTimer = setInterval(pollRenderProgress, 2000);
    }

    function pollRenderProgress() {
        fetch(settings.backendUrl + "/api/chat/render-progress", { method: "GET" })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                if (!data.success) return;

                var pct = data.percent || 0;
                var status = data.status || "idle";

                if (renderProgressEl) {
                    var fill = renderProgressEl.querySelector(".progress-fill");
                    var text = renderProgressEl.querySelector(".progress-text");
                    if (fill) fill.style.width = pct + "%";
                    if (text) {
                        if (status === "complete") {
                            text.textContent = "Render complete!";
                        } else if (status === "error") {
                            text.textContent = "Render failed: " + (data.error || "Unknown error");
                        } else {
                            text.textContent = "Rendering: " + pct + "% (frame " + (data.frame || 0) + ")";
                        }
                    }
                }

                if (status === "complete" || status === "error" || status === "idle") {
                    clearInterval(renderPollTimer);
                    renderPollTimer = null;
                }
            })
            .catch(function () {
                // Silently ignore fetch errors during polling
            });
    }

    // ── Start ──────────────────────────────────────────────────
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
