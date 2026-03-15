"""
Plugin marketplace system for ae-automation.

Provides a local plugin registry that manages community templates and custom
actions.  Plugins live in PLUGINS_DIR (per-user appdata) and are discovered
by their ``plugin.json`` manifest.

Usage standalone (CLI)::

    registry = PluginRegistry()
    registry.list_plugins()

Usage via Client mixin::

    client = Client()
    client.list_plugins()
    client.run_plugin("lower-third")
"""

from __future__ import annotations

import json
import os
import shutil
import zipfile
from typing import Any

from ae_automation.logging_config import get_logger
from ae_automation.settings import _appdata, get_ae_version

logger = get_logger(__name__)

# ── Paths ────────────────────────────────────────────────────
PLUGINS_DIR: str = os.path.join(_appdata, "ae_automation", "plugins")
BUILTIN_PLUGINS_DIR: str = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "builtin_plugins"
)

# Ensure the plugins directory exists
os.makedirs(PLUGINS_DIR, exist_ok=True)

VALID_PLUGIN_TYPES = {"template", "action", "bundle"}

REQUIRED_MANIFEST_KEYS = {"name", "version", "description", "author", "type"}


# ── Helpers ──────────────────────────────────────────────────

def _read_manifest(plugin_dir: str) -> dict[str, Any] | None:
    """Read and validate a plugin.json manifest from *plugin_dir*.

    Returns ``None`` when the manifest is missing or malformed.
    """
    manifest_path = os.path.join(plugin_dir, "plugin.json")
    if not os.path.isfile(manifest_path):
        return None
    try:
        with open(manifest_path, "r", encoding="utf-8") as fh:
            data: dict[str, Any] = json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Bad manifest in %s: %s", plugin_dir, exc)
        return None

    # Minimal validation
    missing = REQUIRED_MANIFEST_KEYS - set(data.keys())
    if missing:
        logger.warning("Manifest in %s missing keys: %s", plugin_dir, missing)
        return None

    if data.get("type") not in VALID_PLUGIN_TYPES:
        logger.warning(
            "Manifest in %s has invalid type '%s'", plugin_dir, data.get("type")
        )
        return None

    # Attach the resolved directory so callers know where files live
    data["_dir"] = plugin_dir
    return data


def _ensure_builtins_installed() -> None:
    """Copy built-in plugins to PLUGINS_DIR if they are not already there."""
    if not os.path.isdir(BUILTIN_PLUGINS_DIR):
        return
    for entry in os.listdir(BUILTIN_PLUGINS_DIR):
        src = os.path.join(BUILTIN_PLUGINS_DIR, entry)
        if not os.path.isdir(src):
            continue
        dest = os.path.join(PLUGINS_DIR, entry)
        if os.path.isdir(dest):
            continue  # already installed
        manifest = _read_manifest(src)
        if manifest is None:
            continue
        shutil.copytree(src, dest)
        logger.info("Auto-installed built-in plugin: %s", entry)


# ── Registry ─────────────────────────────────────────────────

class PluginRegistry:
    """Manages installed plugins in PLUGINS_DIR."""

    def __init__(self, plugins_dir: str | None = None) -> None:
        self.plugins_dir = plugins_dir or PLUGINS_DIR
        os.makedirs(self.plugins_dir, exist_ok=True)
        _ensure_builtins_installed()

    # ── Queries ──────────────────────────────────────────────

    def list_plugins(self) -> list[dict[str, Any]]:
        """Return metadata dicts for every installed plugin."""
        plugins: list[dict[str, Any]] = []
        if not os.path.isdir(self.plugins_dir):
            return plugins
        for entry in sorted(os.listdir(self.plugins_dir)):
            plugin_dir = os.path.join(self.plugins_dir, entry)
            if not os.path.isdir(plugin_dir):
                continue
            manifest = _read_manifest(plugin_dir)
            if manifest is not None:
                plugins.append(manifest)
        return plugins

    def get_plugin(self, name: str) -> dict[str, Any] | None:
        """Get a single plugin's metadata by *name*, or ``None``."""
        plugin_dir = os.path.join(self.plugins_dir, name)
        if os.path.isdir(plugin_dir):
            return _read_manifest(plugin_dir)
        # Fallback: linear scan (name may differ from directory)
        for plugin in self.list_plugins():
            if plugin.get("name") == name:
                return plugin
        return None

    def search_plugins(
        self,
        query: str = "",
        plugin_type: str = "",
        tags: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Filter installed plugins by free-text *query*, *plugin_type*, or *tags*."""
        results: list[dict[str, Any]] = []
        query_lower = query.lower()
        tags_lower = [t.lower() for t in (tags or [])]

        for plugin in self.list_plugins():
            # Type filter
            if plugin_type and plugin.get("type") != plugin_type:
                continue

            # Tag filter (all requested tags must be present)
            if tags_lower:
                plugin_tags = [t.lower() for t in plugin.get("tags", [])]
                if not all(t in plugin_tags for t in tags_lower):
                    continue

            # Free-text query (matches name, description, or tags)
            if query_lower:
                haystack = " ".join([
                    plugin.get("name", ""),
                    plugin.get("description", ""),
                    " ".join(plugin.get("tags", [])),
                ]).lower()
                if query_lower not in haystack:
                    continue

            results.append(plugin)
        return results

    def get_plugin_config(self, name: str) -> dict[str, Any] | None:
        """Load and return the plugin's ``config.json`` for template plugins."""
        plugin = self.get_plugin(name)
        if plugin is None:
            return None
        config_rel = plugin.get("files", {}).get("config", "config.json")
        config_path = os.path.join(plugin["_dir"], config_rel)
        if not os.path.isfile(config_path):
            return None
        try:
            with open(config_path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            logger.error("Failed to read config for plugin '%s': %s", name, exc)
            return None

    def check_plugin_compat(self, name: str) -> dict[str, Any]:
        """Check whether *name* is compatible with the current AE version.

        Returns a dict with ``compatible`` (bool), ``ae_version`` (detected),
        and ``ae_min_version`` (required by plugin).
        """
        plugin = self.get_plugin(name)
        if plugin is None:
            return {
                "compatible": False,
                "error": f"Plugin '{name}' not found",
                "ae_version": None,
                "ae_min_version": None,
            }

        ae_min = plugin.get("ae_min_version")
        ae_version = get_ae_version()

        if ae_version is None:
            return {
                "compatible": True,
                "warning": "AE version could not be detected; skipping compat check",
                "ae_version": None,
                "ae_min_version": ae_min,
            }

        compatible = ae_min is None or ae_version >= ae_min
        result: dict[str, Any] = {
            "compatible": compatible,
            "ae_version": ae_version,
            "ae_min_version": ae_min,
        }
        if not compatible:
            result["error"] = (
                f"Plugin requires AE {ae_min}+ but detected AE {ae_version}"
            )
        return result

    # ── Mutations ────────────────────────────────────────────

    def install_plugin(self, source: str) -> dict[str, Any]:
        """Install a plugin from a local directory or ``.zip`` file.

        Copies the plugin into ``PLUGINS_DIR`` and returns its manifest.
        Raises ``ValueError`` on invalid source or manifest.
        """
        source = os.path.abspath(source)

        if zipfile.is_zipfile(source):
            return self._install_from_zip(source)
        elif os.path.isdir(source):
            return self._install_from_dir(source)
        else:
            raise ValueError(
                f"Source is neither a directory nor a zip file: {source}"
            )

    def _install_from_dir(self, src_dir: str) -> dict[str, Any]:
        manifest = _read_manifest(src_dir)
        if manifest is None:
            raise ValueError(
                f"No valid plugin.json found in {src_dir}"
            )
        name = manifest["name"]
        dest = os.path.join(self.plugins_dir, name)
        if os.path.isdir(dest):
            shutil.rmtree(dest)
        shutil.copytree(src_dir, dest)
        # Re-read from installed location
        installed = _read_manifest(dest)
        if installed is None:
            raise ValueError("Plugin installed but manifest unreadable")
        logger.info("Installed plugin '%s' from directory", name)
        return installed

    def _install_from_zip(self, zip_path: str) -> dict[str, Any]:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(tmp)

            # The zip may contain a single top-level directory or files at root
            entries = os.listdir(tmp)
            if len(entries) == 1 and os.path.isdir(os.path.join(tmp, entries[0])):
                extract_dir = os.path.join(tmp, entries[0])
            else:
                extract_dir = tmp

            return self._install_from_dir(extract_dir)

    def uninstall_plugin(self, name: str) -> bool:
        """Remove an installed plugin. Returns ``True`` if removed."""
        plugin_dir = os.path.join(self.plugins_dir, name)
        if not os.path.isdir(plugin_dir):
            # Try finding by manifest name
            for plugin in self.list_plugins():
                if plugin.get("name") == name:
                    plugin_dir = plugin["_dir"]
                    break
            else:
                return False
        shutil.rmtree(plugin_dir)
        logger.info("Uninstalled plugin '%s'", name)
        return True


# ── Client Mixin ─────────────────────────────────────────────

class PluginMixin:
    """Mixin that exposes plugin operations on the Client instance."""

    _plugin_registry: PluginRegistry | None = None

    @property
    def plugin_registry(self) -> PluginRegistry:
        if self._plugin_registry is None:
            self._plugin_registry = PluginRegistry()
        return self._plugin_registry

    def list_plugins(self) -> list[dict[str, Any]]:
        """List all installed plugins."""
        return self.plugin_registry.list_plugins()

    def install_plugin(self, source: str) -> dict[str, Any]:
        """Install a plugin from a local directory or zip file."""
        return self.plugin_registry.install_plugin(source)

    def run_plugin(self, name: str, overrides: dict[str, Any] | None = None) -> Any:
        """Load a template plugin's config and run it through startBot.

        *overrides* is an optional dict merged into the plugin config before
        execution (e.g. to set ``output_dir``).
        """
        plugin = self.plugin_registry.get_plugin(name)
        if plugin is None:
            raise ValueError(f"Plugin '{name}' not found")

        ptype = plugin.get("type", "template")
        if ptype not in ("template", "bundle"):
            raise ValueError(
                f"Plugin '{name}' is type '{ptype}' and cannot be run as a template"
            )

        config = self.plugin_registry.get_plugin_config(name)
        if config is None:
            raise ValueError(f"Plugin '{name}' has no loadable config.json")

        # Apply overrides
        if overrides:
            for key, val in overrides.items():
                if key in config:
                    if isinstance(config[key], dict) and isinstance(val, dict):
                        config[key].update(val)
                    else:
                        config[key] = val
                else:
                    config[key] = val

        # Write a temporary config and run through the bot pipeline
        import tempfile

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as tmp:
            json.dump(config, tmp, indent=2)
            tmp_path = tmp.name

        try:
            # startBot is provided by botMixin on the Client
            return self.startBot(tmp_path)  # type: ignore[attr-defined]
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
