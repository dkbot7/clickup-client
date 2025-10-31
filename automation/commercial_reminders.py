"""
Automação: Lembretes Comerciais via WhatsApp
Executa: A cada 1 hora (via GitHub Actions)

Funcionalidade:
- Lembrete 24h antes da reunião
- Lembrete 1h antes da reunião
- Usa custom field "WhatsApp" e "Agendamento"
"""
from src.clickup_api.client import KaloiClickUpClient
from src.integrations.whatsapp_client import InteraktWhatsAppClient
from datetime import datetime, timedelta
import os


# IDs do ClickUp
LIST_ID_AGENDA_COMERCIAL = "901305749631"
LIST_ID_SESSAO_ESTRATEGICA = "901305749633"

# Custom Field IDs
CUSTOM_FIELD_WHATSAPP = "08f6f16e-6425-4806-954f-b78b7abd1e57"
CUSTOM_FIELD_AGENDAMENTO = "6aefbfe5-75af-4fd2-b9ba-2047b40ce82f"
CUSTOM_FIELD_MEETING_URL = "ffb916ff-2f9a-4d00-809f-a82765f08c90"


def send_meeting_reminders():
    """
    Envia lembretes de reuniões via WhatsApp

    Horários:
    - 24h antes: Lembrete amigável
    - 1h antes: Lembrete urgente
    """

    clickup = KaloiClickUpClient()
    whatsapp = InteraktWhatsAppClient()

    print("=" * 70)
    print("ENVIANDO LEMBRETES DE REUNIÕES VIA WHATSAPP")
    print("=" * 70)
    print()

    # Lists a verificar
    lists_to_check = {
        "Agenda Comercial": LIST_ID_AGENDA_COMERCIAL,
        "Sessão Estratégica": LIST_ID_SESSAO_ESTRATEGICA
    }

    lembretes_enviados = {
        "24h": 0,
        "1h": 0,
        "erros": 0
    }

    for list_name, list_id in lists_to_check.items():
        print(f"Verificando: {list_name}")
        print("-" * 70)

        tasks = clickup.get_tasks(
            list_id,
            paginate=True,
            arquivada=False,
            incluir_fechadas=False
        )

        if not tasks:
            print(f"  Sem reuniões agendadas")
            print()
            continue

        print(f"  {len(tasks)} reunião(ões) encontrada(s)")
        print()

        for task in tasks:
            task_id = task['id']
            task_name = task['name']

            # Obter custom fields
            custom_fields = {
                field['id']: field for field in task.get('custom_fields', [])
            }

            # Obter data de agendamento
            agendamento_field = custom_fields.get(CUSTOM_FIELD_AGENDAMENTO)
            if not agendamento_field or not agendamento_field.get('value'):
                print(f"  ⚠️  {task_name}: Sem data de agendamento")
                continue

            # Converter timestamp para datetime
            agendamento_ts = int(agendamento_field['value'])
            meeting_time = datetime.fromtimestamp(agendamento_ts / 1000)

            # Calcular diferença de tempo
            now = datetime.now()
            hours_until = (meeting_time - now).total_seconds() / 3600

            # Obter WhatsApp do cliente
            whatsapp_field = custom_fields.get(CUSTOM_FIELD_WHATSAPP)
            if not whatsapp_field or not whatsapp_field.get('value'):
                print(f"  ⚠️  {task_name}: Sem WhatsApp cadastrado")
                continue

            phone = whatsapp_field['value']

            # Obter link da reunião (opcional)
            meeting_url_field = custom_fields.get(CUSTOM_FIELD_MEETING_URL)
            meeting_url = meeting_url_field.get('value') if meeting_url_field else None

            # Verificar se já foi enviado (via tags)
            current_tags = [tag['name'] for tag in task.get('tags', [])]

            # LEMBRETE 24H ANTES
            if 23.5 <= hours_until <= 24.5 and 'lembrete-24h-enviado' not in current_tags:
                print(f"  📅 Enviando lembrete 24h: {task_name}")

                # Preparar mensagem
                message = f"""Olá! 👋

Lembrete: Você tem uma reunião marcada para *amanhã*!

📅 *{task_name}*
🕐 {meeting_time.strftime('%d/%m/%Y às %H:%M')}"""

                if meeting_url:
                    message += f"\n🔗 Link: {meeting_url}"

                message += "\n\nNos vemos lá!"

                # Enviar WhatsApp
                result = whatsapp.send_message(phone, message, track_id=task_id)

                if result.get('success'):
                    # Marcar como enviado
                    clickup.add_tag(task_id, 'lembrete-24h-enviado')
                    lembretes_enviados["24h"] += 1
                    print(f"     ✅ Enviado para {phone}")
                else:
                    lembretes_enviados["erros"] += 1
                    print(f"     ❌ Erro ao enviar")

                print()

            # LEMBRETE 1H ANTES
            elif 0.9 <= hours_until <= 1.1 and 'lembrete-1h-enviado' not in current_tags:
                print(f"  ⏰ Enviando lembrete 1h: {task_name}")

                # Mensagem mais urgente
                message = f"""⏰ *LEMBRETE IMPORTANTE*

Sua reunião é *daqui a 1 hora*!

📅 {task_name}
🕐 {meeting_time.strftime('%H:%M')}"""

                if meeting_url:
                    message += f"\n🔗 Link: {meeting_url}"

                message += "\n\nAté já!"

                # Enviar WhatsApp
                result = whatsapp.send_message(phone, message, track_id=task_id)

                if result.get('success'):
                    # Marcar como enviado
                    clickup.add_tag(task_id, 'lembrete-1h-enviado')
                    lembretes_enviados["1h"] += 1
                    print(f"     ✅ Enviado para {phone}")
                else:
                    lembretes_enviados["erros"] += 1
                    print(f"     ❌ Erro ao enviar")

                print()

        print()

    # Resumo
    print("=" * 70)
    print("RESUMO DOS LEMBRETES ENVIADOS")
    print("=" * 70)
    print(f"📅 24h antes: {lembretes_enviados['24h']}")
    print(f"⏰ 1h antes: {lembretes_enviados['1h']}")
    print(f"❌ Erros: {lembretes_enviados['erros']}")
    print()

    total = lembretes_enviados['24h'] + lembretes_enviados['1h']
    if total == 0:
        print("✅ Nenhum lembrete necessário no momento.")
    else:
        print(f"Total de lembretes: {total}")

    print()


if __name__ == "__main__":
    try:
        send_meeting_reminders()
        print("✅ Verificação de lembretes concluída!")
    except Exception as e:
        print(f"❌ Erro durante envio de lembretes: {e}")
        import traceback
        traceback.print_exc()
