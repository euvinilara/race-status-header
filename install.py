"""Install reviewed public files into one explicit profile; never enable/restart."""
import argparse
from pathlib import Path
import tempfile

NAME = 'race-status-header'
FILES = ('__init__.py', 'SKILL.md', 'plugin.yaml', 'LICENSE')
SOURCE = Path(__file__).resolve().parent


def install(home):
    """No overwrites: an identical install is a no-op, differences are refused."""
    home = Path(home).expanduser().absolute()
    if any(p.is_symlink() for p in (home, *home.parents)):
        raise ValueError('Profile path must not contain symlinks')
    if not home.is_dir():
        raise ValueError('Select an existing profile directory with --home')
    parent = home / 'plugins'
    target = parent / NAME
    if parent.is_symlink() or target.is_symlink():
        raise ValueError('Plugin paths must not be symlinks')
    payload = {name: (SOURCE / name).read_bytes() for name in FILES}
    if target.exists():
        if not target.is_dir() or any(
            (target / name).is_symlink() or not (target / name).is_file()
            or (target / name).read_bytes() != data
            for name, data in payload.items()
        ):
            raise ValueError('Existing plugin differs; preserve/review it before updating')
        return 'Identical package already installed; activation state unchanged.'
    parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.race-install-', dir=parent) as tmp:
        staged = Path(tmp) / NAME
        staged.mkdir()
        for name, data in payload.items():
            (staged / name).write_bytes(data)
        # Rename only after every file is ready; never merge partial installs.
        staged.rename(target)
    return 'Installed files only; enable explicitly with Hermes for this profile.'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', required=True, help='Existing intended Hermes profile home')
    args = parser.parse_args()
    try:
        print(install(args.home))
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Installation refused: {exc}\n')


if __name__ == '__main__':
    main()
