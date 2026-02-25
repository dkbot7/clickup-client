---
id: PRJ-03
titulo: Gestor Preenchido → Auto-assign
departamento: Projetos
space: Projetos
list: Projetos Internos
list_id: "901307128249"
ferramenta: ClickUp Nativo
prioridade: ALTA
tempo_setup: 2 min
economia_mensal: 30 min/semana
status: pendente
---

# PRJ-03 — Gestor de Projetos Preenchido → Auto-assign

## O que faz
Quando o custom field **"Gestor de Projetos"** é preenchido ou alterado, adiciona automaticamente esse usuário como **assignee** da task.

## Por que é importante
Elimina a duplicação de trabalho — define o gestor em um único lugar e o sistema aplica em todos os campos relevantes.

## Como criar no ClickUp

1. Abrir o Space **Projetos**
2. Ir em **Automations**
3. Clicar em **+ Add Automation**
4. Configurar:

```
TRIGGER:
  Tipo: Custom field changes
  Campo: Gestor de Projetos
  Condição: Is set (foi preenchido)

ACTIONS:
  1. Assign to → [value of custom field "Gestor de Projetos"]
  2. Post a comment → "✅ Gestor atribuído como responsável automaticamente."
```

5. Nomear: `[PRJ-03] Gestor preenchido → Auto-assign`
6. Ativar e testar

## Resultado esperado
- Assignee sempre alinhado com o campo Gestor de Projetos
- Zero inconsistências entre campo e assignee

## Observações
- O campo "Gestor de Projetos" deve ser do tipo **People** (não texto)
- Se for dropdown de texto, a automação não consegue adicionar como assignee automaticamente — nesse caso, usar Make
