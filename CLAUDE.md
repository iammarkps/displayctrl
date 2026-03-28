# displayctrl

## Tools

- **Python package manager**: uv (use `uv pip install`, `uv run`, etc. — never bare `pip`)

## Dev commands

- Install as tool: `uv tool install .` (see caveat below about caching)
- Dev install: `uv pip install -e .`
- Run without installing: `uvx --from . displayctrl <enable|disable|list>`

## uv tool install caching

- `uv tool install --force .` does NOT rebuild if the version number (`0.1.0`) hasn't changed — it serves a cached wheel with stale code
- To install updated source: run `uv cache clean` first, then `uv tool install .`; or `uv tool uninstall displayctrl && uv cache clean && uv tool install .`
- Always verify the installed code matches source after reinstalling (e.g. grep for a known function)

## CoreGraphics API notes

- `CGGetActiveDisplayList` only returns enabled displays — disabled ones disappear from this list
- `CGGetOnlineDisplayList` also does NOT return displays disabled via `CGSConfigureDisplayEnabled` — don't rely on it for re-enabling
- Because no CG API enumerates disabled displays, we persist display IDs to `~/.displayctrl_disabled.json` on disable and read them back on enable
- Display IDs for Thunderbolt docks can be any value (not just small integers) — never brute-force ID ranges
- `CGCompleteDisplayConfiguration` must use `kCGConfigurePermanently` (mode 2), not `kCGConfigureForSession` (mode 0) — mode 0 silently no-ops when re-enabling displays that have been removed from the online list
