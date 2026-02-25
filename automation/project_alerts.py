"""
Automacao: Alertas de Projetos
Executa: Diariamente as 9h (via GitHub Actions)

Automacoes implementadas:
- PRJ-04: Prazo vencido -> Tag "atrasado" + comentario
- PRJ-05: Alertas progressivos 7/3/1 dias antes do prazo
- PRJ-06: Campo Risco = Alto ou Critico -> tag + comentario
- PRJ-07: Valor > R$50k -> Tag "alto-valor"
- PRJ-08: Valor Gasto > Orcamento -> tag "orcamento-excedido" + comentario

Custom fields confirmados via API (Projetos Internos):
  Valor:       2aca62aa-12c2-4911-8081-453926e59577
  Orcamento:   5123a4f6-b79c-49aa-b3a9-db260f56c31f
  Valor Gasto: 61eb9626-42ca-4117-a87e-a2948800cfe1
  Risco:       fc82fac4-449b-4e2e-8c6d-0242f1084667
               (dropdown: 0=Baixo, 1=Medio, 2=Alto, 3=Critico)
"""
from src.clickup_api.client import KaloiClickUpClient
from datetime import datetime, timedelta
import os


LIST_ID_PROJETOS_INTERNOS = os.environ.get("LIST_ID_PROJETOS_INTERNOS")
LIST_ID_PROJETOS_EXTERNOS = os.environ.get("LIST_ID_PROJETOS_EXTERNOS")

CUSTOM_FIELD_VALOR = "2aca62aa-12c2-4911-8081-453926e59577"
CUSTOM_FIELD_ORCAMENTO = "5123a4f6-b79c-49aa-b3a9-db260f56c31f"
CUSTOM_FIELD_VALOR_GASTO = "61eb9626-42ca-4117-a87e-a2948800cfe1"
CUSTOM_FIELD_RISCO = "fc82fac4-449b-4e2e-8c6d-0242f1084667"


def run_project_alerts():
    client = KaloiClickUpClient()
    today = datetime.now()

    lists_to_check = {
        "Projetos Internos": LIST_ID_PROJETOS_INTERNOS,
        "Projetos Externos": LIST_ID_PROJETOS_EXTERNOS,
    }

    totais = {"7_dias": 0, "3_dias": 0, "1_dia": 0, "vencido": 0,
              "alto_valor": 0, "risco_alto": 0, "orcamento_excedido": 0}

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
            # Status finais reais em Projetos Internos: "finalizado", "paralisado", "encerramento"
            if due_date and status not in ("finalizado", "paralisado", "encerramento", "concluido", "concluído", "closed", "complete"):
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
                        f"Vencimento era {due.strftime('%d/%m/%Y')}. Acao imediata necessaria."
                    )
                    totais["vencido"] += 1

            custom_fields = {f["id"]: f for f in task.get("custom_fields", [])}

            # --- PRJ-07: Valor > R$50k ---
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

            # --- PRJ-06: Risco Alto ou Critico ---
            # Risco dropdown: 0=Baixo, 1=Medio, 2=Alto, 3=Critico
            risco_field = custom_fields.get(CUSTOM_FIELD_RISCO)
            if risco_field and risco_field.get("value") is not None:
                try:
                    risco_idx = int(risco_field["value"])
                    risco_label = {0: "Baixo", 1: "Medio", 2: "Alto", 3: "Critico"}.get(risco_idx, "")
                    if risco_idx >= 2 and "risco-alto-notificado" not in current_tags:
                        print(f"  [PRJ-06] {task_name} - Risco {risco_label}")
                        client.add_tag(task_id, "risco-alto-notificado")
                        client.update_task(task_id, priority=1)
                        client.post_task_comment(
                            task_id,
                            f"RISCO {risco_label.upper()} DETECTADO!\n\n"
                            f"Acoes necessarias:\n"
                            f"1. Revisar fatores de risco imediatamente\n"
                            f"2. Acionar gestor do projeto\n"
                            f"3. Elaborar plano de mitigacao\n"
                            f"4. Comunicar stakeholders"
                        )
                        totais["risco_alto"] += 1
                except (ValueError, TypeError):
                    pass

            # --- PRJ-08: Valor Gasto > Orcamento ---
            orcamento_field = custom_fields.get(CUSTOM_FIELD_ORCAMENTO)
            gasto_field = custom_fields.get(CUSTOM_FIELD_VALOR_GASTO)
            if orcamento_field and gasto_field:
                try:
                    orcamento = float(orcamento_field.get("value") or 0)
                    gasto = float(gasto_field.get("value") or 0)
                    if orcamento > 0 and gasto > orcamento and "orcamento-excedido" not in current_tags:
                        excedido = gasto - orcamento
                        pct = (gasto / orcamento - 1) * 100
                        print(f"  [PRJ-08] {task_name} - Orcamento excedido em R${excedido:,.2f} ({pct:.1f}%)")
                        client.add_tag(task_id, "orcamento-excedido")
                        client.update_task(task_id, priority=1)
                        client.post_task_comment(
                            task_id,
                            f"ORCAMENTO EXCEDIDO!\n\n"
                            f"Orcamento: R$ {orcamento:,.2f}\n"
                            f"Valor Gasto: R$ {gasto:,.2f}\n"
                            f"Excedente: R$ {excedido:,.2f} ({pct:.1f}% acima)\n\n"
                            f"Acoes necessarias:\n"
                            f"1. Revisar lancamentos de custos\n"
                            f"2. Renegociar escopo ou orcamento\n"
                            f"3. Comunicar cliente/diretoria"
                        )
                        totais["orcamento_excedido"] += 1
                except (ValueError, TypeError):
                    pass

    print(f"\n{'='*60}")
    print("RESUMO - PROJECT ALERTS")
    print(f"{'='*60}")
    print(f"Alertas 7 dias:       {totais['7_dias']}")
    print(f"Alertas 3 dias:       {totais['3_dias']}")
    print(f"Alertas 1 dia:        {totais['1_dia']}")
    print(f"Projetos vencidos:    {totais['vencido']}")
    print(f"Alto valor:           {totais['alto_valor']}")
    print(f"Risco alto/critico:   {totais['risco_alto']}")
    print(f"Orcamento excedido:   {totais['orcamento_excedido']}")
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
