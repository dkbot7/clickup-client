---
id: FIN-02
titulo: Alerta de Vencimento - 3 Dias Antes
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

# FIN-02 — Alerta de Vencimento 3 Dias Antes

## O que faz
Quando uma conta a pagar está a **3 dias do vencimento**, sobe a prioridade para **Alta**, adiciona a tag `urgente` e posta um comentário de alerta.

## Por que é importante
Segunda camada de alerta — deixa a task visualmente destacada e notifica o responsável com urgência.

## Como criar no ClickUp

1. Abrir o Space **Gestão Administrativa**
2. Ir em **Automations**
3. Clicar em **+ Add Automation**
4. Configurar:

```
TRIGGER:
  Tipo: Due date
  Condição: 3 days before due date

CONDITION:
  Status is not "pago"

ACTIONS:
  1. Change priority → High
  2. Add tag → "urgente"
  3. Post a comment → "🔥 URGENTE: Esta conta vence em 3 dias! Providenciar pagamento."
```

5. Nomear: `[FIN-02] Alerta 3 dias - Contas a Pagar`
6. Ativar e testar

## Resultado esperado
- Prioridade da task muda para Alta (fica laranja)
- Tag `urgente` adicionada
- Comentário de alerta postado

## Observações
- Depende de FIN-01 já ter sido criado antes
- Complementada por FIN-03 (1 dia)
