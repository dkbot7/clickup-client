---
id: WKF-02
titulo: Status "em andamento" → Notificar Assignees
departamento: Geral
space: Todos
ferramenta: ClickUp Nativo
prioridade: BAIXA
tempo_setup: 2 min
economia_mensal: 15 min
status: pendente
---

# WKF-02 — Status "em andamento" → Notificar Assignees

## O que faz
Quando uma task tem o status alterado para **"em andamento"**, posta um comentário notificando os assignees de que a execução começou.

## Por que é importante
Alinha a equipe automaticamente quando uma task entra em execução — sem precisar comunicar manualmente.

## Como criar no ClickUp

```
TRIGGER:
  Tipo: Status changes
  Condição: Changes to "em andamento"

ACTIONS:
  1. Post comment → "▶️ Task iniciada! @assignees — execução em andamento."
```

Nome: `[WKF-02] Status em andamento → Notificar`

## Observações
- Útil principalmente em tasks com múltiplos assignees
- Pode ser expandida para notificar também os watchers
