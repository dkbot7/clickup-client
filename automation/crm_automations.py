"""
Automacao: CRM Automations (Polling a cada 30 min)
Executa: A cada 30 minutos (via GitHub Actions)

Automacoes implementadas:
- CRM-02: Status "em qualificacao" -> comentario notificando SDR
- CRM-03: Status "reuniao agendada" -> cria evento no Google Calendar
- CRM-04: Status "negociando proposta" -> gera Google Doc a partir de template
- CRM-06: Status "perdido/nao qualificado" -> tag para-reativar + comentario

Status reais confirmados via API:
  Agenda Comercial: "em qualificacao" nao existe — usar "lead qualificado"
                    "reuniao/visita agendada", "negociando proposta",
                    "perdido/nao qualificado"
  Sessao Estrategica: "em qualificacao", "reuniao agendada",
                      "negocio fechado", "perdido", "desqualificado"
"""
import os
import sys
from datetime import datetime, timedelta, timezone

from src.clickup_api.client import KaloiClickUpClient
from src.google_api.client import get_calendar_service, get_docs_service, get_drive_service

CALENDAR_ID = os.environ.get("GOOGLE_CALENDAR_ID", "dkbotdani@gmail.com")
DOCS_TEMPLATE_ID = os.environ.get("GOOGLE_DOCS_TEMPLATE_PROPOSTA_ID", "")

LIST_ID_AGENDA_COMERCIAL = os.environ.get("LIST_ID_AGENDA_COMERCIAL")
LIST_ID_SESSAO_ESTRATEGICA = os.environ.get("LIST_ID_SESSAO_ESTRATEGICA")

# Custom field IDs
CF_AGENDAMENTO = "6aefbfe5-75af-4fd2-b9ba-2047b40ce82f"
CF_WHATSAPP = "08f6f16e-6425-4806-954f-b78b7abd1e57"
CF_EMAIL = "3eab1669-0b0b-44b6-98aa-0fb091f59d6b"
CF_RAZAO_SOCIAL = "4493bc59-0f2b-4f24-85b8-57a9c1e8377a"
CF_VALOR_VENDA = "e65d7c12-1790-451e-866f-f7841c3aceb9"
CF_SDR = "2f6d8cd0-9249-477d-8142-5730cdca6ae8"


def get_cf(task, field_id):
    """Retorna o valor de um custom field pelo ID."""
    for f in task.get("custom_fields", []):
        if f["id"] == field_id:
            return f.get("value")
    return None


def run_crm_automations():
    client = KaloiClickUpClient()
    totais = {"crm02": 0, "crm03": 0, "crm04": 0, "crm06": 0}

    listas = {
        "Agenda Comercial": LIST_ID_AGENDA_COMERCIAL,
        "Sessao Estrategica": LIST_ID_SESSAO_ESTRATEGICA,
    }

    for list_name, list_id in listas.items():
        if not list_id:
            print(f"Pulando {list_name}: LIST_ID nao configurado")
            continue

        print(f"\n{'='*60}")
        print(f"Verificando CRM: {list_name}")
        print(f"{'='*60}")

        tasks = client.get_tasks(list_id, paginate=True, arquivada=False, incluir_fechadas=False)
        print(f"  {len(tasks)} task(s) encontrada(s)")

        for task in tasks:
            task_id = task["id"]
            task_name = task["name"]
            status = task.get("status", {}).get("status", "").lower().strip()
            current_tags = [t["name"] for t in task.get("tags", [])]

            # --- CRM-02: Status qualificacao -> notifica SDR ---
            qualificacao_statuses = ("em qualificacao", "em qualificação", "lead qualificado")
            if status in qualificacao_statuses and "sdr-notificado" not in current_tags:
                print(f"  [CRM-02] {task_name} - notificando SDR")
                client.add_tag(task_id, "sdr-notificado")
                client.post_task_comment(
                    task_id,
                    f"Lead em qualificacao! SDR responsavel: verificar dados e agendar contato.\n\n"
                    f"Acoes necessarias:\n"
                    f"1. Revisar dados do lead\n"
                    f"2. Verificar historico de interacoes\n"
                    f"3. Definir abordagem de contato\n"
                    f"4. Atualizar status apos contato"
                )
                totais["crm02"] += 1

            # --- CRM-03: Status reuniao agendada -> Google Calendar ---
            reuniao_statuses = ("reuniao agendada", "reuniao/visita agendada",
                                "reunião agendada", "reunião/visita agendada",
                                "em reuniao", "em reunião")
            if status in reuniao_statuses and "calendario-criado" not in current_tags:
                agendamento_ts = get_cf(task, CF_AGENDAMENTO)
                if agendamento_ts:
                    try:
                        meeting_dt = datetime.fromtimestamp(int(agendamento_ts) / 1000, tz=timezone.utc)
                        event_link = _create_calendar_event(task_name, meeting_dt, task.get("url", ""))
                        client.add_tag(task_id, "calendario-criado")
                        msg = f"Evento criado no Google Calendar!\nData: {meeting_dt.strftime('%d/%m/%Y as %H:%M')}"
                        if event_link:
                            msg += f"\nLink: {event_link}"
                        client.post_task_comment(task_id, msg)
                        print(f"  [CRM-03] {task_name} - evento no Calendar criado")
                        totais["crm03"] += 1
                    except Exception as e:
                        print(f"  [CRM-03] ERRO em {task_name}: {e}")
                else:
                    print(f"  [CRM-03] {task_name} - sem data de Agendamento, pulando")

            # --- CRM-04: Status negociando proposta -> Google Docs ---
            proposta_statuses = ("negociando proposta",)
            if status in proposta_statuses and "proposta-gerada" not in current_tags:
                try:
                    razao_social = get_cf(task, CF_RAZAO_SOCIAL) or task_name
                    valor = get_cf(task, CF_VALOR_VENDA)
                    doc_url = _create_proposal_doc(razao_social, valor, task.get("url", ""))
                    client.add_tag(task_id, "proposta-gerada")
                    msg = f"Proposta gerada automaticamente!\nCliente: {razao_social}"
                    if doc_url:
                        msg += f"\nDocumento: {doc_url}"
                    client.post_task_comment(task_id, msg)
                    print(f"  [CRM-04] {task_name} - proposta no Docs gerada")
                    totais["crm04"] += 1
                except Exception as e:
                    print(f"  [CRM-04] ERRO em {task_name}: {e}")

            # --- CRM-06: Status perdido -> tag para-reativar ---
            perdido_statuses = ("perdido/nao qualificado", "perdido/não qualificado",
                                "perdido", "desqualificado")
            if status in perdido_statuses and "para-reativar" not in current_tags:
                print(f"  [CRM-06] {task_name} - marcando para reativacao")
                client.add_tag(task_id, "para-reativar")
                client.post_task_comment(
                    task_id,
                    f"Lead marcado como perdido.\n\n"
                    f"Acoes de remarketing:\n"
                    f"1. Adicionar a lista de remarketing\n"
                    f"2. Agendar recontato em 30/60/90 dias\n"
                    f"3. Incluir em campanhas de nurturing\n"
                    f"4. Revisar motivo da perda para melhorar o processo"
                )
                totais["crm06"] += 1

    print(f"\n{'='*60}")
    print("RESUMO - CRM AUTOMATIONS")
    print(f"{'='*60}")
    print(f"[CRM-02] SDR notificado:     {totais['crm02']}")
    print(f"[CRM-03] Eventos Calendar:   {totais['crm03']}")
    print(f"[CRM-04] Propostas no Docs:  {totais['crm04']}")
    print(f"[CRM-06] Para reativar:      {totais['crm06']}")
    total = sum(totais.values())
    if total == 0:
        print("Nenhuma acao necessaria no momento.")
    else:
        print(f"Total de acoes: {total}")


def _create_calendar_event(title, start_dt, task_url):
    """Cria evento no Google Calendar e retorna o link."""
    service = get_calendar_service()
    end_dt = start_dt + timedelta(hours=1)

    event = {
        "summary": title,
        "description": f"Reuniao comercial criada automaticamente pelo sistema Kaloi.\n\nTask ClickUp: {task_url}",
        "start": {"dateTime": start_dt.isoformat(), "timeZone": "America/Sao_Paulo"},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": "America/Sao_Paulo"},
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "popup", "minutes": 60},
                {"method": "popup", "minutes": 10},
            ],
        },
    }

    result = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return result.get("htmlLink", "")


def _create_proposal_doc(client_name, valor, task_url):
    """Copia o template de proposta e preenche com dados do cliente."""
    if not DOCS_TEMPLATE_ID:
        print("  DOCS_TEMPLATE_ID nao configurado, pulando geracao de proposta")
        return None

    drive_service = get_drive_service()

    # Copiar template
    today_str = datetime.now().strftime("%d/%m/%Y")
    copy_title = f"Proposta - {client_name} - {today_str}"
    copy = drive_service.files().copy(
        fileId=DOCS_TEMPLATE_ID,
        body={"name": copy_title}
    ).execute()
    doc_id = copy["id"]

    # Substituir placeholders no documento
    from src.google_api.client import get_docs_service
    docs_service = get_docs_service()

    valor_str = f"R$ {float(valor):,.2f}" if valor else "A definir"
    replacements = {
        "{{NOME_CLIENTE}}": client_name,
        "{{DATA}}": today_str,
        "{{VALOR}}": valor_str,
        "{{TASK_URL}}": task_url,
    }

    requests = []
    for placeholder, value in replacements.items():
        requests.append({
            "replaceAllText": {
                "containsText": {"text": placeholder, "matchCase": True},
                "replaceText": value,
            }
        })

    if requests:
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": requests}
        ).execute()

    # Retornar link do documento
    return f"https://docs.google.com/document/d/{doc_id}/edit"


if __name__ == "__main__":
    try:
        run_crm_automations()
        print("\nConcluido com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        raise
