#!/usr/bin/env bash
# Usage: terminal.sh LAB_ID LAB_TITLE  (start_lab.sh calls this after setup)
set -euo pipefail
lab_kit="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export LAB_ID="${1:?lab id}" LAB_TITLE="${2:-$1}"
export LAB_SSH_CONFIG="${LAB_SSH_CONFIG:-$lab_kit/../.connection/ssh_config}"
export BASH_SILENCE_DEPRECATION_WARNING=1
export LAB_CHECKER="$lab_kit/check.py"
if [[ ! -f "$LAB_SSH_CONFIG" ]]; then
    printf 'Configure your private SSH connection first: run bash start_lab.sh at the repository root.\n' >&2
    exit 1
fi
printf '%s terminal. ssh and scp use your private lab connection; check_lab checks your work.\n' "$LAB_TITLE"
printf 'Use exit to leave this starting terminal when finished.\n'
exec bash --noprofile --rcfile "$lab_kit/terminal.rc" -i
