"""
AE Version Compatibility — knowledge base for JSX script compatibility
across After Effects versions.

Tracks which scripts work on which AE versions, known freezes, workarounds,
and deprecated APIs. The runScript method checks this before executing.
"""

from __future__ import annotations

from typing import Any

# ── Compatibility Database ──────────────────────────────────
# Each entry: script name → compatibility info
# "min_version": oldest AE version that supports this script
# "max_version": newest AE version tested (None = no upper bound)
# "known_issues": version-specific bugs/freezes
# "workaround": alternative approach for unsupported versions
# "deprecated_apis": ExtendScript APIs used that are deprecated in certain versions
# "notes": human-readable context

SCRIPT_COMPAT: dict[str, dict[str, Any]] = {
    # ── Core Scripts (work everywhere) ──────────────────────
    "file_map.jsx": {
        "min_version": 2020,
        "notes": "Core project mapping. Uses app.project.items iteration.",
    },
    "addComp.jsx": {
        "min_version": 2020,
        "notes": "Uses app.project.items.addComp() — stable across all versions.",
    },
    "save_project.jsx": {
        "min_version": 2020,
        "notes": "Uses app.project.save() — universal.",
    },
    "create_folder.jsx": {
        "min_version": 2020,
        "notes": "Uses FolderItem creation — universal.",
    },
    "selectItem.jsx": {
        "min_version": 2020,
        "notes": "Basic item selection — universal.",
    },
    "selectItemByName.jsx": {
        "min_version": 2020,
        "notes": "Name-based item selection — universal.",
    },
    "renameItem.jsx": {
        "min_version": 2020,
        "notes": "Item renaming — universal.",
    },
    "importFile.jsx": {
        "min_version": 2020,
        "notes": "File import via ImportOptions — universal.",
    },
    "workAreaComp.jsx": {
        "min_version": 2020,
        "notes": "Work area start/duration — universal.",
    },
    "run_command.jsx": {
        "min_version": 2020,
        "notes": "app.executeCommand() — universal.",
    },

    # ── Layer Operations ────────────────────────────────────
    "update_properties.jsx": {
        "min_version": 2020,
        "notes": "Property access via dot-notation. Uses propertyParser from framework.js.",
        "known_issues": {
            2020: "Some expression controls may not be accessible via scripting.",
        },
    },
    "update_properties_frame.jsx": {
        "min_version": 2020,
        "notes": "Keyframe setting via setValueAtTime(). Universal but slow on comps with many keyframes.",
    },
    "add_marker.jsx": {
        "min_version": 2020,
        "notes": "MarkerValue + setValueAtTime — universal.",
    },
    "add_resource.jsx": {
        "min_version": 2020,
        "notes": "Adds footage items to comp layers — universal.",
    },
    "update_resource.jsx": {
        "min_version": 2020,
        "notes": "Updates layer timing properties — universal.",
    },
    "selectLayerByLayer.jsx": {
        "min_version": 2020,
        "notes": "Layer selection by name — universal.",
    },
    "selectLayerByIndex.jsx": {
        "min_version": 2020,
        "notes": "Layer selection by index — universal.",
    },
    "selectItemLayer.jsx": {
        "min_version": 2020,
        "notes": "Item + layer selection — universal.",
    },

    # ── Composition Duplication ─────────────────────────────
    "duplicate_comp.jsx": {
        "min_version": 2020,
        "notes": "Basic comp duplication. Uses .duplicate() method.",
    },
    "duplicate_comp_1.jsx": {
        "min_version": 2020,
        "notes": "Comp duplication variant 1.",
    },
    "duplicate_comp_2.jsx": {
        "min_version": 2020,
        "notes": "Comp duplication with folder placement and layer mapping.",
        "known_issues": {
            2020: "Deep nested comp references may not remap correctly.",
            2021: "Deep nested comp references may not remap correctly.",
        },
    },
    "duplicate_folder_items.jsx": {
        "min_version": 2022,
        "notes": "Bulk folder item duplication. Uses newer project item APIs.",
        "known_issues": {
            2020: "May freeze on large projects (100+ items). Use individual duplication instead.",
            2021: "May freeze on large projects (100+ items). Use individual duplication instead.",
        },
        "workaround": "For AE 2020-2021, duplicate items one at a time with duplicate_comp.jsx.",
    },

    # ── Layer Creation ──────────────────────────────────────
    "add_text_layer.jsx": {
        "min_version": 2020,
        "notes": "TextLayer creation. TextDocument API is stable across versions.",
        "known_issues": {
            2020: "Some font properties (tracking, leading) may not apply via scripting.",
        },
    },
    "add_solid_layer.jsx": {
        "min_version": 2020,
        "notes": "Solid layer creation — universal.",
    },
    "add_null_layer.jsx": {
        "min_version": 2020,
        "notes": "Null layer creation — universal.",
    },
    "add_shape_layer.jsx": {
        "min_version": 2020,
        "notes": "Shape layer creation. Complex shape groups may behave differently across versions.",
        "known_issues": {
            2020: "Parametric shape properties have limited scripting access.",
            2021: "Parametric shape properties have limited scripting access.",
        },
    },

    # ── Transitions ─────────────────────────────────────────
    "add_transition.jsx": {
        "min_version": 2022,
        "notes": "Adds keyframe-based transitions (fade, slide, wipe). Uses expression controls.",
        "known_issues": {
            2020: "Expression control access may cause freeze. Avoid on AE 2020.",
            2021: "Expression control access may cause freeze. Avoid on AE 2021.",
        },
        "workaround": "For AE 2020-2021, apply transitions manually or use simpler opacity keyframes.",
    },

    # ── Rendering ───────────────────────────────────────────
    "renderComp.jsx": {
        "min_version": 2020,
        "notes": "Adds comp to render queue. RenderQueueItem API is stable.",
        "known_issues": {
            2020: "Output module templates may have different names than newer versions.",
        },
    },

    # ── Project Operations ──────────────────────────────────
    "create_new_project.jsx": {
        "min_version": 2020,
        "notes": "Creates a new AE project file — universal.",
    },
    "openItemName.jsx": {
        "min_version": 2020,
        "notes": "Opens item by name — universal.",
    },
    "search_folder_items.jsx": {
        "min_version": 2022,
        "notes": "Searches folder contents with filtering.",
        "known_issues": {
            2020: "FolderItem.items iteration may be slow or incomplete.",
            2021: "FolderItem.items iteration may be slow or incomplete.",
        },
    },
    "check_scripting_enabled.jsx": {
        "min_version": 2020,
        "notes": "Checks if scripting preferences allow file writes.",
    },
    "getMarker.jsx": {
        "min_version": 2020,
        "notes": "Reads marker data — universal.",
    },
    "add_comp_to_templates.jsx": {
        "min_version": 2020,
        "notes": "Adds comp to template timeline — universal.",
    },

    # ── Debug Scripts ───────────────────────────────────────
    "debug_create_comp.jsx": {
        "min_version": 2020,
        "notes": "Debug version of comp creation with extra logging.",
    },
    "debug_save_project.jsx": {
        "min_version": 2020,
        "notes": "Debug version of save with extra logging.",
    },

    # ── Background Services ─────────────────────────────────
    "ae_command_runner.jsx": {
        "min_version": 2020,
        "notes": "Startup script that monitors queue folder. Uses app.scheduleTask() for polling.",
        "known_issues": {
            2020: "app.scheduleTask() interval may drift. Use longer poll intervals (1000ms+).",
        },
    },
    "ae_server.jsx": {
        "min_version": 2022,
        "notes": "Server variant of command runner. May not work on older AE versions.",
        "known_issues": {
            2020: "Socket object not available in all AE 2020 builds.",
            2021: "Socket object not available in all AE 2021 builds.",
        },
    },
}


def check_script_compat(script_name: str, ae_version: int | None) -> dict[str, Any]:
    """Check if a JSX script is compatible with the given AE version.

    Returns:
        {
            "compatible": True/False,
            "script": "script_name.jsx",
            "ae_version": 2026,
            "issues": ["issue description", ...],
            "workaround": "alternative approach" or None,
            "notes": "general notes" or None,
        }
    """
    result: dict[str, Any] = {
        "compatible": True,
        "script": script_name,
        "ae_version": ae_version,
        "issues": [],
        "workaround": None,
        "notes": None,
    }

    info = SCRIPT_COMPAT.get(script_name)
    if not info:
        # Unknown script — allow it but flag it
        result["notes"] = "No compatibility data available for this script."
        return result

    result["notes"] = info.get("notes")

    if ae_version is None:
        # Can't check without a version
        result["notes"] = "AE version unknown — cannot verify compatibility."
        return result

    # Check minimum version
    min_ver = info.get("min_version", 2020)
    if ae_version < min_ver:
        result["compatible"] = False
        result["issues"].append(
            f"Requires AE {min_ver}+, but detected AE {ae_version}."
        )
        if info.get("workaround"):
            result["workaround"] = info["workaround"]
        return result

    # Check max version
    max_ver = info.get("max_version")
    if max_ver and ae_version > max_ver:
        result["issues"].append(
            f"Only tested up to AE {max_ver}. AE {ae_version} may have breaking changes."
        )

    # Check known issues for this specific version
    known = info.get("known_issues", {})
    if ae_version in known:
        result["issues"].append(known[ae_version])
        if info.get("workaround"):
            result["workaround"] = info["workaround"]

    return result


def get_all_compat(ae_version: int | None) -> list[dict[str, Any]]:
    """Get compatibility report for ALL scripts against a given AE version."""
    results = []
    for script_name in sorted(SCRIPT_COMPAT.keys()):
        results.append(check_script_compat(script_name, ae_version))
    return results


def get_incompatible_scripts(ae_version: int | None) -> list[dict[str, Any]]:
    """Get only scripts with issues for the given AE version."""
    return [
        r for r in get_all_compat(ae_version)
        if not r["compatible"] or r["issues"]
    ]
