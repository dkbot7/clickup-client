---
id: TAG-02
titulo: Tag "interno" → Valor = R$ 0
departamento: Projetos
space: Projetos
list: Projetos Internos
list_id: "901307128249"
ferramenta: ClickUp Nativo
prioridade: MÉDIA
tempo_setup: 2 min
economia_mensal: 15 min
status: pendente
---

# TAG-02 — Tag "interno" → Valor = R$ 0

## O que faz
Quando a tag **`interno`** é adicionada a uma task de projeto, define automaticamente o custom field **"Valor"** como **R$ 0**.

## Por que é importante
Projetos internos não geram receita — essa automação garante que o campo financeiro fique correto sem preenchimento manual.

## Como criar no ClickUp

1. Abrir o Space **Projetos**
2. Ir em **Automations**
3. Clicar em **+ Add Automation**
4. Configurar:

```
TRIGGER:
  Tipo: Tag added
  Condição: Tag "interno" is added

ACTIONS:
  1. Set custom field "Valor" → 0
  2. Post comment → "ℹ️ Projeto interno — valor definido como R$ 0 automaticamente."
```

5. Nomear: `[TAG-02] Tag interno → Valor R$0`
6. Ativar e testar

## Resultado esperado
- Campo "Valor" zerado automaticamente ao marcar como interno
- Sem necessidade de preencher manualmente

## Observações
- O campo "Valor" deve ser do tipo Currency ou Number
- Se o campo não existir, criar antes de configurar a automação
