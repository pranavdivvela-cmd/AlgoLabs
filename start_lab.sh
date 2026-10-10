#!/usr/bin/env bash
# Usage: bash start_lab.sh [labN]   (asks which lab when omitted)
set -euo pipefail
lab_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
for lab_command in bash python3 ssh ssh-keygen scp chmod ls cat diff zip unzip tar; do
    command -v "$lab_command" >/dev/null || { printf 'Missing command: %s. Ask your instructor for setup help.\n' "$lab_command" >&2; exit 1; }
done
python3 -B "$lab_root/kit/student_start.py" "$@"
lab_id="$(cat "$lab_root/.connection/current_lab")"
lab_title="$(python3 -B -c 'import sys; sys.path.insert(0, sys.argv[1]); import labs; print(labs.Lab(sys.argv[2]).title)' "$lab_root/kit" "$lab_id")"
cd -- "$(cat "$lab_root/.connection/current_dir")"
exec bash "$lab_root/kit/terminal.sh" "$lab_id" "$lab_title"
