# 🔬 Pesquisa Técnica: Funcionalidades Avançadas (C-H)

**Data:** 2025-10-31
**Pesquisador:** Sistema Kaloi (Claude Code)
**Objetivo:** Documentar 6 funcionalidades avançadas da API ClickUp v2

---

## 📋 Índice

1. [C. Attachments (Anexos)](#c-attachments-anexos)
2. [D. Checklists (Listas de Verificação)](#d-checklists-listas-de-verificação)
3. [E. Goals (Objetivos/Metas)](#e-goals-objetivosmetas)
4. [F. Members (Gerenciamento de Membros)](#f-members-gerenciamento-de-membros)
5. [G. Webhooks (Notificações)](#g-webhooks-notificações)
6. [H. Views (Visualizações Customizadas)](#h-views-visualizações-customizadas)
7. [Checklist de Implementação](#checklist-de-implementação)

---

# C. Attachments (Anexos)

## 🎯 Resumo

✅ **Upload de arquivos para tasks**
✅ **Tamanho máximo: 1 GB**
✅ **Multipart/form-data obrigatório**
✅ **Apenas arquivos locais (não cloud)**
⚠️ **Não retorna attachments de docs**

## 🔌 Endpoints

### 1. Upload Attachment
**Endpoint:** `POST /task/{task_id}/attachment`

**Headers:**
```http
Authorization: YOUR_TOKEN
Content-Type: multipart/form-data
```

**Request (Python):**
```python
file = {"attachment": ('filename.png', open('file.png', 'rb'))}
headers = {'Authorization': token}
response = requests.post(
    f'https://api.clickup.com/api/v2/task/{task_id}/attachment',
    files=file,
    headers=headers
)
```

**Limitações:**
- ✅ Tamanho máximo: 1 GB
- ✅ Sem restrição de tipo de arquivo
- ❌ Arquivos em cloud não suportados
- ❌ Múltiplos files: usar `attachment[0]`, `attachment[1]`

## 💡 Implementação

```python
def upload_attachment(self, task_id: str, file_path: str) -> Optional[Dict]:
    """
    Faz upload de anexo para uma task.

    Args:
        task_id: ID da task
        file_path: Caminho do arquivo local

    Returns:
        dict com dados do attachment
    """
    import os

    if not os.path.exists(file_path):
        print(f"[red]✗ Arquivo não encontrado: {file_path}[/red]")
        return None

    filename = os.path.basename(file_path)

    with open(file_path, 'rb') as f:
        files = {"attachment": (filename, f)}

        result = self._request(
            "POST",
            f"task/{task_id}/attachment",
            files=files
        )

    if result:
        print(f"[green]✓ Anexo enviado: {filename}[/green]")

    return result
```

## 📚 Referências
- https://developer.clickup.com/reference/createtaskattachment
- https://developer.clickup.com/docs/attachments

---

# D. Checklists (Listas de Verificação)

## 🎯 Resumo

✅ **Criar checklists em tasks**
✅ **Adicionar/editar items**
✅ **Reordenar checklists**
✅ **Marcar items como concluídos**

## 🔌 Endpoints

### 1. Create Checklist
**Endpoint:** `POST /task/{task_id}/checklist`

**Request Body:**
```json
{
  "name": "Checklist de Deploy"
}
```

### 2. Create Checklist Item
**Endpoint:** `POST /checklist/{checklist_id}/checklist_item`

**Request Body:**
```json
{
  "name": "Rodar testes unitários",
  "assignee": 123456
}
```

### 3. Edit Checklist Item
**Endpoint:** `PUT /checklist/{checklist_id}/checklist_item/{item_id}`

**Request Body:**
```json
{
  "name": "Atualizar nome do item",
  "resolved": true,
  "assignee": 789012
}
```

### 4. Delete Checklist
**Endpoint:** `DELETE /checklist/{checklist_id}`

## 💡 Implementação

```python
def create_checklist(
    self,
    task_id: str,
    name: str
) -> Optional[Dict]:
    """Cria checklist em uma task."""
    payload = {"name": name}
    result = self._request(
        "POST",
        f"task/{task_id}/checklist",
        json=payload
    )

    if result:
        print(f"[green]✓ Checklist criada: {name}[/green]")

    return result


def add_checklist_item(
    self,
    checklist_id: str,
    name: str,
    assignee: Optional[int] = None
) -> Optional[Dict]:
    """Adiciona item a um checklist."""
    payload = {"name": name}

    if assignee:
        payload["assignee"] = assignee

    result = self._request(
        "POST",
        f"checklist/{checklist_id}/checklist_item",
        json=payload
    )

    if result:
        print(f"[green]✓ Item adicionado: {name}[/green]")

    return result


def complete_checklist_item(
    self,
    checklist_id: str,
    item_id: str
) -> Optional[Dict]:
    """Marca item como concluído."""
    return self._request(
        "PUT",
        f"checklist/{checklist_id}/checklist_item/{item_id}",
        json={"resolved": True}
    )
```

## 📚 Referências
- https://developer.clickup.com/reference/createchecklist
- https://developer.clickup.com/reference/createchecklistitem
- https://developer.clickup.com/reference/editchecklistitem

---

# E. Goals (Objetivos/Metas)

## 🎯 Resumo

✅ **Criar metas quantitativas**
✅ **Targets com progresso**
✅ **Múltiplos owners**
✅ **Due dates**

## 🔌 Endpoints

### 1. Create Goal
**Endpoint:** `POST /team/{team_id}/goal`

**Request Body:**
```json
{
  "name": "Aumentar Vendas Q1 2025",
  "description": "Meta de vendas para o primeiro trimestre",
  "due_date": 1735689600000,
  "color": "#FF6B6B",
  "multiple_owners": true,
  "owners": [123456, 789012]
}
```

### 2. Get Goals
**Endpoint:** `GET /team/{team_id}/goal`

### 3. Get Goal
**Endpoint:** `GET /goal/{goal_id}`

**Resposta:**
```json
{
  "goal": {
    "id": "goal_123",
    "name": "Aumentar Vendas Q1 2025",
    "description": "...",
    "due_date": "1735689600000",
    "color": "#FF6B6B",
    "owners": [...],
    "key_results": [
      {
        "id": "kr_1",
        "name": "Atingir R$ 100.000",
        "type": "number",
        "steps_start": 0,
        "steps_end": 100000,
        "steps_current": 45000
      }
    ]
  }
}
```

## 💡 Implementação

```python
def create_goal(
    self,
    name: str,
    team_id: Optional[str] = None,
    description: Optional[str] = None,
    due_date: Optional[int] = None,
    color: Optional[str] = None,
    owners: Optional[List[int]] = None
) -> Optional[Dict]:
    """
    Cria uma meta (goal) no workspace.

    Args:
        name: Nome da meta
        team_id: ID do workspace
        description: Descrição
        due_date: Timestamp Unix em ms
        color: Cor em hex (#RRGGBB)
        owners: Lista de user IDs

    Returns:
        dict com goal criado
    """
    tid = team_id or self.team_id

    payload = {"name": name}

    if description:
        payload["description"] = description
    if due_date:
        payload["due_date"] = due_date
    if color:
        payload["color"] = color
    if owners:
        payload["owners"] = owners
        payload["multiple_owners"] = len(owners) > 1

    result = self._request("POST", f"team/{tid}/goal", json=payload)

    if result:
        print(f"[green]✓ Meta criada: {name}[/green]")

    return result


def get_goals(self, team_id: Optional[str] = None) -> Optional[Dict]:
    """Lista todas as metas do workspace."""
    tid = team_id or self.team_id
    return self._request("GET", f"team/{tid}/goal")


def get_goal(self, goal_id: str) -> Optional[Dict]:
    """Busca meta específica com seus targets."""
    return self._request("GET", f"goal/{goal_id}")
```

## 📚 Referências
- https://developer.clickup.com/reference/creategoal
- https://developer.clickup.com/reference/getgoals
- https://developer.clickup.com/reference/getgoal

---

# F. Members (Gerenciamento de Membros)

## 🎯 Resumo

✅ **Listar membros por List/Task**
✅ **Adicionar assignees**
✅ **User Groups**
⚠️ **Não assign teams diretamente**

## 🔌 Endpoints

### 1. Get List Members
**Endpoint:** `GET /list/{list_id}/member`

### 2. Get Task Members
**Endpoint:** `GET /task/{task_id}/member`

### 3. Add Assignee (via Update Task)
**Endpoint:** `PUT /task/{task_id}`

**Request Body:**
```json
{
  "assignees": {
    "add": [123456, 789012],
    "rem": []
  }
}
```

### 4. Get Authorized Teams (Workspaces)
**Endpoint:** `GET /team`

**Retorna:** Lista de workspaces e seus membros

## 💡 Implementação

```python
def get_list_members(self, list_id: str) -> Optional[Dict]:
    """Lista membros com acesso a uma lista."""
    result = self._request("GET", f"list/{list_id}/member")

    if result:
        members = result.get("members", [])
        print(f"[green]✓ {len(members)} membros encontrados[/green]")

    return result


def add_assignees(
    self,
    task_id: str,
    user_ids: List[int]
) -> Optional[Dict]:
    """
    Adiciona assignees a uma task.

    Args:
        task_id: ID da task
        user_ids: Lista de user IDs para adicionar

    Returns:
        dict com task atualizada
    """
    payload = {
        "assignees": {
            "add": user_ids,
            "rem": []
        }
    }

    result = self._request("PUT", f"task/{task_id}", json=payload)

    if result:
        print(f"[green]✓ {len(user_ids)} assignees adicionados[/green]")

    return result


def remove_assignees(
    self,
    task_id: str,
    user_ids: List[int]
) -> Optional[Dict]:
    """Remove assignees de uma task."""
    payload = {
        "assignees": {
            "add": [],
            "rem": user_ids
        }
    }

    return self._request("PUT", f"task/{task_id}", json=payload)
```

## ⚠️ Limitações

- ❌ Não é possível assignar **teams** (apenas indivíduos)
- ⚠️ `assignees` são arrays de integers (user IDs)
- ⚠️ Team IDs são GUIDs (não compatíveis)

## 📚 Referências
- https://developer.clickup.com/reference/getlistmembers
- https://developer.clickup.com/reference/gettaskmembers

---

# G. Webhooks (Notificações)

## 🎯 Resumo

✅ **Receber eventos em tempo real**
✅ **20+ tipos de eventos**
✅ **Signature verification**
✅ **Health monitoring**
⚠️ **IP dinâmico (não dedicado)**

## 🔌 Endpoints

### 1. Create Webhook
**Endpoint:** `POST /team/{team_id}/webhook`

**Request Body:**
```json
{
  "endpoint": "https://seu-servidor.com/clickup-webhook",
  "events": [
    "taskCreated",
    "taskUpdated",
    "taskDeleted"
  ],
  "space_id": "901234567"
}
```

### 2. Get Webhooks
**Endpoint:** `GET /team/{team_id}/webhook`

### 3. Update Webhook
**Endpoint:** `PUT /webhook/{webhook_id}`

### 4. Delete Webhook
**Endpoint:** `DELETE /webhook/{webhook_id}`

## 📡 Eventos Disponíveis

### Task Events
- `taskCreated` - Task criada
- `taskUpdated` - Task atualizada
- `taskDeleted` - Task deletada
- `taskPriorityUpdated` - Prioridade alterada
- `taskStatusUpdated` - Status alterado
- `taskAssigneeUpdated` - Assignee mudou
- `taskDueDateUpdated` - Due date alterada
- `taskTagUpdated` - Tags modificadas
- `taskMoved` - Task movida
- `taskCommentPosted` - Comentário adicionado
- `taskTimeEstimateUpdated` - Estimativa alterada

### List Events
- `listCreated`
- `listUpdated`
- `listDeleted`

### Folder Events
- `folderCreated`
- `folderUpdated`
- `folderDeleted`

### Space Events
- `spaceCreated`
- `spaceUpdated`
- `spaceDeleted`

### Goal Events
- `goalCreated`
- `goalUpdated`
- `goalDeleted`

## 🔐 Webhook Signature Verification

```python
import hmac
import hashlib

def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """
    Verifica assinatura do webhook ClickUp.

    Args:
        payload: Body da requisição (bytes)
        signature: Header X-Signature
        secret: Webhook secret do ClickUp

    Returns:
        True se válido
    """
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)
```

## 💡 Implementação (Webhook Listener)

```python
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)
WEBHOOK_SECRET = "your_webhook_secret"

@app.route('/clickup-webhook', methods=['POST'])
def clickup_webhook():
    """Endpoint para receber webhooks do ClickUp."""

    # Verificar signature
    signature = request.headers.get('X-Signature')
    payload = request.get_data()

    if not verify_signature(payload, signature, WEBHOOK_SECRET):
        return jsonify({"error": "Invalid signature"}), 401

    # Processar evento
    data = request.json
    event_type = data.get('event')

    if event_type == 'taskCreated':
        task_id = data['task_id']
        print(f"Nova task criada: {task_id}")
        # Processar...

    elif event_type == 'taskUpdated':
        task_id = data['task_id']
        print(f"Task atualizada: {task_id}")
        # Processar...

    return jsonify({"status": "received"}), 200


def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verifica assinatura HMAC SHA256."""
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)


if __name__ == '__main__':
    app.run(port=5000)
```

## 💡 Implementação (Criar Webhook)

```python
def create_webhook(
    self,
    endpoint_url: str,
    events: List[str],
    team_id: Optional[str] = None,
    space_id: Optional[str] = None,
    folder_id: Optional[str] = None,
    list_id: Optional[str] = None
) -> Optional[Dict]:
    """
    Cria um webhook.

    Args:
        endpoint_url: URL que receberá os eventos
        events: Lista de eventos (ex: ["taskCreated", "taskUpdated"])
        team_id: ID do workspace
        space_id: Filtrar por space (opcional)
        folder_id: Filtrar por folder (opcional)
        list_id: Filtrar por list (opcional)

    Returns:
        dict com webhook criado
    """
    tid = team_id or self.team_id

    payload = {
        "endpoint": endpoint_url,
        "events": events
    }

    # Apenas UM filtro de localização
    if space_id:
        payload["space_id"] = space_id
    elif folder_id:
        payload["folder_id"] = folder_id
    elif list_id:
        payload["list_id"] = list_id

    result = self._request("POST", f"team/{tid}/webhook", json=payload)

    if result:
        webhook_id = result.get("id")
        print(f"[green]✓ Webhook criado: {webhook_id}[/green]")

    return result


def get_webhooks(self, team_id: Optional[str] = None) -> Optional[Dict]:
    """Lista todos os webhooks."""
    tid = team_id or self.team_id
    return self._request("GET", f"team/{tid}/webhook")


def delete_webhook(self, webhook_id: str) -> bool:
    """Deleta um webhook."""
    result = self._request("DELETE", f"webhook/{webhook_id}")

    if result is not None:
        print(f"[green]✓ Webhook deletado[/green]")
        return True

    return False
```

## ⚠️ Notas Importantes

- ClickUp **NÃO tem IP dedicado** para webhooks
- Usar **HTTPS** (recomendado)
- Health check: ClickUp pinga endpoint periodicamente
- Timeout: Endpoint deve responder em < 30s
- Adicionar attachment **não** dispara `taskUpdated`

## 📚 Referências
- https://developer.clickup.com/reference/createwebhook
- https://developer.clickup.com/docs/webhooks
- https://developer.clickup.com/docs/webhooksignature

---

# H. Views (Visualizações Customizadas)

## 🎯 Resumo

✅ **Criar views em qualquer nível**
✅ **4 tipos: list, board, calendar, gantt**
✅ **Grouping, sorting, filtering**
✅ **Update configurações**
❌ **Page views não suportadas (Docs, Whiteboards)**

## 🔌 Endpoints

### 1. Get List Views
**Endpoint:** `GET /list/{list_id}/view`

### 2. Get Folder Views
**Endpoint:** `GET /folder/{folder_id}/view`

### 3. Get Space Views
**Endpoint:** `GET /space/{space_id}/view`

### 4. Get Workspace Views
**Endpoint:** `GET /team/{team_id}/view`

### 5. Get View
**Endpoint:** `GET /view/{view_id}`

### 6. Get View Tasks
**Endpoint:** `GET /view/{view_id}/task`

### 7. Update View
**Endpoint:** `PUT /view/{view_id}`

**Request Body:**
```json
{
  "name": "Minha View Customizada",
  "grouping": {
    "field": "status",
    "dir": 1
  },
  "sorting": {
    "fields": [
      {
        "field": "due_date",
        "dir": 1
      }
    ]
  },
  "filters": {
    "op": "AND",
    "fields": [
      {
        "field": "priority",
        "operator": "=",
        "value": 2
      }
    ]
  }
}
```

## 📊 Tipos de View

| Tipo | Valor | Descrição |
|------|-------|-----------|
| `list` | - | Lista simples |
| `board` | - | Kanban board |
| `calendar` | - | Visualização de calendário |
| `gantt` | - | Gráfico de Gantt |

## 🏗️ Níveis de Hierarquia

| Nível | Type Value |
|-------|------------|
| Workspace | 7 |
| Space | 4 |
| Folder | 5 |
| List | 6 |

## 💡 Implementação

```python
def get_list_views(self, list_id: str) -> Optional[Dict]:
    """Lista views de uma lista."""
    result = self._request("GET", f"list/{list_id}/view")

    if result:
        views = result.get("views", [])
        print(f"[green]✓ {len(views)} views encontradas[/green]")

    return result


def get_view(self, view_id: str) -> Optional[Dict]:
    """Busca view específica."""
    return self._request("GET", f"view/{view_id}")


def get_view_tasks(
    self,
    view_id: str,
    page: int = 0
) -> Optional[Dict]:
    """
    Busca tasks de uma view.

    Args:
        view_id: ID da view
        page: Página (padrão: 0)

    Returns:
        dict com tasks da view
    """
    params = {"page": page}
    result = self._request("GET", f"view/{view_id}/task", params=params)

    if result:
        tasks = result.get("tasks", [])
        print(f"[green]✓ {len(tasks)} tasks na view[/green]")

    return result


def update_view(
    self,
    view_id: str,
    name: Optional[str] = None,
    grouping: Optional[Dict] = None,
    sorting: Optional[Dict] = None,
    filters: Optional[Dict] = None
) -> Optional[Dict]:
    """
    Atualiza configurações de uma view.

    Args:
        view_id: ID da view
        name: Novo nome
        grouping: Agrupamento {"field": "status", "dir": 1}
        sorting: Ordenação {"fields": [{"field": "due_date", "dir": 1}]}
        filters: Filtros {"op": "AND", "fields": [...]}

    Returns:
        dict com view atualizada
    """
    payload = {}

    if name:
        payload["name"] = name
    if grouping:
        payload["grouping"] = grouping
    if sorting:
        payload["sorting"] = sorting
    if filters:
        payload["filters"] = filters

    result = self._request("PUT", f"view/{view_id}", json=payload)

    if result:
        print(f"[green]✓ View atualizada[/green]")

    return result
```

## 📚 Referências
- https://developer.clickup.com/docs/views
- https://developer.clickup.com/reference/getlistviews
- https://developer.clickup.com/reference/updateview
- https://developer.clickup.com/docs/filter-views

---

# ✅ Checklist de Implementação

## Attachments (C)
- [ ] Implementar `upload_attachment(task_id, file_path)`
- [ ] Validar tamanho < 1GB
- [ ] Suporte a múltiplos arquivos
- [ ] Tratamento de erros (arquivo não existe, etc)

## Checklists (D)
- [ ] Implementar `create_checklist(task_id, name)`
- [ ] Implementar `add_checklist_item(checklist_id, name, assignee)`
- [ ] Implementar `complete_checklist_item(checklist_id, item_id)`
- [ ] Implementar `delete_checklist(checklist_id)`

## Goals (E)
- [ ] Implementar `create_goal(name, due_date, owners)`
- [ ] Implementar `get_goals(team_id)`
- [ ] Implementar `get_goal(goal_id)`
- [ ] Suporte a targets/key results

## Members (F)
- [ ] Implementar `get_list_members(list_id)`
- [ ] Implementar `get_task_members(task_id)`
- [ ] Implementar `add_assignees(task_id, user_ids)`
- [ ] Implementar `remove_assignees(task_id, user_ids)`

## Webhooks (G)
- [ ] Implementar `create_webhook(endpoint, events, filters)`
- [ ] Implementar `get_webhooks(team_id)`
- [ ] Implementar `delete_webhook(webhook_id)`
- [ ] Criar exemplo de webhook listener (Flask/FastAPI)
- [ ] Implementar signature verification

## Views (H)
- [ ] Implementar `get_list_views(list_id)`
- [ ] Implementar `get_view(view_id)`
- [ ] Implementar `get_view_tasks(view_id)`
- [ ] Implementar `update_view(view_id, ...)`
- [ ] Suporte a filtros, grouping e sorting

---

**Autor:** Sistema Kaloi (Claude Code)
**Data:** 2025-10-31
**Versão:** 1.0
