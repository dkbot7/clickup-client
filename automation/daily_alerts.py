"""
Automação: Alertas Diários de Contas a Pagar
Executa: Diariamente às 9h (via GitHub Actions)

Funcionalidade:
- Alerta 7 dias antes do vencimento
- Alerta 3 dias antes (urgente)
- Alerta 1 dia antes (muito urgente)
- Alerta vencido (criar task de revisão)
"""
from src.clickup_api.client import KaloiClickUpClient
from datetime import datetime, timedelta
import os


# IDs do ClickUp (via variáveis de ambiente)
LIST_ID_CONTAS_PAGAR = os.environ.get("LIST_ID_CONTAS_PAGAR")
SPACE_ID_GESTAO_ADM = os.environ.get("SPACE_ID_GESTAO_ADM")


def check_overdue_bills():
    """
    Verifica contas a pagar e envia alertas baseados na data de vencimento

    Alertas:
    - 7 dias antes: Tag 'vencendo-em-breve'
    - 3 dias antes: Tag 'urgente' + comentário
    - 1 dia antes: Tag 'muito-urgente' + comentário
    - Vencido: Tag 'atrasado' + criar task de revisão
    """

    client = KaloiClickUpClient()

    print("=" * 70)
    print("VERIFICANDO CONTAS A PAGAR - ALERTAS DE VENCIMENTO")
    print("=" * 70)
    print()

    # Buscar todas as tasks de contas a pagar (não arquivadas)
    tasks = client.get_tasks(
        LIST_ID_CONTAS_PAGAR,
        paginate=True,
        arquivada=False,
        incluir_fechadas=False
    )

    if not tasks:
        print("Nenhuma conta a pagar encontrada.")
        return

    print(f"Total de contas a pagar: {len(tasks)}")
    print()

    alertas_enviados = {
        "7_dias": 0,
        "3_dias": 0,
        "1_dia": 0,
        "vencido": 0
    }

    for task in tasks:
        task_id = task['id']
        task_name = task['name']
        due_date = task.get('due_date')

        if not due_date:
            print(f"⚠️  {task_name}: SEM DATA DE VENCIMENTO")
            continue

        # Converter timestamp para datetime
        due = datetime.fromtimestamp(int(due_date) / 1000)
        today = datetime.now()
        days_until = (due - today).days

        # Obter tags atuais
        current_tags = [tag['name'] for tag in task.get('tags', [])]

        # 7 DIAS ANTES
        if days_until == 7 and 'vencendo-em-breve' not in current_tags:
            print(f"⚠️  {task_name}")
            print(f"   Vence em 7 dias ({due.strftime('%d/%m/%Y')})")

            # Adicionar tag
            client.add_tag(task_id, 'vencendo-em-breve')

            # Comentário
            client.post_task_comment(
                task_id,
                "⚠️ **ATENÇÃO:** Esta conta vence em 7 dias!"
            )

            alertas_enviados["7_dias"] += 1
            print()

        # 3 DIAS ANTES
        elif days_until == 3 and 'urgente' not in current_tags:
            print(f"🔥 {task_name}")
            print(f"   Vence em 3 dias ({due.strftime('%d/%m/%Y')})")

            # Adicionar tag
            client.add_tag(task_id, 'urgente')

            # Comentário mais enfático
            client.post_task_comment(
                task_id,
                "🔥 **URGENTE:** Esta conta vence em 3 dias!\n\n"
                "Por favor, providencie o pagamento o quanto antes."
            )

            # Atualizar prioridade
            client.update_task(task_id, priority=2)  # Alta

            alertas_enviados["3_dias"] += 1
            print()

        # 1 DIA ANTES
        elif days_until == 1 and 'muito-urgente' not in current_tags:
            print(f"🚨 {task_name}")
            print(f"   Vence AMANHÃ ({due.strftime('%d/%m/%Y')})")

            # Adicionar tag
            client.add_tag(task_id, 'muito-urgente')

            # Comentário crítico
            client.post_task_comment(
                task_id,
                "🚨 **MUITO URGENTE:** Esta conta vence AMANHÃ!\n\n"
                f"Data de vencimento: {due.strftime('%d/%m/%Y')}\n"
                "**AÇÃO IMEDIATA NECESSÁRIA!**"
            )

            # Prioridade urgente
            client.update_task(task_id, priority=1)  # Urgente

            alertas_enviados["1_dia"] += 1
            print()

        # VENCIDO
        elif days_until < 0 and 'atrasado' not in current_tags:
            dias_atrasado = abs(days_until)
            print(f"🔴 {task_name}")
            print(f"   VENCIDO há {dias_atrasado} dia(s)")

            # Adicionar tag
            client.add_tag(task_id, 'atrasado')

            # Comentário de atraso
            client.post_task_comment(
                task_id,
                f"🔴 **VENCIDO:** Esta conta está atrasada há {dias_atrasado} dia(s)!\n\n"
                f"Data de vencimento: {due.strftime('%d/%m/%Y')}\n"
                f"**Possível cobrança de juros e multa.**\n\n"
                "Uma task de revisão foi criada."
            )

            # Criar task de revisão
            client.create_task(
                list_id=LIST_ID_CONTAS_PAGAR,
                name=f"🔴 REVISAR: {task_name} (ATRASADO)",
                description=(
                    f"Conta vencida há {dias_atrasado} dia(s).\n\n"
                    f"**Task original:** {task['url']}\n\n"
                    f"**Ações necessárias:**\n"
                    f"1. Verificar se foi paga\n"
                    f"2. Calcular juros/multa\n"
                    f"3. Providenciar pagamento imediato\n"
                    f"4. Atualizar status da task original"
                ),
                priority=1,  # Urgente
                tags=['revisar', 'atrasado', 'urgente']
            )

            alertas_enviados["vencido"] += 1
            print()

    # Resumo
    print("=" * 70)
    print("RESUMO DOS ALERTAS ENVIADOS")
    print("=" * 70)
    print(f"⚠️  7 dias antes: {alertas_enviados['7_dias']}")
    print(f"🔥 3 dias antes: {alertas_enviados['3_dias']}")
    print(f"🚨 1 dia antes: {alertas_enviados['1_dia']}")
    print(f"🔴 Vencidos: {alertas_enviados['vencido']}")
    print()

    total = sum(alertas_enviados.values())
    if total == 0:
        print("✅ Nenhum alerta necessário no momento.")
    else:
        print(f"Total de alertas: {total}")

    print()


if __name__ == "__main__":
    try:
        check_overdue_bills()
        print("✅ Verificação concluída com sucesso!")
    except Exception as e:
        print(f"❌ Erro durante verificação: {e}")
        import traceback
        traceback.print_exc()
