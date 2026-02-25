---
id: PRJ-05
titulo: Alertas Progressivos 7/3/1 Dias Antes do Prazo
departamento: Projetos
space: Projetos
list: Projetos Internos
list_id: "901307128249"
ferramenta: ClickUp Nativo
prioridade: ALTA
tempo_setup: 10 min
economia_mensal: 3h
status: pendente
---

# PRJ-05 — Alertas Progressivos 7/3/1 Dias Antes do Prazo

## O que faz
Cria três camadas de alertas antes do vencimento de um projeto, escalando gradualmente a urgência.

## Por que é importante
Evita surpresas — o gestor é avisado com antecedência suficiente para reagir antes do prazo vencer.

## Como criar no ClickUp

Criar **3 automações separadas**:

### Automação 1 — 7 dias antes
```
TRIGGER: Due date, 7 days before
CONDITION: Status is not "concluído"
ACTIONS:
  1. Add tag → "vencendo-em-breve"
  2. Post comment → "⚠️ Este projeto vence em 7 dias. Verificar progresso."
```
Nome: `[PRJ-05a] Alerta 7 dias - Projetos`

### Automação 2 — 3 dias antes
```
TRIGGER: Due date, 3 days before
CONDITION: Status is not "concluído"
ACTIONS:
  1. Change priority → High
  2. Add tag → "urgente"
  3. Post comment → "🔥 Este projeto vence em 3 dias! Prioridade alta."
```
Nome: `[PRJ-05b] Alerta 3 dias - Projetos`

### Automação 3 — 1 dia antes
```
TRIGGER: Due date, 1 day before
CONDITION: Status is not "concluído"
ACTIONS:
  1. Change priority → Urgent
  2. Add tag → "muito-urgente"
  3. Post comment → "🚨 Este projeto vence AMANHÃ! Ação imediata necessária."
```
Nome: `[PRJ-05c] Alerta 1 dia - Projetos`

## Resultado esperado
- Três camadas de alertas visíveis na task
- Prioridade escalada automaticamente
- Gestor sempre informado com antecedência

## Observações
- Estrutura idêntica às automações financeiras (FIN-01, FIN-02, FIN-03)
- Pode ser replicada para outros spaces com due dates importantes
