#!/usr/bin/env python3
"""Small helpers shared by every lab's Codespace tooling."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
CONNECTION = ROOT / '.connection'
SSH_CONFIG = CONNECTION / 'ssh_config'


def valid_id(value):
    return re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,23}', value) is not None


def plain_path(path):
    path = Path(path).absolute()
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('A lab path contains a symbolic link. Use a real directory.')
    return path


def ssh_command(config=SSH_CONFIG):
    return ['ssh', '-F', str(Path(config).resolve()), '-o', 'BatchMode=yes',
            '-o', 'ConnectTimeout=12', 'lab-server']


def read_marker(name):
    """Read a one-line private marker in .connection/, or None."""
    path = plain_path(CONNECTION / name)
    if not path.exists():
        return None
    if not path.is_file():
        raise ValueError('Invalid local setup marker. Ask your instructor for help.')
    return path.read_text(encoding='utf-8').strip() or None


def write_marker(name, value):
    path = plain_path(CONNECTION / name)
    if path.exists() and not path.is_file():
        raise ValueError('Invalid local setup marker. Ask your instructor for help.')
    path.write_text(value + '\n', encoding='utf-8')
    path.chmod(0o600)
