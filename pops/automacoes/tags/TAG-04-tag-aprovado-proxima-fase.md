---
id: TAG-04
titulo: Tag "aprovado" → Mover para Próxima Fase
departamento: Geral
space: Projetos / Marketing
ferramenta: ClickUp Nativo
prioridade: MÉDIA
tempo_setup: 3 min
economia_mensal: 30 min
status: pendente
---

# TAG-04 — Tag "aprovado" → Mover para Próxima Fase

## O que faz
Quando a tag **`aprovado`** é adicionada a uma task, muda o status para o próximo estágio do workflow automaticamente.

## Por que é importante
Simplifica o processo de aprovação — quem aprova só precisa adicionar a tag, e o sistema cuida do restante.

## Como criar no ClickUp

1. Abrir o Space desejado (Projetos ou Marketing)
2. Ir em **Automations**
3. Clicar em **+ Add Automation**
4. Configurar:

```
TRIGGER:
  Tipo: Tag added
  Condição: Tag "aprovado" is added

ACTIONS:
  1. Change status → [próximo status do workflow, ex: "em produção" ou "publicado"]
  2. Post comment → "✅ Aprovado! Status atualizado automaticamente para a próxima fase."
```

5. Nomear: `[TAG-04] Tag aprovado → Próxima fase`
6. Ativar e testar

## Resultado esperado
- Status avança automaticamente ao aprovar
- Histórico de aprovação registrado via comentário

## Observações
- O status "próxima fase" varia por space — ajustar conforme o workflow de cada list
- Para Marketing: "aprovado" → "agendado para publicação"
- Para Projetos: "aprovado" → "em andamento" ou "entregue"
- Criar uma versão da automação por space com o status correto de cada um
