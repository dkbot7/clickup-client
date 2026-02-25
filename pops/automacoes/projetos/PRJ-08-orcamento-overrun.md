---
id: PRJ-08
titulo: Orçamento Excedido → Alerta
departamento: Projetos
space: Projetos
list: Projetos Internos
list_id: "901307128249"
ferramenta: ClickUp Nativo
prioridade: MÉDIA
tempo_setup: 5 min
economia_mensal: 1h
status: pendente
---

# PRJ-08 — Orçamento Excedido → Alerta

## O que faz
Quando o custom field **"Valor Gasto"** ultrapassa o custom field **"Orçamento"**, adiciona a tag `overrun` e posta um comentário de alerta financeiro.

## Por que é importante
Detecta estouro de orçamento automaticamente, antes que o problema se agrave.

## Como criar no ClickUp

1. Abrir o Space **Projetos**
2. Ir em **Automations**
3. Clicar em **+ Add Automation**
4. Configurar:

```
TRIGGER:
  Tipo: Custom field changes
  Campo: Valor Gasto
  Condição: Greater than field "Orçamento"

ACTIONS:
  1. Add tag → "overrun"
  2. Change priority → High
  3. Post comment → "⚠️ ORÇAMENTO EXCEDIDO! O valor gasto ultrapassou o orçamento previsto. Revisar imediatamente."
```

5. Nomear: `[PRJ-08] Orçamento excedido → Alerta overrun`
6. Ativar e testar

## Resultado esperado
- Tag `overrun` adicionada
- Prioridade sobe para Alta
- Alerta visível para todos os membros

## Observações
- Requer dois custom fields: "Orçamento" e "Valor Gasto" (ambos tipo Currency/Number)
- Criar os campos antes de configurar a automação
- O ClickUp permite comparar campos do mesmo tipo nativo
