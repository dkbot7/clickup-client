---
id: PRJ-06
titulo: Risco "Alto" → Criar Plano de Mitigação
departamento: Projetos
space: Projetos
list: Projetos Internos
list_id: "901307128249"
ferramenta: ClickUp Nativo
prioridade: MÉDIA
tempo_setup: 5 min
economia_mensal: 2h
status: pendente
---

# PRJ-06 — Risco "Alto" → Criar Plano de Mitigação

## O que faz
Quando o custom field **"Risco"** de um projeto é definido como **"Alto"**, cria automaticamente uma task de plano de mitigação e notifica o gestor.

## Por que é importante
Garante que riscos críticos sejam tratados imediatamente com um item de ação concreto.

## Como criar no ClickUp

1. Abrir o Space **Projetos**
2. Ir em **Automations**
3. Clicar em **+ Add Automation**
4. Configurar:

```
TRIGGER:
  Tipo: Custom field changes
  Campo: Risco
  Condição: Changes to "Alto"

ACTIONS:
  1. Add tag → "risco-alto"
  2. Post comment → "🔴 RISCO ALTO identificado! Plano de mitigação criado automaticamente."
  3. Create task →
      Name: "⚠️ PLANO DE MITIGAÇÃO: [task name]"
      List: Projetos Internos
      Priority: High
      Description: "Risco alto identificado neste projeto. Ações necessárias:\n1. Identificar causa raiz\n2. Definir ações corretivas\n3. Atribuir responsável\n4. Definir prazo de resolução"
      Tags: risco, mitigacao
```

5. Nomear: `[PRJ-06] Risco Alto → Plano de mitigação`
6. Ativar e testar

## Resultado esperado
- Tag `risco-alto` adicionada visualmente
- Task de plano de mitigação criada automaticamente
- Comentário de alerta postado

## Observações
- O custom field "Risco" deve existir com opções: Baixo, Médio, Alto
- Se não existir, criar antes de configurar a automação
