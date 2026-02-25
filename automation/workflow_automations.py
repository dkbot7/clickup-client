"""
Automação: Workflow Automations (Polling a cada 30 min)
Executa: A cada 30 minutos (via GitHub Actions)

Automações implementadas:
- PRJ-01: Checklist "Testes e Validacao" 100% → Status monitoramento
- PRJ-02: Checklist progresso → Tag de fase
- PRJ-03: Gestor de Projetos preenchido → Auto-assign
- TAG-01: Tag "urgente" → Prioridade Urgente
- TAG-02: Tag "interno" → Valor = 0
- TAG-03: Tag "bloqueado" → Task de desbloqueio
- TAG-04: Tag "aprovado" → Comentario de proxima fase
- WKF-01: Status "concluido" → Comentario de celebracao
- WKF-02: Status "em andamento" → Notificar assignees
- WKF-03: Checklist "Planejamento Estrategico" 100% → Tag
- COM-03: Status "Negocio Fechado" → Task de onboarding
"""
from src.clickup_api.client import KaloiClickUpClient
from datetime import datetime
import os
import requests


# IDs das lists
LIST_ID_PROJETOS_INTERNOS = os.environ.get("LIST_ID_PROJETOS_INTERNOS")
LIST_ID_PROJETOS_EXTERNOS = os.environ.get("LIST_ID_PROJETOS_EXTERNOS")
LIST_ID_AGENDA_COMERCIAL = os.environ.get("LIST_ID_AGENDA_COMERCIAL")
LIST_ID_SESSAO_ESTRATEGICA = os.environ.get("LIST_ID_SESSAO_ESTRATEGICA")

# Custom field IDs
CUSTOM_FIELD_GESTOR = "03330b23-c1bf-4d0f-8aa9-fc0985110b86"
CUSTOM_FIELD_VALOR = "2aca62aa-12c2-4911-8081-453926e59577"

CLICKUP_TOKEN = os.environ.get("CLICKUP_API_TOKEN") or os.environ.get("CLICKUP_TOKEN")


def get_checklist_progress(task):
    """Retorna progresso geral de todos os checklists (0-100)."""
    checklists = task.get("checklists", [])
    if not checklists:
        return None
    total = sum(len(c.get("items", [])) for c in checklists)
    resolved = sum(
        sum(1 for item in c.get("items", []) if item.get("resolved"))
        for c in checklists
    )
    if total == 0:
        return None
    return int((resolved / total) * 100)


def get_checklist_completion(task, checklist_name):
    """Verifica se um checklist especifico esta 100% completo."""
    for checklist in task.get("checklists", []):
        if checklist.get("name", "").strip() == checklist_name:
            items = checklist.get("items", [])
            if not items:
                return False
            return all(item.get("resolved") for item in items)
    return False


def set_task_priority_direct(task_id, priority):
    """Muda prioridade diretamente via API (1=urgente, 2=alta, 3=normal, 4=baixa)."""
    headers = {"Authorization": CLICKUP_TOKEN, "Content-Type": "application/json"}
    requests.put(
        f"https://api.clickup.com/api/v2/task/{task_id}",
        json={"priority": priority},
        headers=headers,
    )


def run_workflow_automations():
    client = KaloiClickUpClient()

    totais = {
        "prj01": 0, "prj02": 0, "prj03": 0,
        "tag01": 0, "tag02": 0, "tag03": 0, "tag04": 0,
        "wkf01": 0, "wkf02": 0, "wkf03": 0,
        "com03": 0,
    }

    # ===== PROJETOS =====
    project_lists = {
        "Projetos Internos": LIST_ID_PROJETOS_INTERNOS,
        "Projetos Externos": LIST_ID_PROJETOS_EXTERNOS,
    }

    for list_name, list_id in project_lists.items():
        if not list_id:
            continue

        print(f"\n{'='*60}")
        print(f"Verificando projetos: {list_name}")
        print(f"{'='*60}")

        tasks = client.get_tasks(list_id, paginate=True, arquivada=False, incluir_fechadas=False)

        for task in tasks:
            task_id = task["id"]
            task_name = task["name"]
            current_tags = [t["name"] for t in task.get("tags", [])]
            status = task.get("status", {}).get("status", "").lower()
            assignees = [a["id"] for a in task.get("assignees", [])]
            custom_fields = {f["id"]: f for f in task.get("custom_fields", [])}

            # --- PRJ-01: Checklist "Testes e Validacao" 100% → Status monitoramento ---
            if get_checklist_completion(task, "Testes e Validacao") and "testes-concluidos" not in current_tags:
                print(f"  [PRJ-01] {task_name} - Testes 100% completos")
                client.add_tag(task_id, "testes-concluidos")
                client.post_task_comment(
                    task_id,
                    "Testes e Validacao concluidos 100%! Status deve ser movido para Monitoramento."
                )
                totais["prj01"] += 1

            # --- PRJ-02: Checklist progresso → Tag de fase ---
            progress = get_checklist_progress(task)
            if progress is not None:
                if progress >= 100 and "fase-entrega" not in current_tags:
                    client.add_tag(task_id, "fase-entrega")
                    client.post_task_comment(task_id, "Checklists 100% concluidos! Fase: Entrega.")
                    totais["prj02"] += 1
                elif progress >= 75 and "fase-revisao" not in current_tags:
                    client.add_tag(task_id, "fase-revisao")
                    client.post_task_comment(task_id, "Checklists 75%! Fase: Revisao.")
                    totais["prj02"] += 1
                elif progress >= 50 and "fase-execucao" not in current_tags:
                    client.add_tag(task_id, "fase-execucao")
                    client.post_task_comment(task_id, "Checklists 50%! Fase: Execucao.")
                    totais["prj02"] += 1
                elif progress >= 25 and "fase-iniciacao" not in current_tags:
                    client.add_tag(task_id, "fase-iniciacao")
                    client.post_task_comment(task_id, "Checklists 25%! Fase: Iniciacao.")
                    totais["prj02"] += 1

            # --- PRJ-03: Gestor de Projetos → Auto-assign ---
            gestor_field = custom_fields.get(CUSTOM_FIELD_GESTOR)
            if gestor_field and gestor_field.get("value"):
                gestores = gestor_field["value"]
                if isinstance(gestores, list):
                    for gestor in gestores:
                        gestor_id = gestor.get("id")
                        if gestor_id and gestor_id not in assignees:
                            print(f"  [PRJ-03] {task_name} - Adicionando gestor como assignee")
                            headers = {"Authorization": CLICKUP_TOKEN, "Content-Type": "application/json"}
                            requests.post(
                                f"https://api.clickup.com/api/v2/task/{task_id}/member",
                                json={"assignees": [gestor_id]},
                                headers=headers,
                            )
                            client.post_task_comment(task_id, "Gestor de Projetos adicionado como responsavel automaticamente.")
                            totais["prj03"] += 1

            # --- PRJ-07: Tag "alto-valor" (redundante com project_alerts, mas garante cobertura) ---
            valor_field = custom_fields.get(CUSTOM_FIELD_VALOR)
            if valor_field and valor_field.get("value"):
                try:
                    if float(valor_field["value"]) > 50000 and "alto-valor" not in current_tags:
                        client.add_tag(task_id, "alto-valor")
                        totais["tag01"] += 1
                except (ValueError, TypeError):
                    pass

            # --- TAG-01: Tag "urgente" → Prioridade Urgente ---
            if "urgente" in current_tags:
                priority = task.get("priority", {})
                if priority and priority.get("id") not in ("1",):
                    print(f"  [TAG-01] {task_name} - Tag urgente → prioridade urgente")
                    set_task_priority_direct(task_id, 1)
                    totais["tag01"] += 1

            # --- TAG-02: Tag "interno" → Valor = 0 ---
            if "interno" in current_tags:
                valor_field = custom_fields.get(CUSTOM_FIELD_VALOR)
                if valor_field and valor_field.get("value") not in (None, "0", 0):
                    print(f"  [TAG-02] {task_name} - Tag interno → valor 0")
                    headers = {"Authorization": CLICKUP_TOKEN, "Content-Type": "application/json"}
                    requests.post(
                        f"https://api.clickup.com/api/v2/task/{task_id}/field/{CUSTOM_FIELD_VALOR}",
                        json={"value": 0},
                        headers=headers,
                    )
                    totais["tag02"] += 1

            # --- TAG-03: Tag "bloqueado" → Task de desbloqueio ---
            if "bloqueado" in current_tags and "desbloqueio-criado" not in current_tags:
                print(f"  [TAG-03] {task_name} - Tag bloqueado → criando task de desbloqueio")
                client.create_task(
                    list_id=list_id,
                    name=f"DESBLOQUEAR: {task_name}",
                    description=(
                        f"Task bloqueada identificada: {task_name}\n\n"
                        f"Acoes necessarias:\n"
                        f"1. Identificar a causa do bloqueio\n"
                        f"2. Definir responsavel pela resolucao\n"
                        f"3. Estimar prazo\n"
                        f"4. Remover tag 'bloqueado' ao resolver"
                    ),
                    priority=2,
                    tags=["desbloqueio", "impedimento"],
                )
                client.add_tag(task_id, "desbloqueio-criado")
                client.post_task_comment(task_id, "Task de desbloqueio criada automaticamente.")
                totais["tag03"] += 1

            # --- TAG-04: Tag "aprovado" → Comentario ---
            if "aprovado" in current_tags and "aprovacao-registrada" not in current_tags:
                print(f"  [TAG-04] {task_name} - Tag aprovado registrada")
                client.add_tag(task_id, "aprovacao-registrada")
                client.post_task_comment(task_id, "Aprovado! Mover para a proxima fase do workflow.")
                totais["tag04"] += 1

            # --- WKF-01: Status "concluido" → Celebracao ---
            if status in ("concluido", "concluído", "complete", "closed") and "celebracao-enviada" not in current_tags:
                print(f"  [WKF-01] {task_name} - Concluido, celebrando!")
                client.add_tag(task_id, "celebracao-enviada")
                client.post_task_comment(task_id, "Task concluida! Otimo trabalho.")
                totais["wkf01"] += 1

            # --- WKF-02: Status "em andamento" → Notificar ---
            if status in ("em andamento", "in progress") and "inicio-notificado" not in current_tags:
                print(f"  [WKF-02] {task_name} - Em andamento, notificando")
                client.add_tag(task_id, "inicio-notificado")
                client.post_task_comment(task_id, "Execucao iniciada! Responsaveis notificados.")
                totais["wkf02"] += 1

            # --- WKF-03: Checklist "Planejamento Estrategico" 100% → Tag ---
            if get_checklist_completion(task, "Planejamento Estrategico") and "planejamento-completo" not in current_tags:
                print(f"  [WKF-03] {task_name} - Planejamento 100%")
                client.add_tag(task_id, "planejamento-completo")
                client.post_task_comment(task_id, "Planejamento Estrategico concluido! Pronto para execucao.")
                totais["wkf03"] += 1

    # ===== COMERCIAL - COM-03 =====
    comercial_lists = {
        "Agenda Comercial": LIST_ID_AGENDA_COMERCIAL,
        "Sessao Estrategica": LIST_ID_SESSAO_ESTRATEGICA,
    }

    for list_name, list_id in comercial_lists.items():
        if not list_id:
            continue

        print(f"\n{'='*60}")
        print(f"Verificando comercial: {list_name}")
        print(f"{'='*60}")

        tasks = client.get_tasks(list_id, paginate=True, arquivada=False, incluir_fechadas=False)

        for task in tasks:
            task_id = task["id"]
            task_name = task["name"]
            current_tags = [t["name"] for t in task.get("tags", [])]
            status = task.get("status", {}).get("status", "").lower()

            # --- COM-03: Status "Negocio Fechado" → Onboarding ---
            if status in ("negocio fechado", "negócio fechado", "won", "fechado") and "onboarding-criado" not in current_tags:
                print(f"  [COM-03] {task_name} - Negocio fechado! Criando onboarding")
                client.create_task(
                    list_id=list_id,
                    name=f"ONBOARDING: {task_name}",
                    description=(
                        f"Novo cliente: {task_name}\n\n"
                        f"Acoes de onboarding:\n"
                        f"1. Enviar formulario de contrato\n"
                        f"2. Aguardar preenchimento\n"
                        f"3. Configurar acesso as ferramentas\n"
                        f"4. Agendar reuniao de kickoff\n"
                        f"5. Enviar boas-vindas"
                    ),
                    priority=2,
                    tags=["onboarding", "novo-cliente"],
                )
                client.add_tag(task_id, "onboarding-criado")
                client.post_task_comment(task_id, "Negocio fechado! Task de onboarding criada automaticamente.")
                totais["com03"] += 1

    # ===== RESUMO =====
    print(f"\n{'='*60}")
    print("RESUMO - WORKFLOW AUTOMATIONS")
    print(f"{'='*60}")
    print(f"[PRJ-01] Testes 100%:          {totais['prj01']}")
    print(f"[PRJ-02] Fase por checklist:   {totais['prj02']}")
    print(f"[PRJ-03] Auto-assign gestor:   {totais['prj03']}")
    print(f"[TAG-01] Urgente → prioridade: {totais['tag01']}")
    print(f"[TAG-02] Interno → valor 0:    {totais['tag02']}")
    print(f"[TAG-03] Bloqueado → tarefa:   {totais['tag03']}")
    print(f"[TAG-04] Aprovado registrado:  {totais['tag04']}")
    print(f"[WKF-01] Concluido celebracao: {totais['wkf01']}")
    print(f"[WKF-02] Em andamento notif.:  {totais['wkf02']}")
    print(f"[WKF-03] Planejamento 100%:    {totais['wkf03']}")
    print(f"[COM-03] Onboarding criado:    {totais['com03']}")
    total = sum(totais.values())
    if total == 0:
        print("Nenhuma acao necessaria no momento.")
    else:
        print(f"Total de acoes: {total}")


if __name__ == "__main__":
    try:
        run_workflow_automations()
        print("\nConcluido com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        raise
