"""Offline registration tests; these do not test a model's compliance."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent


class PluginContract(unittest.TestCase):
    def test_registers_public_guidance(self):
        path = ROOT / '__init__.py'
        self.assertTrue(path.is_file(), 'plugin entry point is missing')
        spec = importlib.util.spec_from_file_location('race_test_plugin', path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        class Context:
            def register_system_prompt_section(self, id, content, **kwargs):
                self.section = (id, content, kwargs)

        ctx = Context()
        module.register(ctx)
        id, content, options = ctx.section
        self.assertEqual(id, 'race-status-header.guidance')
        self.assertIn('🟢 ⚑ Executando', content)
        self.assertIn('schemas de ferramentas prevalecem', content)
        self.assertIn('parar de usar', content)
        self.assertNotIn('version:', content)
        self.assertEqual(options['position'], 'after_memory')
        self.assertLessEqual(len(content), options['max_chars'])
        self.assertLessEqual(options['max_chars'], 4000)
        with self.assertRaisesRegex(RuntimeError, 'register_system_prompt_section'):
            module.register(object())


if __name__ == '__main__':
    unittest.main()
