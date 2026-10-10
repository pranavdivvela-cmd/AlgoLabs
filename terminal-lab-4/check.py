#!/usr/bin/env python3
"""check_lab: ungraded hints on Codespace files, then official grading on the lab server.

The graded tests run on the server (`check_lab lab4` there) and are not part of
this repository. The hints below only look at files that exist in the Codespace,
which the server cannot see; they never change the score."""
import argparse
import hashlib
import io
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tarfile
import zipfile
import setup

UPLOAD = b'Prepared in my starting terminal\n'
EDITED = UPLOAD + b'Edited on the server\n'
UPLOAD_WINDOWS = UPLOAD.replace(b'\n', b'\r\n')
EDITED_WINDOWS = UPLOAD_WINDOWS + b'Edited on the server\n'
LIMIT = 256 * 1024


def read(root, name):
    """Reject links, special files and oversized files before opening."""
    root = setup.plain_path(root)
    path = setup.plain_path(root / name)
    if not path.is_relative_to(root):
        raise ValueError('Path leaves the lab folder')
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_size > LIMIT:
        raise ValueError('Expected a small regular file')
    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0) | getattr(os, 'O_BINARY', 0))
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode):
            raise ValueError('Expected a regular file')
        data = stream.read(LIMIT + 1)
    if len(data) > LIMIT:
        raise ValueError('File is too large')
    return data


def digest(data):
    return hashlib.sha256(data).hexdigest()


def archive_valid(data, kind, lab_id):
    expected = {'project/' + name: value for name, value in setup.project(lab_id).items()}
    found = {}
    names = set()
    if kind == 'zip':
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            members = archive.infolist()
            if len(members) > 8:
                return False
            for member in members:
                name = member.filename.replace('\\', '/')
                if name in names:
                    return False
                names.add(name)
                mode = member.external_attr >> 16
                if stat.S_ISLNK(mode):
                    return False
                if name.endswith('/'):
                    if name != 'project/' or member.file_size != 0:
                        return False
                elif name not in expected or member.file_size > LIMIT or stat.S_ISLNK(mode):
                    return False
                else:
                    found[name] = archive.read(member)
    else:
        with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as archive:
            for index, member in enumerate(archive):
                if index >= 8 or member.name in names:
                    return False
                names.add(member.name)
                if member.isdir():
                    if member.name.rstrip('/') != 'project':
                        return False
                elif not member.isfile() or member.name not in expected or member.size > LIMIT:
                    return False
                else:
                    found[member.name] = archive.extractfile(member).read(LIMIT + 1)
    return found == expected


def originals_ok(root, lab_id, side):
    return all(read(root, name) == data for name, data in setup.originals(lab_id, side).items())



def available_archives(folder):
    return [(name, kind) for name, kind in [('project.zip', 'zip'), ('project.tar.gz', 'tar')]
            if (folder / name).exists() or (folder / name).is_symlink()]


def evaluate_local(root, lab_id, evidence):
    results = []

    def test(label, operation):
        try:
            ok = bool(operation())
        except (OSError, ValueError, UnicodeError, zipfile.BadZipFile, tarfile.TarError, RuntimeError):
            ok = False
        results.append({'label': label, 'ok': ok})

    test('Starting-machine originals unchanged', lambda: originals_ok(root, lab_id, 'local'))
    test('Starting-machine upload remains the original one-line file', lambda: read(root, 'work/upload.txt') in (UPLOAD, UPLOAD_WINDOWS))
    test('Downloaded upload includes the server edit', lambda: read(root, 'work/recovered/upload.txt') in (EDITED, EDITED_WINDOWS)
         and digest(read(root, 'work/recovered/upload.txt')) == evidence.get('work/upload.txt'))
    test('connected.txt is absent on the starting machine', lambda: not (root / 'connected.txt').exists() and not (root / 'connected.txt').is_symlink())
    test('Local archive is valid and matches an uploaded server archive', lambda: any(
        archive_valid(read(root, 'work/' + name), kind, lab_id)
        and digest(read(root, 'work/' + name)) == evidence.get('challenge-delivery/' + name)
        for name, kind in available_archives(root / 'work')))
    test('Downloaded permissions report matches the server report', lambda: bool(evidence.get('challenge-delivery/permissions-report.txt'))
         and digest(read(root, 'work/permissions-report.txt')) == evidence['challenge-delivery/permissions-report.txt'])
    return results


def ssh_command(config):
    return ['ssh', '-F', str(Path(config).resolve()), '-o', 'BatchMode=yes',
            '-o', 'ConnectTimeout=12', 'lab-server']


EVIDENCE = ('work/upload.txt', 'challenge-delivery/permissions-report.txt',
            'challenge-delivery/project.zip', 'challenge-delivery/project.tar.gz')


def fetch_evidence(config):
    """SHA-256 of the student's own server copies, to compare with local copies."""
    command = 'cd ~/lab-work/lab4 2>/dev/null && sha256sum -- ' + ' '.join(EVIDENCE) + ' 2>/dev/null; true'
    process = subprocess.run(ssh_command(config) + [command], text=True, encoding='utf-8',
                             capture_output=True, timeout=45)
    if process.returncode:
        raise ValueError('Could not reach the server: ' + process.stderr.strip())
    evidence = {}
    for line in process.stdout.splitlines():
        value, _, name = line.partition('  ')
        if name in EVIDENCE and re.fullmatch(r'[0-9a-f]{64}', value):
            evidence[name] = value
    return evidence


def local_hints(root, config):
    root = setup.plain_path(root)
    match = re.fullmatch(rb'LAB_ID=([A-Za-z0-9_-]+)\nDATA_VERSION=lab4-v1\nSIDE=local\n', read(root, 'identity.txt'))
    if not match or not setup.valid_id(match.group(1).decode()):
        raise ValueError('run check_lab from your Codespace Lab 4 folder to see local hints')
    results = evaluate_local(root, match.group(1).decode(), fetch_evidence(config))
    print('Local hints (Codespace files only; not graded):')
    for item in results:
        print(('  PASS: ' if item['ok'] else '  HINT: ') + item['label'])
    print()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, help='Local Lab 4 folder (default: current directory)')
    parser.add_argument('--config', type=Path, default=Path(__file__).resolve().parent.parent / '.connection/ssh_config')
    args = parser.parse_args()
    try:
        local_hints(args.root or Path.cwd(), args.config)
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print('Local hints skipped: ' + str(error) + '\n', file=sys.stderr)
    print('Requesting official grading from the lab server...\n', flush=True)
    try:
        process = subprocess.run(ssh_command(args.config) + ['check_lab lab4'], timeout=120)
    except subprocess.TimeoutExpired:
        print('CHECK: the server did not answer in time. Try again.', file=sys.stderr)
        return 2
    if process.returncode == 255:
        print('CHECK: could not connect to the lab server. Check your connection and try again.', file=sys.stderr)
    return process.returncode


if __name__ == '__main__':
    sys.exit(main())
