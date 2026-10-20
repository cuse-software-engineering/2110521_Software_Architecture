#!/bin/bash
# cap.sh <name> <command string>  -> runs the command, saves "$ cmd" + output to captures/terminal/<name>.txt
name="$1"; shift; cmd="$*"
out="$(dirname "$0")/../captures/terminal/$name.txt"
{ echo "\$ $cmd"; bash -c "$cmd" 2>&1; echo "[exit $?]"; } | tee "$out"
