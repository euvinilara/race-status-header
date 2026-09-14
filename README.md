# race-status-header

**Autoria:** Vinicius Lara (euvinilara), com Hermes Agent.
**Versão:** 0.1.0 — convenção visual e comportamental para conversas com agentes.
**Licença:** MIT. Consulte [LICENSE](LICENSE).
**Repositório:** https://github.com/euvinilara/race-status-header

> Você não deveria precisar perguntar ao agente se ele está trabalhando ou esperando por você.

## Origem e proposta

Vini ficou sem saber se Kairos estava executando ou aguardando uma resposta.
Propôs um cabeçalho com sinaleiro e depois a metáfora de corrida. A proposta
transforma essa ambiguidade em estado, próxima ação e responsável visíveis,
sem fazer da corrida uma cobrança. Não inclui transcrições ou dados privados.

A primeira linha acompanha cada mensagem textual da conversa, salvo formatos
exatos, schemas de ferramentas e instruções superiores. O estado depende de
evidências: não é telemetria, monitor, processo ou garantia de progresso.
Sem imagens, integrações de mensageria, APIs ou alterações de infraestrutura.
Sem dependências de monitoramento; o helper opcional usa somente Python padrão.

## Exemplos rápidos (sintéticos)

| Bom | Por quê |
|---|---|
| 🟢 ⚑ Executando · Próximo: conferir arquivo · Vez: Kairos | A chamada de leitura começa nesta mesma resposta. |
| 🟡 ⚑ Aguardando você · Próximo: escolher opção · Vez: você | Uma decisão humana impede continuar. |
| 🔴 ⚑ Bloqueado · Próximo: renovar acesso · Vez: você | Acesso expirado foi confirmado; não esconder o impedimento. |
| 🏁 Concluído · Entrega: rascunho revisado | Só o rascunho foi concluído, não sua publicação. |
| 💬 Em conversa | Exploração sem transformar tudo em tarefa. |

**Ruins:** “Concluído” após mero despacho; “Executando” só porque apareceu
`running`; “Aguardando você” quando o agente pode continuar sozinho; sinalizar
só com cor; dizer “projeto concluído” quando apenas uma etapa terminou.

Em paralelo, manter um estado focal e uma nota, se relevante: “Rascunho entregue.
Outra frente: execução confirmada, resultado ainda não verificado.” Não chamar
esse conjunto de projeto concluído nem inventar notificações futuras.

Círculo colorido + ⚑ + palavras é intencional: bandeiras verdes/amarelas não
existem como emojis portáteis. A cor não é o único canal de informação.

`examples.json` contém cenários bons e ruins, com evidências **declaradas para
teste**, não observações reais. O helper verifica a coerência dessas declarações;
não compreende texto livre nem valida comportamento de um agente real.

## Instalação manual no Hermes

Publicar a skill não a instala nem altera seu agente automaticamente.

Consulte a [documentação oficial do Hermes](https://hermes-agent.nousresearch.com/docs/)
e confirme o diretório de skills do **perfil desejado**. Copie manualmente o
pacote para uma pasta `race-status-header` nesse diretório, preservando SKILL.md
e seus arquivos auxiliares. Abrir uma nova sessão e solicitar o carregamento
da skill pelo nome. Não alterar outro perfil nem prometer ativação global ou
persistência automática. Este texto não executa instalação.

## Teste local opcional

No diretório deste pacote, pelo terminal:

```sh
python3 -B -m unittest -v test_static.py
```

No Hermes: `terminal(command="python3 -B -m unittest -v test_static.py")`, com
o diretório de trabalho apontando para o pacote.

Arquivos: `SKILL.md`, este `README.md`, `examples.json`, `test_static.py`.
O teste confere frontmatter no subconjunto usado aqui, formato dos cabeçalhos,
fixtures e rejeições esperadas. Não é parser YAML geral nem validador oficial
Hermes. Não faz rede, não chama modelo e não modifica o runtime. Sucesso local
não demonstra execução em produção, instalação ou conformidade permanente.
