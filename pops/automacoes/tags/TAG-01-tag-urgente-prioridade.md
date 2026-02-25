---
id: TAG-01
titulo: Tag "urgente" → Prioridade Urgente + Notificar
departamento: Geral
space: Todos
ferramenta: ClickUp Nativo
prioridade: ALTA
tempo_setup: 2 min
economia_mensal: 30 min
status: pendente
---

# TAG-01 — Tag "urgente" → Prioridade Urgente + Notificar

## O que faz
Quando a tag **`urgente`** é adicionada a qualquer task, muda automaticamente a prioridade para **Urgente** e posta um comentário de alerta.

## Por que é importante
Garante consistência — adicionar a tag urgente tem sempre o mesmo efeito em qualquer space ou list.

## Como criar no ClickUp

1. Abrir o Space desejado
2. Ir em **Automations**
3. Clicar em **+ Add Automation**
4. Configurar:

```
TRIGGER:
  Tipo: Tag added
  Condição: Tag "urgente" is added

ACTIONS:
  1. Change priority → Urgent
  2. Post comment → "🚨 Tag URGENTE adicionada — prioridade atualizada para Urgente."
```

5. Nomear: `[TAG-01] Tag urgente → Prioridade urgente`
6. Ativar em todos os spaces relevantes

## Observações
- Criar essa automação em cada space onde se usa a tag "urgente"
- Ou criar no nível do Workspace se o ClickUp permitir
- Simples, rápida de configurar e alto impacto visual
