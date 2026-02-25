---
id: FIN-01
titulo: Alerta de Vencimento - 7 Dias Antes
departamento: Financeiro
space: Gestão Administrativa
list: Contas a Pagar
list_id: "901305573710"
ferramenta: ClickUp Nativo
prioridade: ALTA
tempo_setup: 5 min
economia_mensal: 1h
status: pendente
---

# FIN-01 — Alerta de Vencimento 7 Dias Antes

## O que faz
Quando uma conta a pagar está a **7 dias do vencimento**, adiciona automaticamente a tag `vencendo-em-breve` e posta um comentário na task.

## Por que é importante
Garante visibilidade antecipada de vencimentos, evitando atrasos e juros.

## Como criar no ClickUp

1. Abrir o Space **Gestão Administrativa**
2. Ir em **Automations** (ícone de raio no menu lateral)
3. Clicar em **+ Add Automation**
4. Configurar:

```
TRIGGER:
  Tipo: Due date
  Condição: 7 days before due date

CONDITION:
  Status is not "pago"

ACTIONS:
  1. Add tag → "vencendo-em-breve"
  2. Post a comment → "⚠️ ATENÇÃO: Esta conta vence em 7 dias!"
```

5. Nomear a automação: `[FIN-01] Alerta 7 dias - Contas a Pagar`
6. Ativar e testar

## Resultado esperado
- Tag `vencendo-em-breve` aparece na task
- Comentário visível para todos os membros
- Notificação para assignee e watchers

## Observações
- Essa é a primeira camada de alerta (mais cedo)
- Complementada por FIN-02 (3 dias) e FIN-03 (1 dia)
- Não exige integração externa
