"""
Automação: Relatórios Semanais Automáticos
Executa: Toda segunda-feira às 9h (via GitHub Actions)

Funcionalidade:
- Relatório de contas a pagar (vencimentos da semana)
- Relatório de reuniões comerciais agendadas
- Relatório de tasks criadas/concluídas
- Estatísticas de produtividade
"""
from src.clickup_api.client import KaloiClickUpClient
from datetime import datetime, timedelta
import os


# IDs do ClickUp (via variáveis de ambiente)
SPACE_ID_GESTAO_ADM = os.environ.get("SPACE_ID_GESTAO_ADM")
SPACE_ID_COMERCIAL = os.environ.get("SPACE_ID_COMERCIAL")
SPACE_ID_PROJETOS = os.environ.get("SPACE_ID_PROJETOS")

LIST_ID_CONTAS_PAGAR = os.environ.get("LIST_ID_CONTAS_PAGAR")
LIST_ID_AGENDA_COMERCIAL = os.environ.get("LIST_ID_AGENDA_COMERCIAL")
LIST_ID_SESSAO_ESTRATEGICA = os.environ.get("LIST_ID_SESSAO_ESTRATEGICA")

# List para postar relatórios (criar uma task semanal)
LIST_ID_RELATORIOS = LIST_ID_CONTAS_PAGAR  # Pode criar uma list específica depois


def generate_weekly_report():
    """
    Gera relatório semanal completo do workspace

    Seções:
    1. Contas a Pagar (próximos 7 dias)
    2. Reuniões Comerciais agendadas
    3. Tasks criadas vs concluídas
    4. Produtividade por Space
    """

    client = KaloiClickUpClient()

    print("=" * 70)
    print("GERANDO RELATÓRIO SEMANAL - ClickUp Workspace")
    print("=" * 70)
    print()

    # Definir período do relatório
    today = datetime.now()
    week_start = today
    week_end = today + timedelta(days=7)

    print(f"Período: {week_start.strftime('%d/%m/%Y')} - {week_end.strftime('%d/%m/%Y')}")
    print()

    # ===== SEÇÃO 1: CONTAS A PAGAR =====
    print("=" * 70)
    print("1. CONTAS A PAGAR - PRÓXIMOS 7 DIAS")
    print("=" * 70)
    print()

    contas_pagar = client.get_tasks(
        LIST_ID_CONTAS_PAGAR,
        paginate=True,
        arquivada=False,
        incluir_fechadas=False
    )

    contas_vencendo = []
    contas_vencidas = []
    total_valor = 0

    for task in contas_pagar:
        due_date = task.get('due_date')
        if not due_date:
            continue

        due = datetime.fromtimestamp(int(due_date) / 1000)
        days_until = (due - today).days

        # Contas dos próximos 7 dias
        if 0 <= days_until <= 7:
            contas_vencendo.append({
                'nome': task['name'],
                'vencimento': due,
                'dias_ate': days_until,
                'url': task['url']
            })

        # Contas já vencidas
        elif days_until < 0:
            contas_vencidas.append({
                'nome': task['name'],
                'vencimento': due,
                'dias_atrasado': abs(days_until),
                'url': task['url']
            })

    print(f"📊 Contas vencendo nos próximos 7 dias: {len(contas_vencendo)}")
    if contas_vencendo:
        contas_vencendo.sort(key=lambda x: x['dias_ate'])
        for conta in contas_vencendo:
            print(f"   • {conta['nome']}")
            print(f"     Vence em {conta['dias_ate']} dia(s) - {conta['vencimento'].strftime('%d/%m/%Y')}")
    else:
        print("   ✅ Nenhuma conta a vencer")

    print()
    print(f"🔴 Contas VENCIDAS: {len(contas_vencidas)}")
    if contas_vencidas:
        contas_vencidas.sort(key=lambda x: x['dias_atrasado'], reverse=True)
        for conta in contas_vencidas:
            print(f"   • {conta['nome']}")
            print(f"     ATRASADO {conta['dias_atrasado']} dia(s) - Venceu {conta['vencimento'].strftime('%d/%m/%Y')}")
    else:
        print("   ✅ Nenhuma conta atrasada")

    print()

    # ===== SEÇÃO 2: REUNIÕES COMERCIAIS =====
    print("=" * 70)
    print("2. REUNIÕES COMERCIAIS - PRÓXIMOS 7 DIAS")
    print("=" * 70)
    print()

    # Agenda Comercial
    agenda_comercial = client.get_tasks(
        LIST_ID_AGENDA_COMERCIAL,
        paginate=True,
        arquivada=False,
        incluir_fechadas=False
    )

    # Sessão Estratégica
    sessao_estrategica = client.get_tasks(
        LIST_ID_SESSAO_ESTRATEGICA,
        paginate=True,
        arquivada=False,
        incluir_fechadas=False
    )

    todas_reunioes = []

    for task in agenda_comercial + sessao_estrategica:
        # Buscar custom field "Agendamento"
        custom_fields = {
            field['id']: field for field in task.get('custom_fields', [])
        }

        agendamento_field = custom_fields.get("YOUR_CUSTOM_FIELD_AGENDAMENTO")
        if not agendamento_field or not agendamento_field.get('value'):
            continue

        agendamento_ts = int(agendamento_field['value'])
        meeting_time = datetime.fromtimestamp(agendamento_ts / 1000)

        # Reuniões dos próximos 7 dias
        hours_until = (meeting_time - today).total_seconds() / 3600
        if 0 <= hours_until <= 168:  # 7 dias = 168 horas
            todas_reunioes.append({
                'nome': task['name'],
                'data': meeting_time,
                'tipo': 'Agenda Comercial' if task['list']['id'] == LIST_ID_AGENDA_COMERCIAL else 'Sessão Estratégica'
            })

    print(f"📅 Reuniões agendadas: {len(todas_reunioes)}")
    if todas_reunioes:
        todas_reunioes.sort(key=lambda x: x['data'])
        for reuniao in todas_reunioes:
            print(f"   • {reuniao['nome']}")
            print(f"     {reuniao['data'].strftime('%d/%m/%Y às %H:%M')} - {reuniao['tipo']}")
    else:
        print("   📭 Nenhuma reunião agendada")

    print()

    # ===== SEÇÃO 3: PRODUTIVIDADE GERAL =====
    print("=" * 70)
    print("3. PRODUTIVIDADE - ÚLTIMOS 7 DIAS")
    print("=" * 70)
    print()

    # Definir data de início (7 dias atrás)
    past_week_start = today - timedelta(days=7)
    past_week_start_ts = int(past_week_start.timestamp() * 1000)

    spaces = {
        "Gestão Administrativa": SPACE_ID_GESTAO_ADM,
        "Comercial": SPACE_ID_COMERCIAL,
        "Projetos": SPACE_ID_PROJETOS
    }

    total_criadas = 0
    total_concluidas = 0

    for space_name, space_id in spaces.items():
        print(f"📂 {space_name}")

        # Buscar space completo
        space_data = client.get_space(space_id)

        # Iterar por todas as lists do space
        criadas = 0
        concluidas = 0

        # Obter todas as tasks do space (via cada folder/list)
        try:
            # Buscar folders do space
            folders = client.get_folders(space_id)

            for folder in folders:
                folder_id = folder['id']

                # Buscar lists de cada folder
                lists = client.get_lists(folder_id)

                for list_obj in lists:
                    list_id = list_obj['id']

                    # Tasks da list
                    tasks = client.get_tasks(
                        list_id,
                        paginate=True,
                        arquivada=False
                    )

                    for task in tasks:
                        # Contar tasks criadas nos últimos 7 dias
                        date_created = int(task.get('date_created', 0))
                        if date_created >= past_week_start_ts:
                            criadas += 1

                        # Contar tasks concluídas nos últimos 7 dias
                        if task.get('status', {}).get('status') == 'closed':
                            date_closed = int(task.get('date_closed', 0))
                            if date_closed >= past_week_start_ts:
                                concluidas += 1

        except Exception as e:
            print(f"   ⚠️ Erro ao buscar tasks: {e}")
            continue

        print(f"   ✅ Tasks criadas: {criadas}")
        print(f"   ✅ Tasks concluídas: {concluidas}")

        if criadas > 0:
            taxa_conclusao = (concluidas / criadas) * 100
            print(f"   📊 Taxa de conclusão: {taxa_conclusao:.1f}%")

        print()

        total_criadas += criadas
        total_concluidas += concluidas

    print("=" * 70)
    print("RESUMO TOTAL")
    print("=" * 70)
    print(f"📝 Total de tasks criadas: {total_criadas}")
    print(f"✅ Total de tasks concluídas: {total_concluidas}")

    if total_criadas > 0:
        taxa_total = (total_concluidas / total_criadas) * 100
        print(f"📊 Taxa de conclusão geral: {taxa_total:.1f}%")

    print()

    # ===== CRIAR TASK DE RELATÓRIO =====
    print("=" * 70)
    print("SALVANDO RELATÓRIO NO CLICKUP")
    print("=" * 70)
    print()

    # Montar descrição do relatório
    relatorio_md = f"""# Relatório Semanal - {today.strftime('%d/%m/%Y')}

## 📊 Contas a Pagar

**Vencendo nos próximos 7 dias:** {len(contas_vencendo)}
"""

    if contas_vencendo:
        relatorio_md += "\n### Vencimentos próximos:\n"
        for conta in contas_vencendo:
            relatorio_md += f"- **{conta['nome']}** - Vence em {conta['dias_ate']} dia(s) ({conta['vencimento'].strftime('%d/%m/%Y')})\n"

    if contas_vencidas:
        relatorio_md += f"\n**🔴 ATENÇÃO:** {len(contas_vencidas)} conta(s) VENCIDA(S)\n"
        for conta in contas_vencidas:
            relatorio_md += f"- **{conta['nome']}** - ATRASADO {conta['dias_atrasado']} dia(s)\n"

    relatorio_md += f"\n## 📅 Reuniões Comerciais\n\n**Agendadas para os próximos 7 dias:** {len(todas_reunioes)}\n"

    if todas_reunioes:
        relatorio_md += "\n"
        for reuniao in todas_reunioes:
            relatorio_md += f"- **{reuniao['nome']}** - {reuniao['data'].strftime('%d/%m/%Y às %H:%M')} ({reuniao['tipo']})\n"

    relatorio_md += f"\n## 📈 Produtividade (últimos 7 dias)\n\n"
    relatorio_md += f"- Tasks criadas: **{total_criadas}**\n"
    relatorio_md += f"- Tasks concluídas: **{total_concluidas}**\n"

    if total_criadas > 0:
        taxa_total = (total_concluidas / total_criadas) * 100
        relatorio_md += f"- Taxa de conclusão: **{taxa_total:.1f}%**\n"

    relatorio_md += f"\n---\n*Relatório gerado automaticamente em {today.strftime('%d/%m/%Y às %H:%M')}*"

    # Criar task de relatório
    try:
        client.create_task(
            list_id=LIST_ID_RELATORIOS,
            name=f"📊 Relatório Semanal - {today.strftime('%d/%m/%Y')}",
            description=relatorio_md,
            priority=3,  # Normal
            tags=['relatorio', 'automacao']
        )
        print("✅ Relatório salvo no ClickUp como task!")
    except Exception as e:
        print(f"❌ Erro ao criar task de relatório: {e}")

    print()


if __name__ == "__main__":
    try:
        generate_weekly_report()
        print("✅ Relatório semanal gerado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {e}")
        import traceback
        traceback.print_exc()
