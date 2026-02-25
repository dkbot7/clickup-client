---
id: WKF-01
titulo: Status "concluído" → Arquivar + Celebração
departamento: Geral
space: Todos
ferramenta: ClickUp Nativo
prioridade: BAIXA
tempo_setup: 2 min
economia_mensal: 15 min
status: pendente
---

# WKF-01 — Status "concluído" → Arquivar + Celebração

## O que faz
Quando uma task tem o status alterado para **"concluído"**, posta um comentário de celebração e opcionalmente arquiva a task após X dias.

## Por que é importante
Encerra o ciclo de vida da task de forma limpa e mantém o workspace organizado.

## Como criar no ClickUp

```
TRIGGER:
  Tipo: Status changes
  Condição: Changes to "concluído"

ACTIONS:
  1. Post comment → "🎉 Task concluída! Ótimo trabalho."
  2. [Opcional] Archive task after 7 days
```

Nome: `[WKF-01] Status concluído → Celebração`

## Observações
- O arquivamento automático é opcional — evitar se a task precisar ficar visível para referência
- Simples e rápida de configurar
