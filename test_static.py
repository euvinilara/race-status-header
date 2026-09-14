"""Contrato estático: evidências das fixtures são sintéticas, não telemetria."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent
FIXTURES = json.loads((ROOT / 'examples.json').read_text(encoding='utf-8'))


def static_valid(header, evidence):
    """Checa formato e flags declaradas; não infere verdade do texto livre."""
    if '\n' in header or len(header) > 160:
        return False
    action = re.fullmatch(
        r'(🟢 ⚑ Executando|🟡 ⚑ Aguardando você|🔴 ⚑ Bloqueado)'
        r' · Próximo: ([^·\n]+) · Vez: ([^·\n]+)', header)
    if action:
        state, next_action, owner = action.groups()
        if not next_action.strip() or not owner.strip():
            return False
        if state.startswith('🟢'):
            return bool(evidence.get('action_confirmed') or
                        evidence.get('tool_same_response'))
        if state.startswith('🟡'):
            return bool(evidence.get('human_required') and
                        not evidence.get('block_confirmed') and owner == 'você')
        return bool(evidence.get('block_confirmed'))
    if re.fullmatch(r'🏁 Concluído · Entrega: [^·\n]+', header):
        return bool(header.split(': ', 1)[1].strip() and
                    evidence.get('verified') and
                    evidence.get('agent_pending') is False and
                    not (evidence.get('mock_only') and
                         evidence.get('claims_production')))
    return header == '💬 Em conversa' and evidence.get('exploration') is True


class StaticContract(unittest.TestCase):
    def test_frontmatter(self):
        text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        self.assertTrue(text.startswith('---\n'))
        front, body = text[4:].split('\n---\n', 1)
        # Leitor restrito ao frontmatter conhecido; não parser YAML geral.
        fields = dict(re.findall(r'^([a-z_]+): (.+)$', front, re.M))
        self.assertEqual(fields['name'], 'race-status-header')
        self.assertRegex(fields['name'], r'^[a-z][a-z0-9-]{0,63}$')
        self.assertLessEqual(len(fields['description']), 60)
        self.assertTrue(fields['description'].endswith('.'))
        self.assertNotIn(':', fields['description'])
        self.assertEqual(fields['version'], '0.2.0')
        self.assertEqual(fields['author'],
                         'Vinicius Lara (euvinilara), Hermes Agent')
        self.assertEqual(fields['license'], 'MIT')
        self.assertEqual(fields['platforms'], '[linux, macos, windows]')
        self.assertIn('metadata:\n  hermes:\n    tags:', front)
        self.assertIn('    related_skills: []', front)
        self.assertTrue(body.strip())
        self.assertLessEqual(len(text), 100000)

    def test_fixture_inventory(self):
        ids = [case['id'] for case in FIXTURES]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), 16)
        self.assertEqual(sum(case['valid'] for case in FIXTURES), 7)
        self.assertTrue(all(case['explanation'] for case in FIXTURES))

    def test_malformed_headers(self):
        for header in ('🟢', '🏁 Concluído', '\n💬 Em conversa',
                       '🔴 ⚑ Bloqueado · Próximo: recuperar acesso · Vez: ',
                       '🟢 ⚑ Executando · Próximo:   · Vez: Kairos'):
            with self.subTest(header=header):
                self.assertFalse(static_valid(header, {'action_confirmed': True,
                                                       'block_confirmed': True}))

    def test_package_scope(self):
        self.assertEqual({p.name for p in ROOT.iterdir() if not p.name.startswith('.') and p.name != '__pycache__'},
                         {'SKILL.md', 'README.md', 'examples.json', 'test_static.py', 'LICENSE',
                          '__init__.py', 'plugin.yaml', 'install.py', 'test_plugin.py',
                          'test_install.py', 'probe_runtime.py', 'CHANGELOG.md'})
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('**Licença:** MIT', readme)
        self.assertIn('github.com/euvinilara/race-status-header', readme)
        self.assertIn('Permission is hereby granted', (ROOT / 'LICENSE').read_text())
        self.assertIn('Não é parser YAML geral', readme.replace('não é', 'Não é'))


def fixture_test(case):
    def test(self):
        self.assertEqual(static_valid(case['header'], case['evidence']),
                         case['valid'], case['explanation'])
    return test


for fixture in FIXTURES:
    setattr(StaticContract, 'test_example_' + fixture['id'], fixture_test(fixture))

if __name__ == '__main__':
    unittest.main(verbosity=2)
