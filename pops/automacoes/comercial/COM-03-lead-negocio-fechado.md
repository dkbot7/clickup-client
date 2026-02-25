---
id: COM-03
titulo: Lead "Negócio Fechado" → Onboarding Automático
departamento: Comercial
space: Comercial
list: Agenda Comercial
list_id: "901305749631"
ferramenta: ClickUp Nativo + Make (opcional)
prioridade: MÉDIA
tempo_setup: 10 min (nativo) / 45 min (Make completo)
economia_mensal: 30 min/cliente
status: pendente
---

# COM-03 — Lead "Negócio Fechado" → Onboarding Automático

## O que faz
Quando uma task no pipeline comercial tem o status alterado para **"Negócio Fechado"**, dispara automaticamente o processo de onboarding do cliente.

## Por que é importante
Elimina o esquecimento de enviar formulário de contrato e onboarding manualmente — baseado na metodologia AS-IS → TO-BE da Aula 02.

## Fluxo AS-IS (manual atual)
```
1. Reunião de vendas → Cliente diz SIM
2. Mover lead para "Negócio Fechado" manualmente
3. Copiar link do formulário de contrato manualmente
4. Enviar no WhatsApp do cliente manualmente
5. Aguardar cliente preencher
6. Cliente avisa que preencheu
7. Copiar dados para CRM manualmente
8. Notificar jurídico manualmente
```

## Fluxo TO-BE (automatizado)
```
1. Reunião de vendas → Cliente diz SIM
2. Mover lead para "Negócio Fechado"
3. [AUTOMÁTICO] Enviar link do formulário no WhatsApp
4. [AUTOMÁTICO] Dados do formulário → preenchidos no ClickUp
5. [AUTOMÁTICO] Task de onboarding criada para equipe
6. [AUTOMÁTICO] Notificação para jurídico (se aplicável)
```

## Implementação ClickUp Nativo (básico)

```
TRIGGER:
  Tipo: Status changes
  Condição: Changes to "Negócio Fechado"

ACTIONS:
  1. Post comment → "🎉 NEGÓCIO FECHADO! Iniciar processo de onboarding."
  2. Create task →
      Name: "🚀 ONBOARDING: [task name]"
      List: Agenda Comercial
      Priority: High
      Tags: onboarding, novo-cliente
      Assignee: [responsável pelo onboarding]
```

Nome: `[COM-03] Negócio Fechado → Onboarding`

## Implementação Make (completo)

Para envio automático de WhatsApp com link do formulário, usar Make:

```
Cenário Make:
  1. Webhook: ClickUp status → "Negócio Fechado"
  2. Get task data (nome, WhatsApp do cliente)
  3. Enviar WhatsApp → "Parabéns! Aqui está o link do formulário: [link]"
  4. Aguardar preenchimento do formulário (webhook do Liteforms)
  5. Criar task de onboarding no ClickUp com dados preenchidos
```

## Observações
- A versão nativa já agrega muito valor com zero custo
- A versão Make completa requer conta no Make e Interakt/WhatsApp
- Basear nos campos espelhados da Aula 02 (formulário ↔ CRM)
