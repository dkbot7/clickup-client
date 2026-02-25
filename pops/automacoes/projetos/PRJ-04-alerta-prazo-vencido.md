---
id: PRJ-04
titulo: Prazo Vencido → Tag + Task de Revisão
departamento: Projetos
space: Projetos
list: Projetos Internos
list_id: "901307128249"
ferramenta: ClickUp Nativo
prioridade: ALTA
tempo_setup: 5 min
economia_mensal: 2h
status: pendente
---

# PRJ-04 — Prazo Vencido → Tag Atrasado + Task de Revisão

## O que faz
Quando o due date de uma task de projeto passa sem o status `concluído`, adiciona a tag `atrasado`, sobe para prioridade Urgente e cria uma task de revisão.

## Por que é importante
Garante que projetos atrasados sejam tratados imediatamente com um item de ação explícito.

## Como criar no ClickUp

1. Abrir o Space **Projetos**
2. Ir em **Automations**
3. Clicar em **+ Add Automation**
4. Configurar:

```
TRIGGER:
  Tipo: Due date
  Condição: Due date passes

CONDITION:
  Status is not "concluído"

ACTIONS:
  1. Change priority → Urgent
  2. Add tag → "atrasado"
  3. Post a comment → "🔴 PRAZO VENCIDO: Este projeto está atrasado. Criar plano de recuperação."
  4. Create task →
      Name: "🔴 REVISAR ATRASO: [task name]"
      List: Projetos Internos
      Priority: Urgent
      Tags: revisar, atrasado
```

5. Nomear: `[PRJ-04] Prazo vencido → Alerta + Revisão`
6. Ativar e testar

## Resultado esperado
- Tag `atrasado` adicionada visualmente
- Prioridade urgente (vermelho)
- Task de revisão criada automaticamente

## Observações
- Trabalha em conjunto com PRJ-05 (alertas preventivos)
- PRJ-05 é preventivo, PRJ-04 é reativo (já atrasou)
