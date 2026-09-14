"""Exercise the offline file installer only, never a real profile."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
FILES = ('__init__.py', 'SKILL.md', 'plugin.yaml', 'LICENSE')


class InstallContract(unittest.TestCase):
    def test_requires_explicit_existing_home(self):
        command = [sys.executable, '-B', str(ROOT / 'install.py')]
        self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
        with tempfile.TemporaryDirectory() as tmp:
            absent = Path(tmp) / 'absent'
            result = subprocess.run(command + ['--home', str(absent)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(absent.exists())

    def test_refuses_symlink_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / 'profile'
            home.mkdir()
            outside = Path(tmp) / 'outside'
            outside.mkdir()
            try:
                (home / 'plugins').symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest('symlink creation unavailable')
            command = [sys.executable, '-B', str(ROOT / 'install.py'), '--home', str(home)]
            result = subprocess.run(command, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list(outside.iterdir()), [])

    def test_idempotent_install_without_config_changes(self):
        self.assertTrue((ROOT / 'install.py').is_file(), 'installer is missing')
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / 'profile'
            home.mkdir()
            config = home / 'config.yaml'
            config.write_text('plugins: {}\n', encoding='utf-8')
            command = [sys.executable, '-B', str(ROOT / 'install.py'),
                       '--home', str(home)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            target = home / 'plugins' / 'race-status-header'
            before = {f: (target / f).stat().st_mtime_ns for f in FILES}
            second = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(before, {f: (target / f).stat().st_mtime_ns for f in FILES})
            self.assertEqual(config.read_text(), 'plugins: {}\n')
            for f in FILES:
                self.assertEqual((target / f).read_bytes(), (ROOT / f).read_bytes())
            # Preserve divergent/local work, even if the directory has our name.
            (target / 'SKILL.md').write_text('local work', encoding='utf-8')
            conflict = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(conflict.returncode, 0)
            self.assertEqual((target / 'SKILL.md').read_text(), 'local work')


if __name__ == '__main__':
    unittest.main()
