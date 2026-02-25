---
id: FIN-03
titulo: Alerta de Vencimento - 1 Dia Antes
departamento: Financeiro
space: Gestão Administrativa
list: Contas a Pagar
list_id: "901305573710"
ferramenta: ClickUp Nativo
prioridade: ALTA
tempo_setup: 5 min
economia_mensal: 30 min
status: pendente
---

# FIN-03 — Alerta de Vencimento 1 Dia Antes

## O que faz
Quando uma conta a pagar vence **amanhã**, sobe a prioridade para **Urgente**, adiciona a tag `muito-urgente` e posta comentário crítico.

## Por que é importante
Última camada de alerta antes do vencimento — prioridade máxima para garantir que o pagamento seja feito.

## Como criar no ClickUp

1. Abrir o Space **Gestão Administrativa**
2. Ir em **Automations**
3. Clicar em **+ Add Automation**
4. Configurar:

```
TRIGGER:
  Tipo: Due date
  Condição: 1 day before due date

CONDITION:
  Status is not "pago"

ACTIONS:
  1. Change priority → Urgent
  2. Add tag → "muito-urgente"
  3. Post a comment → "🚨 MUITO URGENTE: Esta conta vence AMANHÃ! AÇÃO IMEDIATA NECESSÁRIA."
```

5. Nomear: `[FIN-03] Alerta 1 dia - Contas a Pagar`
6. Ativar e testar

## Resultado esperado
- Prioridade muda para Urgente (fica vermelho)
- Tag `muito-urgente` adicionada
- Comentário crítico visível

## Observações
- Terceira e última camada de alerta preventivo
- Complementada por FIN-04 (já vencida)
