---
id: PRJ-07
titulo: Valor > R$50k → Notificar Diretoria
departamento: Projetos
space: Projetos
list: Projetos Internos
list_id: "901307128249"
ferramenta: ClickUp Nativo
prioridade: MÉDIA
tempo_setup: 2 min
economia_mensal: 30 min
status: pendente
---

# PRJ-07 — Valor > R$50k → Notificar Diretoria

## O que faz
Quando o custom field **"Valor"** de um projeto é preenchido com um valor acima de **R$ 50.000**, posta um comentário de alerta e adiciona a tag `alto-valor`.

## Por que é importante
Projetos de alto valor requerem atenção e aprovação especial da diretoria.

## Como criar no ClickUp

1. Abrir o Space **Projetos**
2. Ir em **Automations**
3. Clicar em **+ Add Automation**
4. Configurar:

```
TRIGGER:
  Tipo: Custom field changes
  Campo: Valor
  Condição: Greater than 50000

ACTIONS:
  1. Add tag → "alto-valor"
  2. Post comment → "💰 PROJETO DE ALTO VALOR: R$50k+. Notificar diretoria para aprovação e acompanhamento especial."
```

5. Nomear: `[PRJ-07] Valor > R$50k → Notificar diretoria`
6. Ativar e testar

## Resultado esperado
- Tag `alto-valor` adicionada
- Comentário de alerta postado
- Membros watchers são notificados

## Observações
- O threshold de R$50k pode ser ajustado conforme necessidade
- O campo "Valor" deve ser do tipo **Currency** ou **Number**
