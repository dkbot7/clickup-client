---
id: COM-02
titulo: Lembrete de Reunião 1h Antes via WhatsApp
departamento: Comercial
space: Comercial
list: Agenda Comercial / Sessão Estratégica
list_ids:
  agenda_comercial: "901305749631"
  sessao_estrategica: "901305749633"
ferramenta: Make + Interakt (WhatsApp)
prioridade: ALTA
tempo_setup: 0 min (já implementado junto com COM-01)
economia_mensal: 1h
status: pendente
dependencias:
  - COM-01 configurado (mesma infraestrutura)
---

# COM-02 — Lembrete de Reunião 1h Antes via WhatsApp

## O que faz
1 hora antes de uma reunião agendada, envia automaticamente uma mensagem WhatsApp urgente para o contato.

## Por que é importante
Lembrete final de curto prazo — garante que o cliente esteja no caminho para a reunião.

## Mensagem enviada

```
⏰ *LEMBRETE IMPORTANTE*

Sua reunião é *daqui a 1 hora*!

📅 [Nome da Reunião]
🕐 [Hora]
🔗 Link: [Meeting URL se disponível]

Até já!
```

## Como funciona

Implementado junto com COM-01 no script `automation/commercial_reminders.py`.

O mesmo workflow verifica reuniões no intervalo de **0.9h a 1.1h** antes do agendamento.

## Como ativar

Ativado automaticamente junto com COM-01 — mesma configuração, mesmo script, mesmo workflow.

## Observações
- Usa a mesma infraestrutura do COM-01
- A tag `lembrete-1h-enviado` é adicionada na task para evitar envio duplicado
- A tag `lembrete-24h-enviado` também é verificada (controle de COM-01)
