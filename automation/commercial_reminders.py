"""
Automacao: Lembretes Comerciais via WhatsApp (API oficial Meta)
Executa: A cada 1 hora (via GitHub Actions)

Automacoes implementadas:
- COM-01: Lembrete 24h antes da reuniao -> WhatsApp
- COM-02: Lembrete 1h antes da reuniao -> WhatsApp

Requisitos:
  WHATSAPP_PHONE_NUMBER_ID  - ID do numero de telefone Meta
  WHATSAPP_ACCESS_TOKEN     - Token de acesso Meta
  WHATSAPP_API_VERSION      - Versao da API (ex: v22.0)

Custom fields usados:
  WhatsApp:    08f6f16e-6425-4806-954f-b78b7abd1e57 (phone)
  Agendamento: 6aefbfe5-75af-4fd2-b9ba-2047b40ce82f (date)
  Meeting URL: ffb916ff-2f9a-4d00-809f-a82765f08c90 (url)

ATENCAO: O token de acesso gerado no painel do desenvolvedor expira em ~24h.
Para producao, gere um token permanente via Sistema de Usuarios no Meta Business Manager.
"""
import os
import requests
from datetime import datetime, timezone
from src.clickup_api.client import KaloiClickUpClient

# WhatsApp API
WA_PHONE_NUMBER_ID = os.environ.get("WHATSAPP_PHONE_NUMBER_ID", "")
WA_ACCESS_TOKEN = os.environ.get("WHATSAPP_ACCESS_TOKEN", "")
WA_API_VERSION = os.environ.get("WHATSAPP_API_VERSION", "v22.0")
WA_API_URL = f"https://graph.facebook.com/{WA_API_VERSION}/{WA_PHONE_NUMBER_ID}/messages"

# ClickUp Lists
LIST_ID_AGENDA_COMERCIAL = os.environ.get("LIST_ID_AGENDA_COMERCIAL")
LIST_ID_SESSAO_ESTRATEGICA = os.environ.get("LIST_ID_SESSAO_ESTRATEGICA")

# Custom fields
CF_WHATSAPP = "08f6f16e-6425-4806-954f-b78b7abd1e57"
CF_AGENDAMENTO = "6aefbfe5-75af-4fd2-b9ba-2047b40ce82f"
CF_MEETING_URL = "ffb916ff-2f9a-4d00-809f-a82765f08c90"


def get_cf(task, field_id):
    for f in task.get("custom_fields", []):
        if f["id"] == field_id:
            return f.get("value")
    return None


def send_whatsapp_text(phone_number, message):
    """Envia mensagem de texto simples via WhatsApp Business API."""
    if not WA_PHONE_NUMBER_ID or not WA_ACCESS_TOKEN:
        print("  ERRO: WHATSAPP_PHONE_NUMBER_ID ou WHATSAPP_ACCESS_TOKEN nao configurados")
        return False

    # Normalizar numero (remover espacos, tracos, garantir codigo do pais)
    phone = phone_number.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if phone.startswith("0"):
        phone = "55" + phone[1:]
    if not phone.startswith("+") and not phone.startswith("55"):
        phone = "55" + phone
    phone = phone.lstrip("+")

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }

    headers = {
        "Authorization": f"Bearer {WA_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(WA_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return True
    else:
        print(f"  ERRO WhatsApp API: {response.status_code} - {response.text[:200]}")
        return False


def run_commercial_reminders():
    client = KaloiClickUpClient()
    now = datetime.now(tz=timezone.utc)
    totais = {"24h": 0, "1h": 0, "sem_whatsapp": 0, "sem_data": 0}

    listas = {
        "Agenda Comercial": LIST_ID_AGENDA_COMERCIAL,
        "Sessao Estrategica": LIST_ID_SESSAO_ESTRATEGICA,
    }

    print("=" * 60)
    print(f"LEMBRETES COMERCIAIS VIA WHATSAPP - {now.strftime('%d/%m/%Y %H:%M')} UTC")
    print("=" * 60)

    for list_name, list_id in listas.items():
        if not list_id:
            continue

        print(f"\n{list_name}:")
        tasks = client.get_tasks(list_id, paginate=True, arquivada=False, incluir_fechadas=False)

        for task in tasks:
            task_id = task["id"]
            task_name = task["name"]
            current_tags = [t["name"] for t in task.get("tags", [])]

            # Obter numero de WhatsApp
            whatsapp = get_cf(task, CF_WHATSAPP)
            if not whatsapp:
                totais["sem_whatsapp"] += 1
                continue

            # Obter data de agendamento
            agendamento_ts = get_cf(task, CF_AGENDAMENTO)
            if not agendamento_ts:
                totais["sem_data"] += 1
                continue

            meeting_dt = datetime.fromtimestamp(int(agendamento_ts) / 1000, tz=timezone.utc)
            hours_until = (meeting_dt - now).total_seconds() / 3600
            meeting_str = meeting_dt.strftime("%d/%m/%Y as %H:%M")

            # Link da reuniao (se disponivel)
            meeting_url = get_cf(task, CF_MEETING_URL) or ""

            # --- COM-01: Lembrete 24h antes ---
            if 23 <= hours_until <= 25 and "lembrete-24h-enviado" not in current_tags:
                print(f"  [COM-01] {task_name} - enviando lembrete 24h para {whatsapp}")
                msg = (
                    f"Ola! Lembrete da sua reuniao marcada para amanha.\n\n"
                    f"Reuniao: {task_name}\n"
                    f"Data/Hora: {meeting_str} (horario de Brasilia)\n"
                )
                if meeting_url:
                    msg += f"Link: {meeting_url}\n"
                msg += "\nAguardamos voce! Qualquer duvida, estamos a disposicao."

                if send_whatsapp_text(whatsapp, msg):
                    client.add_tag(task_id, "lembrete-24h-enviado")
                    client.post_task_comment(task_id, f"Lembrete de 24h enviado via WhatsApp para {whatsapp}")
                    totais["24h"] += 1

            # --- COM-02: Lembrete 1h antes ---
            elif 0.75 <= hours_until <= 1.25 and "lembrete-1h-enviado" not in current_tags:
                print(f"  [COM-02] {task_name} - enviando lembrete 1h para {whatsapp}")
                msg = (
                    f"Sua reuniao comeca em 1 hora!\n\n"
                    f"Reuniao: {task_name}\n"
                    f"Horario: {meeting_str}\n"
                )
                if meeting_url:
                    msg += f"Acesse aqui: {meeting_url}\n"
                msg += "\nNos vemos em breve!"

                if send_whatsapp_text(whatsapp, msg):
                    client.add_tag(task_id, "lembrete-1h-enviado")
                    client.post_task_comment(task_id, f"Lembrete de 1h enviado via WhatsApp para {whatsapp}")
                    totais["1h"] += 1

    print(f"\n{'='*60}")
    print("RESUMO - LEMBRETES COMERCIAIS")
    print(f"{'='*60}")
    print(f"[COM-01] Lembretes 24h enviados:  {totais['24h']}")
    print(f"[COM-02] Lembretes 1h enviados:   {totais['1h']}")
    print(f"Sem WhatsApp cadastrado:           {totais['sem_whatsapp']}")
    print(f"Sem data de agendamento:           {totais['sem_data']}")
    total = totais["24h"] + totais["1h"]
    if total == 0:
        print("Nenhum lembrete necessario no momento.")
    else:
        print(f"Total enviados: {total}")


if __name__ == "__main__":
    try:
        run_commercial_reminders()
        print("\nConcluido com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        raise
