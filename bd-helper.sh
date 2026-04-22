#!/bin/bash
# Helper script for Beads commands
# Ensures PATH is set correctly for bd command

export PATH="/opt/homebrew/bin:$PATH:/Users/mattbeane/go/bin"

bd "$@"

# Auto-regenerate Beadspace visualization after any bd command
# Run in background to avoid slowing down the command
if [ -f "$HOME/knowledge-work/visualize-beadspace.py" ]; then
    /opt/homebrew/bin/python3 "$HOME/knowledge-work/visualize-beadspace.py" > /dev/null 2>&1 &
fi
