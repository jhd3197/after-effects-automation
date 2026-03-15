from __future__ import annotations

import glob
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
env_path: Path = Path(".env")
load_dotenv(dotenv_path=env_path)


# ── Platform Detection ──────────────────────────────────────
IS_WINDOWS: bool = sys.platform == "win32"
IS_MACOS: bool = sys.platform == "darwin"
IS_LINUX: bool = sys.platform.startswith("linux")


# ── Data Directory (cross-platform) ─────────────────────────
def _get_appdata() -> str:
    """Get the platform-appropriate application data directory."""
    appdata = os.getenv("APPDATA")
    if appdata:
        return appdata
    if IS_MACOS:
        return os.path.join(os.path.expanduser("~"), "Library", "Application Support")
    return os.path.join(os.path.expanduser("~"), ".local", "share")


_appdata: str = _get_appdata()


# ── AE Auto-Discovery ───────────────────────────────────────
def discover_all_ae_installs() -> list[dict[str, str | int | None]]:
    """Find all After Effects installations on this machine.

    Returns a list of dicts sorted newest-first:
        [{"path": "...", "version": 2026, "has_aerender": True}, ...]
    """
    candidates: list[dict[str, str | int | None]] = []

    if IS_WINDOWS:
        program_dirs = [
            os.environ.get("PROGRAMFILES", "C:/Program Files"),
            os.environ.get("PROGRAMFILES(X86)", "C:/Program Files (x86)"),
        ]
        for prog_dir in program_dirs:
            if not prog_dir:
                continue
            pattern = os.path.join(prog_dir, "Adobe", "Adobe After Effects *", "Support Files")
            for match in glob.glob(pattern):
                version = _extract_version_from_path(match)
                exe = os.path.join(match, "aerender.exe")
                candidates.append(
                    {
                        "path": match,
                        "version": version,
                        "has_aerender": os.path.isfile(exe),
                    }
                )

    elif IS_MACOS:
        for match in glob.glob("/Applications/Adobe After Effects *"):
            version = _extract_version_from_path(match)
            aerender = os.path.join(match, "aerender")
            candidates.append(
                {
                    "path": match,
                    "version": version,
                    "has_aerender": os.path.isfile(aerender),
                }
            )

    # Sort newest first
    candidates.sort(key=lambda c: c.get("version") or 0, reverse=True)
    return candidates


def discover_ae_folder() -> str | None:
    """Auto-discover the best After Effects installation.

    Always picks the latest version with aerender. If none have aerender,
    picks the latest directory anyway.
    """
    installs = discover_all_ae_installs()

    # Prefer installs with aerender
    for inst in installs:
        if inst["has_aerender"] and os.path.isdir(str(inst["path"])):
            return str(inst["path"])

    # Fallback: any install dir
    for inst in installs:
        if os.path.isdir(str(inst["path"])):
            return str(inst["path"])

    return None


def _extract_version_from_path(path: str) -> int | None:
    """Extract the AE version year from a path like '.../Adobe After Effects 2026/...'"""
    match = re.search(r"After Effects (\d{4})", path)
    if match:
        return int(match.group(1))
    # Also try CC versions (older)
    match = re.search(r"After Effects CC (\d{4})", path)
    if match:
        return int(match.group(1))
    return None


def get_ae_version() -> int | None:
    """Get the detected AE version year from the active AE folder."""
    return _extract_version_from_path(AFTER_EFFECT_FOLDER) if AFTER_EFFECT_FOLDER else None


def _get_ae_folder() -> str:
    """Resolve the AE folder: auto-discovery first, env var as override."""
    # Auto-discover always runs — picks latest version
    discovered = discover_ae_folder()

    # Env var overrides if explicitly set
    env_val = os.getenv("AFTER_EFFECT_FOLDER")
    if env_val:
        return env_val

    if discovered:
        return discovered

    return ""


def _get_aerender_path(ae_folder: str) -> str:
    """Resolve aerender path: env var > derived from AE folder."""
    env_val = os.getenv("AERENDER_PATH")
    if env_val:
        return env_val
    if not ae_folder:
        return ""
    exe = "aerender.exe" if IS_WINDOWS else "aerender"
    return os.path.join(ae_folder, exe)


# ── CEP Extension Directory (cross-platform) ────────────────
def get_cep_extensions_dir() -> str:
    """Get the platform-appropriate CEP extensions directory."""
    if IS_WINDOWS:
        return os.path.join(_appdata, "Adobe", "CEP", "extensions")
    elif IS_MACOS:
        return os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Application Support",
            "Adobe",
            "CEP",
            "extensions",
        )
    # Linux (experimental)
    return os.path.join(os.path.expanduser("~"), ".adobe", "CEP", "extensions")


# ── Settings ────────────────────────────────────────────────
CACHE_FOLDER: str = os.getenv("CACHE_FOLDER", os.path.join(_appdata, "ae_automation", "cache"))
AFTER_EFFECT_FOLDER: str = _get_ae_folder()
AFTER_EFFECT_PROJECT_FOLDER: str = os.getenv("AFTER_EFFECT_PROJECT_FOLDER", "au-automate")
QUEUE_FOLDER: str = os.path.join(_appdata, "ae_automation", "queue")
AERENDER_PATH: str = _get_aerender_path(AFTER_EFFECT_FOLDER)

# Ensure directories exist
os.makedirs(CACHE_FOLDER, exist_ok=True)
os.makedirs(QUEUE_FOLDER, exist_ok=True)

# Package resources path
PACKAGE_DIR: str = os.path.dirname(os.path.abspath(__file__))
JS_DIR: str = os.path.join(PACKAGE_DIR, "mixins", "js")


# ── Validation ──────────────────────────────────────────────
def validate_settings() -> None:
    """Validate required settings and paths."""
    from ae_automation.exceptions import AENotFoundError, ConfigValidationError

    if not AFTER_EFFECT_FOLDER or not os.path.exists(AFTER_EFFECT_FOLDER):
        discovered = discover_ae_folder()
        hint = ""
        if discovered:
            hint = f"\n  Auto-discovered: {discovered}\n  Set AFTER_EFFECT_FOLDER={discovered} in .env"
        else:
            hint = (
                "\n  No After Effects installation found."
                "\n  Set AFTER_EFFECT_FOLDER in .env to your AE Support Files path."
                "\n  Example: AFTER_EFFECT_FOLDER=C:/Program Files/Adobe/Adobe After Effects 2025/Support Files"
            )
        raise AENotFoundError(path=AFTER_EFFECT_FOLDER or "(not set)" + hint)

    if not AERENDER_PATH or not os.path.exists(AERENDER_PATH):
        raise AENotFoundError(path=AERENDER_PATH or "(not set)")

    if not os.path.exists(JS_DIR):
        raise ConfigValidationError(field="JS_DIR", detail=f"JavaScript files directory not found: {JS_DIR}")


def get_discovery_report() -> dict[str, object]:
    """Return a diagnostic report of the current platform and AE discovery state."""
    return {
        "platform": sys.platform,
        "is_windows": IS_WINDOWS,
        "is_macos": IS_MACOS,
        "is_linux": IS_LINUX,
        "appdata": _appdata,
        "ae_folder": AFTER_EFFECT_FOLDER,
        "ae_folder_exists": bool(AFTER_EFFECT_FOLDER) and os.path.exists(AFTER_EFFECT_FOLDER),
        "ae_version": get_ae_version(),
        "aerender_path": AERENDER_PATH,
        "aerender_exists": bool(AERENDER_PATH) and os.path.exists(AERENDER_PATH),
        "all_ae_installs": discover_all_ae_installs(),
        "cache_folder": CACHE_FOLDER,
        "queue_folder": QUEUE_FOLDER,
        "js_dir": JS_DIR,
        "js_dir_exists": os.path.exists(JS_DIR),
        "cep_extensions_dir": get_cep_extensions_dir(),
        "env_overrides": {
            "AFTER_EFFECT_FOLDER": os.getenv("AFTER_EFFECT_FOLDER"),
            "AERENDER_PATH": os.getenv("AERENDER_PATH"),
            "CACHE_FOLDER": os.getenv("CACHE_FOLDER"),
            "PROMPTURE_PATH": os.getenv("PROMPTURE_PATH"),
        },
    }
