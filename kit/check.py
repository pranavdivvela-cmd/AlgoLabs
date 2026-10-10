#!/usr/bin/env python3
"""check_lab [LAB]: optional ungraded Codespace hints, then official grading on the lab server.

The graded tests run on the server (`check_lab LAB` there) and are not part of
this repository. LAB defaults to the lab this terminal was opened for."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import common
import labs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lab', nargs='?', default=os.environ.get('LAB_ID'), help='Lab to check, for example lab5')
    parser.add_argument('--root', type=Path, help='Local lab folder for hints (default: current directory)')
    parser.add_argument('--config', type=Path, default=common.SSH_CONFIG)
    args = parser.parse_args()
    try:
        lab = labs.Lab(args.lab) if args.lab else labs.choose()
    except (OSError, ValueError) as error:
        print('CHECK: ' + str(error), file=sys.stderr)
        return 2
    hints = lab.hook('local_hints')
    if hints:
        try:
            hints(args.root or Path.cwd(), args.config)
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            print('Local hints skipped: ' + str(error) + '\n', file=sys.stderr)
    print(f'Requesting official grading of {lab.id} from the lab server...\n', flush=True)
    try:
        process = subprocess.run(common.ssh_command(args.config) + ['check_lab ' + lab.id], timeout=120)
    except subprocess.TimeoutExpired:
        print('CHECK: the server did not answer in time. Try again.', file=sys.stderr)
        return 2
    if process.returncode == 255:
        print('CHECK: could not connect to the lab server. Check your connection and try again.', file=sys.stderr)
    return process.returncode


if __name__ == '__main__':
    sys.exit(main())
