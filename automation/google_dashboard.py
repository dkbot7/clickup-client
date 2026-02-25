"""
Automacao: Google Sheets Dashboard Diario
Executa: Todo dia as 8h (via GitHub Actions)

Automacoes implementadas:
- ANALYTICS-03: Busca tasks de Projetos, Comercial e Financeiro
                e atualiza o Google Sheets com os dados do dia

Abas criadas/atualizadas:
  - Projetos: nome, status, valor, orcamento, valor gasto, risco, prazo
  - Comercial: lead, status, agendamento, valor da venda
  - Financeiro: conta, valor, vencimento, dias ate vencer, status
  - Resumo: metricas gerais (contagens, totais)
"""
import os
from datetime import datetime

from src.clickup_api.client import KaloiClickUpClient
from src.google_api.client import get_sheets_service

SHEETS_ID = os.environ.get("GOOGLE_SHEETS_ID_DASHBOARD", "")

LIST_ID_PROJETOS_INTERNOS = os.environ.get("LIST_ID_PROJETOS_INTERNOS")
LIST_ID_PROJETOS_EXTERNOS = os.environ.get("LIST_ID_PROJETOS_EXTERNOS")
LIST_ID_AGENDA_COMERCIAL = os.environ.get("LIST_ID_AGENDA_COMERCIAL")
LIST_ID_SESSAO_ESTRATEGICA = os.environ.get("LIST_ID_SESSAO_ESTRATEGICA")
LIST_ID_CONTAS_PAGAR = os.environ.get("LIST_ID_CONTAS_PAGAR")

# Custom fields
CF_VALOR = "2aca62aa-12c2-4911-8081-453926e59577"
CF_ORCAMENTO = "5123a4f6-b79c-49aa-b3a9-db260f56c31f"
CF_VALOR_GASTO = "61eb9626-42ca-4117-a87e-a2948800cfe1"
CF_RISCO = "fc82fac4-449b-4e2e-8c6d-0242f1084667"
CF_AGENDAMENTO = "6aefbfe5-75af-4fd2-b9ba-2047b40ce82f"
CF_VALOR_VENDA = "e65d7c12-1790-451e-866f-f7841c3aceb9"

RISCO_LABELS = {0: "Baixo", 1: "Medio", 2: "Alto", 3: "Critico"}


def get_cf(task, field_id):
    for f in task.get("custom_fields", []):
        if f["id"] == field_id:
            return f.get("value")
    return None


def ts_to_date(ts):
    if not ts:
        return ""
    try:
        return datetime.fromtimestamp(int(ts) / 1000).strftime("%d/%m/%Y")
    except Exception:
        return ""


def days_until(ts):
    if not ts:
        return ""
    try:
        due = datetime.fromtimestamp(int(ts) / 1000)
        diff = (due - datetime.now()).days
        return diff
    except Exception:
        return ""


def clear_and_write(service, sheet_name, headers, rows):
    """Limpa a aba e escreve headers + dados."""
    range_clear = f"{sheet_name}!A1:Z10000"
    service.spreadsheets().values().clear(
        spreadsheetId=SHEETS_ID, range=range_clear
    ).execute()

    values = [headers] + rows
    service.spreadsheets().values().update(
        spreadsheetId=SHEETS_ID,
        range=f"{sheet_name}!A1",
        valueInputOption="USER_ENTERED",
        body={"values": values},
    ).execute()
    print(f"  Aba '{sheet_name}': {len(rows)} linha(s) escritas")


def ensure_sheets_exist(service, sheet_names):
    """Cria abas que ainda nao existem."""
    meta = service.spreadsheets().get(spreadsheetId=SHEETS_ID).execute()
    existing = {s["properties"]["title"] for s in meta.get("sheets", [])}

    requests = []
    for name in sheet_names:
        if name not in existing:
            requests.append({"addSheet": {"properties": {"title": name}}})

    if requests:
        service.spreadsheets().batchUpdate(
            spreadsheetId=SHEETS_ID,
            body={"requests": requests}
        ).execute()
        print(f"  Abas criadas: {[r['addSheet']['properties']['title'] for r in requests]}")


def run_google_dashboard():
    if not SHEETS_ID:
        print("GOOGLE_SHEETS_ID_DASHBOARD nao configurado")
        return

    client = KaloiClickUpClient()
    service = get_sheets_service()
    today_str = datetime.now().strftime("%d/%m/%Y %H:%M")

    print(f"\n{'='*60}")
    print(f"ATUALIZANDO DASHBOARD - {today_str}")
    print(f"{'='*60}")

    ensure_sheets_exist(service, ["Projetos", "Comercial", "Financeiro", "Resumo"])

    # ===== ABA PROJETOS =====
    print("\nBuscando Projetos...")
    proj_headers = ["Nome", "Status", "Valor (R$)", "Orcamento (R$)", "Valor Gasto (R$)",
                    "Risco", "Prazo", "Dias ate Prazo", "Atualizado em"]
    proj_rows = []

    for list_id in [LIST_ID_PROJETOS_INTERNOS, LIST_ID_PROJETOS_EXTERNOS]:
        if not list_id:
            continue
        tasks = client.get_tasks(list_id, paginate=True, arquivada=False, incluir_fechadas=False)
        for t in tasks:
            valor = get_cf(t, CF_VALOR) or ""
            orcamento = get_cf(t, CF_ORCAMENTO) or ""
            valor_gasto = get_cf(t, CF_VALOR_GASTO) or ""
            risco_idx = get_cf(t, CF_RISCO)
            risco = RISCO_LABELS.get(int(risco_idx), "") if risco_idx is not None else ""
            prazo = ts_to_date(t.get("due_date"))
            dias = days_until(t.get("due_date"))
            status = t.get("status", {}).get("status", "")
            proj_rows.append([t["name"], status, valor, orcamento, valor_gasto,
                               risco, prazo, dias, today_str])

    clear_and_write(service, "Projetos", proj_headers, proj_rows)

    # ===== ABA COMERCIAL =====
    print("\nBuscando Comercial...")
    com_headers = ["Nome / Lead", "Lista", "Status", "Agendamento", "Valor da Venda (R$)", "Atualizado em"]
    com_rows = []

    for list_id, list_label in [(LIST_ID_AGENDA_COMERCIAL, "Agenda Comercial"),
                                 (LIST_ID_SESSAO_ESTRATEGICA, "Sessao Estrategica")]:
        if not list_id:
            continue
        tasks = client.get_tasks(list_id, paginate=True, arquivada=False, incluir_fechadas=False)
        for t in tasks:
            agendamento = ts_to_date(get_cf(t, CF_AGENDAMENTO))
            valor_venda = get_cf(t, CF_VALOR_VENDA) or ""
            status = t.get("status", {}).get("status", "")
            com_rows.append([t["name"], list_label, status, agendamento, valor_venda, today_str])

    clear_and_write(service, "Comercial", com_headers, com_rows)

    # ===== ABA FINANCEIRO =====
    print("\nBuscando Financeiro...")
    fin_headers = ["Conta", "Valor (R$)", "Vencimento", "Dias ate Vencer", "Status", "Atualizado em"]
    fin_rows = []

    if LIST_ID_CONTAS_PAGAR:
        tasks = client.get_tasks(LIST_ID_CONTAS_PAGAR, paginate=True, arquivada=False, incluir_fechadas=False)
        for t in tasks:
            valor = get_cf(t, CF_VALOR) or ""
            vencimento = ts_to_date(t.get("due_date"))
            dias = days_until(t.get("due_date"))
            status = t.get("status", {}).get("status", "")
            fin_rows.append([t["name"], valor, vencimento, dias, status, today_str])

    clear_and_write(service, "Financeiro", fin_headers, fin_rows)

    # ===== ABA RESUMO =====
    print("\nAtualizando Resumo...")
    contas_vencidas = sum(1 for r in fin_rows if isinstance(r[3], int) and r[3] < 0)
    contas_vencendo = sum(1 for r in fin_rows if isinstance(r[3], int) and 0 <= r[3] <= 7)
    proj_alto_risco = sum(1 for r in proj_rows if r[5] in ("Alto", "Critico"))
    proj_atrasados = sum(1 for r in proj_rows if isinstance(r[7], int) and r[7] < 0)
    leads_ativos = sum(1 for r in com_rows if r[2] not in ("perdido", "perdido/nao qualificado",
                                                             "desqualificado", "negocio fechado"))

    resumo_headers = ["Metrica", "Valor", "Atualizado em"]
    resumo_rows = [
        ["Total de Projetos", len(proj_rows), today_str],
        ["Projetos Atrasados", proj_atrasados, today_str],
        ["Projetos Alto Risco / Critico", proj_alto_risco, today_str],
        ["Total de Leads Ativos", leads_ativos, today_str],
        ["Total Contas a Pagar", len(fin_rows), today_str],
        ["Contas Vencidas", contas_vencidas, today_str],
        ["Contas Vencendo em 7 dias", contas_vencendo, today_str],
    ]
    clear_and_write(service, "Resumo", resumo_headers, resumo_rows)

    print(f"\n{'='*60}")
    print("DASHBOARD ATUALIZADO COM SUCESSO")
    print(f"{'='*60}")
    print(f"Projetos: {len(proj_rows)} | Leads: {len(com_rows)} | Financeiro: {len(fin_rows)}")


if __name__ == "__main__":
    try:
        run_google_dashboard()
        print("\nConcluido com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        raise
