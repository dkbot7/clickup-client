"""
Automacao: Relatorio Semanal de Contas a Pagar (FIN-06)
Executa: Toda segunda-feira as 9h (via GitHub Actions)

Funcionalidade:
- Exporta Contas a Pagar para aba "Relatorio Semanal" no Google Sheets
- Destaca contas vencidas e vencendo nos proximos 7 dias
- Atualiza aba "Resumo Semanal" com metricas financeiras da semana
"""
import os
from datetime import datetime

from src.clickup_api.client import KaloiClickUpClient
from src.google_api.client import get_sheets_service

SHEETS_ID = os.environ.get("GOOGLE_SHEETS_ID_DASHBOARD", "")
LIST_ID_CONTAS_PAGAR = os.environ.get("LIST_ID_CONTAS_PAGAR")
CF_VALOR = "2aca62aa-12c2-4911-8081-453926e59577"


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
        return None
    try:
        return (datetime.fromtimestamp(int(ts) / 1000) - datetime.now()).days
    except Exception:
        return None


def ensure_sheet(service, name):
    meta = service.spreadsheets().get(spreadsheetId=SHEETS_ID).execute()
    existing = {s["properties"]["title"] for s in meta.get("sheets", [])}
    if name not in existing:
        service.spreadsheets().batchUpdate(
            spreadsheetId=SHEETS_ID,
            body={"requests": [{"addSheet": {"properties": {"title": name}}}]}
        ).execute()
        print(f"  Aba '{name}' criada")


def clear_and_write(service, sheet_name, headers, rows):
    service.spreadsheets().values().clear(
        spreadsheetId=SHEETS_ID, range=f"{sheet_name}!A1:Z10000"
    ).execute()
    service.spreadsheets().values().update(
        spreadsheetId=SHEETS_ID,
        range=f"{sheet_name}!A1",
        valueInputOption="USER_ENTERED",
        body={"values": [headers] + rows},
    ).execute()
    print(f"  Aba '{sheet_name}': {len(rows)} linha(s) escritas")


def generate_weekly_report():
    if not SHEETS_ID:
        print("GOOGLE_SHEETS_ID_DASHBOARD nao configurado")
        return

    client = KaloiClickUpClient()
    service = get_sheets_service()
    today = datetime.now()
    today_str = today.strftime("%d/%m/%Y %H:%M")
    semana_str = today.strftime("%d/%m/%Y")

    print("=" * 60)
    print(f"RELATORIO SEMANAL - {semana_str}")
    print("=" * 60)

    ensure_sheet(service, "Relatorio Semanal")
    ensure_sheet(service, "Resumo Semanal")

    tasks = client.get_tasks(LIST_ID_CONTAS_PAGAR, paginate=True,
                             arquivada=False, incluir_fechadas=False)
    print(f"\n{len(tasks)} conta(s) encontrada(s)")

    headers = ["Conta", "Valor (R$)", "Vencimento", "Dias ate Vencer",
               "Situacao", "Status ClickUp", "Gerado em"]
    rows = []
    total_valor = 0.0
    count_vencidas = count_vencendo_7d = count_ok = 0
    valor_vencidas = valor_vencendo = 0.0

    for task in tasks:
        valor_raw = get_cf(task, CF_VALOR)
        valor = float(valor_raw) if valor_raw else 0.0
        total_valor += valor
        vencimento = ts_to_date(task.get("due_date"))
        dias = days_until(task.get("due_date"))
        status = task.get("status", {}).get("status", "")

        if dias is None:
            situacao = "Sem data"
        elif dias < 0:
            situacao = f"VENCIDA ({abs(dias)}d atrasada)"
            count_vencidas += 1
            valor_vencidas += valor
        elif dias <= 7:
            situacao = f"Vence em {dias}d"
            count_vencendo_7d += 1
            valor_vencendo += valor
        else:
            situacao = f"OK ({dias}d)"
            count_ok += 1

        rows.append([task["name"], f"{valor:,.2f}" if valor else "",
                     vencimento, dias if dias is not None else "",
                     situacao, status, today_str])

    rows.sort(key=lambda r: (r[3] if isinstance(r[3], int) else 9999))
    clear_and_write(service, "Relatorio Semanal", headers, rows)

    resumo_rows = [
        ["Total de Contas", len(tasks), semana_str],
        ["Total a Pagar (R$)", f"{total_valor:,.2f}", semana_str],
        ["Contas VENCIDAS", count_vencidas, semana_str],
        ["Valor em Atraso (R$)", f"{valor_vencidas:,.2f}", semana_str],
        ["Vencendo em 7 dias", count_vencendo_7d, semana_str],
        ["Valor vencendo (R$)", f"{valor_vencendo:,.2f}", semana_str],
        ["Contas em dia", count_ok, semana_str],
    ]
    clear_and_write(service, "Resumo Semanal",
                    ["Metrica", "Valor", "Semana de"], resumo_rows)

    print(f"\nTotal de contas:    {len(tasks)}")
    print(f"Total a pagar:      R$ {total_valor:,.2f}")
    print(f"Contas vencidas:    {count_vencidas} (R$ {valor_vencidas:,.2f})")
    print(f"Vencendo em 7d:     {count_vencendo_7d} (R$ {valor_vencendo:,.2f})")
    print(f"Contas em dia:      {count_ok}")


if __name__ == "__main__":
    try:
        generate_weekly_report()
        print("\nConcluido com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        raise
