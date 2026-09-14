"""Opt-in stable prompt guidance; no hooks, tools, messages or model calls."""
from pathlib import Path


SECTION_ID = 'race-status-header.guidance'
MAX_CHARS = 4000


def register(ctx):
    """Read public instructions once; Hermes owns new-session prompt freezing."""
    add_section = getattr(ctx, 'register_system_prompt_section', None)
    if not callable(add_section):
        raise RuntimeError(
            'race-status-header requires register_system_prompt_section; '
            'use the manual skill on older Hermes versions.')
    text = (Path(__file__).parent / 'SKILL.md').read_text(encoding='utf-8')
    _, body = text[4:].split('\n---\n', 1)
    guidance = (
        'Convenção opt-in deste perfil. Aplicar nas mensagens normais, respeitando '
        'as exceções abaixo. Se a pessoa pedir para parar de usar os cabeçalhos '
        'nesta conversa, respeitar a partir desse turno; não editar o passado.\n\n'
        + '## Procedimento\n'
        + body.split('\n## Procedimento\n', 1)[1].split('\n## Verificação\n', 1)[0].strip()
    )
    if len(guidance) > MAX_CHARS:
        raise ValueError('race-status-header guidance exceeds its prompt budget')
    add_section(SECTION_ID, guidance, position='after_memory', max_chars=MAX_CHARS)
