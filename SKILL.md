---
name: race-status-header
description: Use para sinalizar estado e vez em conversas.
version: 0.2.0
author: Vinicius Lara (euvinilara), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [conversation, status, accessibility]
    related_skills: []
---

# Race Status Header

Convenção comportamental de cabeçalhos baseada em evidências disponíveis.
Não é monitor, processo em segundo plano nem garantia de execução ou progresso.
Sem dependências para uso manual; o plugin opcional exige Hermes compatível.
Instalação e ativação por perfil: consultar `README.md`. Publicar ou copiar a
skill não ativa um processo já iniciado nem reescreve sessões existentes.

## Quando usar

- Quando a pessoa quiser distinguir ação do agente, decisão humana e conversa.
- Aplicar em cada mensagem textual do assistente na conversa enquanto adotada.
- Não usar a metáfora de corrida para cobrar velocidade, produtividade ou resposta.
- Não usar para substituir ferramentas, supervisão ou prova de conclusão.

## Procedimento

1. Identificar o escopo focal e a evidência mais recente. Recibo/despacho não
   confirma execução; `running` não comprova progresso; plano não é ação;
   testes com mocks não demonstram funcionamento em produção.
2. Escolher o estado da tabela e escrever o cabeçalho na primeira linha.
   Antes de ferramenta, Executando é permitido se a ação começar na mesma
   resposta com a chamada correspondente. Nunca prometer e encerrar sem agir.
3. Manter a linha curta para celular. No corpo, dar somente evidência, entrega,
   impedimento ou pergunta necessária. Não transformar exploração em tarefa.
4. Reavaliar a cada mensagem normal; não criar cron, atualizações automáticas,
   mensagens periódicas ou spam para sustentar o cabeçalho.
5. Antes de concluir, conferir entrega específica e ausência de pendência do
   agente naquele escopo. Se a evidência faltar, declarar a incerteza e verificar;
   não inventar progresso, bloqueio ou necessidade de resposta humana.

## Estados e formato

| Estado | Primeira linha | Critério |
|---|---|---|
| Ação | 🟢 ⚑ Executando · Próximo: verificar resultado · Vez: Kairos | Ação real em curso ou iniciada com ferramenta nesta resposta. |
| Decisão | 🟡 ⚑ Aguardando você · Próximo: escolher opção · Vez: você | Decisão ou informação humana realmente necessária; perguntar o mínimo no corpo. |
| Impedimento | 🔴 ⚑ Bloqueado · Próximo: recuperar acesso · Vez: Kairos | Impedimento confirmado; explicar evidência e responsável pela próxima ação. |
| Entrega | 🏁 Concluído · Entrega: rascunho revisado | Entrega delimitada e verificada, sem pendência do agente nesse escopo. |
| Exploração | 💬 Em conversa | Troca de ideias sem tarefa artificial nem obrigação de responder. |

`Próximo` descreve ação concreta; `Vez` identifica seu responsável, não atribui
culpa. Kairos é o nome do agente neste padrão; adaptar ao nome adotado na conversa.
Em bloqueio, não atribuir responsabilidade a terceiros sem evidência; se não
souber quem resolve, a próxima ação pode ser Kairos identificar o responsável.
Se um impedimento técnico confirmado exigir ação humana, usar Bloqueado com
Vez: você; não escondê-lo atrás de Aguardando você.

## Escopo e exceções

- Subtarefa concluída não encerra projeto aberto. Nomear a entrega exata.
- Em paralelo, usar um cabeçalho focal e, apenas se relevante, uma nota curta
  sobre outra frente com estado comprovado. Uma resposta final pode concluir
  o rascunho e informar que outra tarefa segue em background; não concluir tudo.
- Se não há input necessário, não escrever Aguardando você nem insinuar que a
  pessoa precisa esperar ou responder. Agir quando cabe ao agente.
- Instruções superiores, segurança, saída JSON exata, resposta somente código
  e schemas de ferramentas prevalecem. Não inserir cabeçalho nesses formatos.
- Cabeçalho pertence à conversa: não injetar em payloads, arquivos, copy pronta
  ou e-mails para terceiros, salvo pedido explícito. Pode ficar fora do bloco
  de copy quando a resposta permitir prosa.

## Armadilhas visuais

Cor nunca é a única informação: círculo colorido + bandeira comum + texto.
Não existem emojis portáteis de bandeiras verdes/amarelas; não prometer que ⚑
terá cor. Renderização varia por cliente. A bandeira quadriculada marca somente
entrega verificada, não recebimento de pedido. Preferir texto claro a decoração.

## Verificação

Revisar primeira linha, escopo, evidência, responsável e próxima ação. Conferir
se nenhum bloqueio foi escondido e se a pessoa realmente precisa intervir.
Consultar `examples.json` para casos sintéticos bons e ruins.
Helper opcional: `terminal(command="python3 -B -m unittest -v test_static.py")`
no diretório do pacote. Ele valida apenas o contrato estático e fixtures locais;
não integra runtime, não observa ferramentas e não atesta produção.
