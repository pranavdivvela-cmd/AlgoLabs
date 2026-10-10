#!/usr/bin/env python3
"""Configure this student's access once, then prepare the chosen lab.

Writes .connection/current_lab and .connection/current_dir for start_lab.sh,
which opens the lab terminal in that folder."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import access_import
import common
import connection
import labs


def configure_access(root, access):
    """Write the private SSH profile for lab-server from an installed access package."""
    access = common.plain_path(access)
    account = json.loads(common.plain_path(access / 'account.json').read_text(encoding='utf-8'))
    fields = set(account) - {'public_key'}
    if fields not in ({'host', 'user', 'port'}, {'host', 'user', 'port', 'host_key_alias'}):
        raise ValueError('Access package is incomplete. Ask your instructor for the correct ZIP.')
    key = common.plain_path(access / 'ssh_key')
    known = common.plain_path(access / 'known_hosts')
    if not key.is_file() or not known.is_file():
        raise ValueError('Missing access files. Extract the complete ZIP before starting.')
    # Some extraction tools discard ZIP permission attributes. Fix only this
    # package's own regular key file, never a global SSH file or linked target.
    key.chmod(0o600)
    config = Path(root) / '.connection/ssh_config'
    connection.configure(account['host'], account['user'], key, known, config, account['port'],
                         account.get('host_key_alias'))
    return config


def roll_asker(given=None):
    """Ask for the roll number only when a lab needs it; remember it afterwards."""
    def ask():
        roll = given or common.read_marker('current_roll') or input('Enter your roll number: ').strip()
        if not common.valid_id(roll):
            raise ValueError('Enter your roll number using 1–24 letters/digits, hyphens or underscores.')
        ask.value = roll
        return roll
    ask.value = None
    return ask


def start(root, lab, access, roll_number=None):
    root = common.plain_path(Path(root).resolve())
    config = configure_access(root, access)
    prepare = lab.hook('prepare')
    ask = roll_asker(roll_number)
    if prepare:
        folder = prepare(root, ask, config)
    else:
        folder = common.plain_path(root / 'lab-work' / lab.id)
        folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    if ask.value:
        common.write_marker('current_roll', ask.value)
    common.write_marker('current_lab', lab.id)
    common.write_marker('current_dir', str(folder))
    return folder


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lab', nargs='?', help='Lab to open, for example lab5 (asks when omitted)')
    parser.add_argument('--lab', dest='lab_option', help=argparse.SUPPRESS)
    parser.add_argument('--roll-number')
    parser.add_argument('--access-zip', type=Path, help='Your individual emailed access ZIP')
    args = parser.parse_args()
    root = common.ROOT
    try:
        lab = labs.choose(args.lab or args.lab_option)
        # Legacy personal laptop kits still contain access/; Codespaces import a
        # separate access-only ZIP into private storage outside Git.
        access = (root / 'access' if (root / 'access').is_dir() and args.access_zip is None
                  else access_import.install(root, args.access_zip))
        folder = start(root, lab, access, args.roll_number)
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        sys.exit('Setup stopped: ' + str(error))
    except (EOFError, KeyboardInterrupt):
        sys.exit('\nSetup stopped.')
    print(f'{lab.title} is ready.')
    print('Local folder: ' + str(folder))
    print('Open ' + str(lab.book.relative_to(root)) + ' and follow the instructions.')


if __name__ == '__main__':
    main()
