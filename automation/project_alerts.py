"""
Automação: Alertas de Projetos
Executa: Diariamente às 9h (via GitHub Actions)

Automações implementadas:
- PRJ-04: Prazo vencido → Tag "atrasado" + Task de revisão
- PRJ-05: Alertas progressivos 7/3/1 dias antes do prazo
- PRJ-07: Valor > R$50k → Tag "alto-valor"
"""
from src.clickup_api.client import KaloiClickUpClient
from datetime import datetime, timedelta
import os


LIST_ID_PROJETOS_INTERNOS = os.environ.get("LIST_ID_PROJETOS_INTERNOS")
LIST_ID_PROJETOS_EXTERNOS = os.environ.get("LIST_ID_PROJETOS_EXTERNOS")

CUSTOM_FIELD_VALOR = "2aca62aa-12c2-4911-8081-453926e59577"


def run_project_alerts():
    client = KaloiClickUpClient()
    today = datetime.now()

    lists_to_check = {
        "Projetos Internos": LIST_ID_PROJETOS_INTERNOS,
        "Projetos Externos": LIST_ID_PROJETOS_EXTERNOS,
    }

    totais = {"7_dias": 0, "3_dias": 0, "1_dia": 0, "vencido": 0, "alto_valor": 0}

    for list_name, list_id in lists_to_check.items():
        if not list_id:
            print(f"Pulando {list_name}: LIST_ID nao configurado")
            continue

        print(f"\n{'='*60}")
        print(f"Verificando: {list_name}")
        print(f"{'='*60}")

        tasks = client.get_tasks(list_id, paginate=True, arquivada=False, incluir_fechadas=False)

        if not tasks:
            print("  Nenhuma task encontrada.")
            continue

        print(f"  {len(tasks)} task(s) encontrada(s)")

        for task in tasks:
            task_id = task["id"]
            task_name = task["name"]
            due_date = task.get("due_date")
            current_tags = [t["name"] for t in task.get("tags", [])]
            status = task.get("status", {}).get("status", "").lower()

            # --- PRJ-05 e PRJ-04: Alertas de prazo ---
            if due_date and status not in ("concluido", "concluído", "closed", "complete"):
                due = datetime.fromtimestamp(int(due_date) / 1000)
                days_until = (due - today).days

                # 7 dias antes
                if days_until == 7 and "vencendo-em-breve" not in current_tags:
                    print(f"  [PRJ-05a] {task_name} - vence em 7 dias")
                    client.add_tag(task_id, "vencendo-em-breve")
                    client.post_task_comment(
                        task_id,
                        f"Atencao: Este projeto vence em 7 dias ({due.strftime('%d/%m/%Y')}). Verificar progresso."
                    )
                    totais["7_dias"] += 1

                # 3 dias antes
                elif days_until == 3 and "prazo-urgente" not in current_tags:
                    print(f"  [PRJ-05b] {task_name} - vence em 3 dias")
                    client.add_tag(task_id, "prazo-urgente")
                    client.update_task(task_id, priority=2)
                    client.post_task_comment(
                        task_id,
                        f"URGENTE: Este projeto vence em 3 dias ({due.strftime('%d/%m/%Y')})! Prioridade elevada."
                    )
                    totais["3_dias"] += 1

                # 1 dia antes
                elif days_until == 1 and "prazo-critico" not in current_tags:
                    print(f"  [PRJ-05c] {task_name} - vence AMANHA")
                    client.add_tag(task_id, "prazo-critico")
                    client.update_task(task_id, priority=1)
                    client.post_task_comment(
                        task_id,
                        f"CRITICO: Este projeto vence AMANHA ({due.strftime('%d/%m/%Y')})! Acao imediata necessaria."
                    )
                    totais["1_dia"] += 1

                # Vencido - PRJ-04
                elif days_until < 0 and "atrasado" not in current_tags:
                    dias_atrasado = abs(days_until)
                    print(f"  [PRJ-04] {task_name} - VENCIDO ha {dias_atrasado} dias")
                    client.add_tag(task_id, "atrasado")
                    client.update_task(task_id, priority=1)
                    client.post_task_comment(
                        task_id,
                        f"PRAZO VENCIDO: Este projeto esta atrasado ha {dias_atrasado} dia(s)! "
                        f"Vencimento era {due.strftime('%d/%m/%Y')}. Uma task de revisao foi criada."
                    )
                    client.create_task(
                        list_id=list_id,
                        name=f"REVISAR ATRASO: {task_name}",
                        description=(
                            f"Projeto atrasado ha {dias_atrasado} dia(s).\n\n"
                            f"Acoes necessarias:\n"
                            f"1. Identificar causa do atraso\n"
                            f"2. Definir novo prazo realista\n"
                            f"3. Comunicar stakeholders\n"
                            f"4. Atualizar status do projeto original"
                        ),
                        priority=1,
                        tags=["revisar", "atrasado"],
                    )
                    totais["vencido"] += 1

            # --- PRJ-07: Valor > R$50k ---
            custom_fields = {f["id"]: f for f in task.get("custom_fields", [])}
            valor_field = custom_fields.get(CUSTOM_FIELD_VALOR)
            if valor_field and valor_field.get("value"):
                try:
                    valor = float(valor_field["value"])
                    if valor > 50000 and "alto-valor" not in current_tags:
                        print(f"  [PRJ-07] {task_name} - Valor R${valor:,.2f} > R$50k")
                        client.add_tag(task_id, "alto-valor")
                        client.post_task_comment(
                            task_id,
                            f"PROJETO DE ALTO VALOR: R$ {valor:,.2f}. Notificar diretoria para acompanhamento especial."
                        )
                        totais["alto_valor"] += 1
                except (ValueError, TypeError):
                    pass

    print(f"\n{'='*60}")
    print("RESUMO - PROJECT ALERTS")
    print(f"{'='*60}")
    print(f"Alertas 7 dias:  {totais['7_dias']}")
    print(f"Alertas 3 dias:  {totais['3_dias']}")
    print(f"Alertas 1 dia:   {totais['1_dia']}")
    print(f"Projetos vencidos: {totais['vencido']}")
    print(f"Alto valor:      {totais['alto_valor']}")
    total = sum(totais.values())
    if total == 0:
        print("Nenhum alerta necessario no momento.")
    else:
        print(f"Total de alertas: {total}")


if __name__ == "__main__":
    try:
        run_project_alerts()
        print("\nConcluido com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        raise
