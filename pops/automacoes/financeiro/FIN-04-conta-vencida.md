---
id: FIN-04
titulo: Conta Vencida - Task de Revisão
departamento: Financeiro
space: Gestão Administrativa
list: Contas a Pagar
list_id: "901305573710"
ferramenta: ClickUp Nativo
prioridade: ALTA
tempo_setup: 5 min
economia_mensal: 2h
status: pendente
---

# FIN-04 — Conta Vencida → Task de Revisão

## O que faz
Quando o due date de uma conta a pagar passa sem o status "pago", adiciona a tag `atrasado`, sobe para prioridade Urgente e cria uma nova task de revisão na mesma list.

## Por que é importante
Garante que nenhuma conta atrasada passe despercebida — cria um item de ação explícito para tratar o atraso.

## Como criar no ClickUp

1. Abrir o Space **Gestão Administrativa**
2. Ir em **Automations**
3. Clicar em **+ Add Automation**
4. Configurar:

```
TRIGGER:
  Tipo: Due date
  Condição: Due date passes (vencimento passou)

CONDITION:
  Status is not "pago"

ACTIONS:
  1. Change priority → Urgent
  2. Add tag → "atrasado"
  3. Post a comment → "🔴 VENCIDO: Esta conta está atrasada. Verificar se foi paga e calcular juros/multa."
  4. Create task →
      Name: "🔴 REVISAR: [task name] (ATRASADO)"
      List: Contas a Pagar
      Priority: Urgent
      Tags: revisar, atrasado
```

5. Nomear: `[FIN-04] Conta vencida - Task de revisão`
6. Ativar e testar

## Resultado esperado
- Tag `atrasado` adicionada na task original
- Nova task de revisão criada automaticamente
- Comentário de alerta postado

## Observações
- Trabalha em conjunto com FIN-01, FIN-02, FIN-03
- A task de revisão deve ser tratada imediatamente pelo responsável financeiro
