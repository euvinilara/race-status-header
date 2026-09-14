# Changelog

## 0.2.0

- Plugin opt-in por perfil usando `register_system_prompt_section`, com a regra
  pública de `SKILL.md` como fonte única e limite explícito de 4000 caracteres.
- Instalador offline idempotente: copia somente arquivos públicos conhecidos,
  não habilita, não sobrescreve divergências e não altera configuração.
- Ativação/desativação pelas operações nativas do Hermes, sem reiniciar serviços.
- Testes de registro, instalação e probe isolado com loader/manager reais.
- Limites explícitos: processos já iniciados não recebem hot-load; conversas
  abertas adotam ou suspendem por instrução futura. Sem garantia de modelo,
  delivery, cache do provedor ou E2E de sessões persistidas.

## 0.1.0

- Convenção visual/comportamental, licença MIT e fixtures estáticas sintéticas.
