# displayctrl

Toggle external displays on/off on macOS using the CoreGraphics private API.

## Install

Install as a standalone tool (isolated env, binary on PATH):

```
uv tool install .
```

Or run without installing:

```
uvx --from . displayctrl <enable|disable|list>
```

## Usage

```
displayctrl <enable|disable|list>
```

- **`list`** -- Print IDs of connected external displays.
- **`disable`** -- Turn off all external displays.
- **`enable`** -- Turn on all displays (brute-forces display IDs 1-10 since disabled displays aren't enumerable).

## Raycast

Script commands are included in the `raycast/` directory. To set up:

1. Open Raycast Settings → Extensions → Script Commands
2. Click **Add Script Directory** and select the `raycast/` folder
3. Search "Display" in Raycast to find **Enable External Displays** and **Disable External Displays**

## Requirements

- macOS
- Python 3.10+

## How it works

Uses `ctypes` to call CoreGraphics functions (`CGGetActiveDisplayList`, `CGSConfigureDisplayEnabled`, etc.) directly, toggling displays in a single configuration transaction without any native dependencies beyond the system frameworks.
