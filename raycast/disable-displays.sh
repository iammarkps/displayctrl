#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Disable External Displays
# @raycast.mode compact

# Optional parameters:
# @raycast.icon 🖥️
# @raycast.packageName Display Control

export PATH="$HOME/.local/bin:$PATH"
displayctrl disable
