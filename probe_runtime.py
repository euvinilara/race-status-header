"""Offline integration probe using a supplied Hermes checkout and its Python.

Only temporary profiles are written. No model or real CLI/gateway turns run.
Internal imports below are test adapters, not dependencies of the plugin.
"""
import argparse
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parent
NAME = 'race-status-header'
MARKER = 'Convenção opt-in deste perfil.'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime-source', required=True, type=Path)
    args = parser.parse_args()
    source = args.runtime_source.resolve()
    if not (source / 'run_agent.py').is_file():
        parser.error('--runtime-source must point to a Hermes checkout')
    sys.path.insert(0, str(source))
    with tempfile.TemporaryDirectory(prefix='race-runtime-') as tmp:
        root = Path(tmp)
        home = root / 'profile'
        home.mkdir()
        # Do not inherit real profile selection, credentials or project plugins.
        env = {key: os.environ[key] for key in ('PATH', 'SYSTEMROOT', 'LANG') if key in os.environ}
        env.update(HOME=str(root), HERMES_HOME=str(home), PYTHONPATH=str(source),
                   HERMES_ENABLE_PROJECT_PLUGINS='false', HERMES_SAFE_MODE='false',
                   PYTHONDONTWRITEBYTECODE='1')
        with patch.dict(os.environ, env, clear=True), patch(
            'socket.socket.connect', side_effect=AssertionError('Network forbidden in offline probe')
        ):
            previous_cwd = Path.cwd()
            os.chdir(root)
            try:
                result = exercise(source, home, root)
            finally:
                os.chdir(previous_cwd)
        print(json.dumps(result, ensure_ascii=False, indent=2))


def exercise(source, home, root):
    import yaml
    from hermes_cli import plugins
    from hermes_cli.plugins import PluginManager
    from agent.system_prompt import build_system_prompt
    from run_agent import AIAgent

    def command(*args):
        result = subprocess.run([sys.executable, '-B', *map(str, args)],
                                env=os.environ.copy(), cwd=root,
                                capture_output=True, text=True, timeout=90)
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)
        return result.stdout

    def cli(*args):
        return command('-m', 'hermes_cli.main', 'plugins', *args)

    def config():
        return yaml.safe_load((home / 'config.yaml').read_text(encoding='utf-8'))

    def new_process(enabled):
        # Independent interpreter, real discovery, no AIAgent or network needed.
        command('-c',
                'import sys; from hermes_cli.plugins import PluginManager; '
                'm = PluginManager(); m.discover_and_load(); '
                's = m.render_system_prompt_sections({}); '
                'assert sum(x.id == "race-status-header.guidance" for x in s) == int(sys.argv[1])',
                int(enabled))

    def agent(name):
        return AIAgent(api_key='offline-placeholder', base_url='http://127.0.0.1:1/v1',
                       model='test/model', provider='openrouter', platform='cli',
                       quiet_mode=True, skip_context_files=True, skip_memory=True,
                       session_id=name)

    manager = PluginManager()
    manager.discover_and_load()
    plugins._plugin_manager = manager
    old = agent('existing-synthetic')
    before = build_system_prompt(old)
    history = [{'role': 'user', 'content': 'synthetic input'},
               {'role': 'assistant', 'content': 'synthetic response'}]
    history_before = copy.deepcopy(history)
    assert MARKER not in before

    command(PACKAGE / 'install.py', '--home', home)
    command(PACKAGE / 'install.py', '--home', home)
    installed = home / 'plugins' / NAME
    for name in ('__init__.py', 'plugin.yaml', 'SKILL.md', 'LICENSE'):
        assert (installed / name).read_bytes() == (PACKAGE / name).read_bytes()
    # Files alone must not opt in.
    unenabled = PluginManager()
    unenabled.discover_and_load()
    assert not any(s.id == NAME + '.guidance' for s in unenabled.render_system_prompt_sections({}))
    new_process(False)

    cli('enable', NAME, '--no-allow-tool-override')
    first_config = config()
    cli('enable', NAME, '--no-allow-tool-override')
    assert config() == first_config
    assert config()['plugins']['enabled'].count(NAME) == 1
    new_process(True)
    manager.discover_and_load()
    assert not any(s.id == NAME + '.guidance' for s in manager.render_system_prompt_sections({}))

    fresh_manager = PluginManager()
    fresh_manager.discover_and_load()
    plugins._plugin_manager = fresh_manager
    fresh = agent('new-synthetic')
    fresh_prompt = build_system_prompt(fresh)
    assert fresh_prompt.count(MARKER) == 1, {
        'count': fresh_prompt.count(MARKER),
        'sections': repr(fresh_manager.render_system_prompt_sections({})),
        'plugin_error': getattr(fresh_manager._plugins.get(NAME), 'error', 'not found'),
    }
    assert 'schemas de ferramentas prevalecem' in fresh_prompt
    assert build_system_prompt(old) == before
    assert history == history_before

    cli('disable', NAME)
    disabled_config = config()
    cli('disable', NAME)
    assert config() == disabled_config
    assert NAME not in config()['plugins'].get('enabled', [])
    assert NAME in config()['plugins']['disabled']
    command(PACKAGE / 'install.py', '--home', home)
    assert config() == disabled_config
    new_process(False)
    disabled = PluginManager()
    disabled.discover_and_load()
    plugins._plugin_manager = disabled
    assert MARKER not in build_system_prompt(agent('new-disabled-synthetic'))
    assert build_system_prompt(fresh) == fresh_prompt
    assert build_system_prompt(old) == before
    assert history == history_before
    return {
        'install_idempotent_and_payload_readback': True,
        'files_without_enable_do_not_register': True,
        'enable_disable_idempotent_config_readback': True,
        'fresh_interpreters_observe_opt_in_and_disable': True,
        'reinstall_does_not_reenable': True,
        'already_discovered_manager_does_not_hot_load': True,
        'new_manager_and_agent_receive_guidance_once': True,
        'disabled_new_manager_and_agent_have_no_guidance': True,
        'existing_agent_prompts_and_synthetic_history_unchanged': True,
        'model_calls': 0,
        'real_cli_gateway_turns_or_delivery_tested': False,
        'sqlite_resume_or_provider_cache_tested': False,
        'scope': 'Real loader/manager/AIAgent prompt builder; temporary profiles and synthetic sessions only.'
    }


if __name__ == '__main__':
    main()
