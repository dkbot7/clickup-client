# 🔬 Pesquisa Técnica: Time Tracking (Rastreamento de Tempo)

**Data:** 2025-10-31
**Pesquisador:** Sistema Kaloi (Claude Code)
**Objetivo:** Registrar e buscar tempo gasto nas tasks via API ClickUp v2

---

## 📋 Índice

1. [Resumo Executivo](#resumo-executivo)
2. [Documentação Oficial da API](#documentação-oficial-da-api)
3. [Endpoints da API](#endpoints-da-api)
4. [Estrutura de Dados](#estrutura-de-dados)
5. [Conceitos Importantes](#conceitos-importantes)
6. [Limitações e Restrições](#limitações-e-restrições)
7. [Implementações Existentes em Python](#implementações-existentes-em-python)
8. [Exemplo de Implementação](#exemplo-de-implementação)
9. [Recomendações para o Projeto](#recomendações-para-o-projeto)
10. [Referências](#referências)
11. [Checklist de Implementação](#checklist-de-implementação)

---

## 🎯 Resumo Executivo

### Descobertas Principais

✅ **Time Tracking é totalmente suportado pela API v2 do ClickUp**
✅ **Dois conjuntos de endpoints: Modernos (recomendados) e Legacy (descontinuados)**
✅ **Suporta timer em tempo real (start/stop) e registro manual de tempo**
✅ **Campos suportados: duration, description, billable, tags**
⚠️ **Duração negativa indica timer em execução**
⚠️ **API retorna últimos 30 dias por padrão**
❌ **Não é possível filtrar por tags ou status billable via API (limitação conhecida)**

### Complexidade de Implementação

| Aspecto | Complexidade | Justificativa |
|---------|--------------|---------------|
| Criar time entry manual | 🟢 Baixa | POST simples com JSON |
| Start/Stop timer | 🟢 Baixa | Endpoints dedicados |
| Buscar time entries | 🟡 Média | Filtros por data e localização |
| Editar time entry | 🟡 Média | Requer timer_id |
| Relatórios complexos | 🔴 Alta | Necessita processamento local |

---

## 📚 Documentação Oficial da API

### Links Principais

**Endpoints Modernos (Recomendados):**
- **Create Time Entry**: https://developer.clickup.com/reference/createatimeentry
- **Get Time Entries**: https://developer.clickup.com/reference/gettimeentrieswithinadaterange
- **Start Timer**: https://developer.clickup.com/reference/startatimeentry
- **Stop Timer**: https://developer.clickup.com/reference/stopatimeentry
- **Get Running Timer**: https://developer.clickup.com/reference/getrunningtimeentry
- **Update Time Entry**: https://developer.clickup.com/reference/updateatimeentry
- **Delete Time Entry**: https://developer.clickup.com/reference/deleteatimeentry
- **Get Time Entry History**: https://developer.clickup.com/reference/gettimeentryhistory

**Endpoints Legacy (Não Recomendados):**
- **Track Time (Legacy)**: https://developer.clickup.com/reference/tracktime
- **Get Tracked Time (Legacy)**: https://developer.clickup.com/reference/gettrackedtime
- **Edit Time Tracked (Legacy)**: https://developer.clickup.com/reference/edittimetracked
- **Delete Time Tracked (Legacy)**: https://developer.clickup.com/reference/deletetimetracked

⚠️ **Recomendação do ClickUp:** "This is a legacy time tracking endpoint. We recommend using the Time Tracking API endpoints to manage time entries."

---

## 🔌 Endpoints da API

### 1. Criar Time Entry (Manual)

**Endpoint:** `POST /team/{team_id}/time_entries`

**Descrição:** Cria um registro de tempo manualmente (sem timer).

**Request Body:**
```json
{
  "duration": 3600000,
  "start": 1701388800000,
  "description": "Desenvolvimento da feature X",
  "billable": true,
  "tid": "task_id",
  "tags": [
    {
      "name": "desenvolvimento",
      "tag_fg": "#000000",
      "tag_bg": "#FF6B6B"
    }
  ]
}
```

**Campos:**
- `duration` (number, obrigatório) - Duração em **milissegundos**
- `start` (number, opcional) - Timestamp Unix em ms (padrão: agora)
- `description` (string, opcional) - Descrição do trabalho
- `billable` (boolean, opcional) - Se é faturável (padrão: false)
- `tid` (string, opcional) - Task ID (pode ser null para tempo geral)
- `tags` (array, opcional) - Tags/labels do time entry

**Resposta:**
```json
{
  "id": "timer_id_123",
  "task": {
    "id": "task_id",
    "name": "Task Name",
    "status": {
      "status": "in progress"
    }
  },
  "user": {
    "id": 123456,
    "username": "John Doe",
    "email": "john@example.com"
  },
  "billable": true,
  "start": "1701388800000",
  "end": "1701392400000",
  "duration": "3600000",
  "description": "Desenvolvimento da feature X",
  "tags": [
    {
      "name": "desenvolvimento",
      "tag_fg": "#000000",
      "tag_bg": "#FF6B6B"
    }
  ],
  "at": "1701388800000"
}
```

---

### 2. Iniciar Timer

**Endpoint:** `POST /team/{team_id}/time_entries/start`

**Descrição:** Inicia um timer em tempo real para o usuário autenticado.

**Request Body:**
```json
{
  "tid": "task_id",
  "description": "Trabalhando na feature",
  "billable": true,
  "tags": [
    {
      "name": "desenvolvimento"
    }
  ]
}
```

**Campos:**
- `tid` (string, obrigatório) - Task ID onde o timer será iniciado
- `description` (string, opcional) - Descrição do trabalho
- `billable` (boolean, opcional) - Se é faturável
- `tags` (array, opcional) - Tags do time entry

**Resposta:**
```json
{
  "id": "timer_id_456",
  "task": {...},
  "user": {...},
  "billable": true,
  "start": "1701388800000",
  "duration": "-3600000",
  "description": "Trabalhando na feature",
  "tags": [...]
}
```

⚠️ **Importante:** `duration` negativa indica timer em execução!

---

### 3. Parar Timer

**Endpoint:** `POST /team/{team_id}/time_entries/stop`

**Descrição:** Para o timer em execução do usuário autenticado.

**Request Body:** (vazio)

**Resposta:**
```json
{
  "id": "timer_id_456",
  "task": {...},
  "user": {...},
  "billable": true,
  "start": "1701388800000",
  "end": "1701392400000",
  "duration": "3600000",
  "description": "Trabalhando na feature"
}
```

---

### 4. Obter Timer em Execução

**Endpoint:** `GET /team/{team_id}/time_entries/current`

**Descrição:** Retorna o timer atualmente em execução do usuário autenticado.

**Query Parameters:** Nenhum

**Resposta (com timer ativo):**
```json
{
  "id": "timer_id_789",
  "task": {...},
  "user": {...},
  "billable": false,
  "start": "1701388800000",
  "duration": "-1800000",
  "description": "Debug do bug #123"
}
```

**Resposta (sem timer ativo):**
```json
{
  "data": []
}
```

---

### 5. Buscar Time Entries

**Endpoint:** `GET /team/{team_id}/time_entries`

**Descrição:** Retorna time entries filtrados por data e localização.

**Query Parameters:**
```
?start_date=1701388800000     # Timestamp Unix em ms (obrigatório)
&end_date=1701475200000       # Timestamp Unix em ms (obrigatório)
&assignee=123456              # User ID (opcional, múltiplos separados por vírgula)
&include_task_tags=true       # Incluir tags da task (opcional)
&include_location_names=true  # Incluir nomes de Space/Folder/List (opcional)
&space_id=901234567          # Filtrar por Space (opcional)
&folder_id=901234568         # Filtrar por Folder (opcional)
&list_id=901234569           # Filtrar por List (opcional)
&task_id=abc123              # Filtrar por Task (opcional)
```

⚠️ **Importante:** Apenas UM filtro de localização por vez (space_id OU folder_id OU list_id OU task_id)

**Comportamento padrão:**
- Retorna últimos **30 dias**
- Apenas time entries do usuário autenticado
- Use `assignee` para buscar de outros usuários

**Resposta:**
```json
{
  "data": [
    {
      "id": "timer_id_1",
      "task": {
        "id": "task_id",
        "name": "Task Name",
        "status": {"status": "in progress"},
        "tags": [...]
      },
      "user": {...},
      "billable": true,
      "start": "1701388800000",
      "end": "1701392400000",
      "duration": "3600000",
      "description": "Desenvolvimento",
      "tags": [...],
      "source": "web timer",
      "at": "1701388800000"
    }
  ]
}
```

---

### 6. Atualizar Time Entry

**Endpoint:** `PUT /team/{team_id}/time_entries/{timer_id}`

**Descrição:** Atualiza um time entry existente.

**Request Body:**
```json
{
  "duration": 7200000,
  "start": 1701388800000,
  "description": "Nova descrição",
  "billable": false,
  "tags": [
    {
      "name": "revisão",
      "tag_fg": "#FFFFFF",
      "tag_bg": "#4A90E2"
    }
  ]
}
```

**Resposta:** Time entry atualizado

---

### 7. Deletar Time Entry

**Endpoint:** `DELETE /team/{team_id}/time_entries/{timer_id}`

**Descrição:** Remove um time entry.

**Request Body:** Nenhum

**Resposta:** `200 OK` (sem body)

---

### 8. Obter Histórico de Time Entry

**Endpoint:** `GET /team/{team_id}/time_entries/{timer_id}/history`

**Descrição:** Retorna histórico de alterações de um time entry.

**Resposta:**
```json
{
  "data": [
    {
      "id": "history_id_1",
      "timer_id": "timer_id_123",
      "user": {...},
      "before": {
        "duration": "3600000",
        "description": "Antiga descrição"
      },
      "after": {
        "duration": "7200000",
        "description": "Nova descrição"
      },
      "date": "1701388800000"
    }
  ]
}
```

---

## 📊 Estrutura de Dados

### Objeto Time Entry

```python
{
    "id": str,                    # UUID do time entry
    "task": {                     # Task associada (pode ser null)
        "id": str,
        "name": str,
        "status": {
            "status": str,
            "color": str,
            "type": str
        },
        "tags": [...]             # Tags da task (se include_task_tags=true)
    },
    "user": {                     # Usuário que registrou o tempo
        "id": int,
        "username": str,
        "email": str,
        "color": str,
        "profilePicture": str
    },
    "billable": bool,             # Se é faturável
    "start": str,                 # Timestamp Unix em ms (string)
    "end": str,                   # Timestamp Unix em ms (string, null se timer rodando)
    "duration": str,              # Duração em ms (negativa = timer rodando)
    "description": str,           # Descrição do trabalho
    "tags": [                     # Tags do time entry
        {
            "name": str,
            "tag_fg": str,        # Cor do texto (hex)
            "tag_bg": str,        # Cor de fundo (hex)
            "creator": int        # User ID do criador
        }
    ],
    "source": str,                # Origem: "web timer", "mobile", "api", etc.
    "at": str,                    # Timestamp de criação (ms)
    "task_location": {            # Localização da task (se include_location_names=true)
        "list_name": str,
        "folder_name": str,
        "space_name": str
    }
}
```

### Tag Object

```python
{
    "name": str,                  # Nome da tag (obrigatório)
    "tag_fg": str,                # Cor do texto em hex (opcional, padrão: #000000)
    "tag_bg": str,                # Cor de fundo em hex (opcional, padrão: #FFFFFF)
    "creator": int                # User ID (apenas na resposta)
}
```

---

## 🧠 Conceitos Importantes

### 1. Duration Negativa = Timer Rodando

```python
# Timer em execução
{
    "duration": "-3600000",   # Negativo!
    "start": "1701388800000",
    "end": null               # Sem end
}

# Timer parado
{
    "duration": "3600000",    # Positivo
    "start": "1701388800000",
    "end": "1701392400000"
}
```

**Cálculo de duração atual de timer rodando:**
```python
import time

duration_abs = abs(int(time_entry["duration"]))  # Remove sinal negativo
start_time = int(time_entry["start"])
current_time = int(time.time() * 1000)  # Agora em ms

elapsed = current_time - start_time
print(f"Timer rodando há {elapsed / 1000 / 60:.0f} minutos")
```

### 2. Timestamps em Milissegundos

```python
# ❌ ERRADO: segundos
start = 1701388800  # 2024-12-01 00:00:00

# ✅ CORRETO: milissegundos
start = 1701388800000  # 2024-12-01 00:00:00

# Converter de datetime para ms
from datetime import datetime
dt = datetime(2024, 12, 1, 15, 30)
timestamp_ms = int(dt.timestamp() * 1000)
```

### 3. Billable vs Non-Billable

```python
# Tempo faturável (cobrar do cliente)
{
    "billable": True,
    "description": "Desenvolvimento de feature"
}

# Tempo não-faturável (interno, reunião, etc)
{
    "billable": False,
    "description": "Reunião de equipe"
}
```

### 4. Time Entry Sem Task

Time entries podem existir **sem task associada** (tempo geral):

```python
# Time entry ligado a task
{
    "tid": "task_id_123",
    "description": "Trabalhando na task"
}

# Time entry geral (sem task)
{
    "tid": None,
    "description": "Reunião de planejamento"
}
```

### 5. Tags de Time Entry vs Tags de Task

```python
# Tags da TASK (categories da task)
task = {
    "tags": [
        {"name": "Frontend", "tag_bg": "#FF6B6B"}
    ]
}

# Tags do TIME ENTRY (categorização do tempo)
time_entry = {
    "tags": [
        {"name": "desenvolvimento", "tag_bg": "#4A90E2"},
        {"name": "código", "tag_bg": "#2ECC71"}
    ]
}
```

São **independentes** e têm propósitos diferentes!

---

## ⚠️ Limitações e Restrições

### 1. Filtros Limitados

**❌ NÃO É POSSÍVEL:**
- Filtrar por tags de time entry
- Filtrar por status billable
- Buscar time entries arquivados

**Feature Request:** Existe solicitação oficial para adicionar filtros de `billable` e `tags`

### 2. Apenas Um Filtro de Localização

```python
# ❌ ERRADO: Múltiplos filtros de localização
params = {
    "space_id": "123",
    "folder_id": "456"  # Apenas um é permitido!
}

# ✅ CORRETO: Um filtro por vez
params = {
    "task_id": "abc123"  # Mais específico
}
```

### 3. Limite de 30 Dias por Padrão

```python
# Sem start_date/end_date = últimos 30 dias
entries = client.get_time_entries(team_id)

# Para buscar período maior, especifique datas
entries = client.get_time_entries(
    team_id,
    start_date=1698796800000,  # 01/11/2024
    end_date=1701475200000     # 01/12/2024
)
```

### 4. Um Timer por Usuário

Cada usuário pode ter apenas **1 timer rodando** por vez:

```python
# Tentar iniciar 2º timer = para o primeiro automaticamente
client.start_timer(team_id, task_id="task1")
client.start_timer(team_id, task_id="task2")  # Para timer de task1
```

### 5. Time Entries de Outros Usuários

```python
# Padrão: apenas seus próprios time entries
entries = client.get_time_entries(team_id, start_date, end_date)

# Para ver de outros usuários: especificar assignee
entries = client.get_time_entries(
    team_id,
    start_date,
    end_date,
    assignee="123456,789012"  # IDs separados por vírgula
)
```

⚠️ **Requer permissões adequadas no workspace!**

---

## 🐍 Implementações Existentes em Python

### 1. **clickupython** (Imzachjohnson)

**URL:** https://github.com/Imzachjohnson/clickupython

**Métodos de Time Tracking:**
```python
from clickupython import ClickUp

client = ClickUp(api_token)

# Obter time entries em range
entries = client.get_time_entries_in_range(
    team_id="123",
    start_date="1701388800000",
    end_date="1701475200000",
    assignees=["456", "789"]
)

# Obter time entry específico
entry = client.get_single_time_entry(
    team_id="123",
    timer_id="timer_456"
)

# Iniciar timer
timer = client.start_timer(
    team_id="123",
    timer_id="task_789"
)

# Parar timer
client.stop_timer(team_id="123")
```

**Prós:**
- ✅ Métodos específicos para time tracking
- ✅ API simples e direta

**Contras:**
- ❌ Não mantido ativamente
- ❌ Não cobre todos os endpoints (ex: tags, update)

### 2. **pyclickup** (jpetrucciani)

**URL:** https://github.com/jpetrucciani/pyclickup

**Abordagem:** Wrapper básico da API

**Uso:**
```python
from pyclickup import ClickUp

client = ClickUp(api_token)
# Acesso direto aos endpoints via requests
```

### 3. **ClickUp** (secdevopsai)

**URL:** https://github.com/secdevopsai/ClickUp

**Status:** Cliente básico, cobertura limitada

---

## 💡 Exemplo de Implementação

### Opção 1: Implementação Básica (Recomendada)

```python
# src/clickup_api/client.py

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta


def create_time_entry(
    self,
    team_id: Optional[str] = None,
    duration: int = None,
    task_id: Optional[str] = None,
    description: Optional[str] = None,
    billable: bool = False,
    start: Optional[int] = None,
    tags: Optional[List[Dict]] = None
) -> Optional[Dict]:
    """
    Cria um registro de tempo manualmente.

    Args:
        team_id: ID do workspace (usa self.team_id se não fornecido)
        duration: Duração em MILISSEGUNDOS (obrigatório)
        task_id: ID da task (opcional, None = tempo geral)
        description: Descrição do trabalho
        billable: Se é faturável (padrão: False)
        start: Timestamp Unix em ms (padrão: agora)
        tags: Lista de tags [{"name": "tag1", "tag_bg": "#FF0000"}]

    Exemplos:
        # 1 hora de trabalho
        client.create_time_entry(
            duration=3600000,  # 1h em ms
            task_id="abc123",
            description="Desenvolvimento da feature X",
            billable=True
        )

        # Com helper de tempo
        from src.clickup_api.helpers.date_utils import fuzzy_time_to_seconds
        duration_ms = fuzzy_time_to_seconds("2 horas") * 1000
        client.create_time_entry(duration=duration_ms, task_id="abc123")

    Returns:
        dict com time entry criado
    """
    tid = team_id or self.team_id

    if not duration:
        print("[red]✗ Duração é obrigatória[/red]")
        return None

    payload = {
        "duration": duration,
        "billable": billable
    }

    if task_id:
        payload["tid"] = task_id

    if description:
        payload["description"] = description

    if start:
        payload["start"] = start

    if tags:
        payload["tags"] = tags

    result = self._request("POST", f"team/{tid}/time_entries", json=payload)

    if result:
        duration_hours = duration / 1000 / 3600
        print(f"[green]✓ Time entry criado: {duration_hours:.2f}h[/green]")

    return result


def start_timer(
    self,
    task_id: str,
    team_id: Optional[str] = None,
    description: Optional[str] = None,
    billable: bool = False,
    tags: Optional[List[Dict]] = None
) -> Optional[Dict]:
    """
    Inicia um timer em tempo real.

    Args:
        task_id: ID da task (obrigatório)
        team_id: ID do workspace (usa self.team_id se não fornecido)
        description: Descrição do trabalho
        billable: Se é faturável
        tags: Tags do time entry

    Exemplos:
        # Iniciar timer simples
        client.start_timer("task_id")

        # Com descrição e billable
        client.start_timer(
            "task_id",
            description="Desenvolvimento",
            billable=True
        )

    Returns:
        dict com timer iniciado (duration negativa!)
    """
    tid = team_id or self.team_id

    payload = {
        "tid": task_id,
        "billable": billable
    }

    if description:
        payload["description"] = description

    if tags:
        payload["tags"] = tags

    result = self._request("POST", f"team/{tid}/time_entries/start", json=payload)

    if result:
        print(f"[green]✓ Timer iniciado na task {task_id}[/green]")

    return result


def stop_timer(self, team_id: Optional[str] = None) -> Optional[Dict]:
    """
    Para o timer em execução do usuário autenticado.

    Args:
        team_id: ID do workspace (usa self.team_id se não fornecido)

    Returns:
        dict com timer parado
    """
    tid = team_id or self.team_id

    result = self._request("POST", f"team/{tid}/time_entries/stop")

    if result:
        duration_ms = int(result.get("duration", 0))
        duration_hours = duration_ms / 1000 / 3600
        print(f"[green]✓ Timer parado: {duration_hours:.2f}h registradas[/green]")

    return result


def get_running_timer(self, team_id: Optional[str] = None) -> Optional[Dict]:
    """
    Obtém o timer atualmente em execução.

    Args:
        team_id: ID do workspace

    Returns:
        dict com timer rodando ou None se não houver
    """
    tid = team_id or self.team_id

    result = self._request("GET", f"team/{tid}/time_entries/current")

    if result and result.get("data"):
        timer = result["data"][0] if isinstance(result["data"], list) else result["data"]
        print(f"[yellow]⏱ Timer rodando: {timer.get('description', 'Sem descrição')}[/yellow]")
        return timer

    print("[blue]ℹ Nenhum timer em execução[/blue]")
    return None


def get_time_entries(
    self,
    team_id: Optional[str] = None,
    start_date: Optional[int] = None,
    end_date: Optional[int] = None,
    assignee: Optional[List[int]] = None,
    task_id: Optional[str] = None,
    **filters
) -> Optional[Dict]:
    """
    Busca time entries filtrados por data e localização.

    Args:
        team_id: ID do workspace
        start_date: Timestamp Unix em ms (padrão: 30 dias atrás)
        end_date: Timestamp Unix em ms (padrão: agora)
        assignee: Lista de user IDs
        task_id: ID da task
        **filters: Outros filtros (space_id, folder_id, list_id, etc)

    Exemplos:
        # Últimos 30 dias (padrão)
        entries = client.get_time_entries()

        # Período específico
        from datetime import datetime, timedelta
        end = int(datetime.now().timestamp() * 1000)
        start = int((datetime.now() - timedelta(days=7)).timestamp() * 1000)
        entries = client.get_time_entries(start_date=start, end_date=end)

        # De uma task específica
        entries = client.get_time_entries(task_id="abc123")

    Returns:
        dict com lista de time entries
    """
    tid = team_id or self.team_id

    params = {}

    # Datas padrão: últimos 30 dias
    if not start_date:
        start_date = int((datetime.now() - timedelta(days=30)).timestamp() * 1000)
    if not end_date:
        end_date = int(datetime.now().timestamp() * 1000)

    params["start_date"] = start_date
    params["end_date"] = end_date

    if assignee:
        params["assignee"] = ",".join(map(str, assignee))

    if task_id:
        params["task_id"] = task_id

    # Outros filtros
    params.update(filters)

    result = self._request("GET", f"team/{tid}/time_entries", params=params)

    if result:
        count = len(result.get("data", []))
        print(f"[green]✓ {count} time entries encontrados[/green]")

    return result


def update_time_entry(
    self,
    timer_id: str,
    team_id: Optional[str] = None,
    **updates
) -> Optional[Dict]:
    """
    Atualiza um time entry existente.

    Args:
        timer_id: ID do time entry
        team_id: ID do workspace
        **updates: Campos a atualizar (duration, description, billable, start, tags)

    Exemplos:
        # Atualizar duração
        client.update_time_entry("timer_id", duration=7200000)

        # Atualizar descrição e billable
        client.update_time_entry(
            "timer_id",
            description="Nova descrição",
            billable=True
        )

    Returns:
        dict com time entry atualizado
    """
    tid = team_id or self.team_id

    result = self._request(
        "PUT",
        f"team/{tid}/time_entries/{timer_id}",
        json=updates
    )

    if result:
        print(f"[green]✓ Time entry atualizado[/green]")

    return result


def delete_time_entry(
    self,
    timer_id: str,
    team_id: Optional[str] = None
) -> bool:
    """
    Deleta um time entry.

    Args:
        timer_id: ID do time entry
        team_id: ID do workspace

    Returns:
        True se deletado com sucesso
    """
    tid = team_id or self.team_id

    result = self._request("DELETE", f"team/{tid}/time_entries/{timer_id}")

    if result is not None:
        print(f"[green]✓ Time entry deletado[/green]")
        return True

    return False
```

### Opção 2: Helper para Calcular Totais

```python
# src/clickup_api/helpers/time_tracking.py

from typing import List, Dict
from datetime import datetime, timedelta


def calculate_total_time(time_entries: List[Dict]) -> Dict[str, float]:
    """
    Calcula totais de tempo de uma lista de time entries.

    Args:
        time_entries: Lista de time entries

    Returns:
        dict com totais (total_ms, total_hours, billable_hours, non_billable_hours)
    """
    total_ms = 0
    billable_ms = 0
    non_billable_ms = 0

    for entry in time_entries:
        duration = abs(int(entry.get("duration", 0)))  # Remove negativo se timer rodando

        total_ms += duration

        if entry.get("billable", False):
            billable_ms += duration
        else:
            non_billable_ms += duration

    return {
        "total_ms": total_ms,
        "total_hours": total_ms / 1000 / 3600,
        "billable_hours": billable_ms / 1000 / 3600,
        "non_billable_hours": non_billable_ms / 1000 / 3600
    }


def format_duration(milliseconds: int) -> str:
    """
    Formata duração em ms para string legível.

    Args:
        milliseconds: Duração em ms

    Returns:
        String formatada (ex: "2h 30m")
    """
    seconds = abs(milliseconds) / 1000
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)

    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"


def group_by_task(time_entries: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Agrupa time entries por task.

    Args:
        time_entries: Lista de time entries

    Returns:
        dict {task_id: [entries]}
    """
    grouped = {}

    for entry in time_entries:
        task = entry.get("task")
        task_id = task.get("id") if task else "no_task"

        if task_id not in grouped:
            grouped[task_id] = []

        grouped[task_id].append(entry)

    return grouped


def group_by_date(time_entries: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Agrupa time entries por data.

    Args:
        time_entries: Lista de time entries

    Returns:
        dict {date_str: [entries]}
    """
    grouped = {}

    for entry in time_entries:
        start_ms = int(entry.get("start", 0))
        date = datetime.fromtimestamp(start_ms / 1000).strftime("%Y-%m-%d")

        if date not in grouped:
            grouped[date] = []

        grouped[date].append(entry)

    return grouped


# Uso
from src.clickup_api.helpers.time_tracking import (
    calculate_total_time,
    format_duration,
    group_by_task
)

entries = client.get_time_entries(task_id="abc123")
totals = calculate_total_time(entries["data"])

print(f"Total: {totals['total_hours']:.2f}h")
print(f"Faturável: {totals['billable_hours']:.2f}h")
print(f"Não-faturável: {totals['non_billable_hours']:.2f}h")
```

---

## 🎯 Recomendações para o Projeto

### 1. Implementação Incremental

**Fase 1 (Básico - Essencial):**
- ✅ Implementar `create_time_entry(duration, task_id, ...)`
- ✅ Implementar `get_time_entries(start_date, end_date, ...)`
- ✅ Implementar `start_timer(task_id)` e `stop_timer()`
- ✅ Implementar `get_running_timer()`

**Fase 2 (Intermediário):**
- ✅ Implementar `update_time_entry(timer_id, ...)`
- ✅ Implementar `delete_time_entry(timer_id)`
- ✅ Criar helpers de cálculo (`calculate_total_time`, etc)
- ✅ Suporte a tags em time entries

**Fase 3 (Avançado):**
- ✅ Relatórios automáticos (por task, por dia, por usuário)
- ✅ Export para CSV/Excel
- ✅ Integração com `fuzzy_time_to_seconds()` para duração
- ✅ Cache de time entries recentes

### 2. Usar Endpoints Modernos

```python
# ✅ BOM: Usar endpoints novos
client.create_time_entry(...)  # /team/{id}/time_entries
client.start_timer(...)        # /team/{id}/time_entries/start

# ❌ EVITAR: Endpoints legacy
client.track_time(...)         # /task/{id}/time - LEGACY
```

### 3. Helpers de Conversão

```python
# Integrar com date_utils existente
from src.clickup_api.helpers.date_utils import fuzzy_time_to_seconds

# Criar time entry com duração em linguagem natural
duration_text = "2 horas e 30 minutos"
duration_seconds = fuzzy_time_to_seconds(duration_text)
duration_ms = duration_seconds * 1000

client.create_time_entry(
    duration=duration_ms,
    task_id="abc123"
)
```

### 4. Validação de Dados

```python
def create_time_entry_safe(client, duration, task_id, **kwargs):
    """Helper com validação"""

    # Validar duração
    if duration <= 0:
        print("Erro: Duração deve ser positiva")
        return None

    # Converter se necessário
    if duration < 1000:  # Provavelmente em segundos
        duration = duration * 1000
        print(f"Convertido para ms: {duration}")

    # Validar task existe
    task = client.get_task(task_id)
    if not task:
        print(f"Erro: Task {task_id} não encontrada")
        return None

    return client.create_time_entry(duration, task_id, **kwargs)
```

### 5. Feedback Visual com Rich

```python
def show_time_summary(time_entries):
    """Mostra resumo visual de time entries"""
    from rich.table import Table
    from rich.console import Console

    console = Console()
    table = Table(title="Time Entries Summary")

    table.add_column("Task", style="cyan")
    table.add_column("Duração", style="green")
    table.add_column("Billable", style="yellow")
    table.add_column("Descrição", style="white")

    for entry in time_entries:
        task_name = entry.get("task", {}).get("name", "Sem task")
        duration = format_duration(int(entry.get("duration", 0)))
        billable = "✓" if entry.get("billable") else "✗"
        description = entry.get("description", "")

        table.add_row(task_name, duration, billable, description)

    console.print(table)
```

---

## 📖 Referências

### Documentação Oficial

**Endpoints Modernos:**
1. https://developer.clickup.com/reference/createatimeentry
2. https://developer.clickup.com/reference/gettimeentrieswithinadaterange
3. https://developer.clickup.com/reference/startatimeentry
4. https://developer.clickup.com/reference/stopatimeentry
5. https://developer.clickup.com/reference/getrunningtimeentry
6. https://developer.clickup.com/reference/updateatimeentry
7. https://developer.clickup.com/reference/deleteatimeentry

**Guias:**
- https://help.clickup.com/hc/en-us/articles/6304106812823-Track-time-on-tasks
- https://help.clickup.com/hc/en-us/articles/6304291811479-Intro-to-time-tracking

### Repositórios GitHub

1. **clickupython**: https://github.com/Imzachjohnson/clickupython
2. **pyclickup**: https://github.com/jpetrucciani/pyclickup
3. **ClickUp**: https://github.com/secdevopsai/ClickUp

---

## ✅ Checklist de Implementação

- [ ] Implementar `create_time_entry(duration, task_id, ...)`
- [ ] Implementar `start_timer(task_id)`
- [ ] Implementar `stop_timer()`
- [ ] Implementar `get_running_timer()`
- [ ] Implementar `get_time_entries(start_date, end_date, ...)`
- [ ] Implementar `update_time_entry(timer_id, ...)`
- [ ] Implementar `delete_time_entry(timer_id)`
- [ ] Criar helper `calculate_total_time(entries)`
- [ ] Criar helper `format_duration(ms)`
- [ ] Criar helper `group_by_task(entries)`
- [ ] Criar helper `group_by_date(entries)`
- [ ] Adicionar suporte a tags em time entries
- [ ] Integrar com `fuzzy_time_to_seconds()` para duração
- [ ] Criar testes unitários
- [ ] Criar exemplos práticos no README
- [ ] Documentar limitações
- [ ] Testar com workspace real

---

**Próximos Passos:**
1. Implementar métodos básicos em `src/clickup_api/client.py`
2. Criar helpers em `src/clickup_api/helpers/time_tracking.py`
3. Criar exemplos em `docs/TIME_TRACKING_EXAMPLES.md`
4. Adicionar testes em `tests/test_time_tracking.py`

---

**Autor:** Sistema Kaloi (Claude Code)
**Data:** 2025-10-31
**Versão:** 1.0
