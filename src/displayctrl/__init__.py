"""Toggle external displays on/off using CoreGraphics."""

import json
import sys
from ctypes import CDLL, POINTER, byref, c_bool, c_int, c_uint32, c_void_p, util
from pathlib import Path


cg = CDLL(util.find_library("CoreGraphics"))

cg.CGGetActiveDisplayList.argtypes = [c_uint32, POINTER(c_uint32), POINTER(c_uint32)]
cg.CGGetActiveDisplayList.restype = c_int
cg.CGDisplayIsBuiltin.argtypes = [c_uint32]
cg.CGDisplayIsBuiltin.restype = c_bool
cg.CGBeginDisplayConfiguration.argtypes = [POINTER(c_void_p)]
cg.CGBeginDisplayConfiguration.restype = c_int
cg.CGCompleteDisplayConfiguration.argtypes = [c_void_p, c_int]
cg.CGCompleteDisplayConfiguration.restype = c_int
cg.CGCancelDisplayConfiguration.argtypes = [c_void_p]
cg.CGCancelDisplayConfiguration.restype = c_int
cg.CGSConfigureDisplayEnabled.argtypes = [c_void_p, c_uint32, c_bool]
cg.CGSConfigureDisplayEnabled.restype = c_int


STATEFILE = Path.home() / ".displayctrl_disabled.json"
kCGConfigurePermanently = 2


def get_external_displays():
    """Return IDs of active external displays."""
    max_displays = 16
    display_ids = (c_uint32 * max_displays)()
    display_count = c_uint32(0)
    if cg.CGGetActiveDisplayList(max_displays, display_ids, byref(display_count)) != 0:
        return []
    return [
        display_ids[i]
        for i in range(display_count.value)
        if not cg.CGDisplayIsBuiltin(display_ids[i])
    ]


def save_disabled_ids(display_ids: list[int]):
    STATEFILE.write_text(json.dumps(display_ids))


def load_disabled_ids() -> list[int]:
    try:
        return json.loads(STATEFILE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def clear_disabled_ids():
    STATEFILE.unlink(missing_ok=True)


def set_displays_enabled(display_ids: list[int], enabled: bool) -> dict[int, bool]:
    """Enable/disable displays in a single configuration transaction."""
    results = {}
    config_ref = c_void_p()
    if cg.CGBeginDisplayConfiguration(byref(config_ref)) != 0:
        return {did: False for did in display_ids}
    for did in display_ids:
        results[did] = cg.CGSConfigureDisplayEnabled(config_ref, did, enabled) == 0
    if not any(results.values()):
        cg.CGCancelDisplayConfiguration(config_ref)
        return results
    cg.CGCompleteDisplayConfiguration(config_ref, kCGConfigurePermanently)
    return results


def toggle_displays(enable: bool):
    if enable:
        displays = load_disabled_ids()
        if not displays:
            print("No saved display IDs found. Nothing to enable.")
            return
        results = set_displays_enabled(displays, True)
        for display_id, ok in results.items():
            status = "OK" if ok else "FAILED"
            print(f"Enabling display {display_id}: {status}")
        clear_disabled_ids()
        return

    displays = get_external_displays()
    if not displays:
        print("No external displays found.")
        return

    save_disabled_ids(displays)
    results = set_displays_enabled(displays, False)
    for display_id, ok in results.items():
        status = "OK" if ok else "FAILED"
        print(f"Disabling display {display_id}: {status}")


def list_displays():
    displays = get_external_displays()
    if not displays:
        print("No external displays found.")
        return
    for display_id in displays:
        print(display_id)


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("enable", "disable", "list"):
        print(f"Usage: {sys.argv[0]} <enable|disable|list>")
        sys.exit(1)

    if sys.argv[1] == "list":
        list_displays()
    else:
        toggle_displays(enable=(sys.argv[1] == "enable"))
