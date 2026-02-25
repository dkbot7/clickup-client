---
id: COM-01
titulo: Lembrete de Reunião 24h Antes via WhatsApp
departamento: Comercial
space: Comercial
list: Agenda Comercial / Sessão Estratégica
list_ids:
  agenda_comercial: "901305749631"
  sessao_estrategica: "901305749633"
ferramenta: Make + Interakt (WhatsApp)
prioridade: ALTA
tempo_setup: 30 min
economia_mensal: 2h
status: pendente
dependencias:
  - Conta Interakt configurada
  - INTERAKT_API_KEY cadastrado como secret no GitHub
  - Custom field "WhatsApp" preenchido nas tasks
  - Custom field "Agendamento" preenchido nas tasks
---

# COM-01 — Lembrete de Reunião 24h Antes via WhatsApp

## O que faz
24 horas antes de uma reunião agendada, envia automaticamente uma mensagem WhatsApp para o contato com lembrete amigável da reunião.

## Por que é importante
Reduz no-shows e garante que o cliente esteja preparado para a reunião.

## Mensagem enviada

```
Olá! 👋

Lembrete: Você tem uma reunião marcada para *amanhã*!

📅 *[Nome da Reunião]*
🕐 [Data] às [Hora]
🔗 Link: [Meeting URL se disponível]

Nos vemos lá!
```

## Pré-requisitos no ClickUp

As tasks das lists devem ter os seguintes custom fields preenchidos:
- **WhatsApp** — número do contato (ex: `5511999999999`)
- **Agendamento** — data e hora da reunião (tipo Date)
- **Meeting URL** — link da reunião (opcional)

## Como funciona (script já criado)

O script `automation/commercial_reminders.py` já implementa essa lógica.

O workflow GitHub Actions (`commercial-reminders.yml`) roda a cada 1 hora e verifica reuniões no intervalo de **23.5h a 24.5h** antes do agendamento.

## Como ativar

1. Configurar conta no **Interakt** (app.interakt.ai)
2. Obter `INTERAKT_API_KEY` e `INTERAKT_API_URL`
3. Cadastrar os secrets no GitHub:
   - `INTERAKT_API_KEY`
   - `INTERAKT_API_URL`
   - `CUSTOM_FIELD_WHATSAPP` (ID do custom field)
   - `CUSTOM_FIELD_AGENDAMENTO` (ID do custom field)
4. Descomentar o `schedule` no arquivo `.github/workflows/commercial-reminders.yml`

## Observações
- Complementado por COM-02 (lembrete 1h antes)
- Requer Interakt — plataforma paga de WhatsApp Business API
- Script Python já está pronto em `automation/commercial_reminders.py`
