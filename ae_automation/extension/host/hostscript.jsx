/**
 * AE Automation Chat — ExtendScript Host
 * Functions called from the CEP panel via CSInterface.evalScript()
 * All return values must be strings (use JSON.stringify for objects)
 */

// ── Project Info ───────────────────────────────────────────
function getProjectInfo() {
    var info = {
        project_name: app.project.file ? app.project.file.name : "Untitled",
        project_path: app.project.file ? app.project.file.fsName : "",
        num_items: app.project.numItems,
        num_comps: 0,
        comp_names: [],
        ae_version: app.version
    };

    for (var i = 1; i <= app.project.numItems; i++) {
        if (app.project.item(i) instanceof CompItem) {
            info.num_comps++;
            info.comp_names.push(app.project.item(i).name);
        }
    }

    return JSON.stringify(info);
}

function listCompositions() {
    var comps = [];
    for (var i = 1; i <= app.project.numItems; i++) {
        var item = app.project.item(i);
        if (item instanceof CompItem) {
            comps.push({
                name: item.name,
                width: item.width,
                height: item.height,
                duration: item.duration,
                fps: item.frameRate,
                num_layers: item.numLayers
            });
        }
    }
    return JSON.stringify(comps);
}

// ── Composition Operations ─────────────────────────────────
function createComp(name, width, height, duration, fps) {
    var comp = app.project.items.addComp(name, width, height, 1, duration, fps);
    return JSON.stringify({
        success: true,
        name: comp.name,
        id: comp.id
    });
}

function findCompByName(name) {
    for (var i = 1; i <= app.project.numItems; i++) {
        if (app.project.item(i) instanceof CompItem && app.project.item(i).name === name) {
            return app.project.item(i);
        }
    }
    return null;
}

// ── Layer Operations ───────────────────────────────────────
function editLayerText(compName, layerName, value) {
    var comp = findCompByName(compName);
    if (!comp) return JSON.stringify({ success: false, error: "Comp not found: " + compName });

    for (var i = 1; i <= comp.numLayers; i++) {
        if (comp.layer(i).name === layerName) {
            var layer = comp.layer(i);
            if (layer.property("Source Text")) {
                layer.property("Source Text").setValue(new TextDocument(value));
                return JSON.stringify({ success: true });
            } else {
                return JSON.stringify({ success: false, error: "Layer is not a text layer" });
            }
        }
    }
    return JSON.stringify({ success: false, error: "Layer not found: " + layerName });
}

function editLayerProperty(compName, layerName, propertyPath, value) {
    var comp = findCompByName(compName);
    if (!comp) return JSON.stringify({ success: false, error: "Comp not found: " + compName });

    for (var i = 1; i <= comp.numLayers; i++) {
        if (comp.layer(i).name === layerName) {
            var prop = navigateProperty(comp.layer(i), propertyPath);
            if (!prop) return JSON.stringify({ success: false, error: "Property not found: " + propertyPath });

            var parsedValue = parseValue(value);
            prop.setValue(parsedValue);
            return JSON.stringify({ success: true });
        }
    }
    return JSON.stringify({ success: false, error: "Layer not found: " + layerName });
}

function setLayerColor(compName, layerName, propertyPath, hex) {
    var rgb = hexToRGB(hex);
    var comp = findCompByName(compName);
    if (!comp) return JSON.stringify({ success: false, error: "Comp not found: " + compName });

    for (var i = 1; i <= comp.numLayers; i++) {
        if (comp.layer(i).name === layerName) {
            var prop = navigateProperty(comp.layer(i), propertyPath);
            if (!prop) return JSON.stringify({ success: false, error: "Property not found: " + propertyPath });

            prop.setValue(rgb);
            return JSON.stringify({ success: true });
        }
    }
    return JSON.stringify({ success: false, error: "Layer not found: " + layerName });
}

function addMarkerToLayer(compName, layerName, markerText, time) {
    var comp = findCompByName(compName);
    if (!comp) return JSON.stringify({ success: false, error: "Comp not found: " + compName });

    for (var i = 1; i <= comp.numLayers; i++) {
        if (comp.layer(i).name === layerName) {
            var marker = new MarkerValue(markerText);
            comp.layer(i).property("Marker").setValueAtTime(time, marker);
            return JSON.stringify({ success: true });
        }
    }
    return JSON.stringify({ success: false, error: "Layer not found: " + layerName });
}

function getCompLayers(compName) {
    var comp = findCompByName(compName);
    if (!comp) return JSON.stringify({ error: "Comp not found: " + compName });

    var layers = [];
    for (var i = 1; i <= comp.numLayers; i++) {
        var layer = comp.layer(i);
        var layerInfo = {
            index: i,
            name: layer.name,
            type: getLayerType(layer),
            enabled: layer.enabled,
            startTime: layer.startTime,
            inPoint: layer.inPoint,
            outPoint: layer.outPoint
        };

        // Get text content if text layer
        if (layer.property("Source Text")) {
            try {
                layerInfo.text = layer.property("Source Text").value.text;
            } catch (e) {}
        }

        layers.push(layerInfo);
    }
    return JSON.stringify(layers);
}

// ── Project Operations ─────────────────────────────────────
function saveProject() {
    app.project.save();
    return JSON.stringify({ success: true });
}

// ── Helpers ────────────────────────────────────────────────
function navigateProperty(layer, path) {
    var parts = path.split(".");
    var prop = layer;
    for (var i = 0; i < parts.length; i++) {
        try {
            prop = prop.property(parts[i]);
        } catch (e) {
            return null;
        }
        if (!prop) return null;
    }
    return prop;
}

function parseValue(val) {
    // Array: "[960,540]"
    if (val.indexOf("[") === 0 && val.indexOf("]") === val.length - 1) {
        var inner = val.substring(1, val.length - 1);
        var parts = inner.split(",");
        var arr = [];
        for (var i = 0; i < parts.length; i++) {
            arr.push(parseFloat(parts[i]));
        }
        return arr;
    }
    // Number
    if (!isNaN(val) && val !== "") {
        return parseFloat(val);
    }
    return val;
}

function hexToRGB(hex) {
    hex = hex.replace("#", "");
    var r = parseInt(hex.substring(0, 2), 16) / 255;
    var g = parseInt(hex.substring(2, 4), 16) / 255;
    var b = parseInt(hex.substring(4, 6), 16) / 255;
    return [r, g, b, 1];
}

function getLayerType(layer) {
    if (layer instanceof TextLayer) return "text";
    if (layer instanceof ShapeLayer) return "shape";
    if (layer instanceof CameraLayer) return "camera";
    if (layer instanceof LightLayer) return "light";
    if (layer instanceof AVLayer) return "av";
    return "unknown";
}
