# 📘 Exemplos Práticos: Time Tracking

**Guia de uso de rastreamento de tempo no ClickUp Client**

---

## 📋 Índice

1. [Setup Inicial](#setup-inicial)
2. [Registrar Tempo Manualmente](#registrar-tempo-manualmente)
3. [Usar Timer em Tempo Real](#usar-timer-em-tempo-real)
4. [Buscar Time Entries](#buscar-time-entries)
5. [Atualizar e Deletar](#atualizar-e-deletar)
6. [Casos de Uso Reais](#casos-de-uso-reais)
7. [Relatórios e Análises](#relatórios-e-análises)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 Setup Inicial

```python
from src.clickup_api.client import KaloiClickUpClient

# Inicializar cliente
client = KaloiClickUpClient()

# IDs necessários
team_id = "YOUR_TEAM_ID"  # Seu workspace ID (do .env)
task_id = "abc123xyz"   # ID da task
```

---

## ⏱️ Registrar Tempo Manualmente

### Exemplo 1: Registrar 1 Hora de Trabalho

```python
# 1 hora = 3600 segundos = 3600000 milissegundos
client.create_time_entry(
    duration=3600000,
    task_id="abc123",
    description="Desenvolvimento da feature X",
    billable=True
)
```

### Exemplo 2: Usando Helper de Tempo

```python
from src.clickup_api.helpers.date_utils import fuzzy_time_to_seconds

# Linguagem natural para duração
duration_text = "2 horas e 30 minutos"
duration_seconds = fuzzy_time_to_seconds(duration_text)
duration_ms = duration_seconds * 1000  # Converter para ms

client.create_time_entry(
    duration=duration_ms,
    task_id="abc123",
    description="Reunião com cliente",
    billable=False
)
```

### Exemplo 3: Registrar Tempo em Horário Específico

```python
from datetime import datetime

# Trabalhou ontem das 14h às 16h (2 horas)
start_time = datetime(2024, 10, 30, 14, 0)  # 30/10/2024 14:00
start_timestamp = int(start_time.timestamp() * 1000)

client.create_time_entry(
    duration=7200000,  # 2 horas em ms
    task_id="abc123",
    start=start_timestamp,
    description="Desenvolvimento backend",
    billable=True
)
```

### Exemplo 4: Tempo Geral (Sem Task)

```python
# Registrar tempo que não está ligado a uma task específica
client.create_time_entry(
    duration=1800000,  # 30 minutos
    task_id=None,      # Sem task
    description="Reunião de planejamento da sprint",
    billable=False
)
```

### Exemplo 5: Com Tags

```python
client.create_time_entry(
    duration=5400000,  # 1.5h
    task_id="abc123",
    description="Code review",
    billable=True,
    tags=[
        {
            "name": "revisão",
            "tag_fg": "#FFFFFF",
            "tag_bg": "#4A90E2"
        },
        {
            "name": "código",
            "tag_fg": "#000000",
            "tag_bg": "#2ECC71"
        }
    ]
)
```

---

## 🎮 Usar Timer em Tempo Real

### Exemplo 1: Iniciar e Parar Timer Simples

```python
# Iniciar timer
client.start_timer(
    task_id="abc123",
    description="Desenvolvimento da API"
)

# ... trabalhar na task ...

# Parar timer
client.stop_timer()
```

### Exemplo 2: Timer com Billable e Tags

```python
# Iniciar timer faturável
client.start_timer(
    task_id="abc123",
    description="Implementação de feature para cliente VIP",
    billable=True,
    tags=[
        {"name": "cliente-vip", "tag_bg": "#FF6B6B"},
        {"name": "desenvolvimento", "tag_bg": "#4A90E2"}
    ]
)

print("⏱ Timer iniciado! Trabalhe na task...")

# Quando terminar
client.stop_timer()
print("✓ Timer parado e tempo registrado!")
```

### Exemplo 3: Verificar Timer em Execução

```python
# Verificar se há timer rodando
timer = client.get_running_timer()

if timer:
    print(f"Timer ativo: {timer.get('description')}")
    print(f"Task: {timer.get('task', {}).get('name')}")

    # Calcular quanto tempo já passou
    import time
    start_ms = int(timer["start"])
    current_ms = int(time.time() * 1000)
    elapsed_ms = current_ms - start_ms
    elapsed_hours = elapsed_ms / 1000 / 3600

    print(f"Tempo decorrido: {elapsed_hours:.2f}h")
else:
    print("Nenhum timer em execução")
```

### Exemplo 4: Trocar de Task (Para Timer Atual e Inicia Novo)

```python
# Parar timer atual
current = client.get_running_timer()
if current:
    client.stop_timer()
    print(f"Timer anterior parado: {current.get('description')}")

# Iniciar novo timer em outra task
client.start_timer(
    task_id="xyz789",
    description="Trabalhando em bug crítico"
)
print("Novo timer iniciado!")
```

### Exemplo 5: Timer com Tratamento de Erro

```python
def start_timer_safe(client, task_id, description, billable=False):
    """Inicia timer com verificação de timer existente"""

    # Verificar se já há timer rodando
    current = client.get_running_timer()

    if current:
        print(f"⚠ Já existe timer rodando: {current.get('description')}")
        resposta = input("Deseja parar e iniciar novo? (s/n): ")

        if resposta.lower() == "s":
            client.stop_timer()
            print("✓ Timer anterior parado")
        else:
            print("Operação cancelada")
            return None

    # Iniciar novo timer
    return client.start_timer(
        task_id=task_id,
        description=description,
        billable=billable
    )

# Uso
start_timer_safe(
    client,
    task_id="abc123",
    description="Desenvolvimento",
    billable=True
)
```

---

## 🔍 Buscar Time Entries

### Exemplo 1: Últimos 30 Dias (Padrão)

```python
# Busca time entries dos últimos 30 dias
entries = client.get_time_entries()

print(f"Total de registros: {len(entries.get('data', []))}")

for entry in entries["data"]:
    duration_h = int(entry["duration"]) / 1000 / 3600
    task_name = entry.get("task", {}).get("name", "Sem task")
    print(f"  • {task_name}: {duration_h:.2f}h - {entry.get('description', '')}")
```

### Exemplo 2: Período Específico (Última Semana)

```python
from datetime import datetime, timedelta

# Definir período
end = datetime.now()
start = end - timedelta(days=7)

# Converter para timestamps em ms
start_ms = int(start.timestamp() * 1000)
end_ms = int(end.timestamp() * 1000)

# Buscar
entries = client.get_time_entries(
    start_date=start_ms,
    end_date=end_ms
)

print(f"Time entries da última semana: {len(entries['data'])}")
```

### Exemplo 3: Filtrar por Task Específica

```python
# Buscar tempo gasto em uma task específica
entries = client.get_time_entries(
    task_id="abc123"
)

# Calcular total
total_ms = sum(abs(int(e["duration"])) for e in entries["data"])
total_hours = total_ms / 1000 / 3600

print(f"Tempo total na task: {total_hours:.2f}h")
```

### Exemplo 4: Buscar de Múltiplos Usuários

```python
# IDs dos usuários (obter com get_user_info ou team members)
user_ids = [123456, 789012, 345678]

entries = client.get_time_entries(
    assignee=user_ids
)

# Agrupar por usuário
from collections import defaultdict
by_user = defaultdict(list)

for entry in entries["data"]:
    user_id = entry["user"]["id"]
    by_user[user_id].append(entry)

# Mostrar total por usuário
for user_id, user_entries in by_user.items():
    total_h = sum(abs(int(e["duration"])) for e in user_entries) / 1000 / 3600
    username = user_entries[0]["user"]["username"]
    print(f"{username}: {total_h:.2f}h")
```

### Exemplo 5: Filtros Avançados

```python
# Buscar com inclusão de informações extras
entries = client.get_time_entries(
    start_date=start_ms,
    end_date=end_ms,
    task_id="abc123",
    include_task_tags=True,        # Incluir tags da task
    include_location_names=True    # Incluir nomes de Space/Folder/List
)

for entry in entries["data"]:
    task_location = entry.get("task_location", {})
    space = task_location.get("space_name", "N/A")
    list_name = task_location.get("list_name", "N/A")

    print(f"Space: {space}, List: {list_name}")
```

---

## ✏️ Atualizar e Deletar

### Exemplo 1: Atualizar Duração

```python
# Aumentar duração de 1h para 2h
timer_id = "timer_abc123"

client.update_time_entry(
    timer_id=timer_id,
    duration=7200000  # 2h em ms
)
```

### Exemplo 2: Atualizar Descrição e Billable

```python
client.update_time_entry(
    timer_id="timer_abc123",
    description="Desenvolvimento completo da feature X (finalizado)",
    billable=True
)
```

### Exemplo 3: Adicionar Tags a Time Entry Existente

```python
client.update_time_entry(
    timer_id="timer_abc123",
    tags=[
        {"name": "concluído", "tag_bg": "#2ECC71"},
        {"name": "revisado", "tag_bg": "#3498DB"}
    ]
)
```

### Exemplo 4: Deletar Time Entry

```python
# Deletar registro incorreto
client.delete_time_entry(timer_id="timer_abc123")
```

### Exemplo 5: Atualizar em Lote

```python
def update_billable_status(client, timer_ids, billable=True):
    """Atualiza status billable de múltiplos time entries"""

    for timer_id in timer_ids:
        client.update_time_entry(
            timer_id=timer_id,
            billable=billable
        )

    print(f"✓ {len(timer_ids)} time entries atualizados para billable={billable}")

# Uso
timer_ids = ["timer1", "timer2", "timer3"]
update_billable_status(client, timer_ids, billable=True)
```

---

## 🎯 Casos de Uso Reais

### Caso 1: Dia de Trabalho Completo

```python
from datetime import datetime, timedelta
from src.clickup_api.helpers.date_utils import fuzzy_time_to_seconds

# Começar o dia
print("🌅 Iniciando dia de trabalho...")

# 9h - 10h30: Desenvolvimento
client.create_time_entry(
    duration=fuzzy_time_to_seconds("1 hora e 30 minutos") * 1000,
    task_id="task_feature_x",
    description="Implementação da API REST",
    billable=True,
    tags=[{"name": "desenvolvimento", "tag_bg": "#4A90E2"}]
)

# 10h30 - 11h: Reunião
client.create_time_entry(
    duration=fuzzy_time_to_seconds("30 minutos") * 1000,
    task_id=None,  # Sem task
    description="Daily stand-up",
    billable=False,
    tags=[{"name": "reunião", "tag_bg": "#FFA500"}]
)

# 11h - 13h: Desenvolvimento (com timer)
client.start_timer(
    task_id="task_feature_x",
    description="Continuação da API REST",
    billable=True
)

# ... trabalhar 2 horas ...

client.stop_timer()

print("✓ Dia registrado com sucesso!")
```

### Caso 2: Relatório Semanal de Horas

```python
def weekly_report(client, user_id=None):
    """Gera relatório de horas da semana"""
    from datetime import datetime, timedelta

    # Última semana
    end = datetime.now()
    start = end - timedelta(days=7)

    entries = client.get_time_entries(
        start_date=int(start.timestamp() * 1000),
        end_date=int(end.timestamp() * 1000),
        assignee=[user_id] if user_id else None
    )

    # Calcular totais
    total_ms = 0
    billable_ms = 0

    for entry in entries["data"]:
        duration = abs(int(entry["duration"]))
        total_ms += duration

        if entry.get("billable"):
            billable_ms += duration

    total_h = total_ms / 1000 / 3600
    billable_h = billable_ms / 1000 / 3600
    non_billable_h = (total_ms - billable_ms) / 1000 / 3600

    print("=" * 50)
    print("RELATÓRIO SEMANAL DE HORAS")
    print("=" * 50)
    print(f"Período: {start.strftime('%d/%m/%Y')} - {end.strftime('%d/%m/%Y')}")
    print(f"\nTotal de registros: {len(entries['data'])}")
    print(f"Total de horas: {total_h:.2f}h")
    print(f"  • Faturáveis: {billable_h:.2f}h ({billable_h/total_h*100:.1f}%)")
    print(f"  • Não-faturáveis: {non_billable_h:.2f}h ({non_billable_h/total_h*100:.1f}%)")
    print("=" * 50)

# Uso
weekly_report(client)
```

### Caso 3: Controle de Timer Automático

```python
class TimerManager:
    """Gerenciador automático de timers"""

    def __init__(self, client):
        self.client = client
        self.current_task = None

    def switch_to_task(self, task_id, description="", billable=False):
        """Troca para outra task automaticamente"""

        # Parar timer atual se houver
        current = self.client.get_running_timer()
        if current:
            self.client.stop_timer()
            print(f"✓ Timer anterior parado")

        # Iniciar novo
        self.client.start_timer(
            task_id=task_id,
            description=description,
            billable=billable
        )

        self.current_task = task_id
        print(f"✓ Timer iniciado na task {task_id}")

    def pause(self):
        """Pausa o timer (para almoço, pausa, etc)"""
        current = self.client.get_running_timer()
        if current:
            self.client.stop_timer()
            print("⏸ Timer pausado")
        else:
            print("Nenhum timer em execução")

    def resume(self):
        """Resume o timer na task atual"""
        if self.current_task:
            self.client.start_timer(
                task_id=self.current_task,
                description="Continuação do trabalho"
            )
            print("▶ Timer resumido")
        else:
            print("Nenhuma task para resumir")

    def finish_day(self):
        """Finaliza o dia de trabalho"""
        current = self.client.get_running_timer()
        if current:
            self.client.stop_timer()
            print("✓ Timer parado")

        print("🏁 Dia de trabalho finalizado!")

# Uso
manager = TimerManager(client)

# Manhã
manager.switch_to_task("task1", "Desenvolvimento", billable=True)

# Pausa para almoço
manager.pause()

# Volta do almoço
manager.resume()

# Trocar para outra task
manager.switch_to_task("task2", "Code review", billable=True)

# Fim do dia
manager.finish_day()
```

### Caso 4: Sincronizar Tempo de Subtasks

```python
def sync_subtasks_time(client, parent_task_id):
    """
    Soma tempo de subtasks e registra no parent
    """

    # Obter parent task
    parent = client.get_task(parent_task_id)
    subtasks = parent.get("subtasks", [])

    if not subtasks:
        print("Nenhuma subtask encontrada")
        return

    # Buscar time entries de cada subtask
    total_ms = 0

    for subtask in subtasks:
        entries = client.get_time_entries(task_id=subtask["id"])

        for entry in entries.get("data", []):
            total_ms += abs(int(entry["duration"]))

    # Registrar total no parent
    if total_ms > 0:
        client.create_time_entry(
            duration=total_ms,
            task_id=parent_task_id,
            description=f"Total consolidado de {len(subtasks)} subtasks"
        )

        total_h = total_ms / 1000 / 3600
        print(f"✓ Tempo consolidado: {total_h:.2f}h")

# Uso
sync_subtasks_time(client, "parent_task_id")
```

### Caso 5: Export para CSV

```python
def export_time_entries_csv(client, filename="time_entries.csv"):
    """Exporta time entries para CSV"""
    import csv
    from datetime import datetime, timedelta

    # Buscar último mês
    end = datetime.now()
    start = end - timedelta(days=30)

    entries = client.get_time_entries(
        start_date=int(start.timestamp() * 1000),
        end_date=int(end.timestamp() * 1000),
        include_task_tags=True,
        include_location_names=True
    )

    # Escrever CSV
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            "Data", "Task", "Duração (h)", "Descrição",
            "Billable", "Tags", "Space", "List"
        ])

        # Dados
        for entry in entries["data"]:
            start_dt = datetime.fromtimestamp(int(entry["start"]) / 1000)
            duration_h = abs(int(entry["duration"])) / 1000 / 3600
            task_name = entry.get("task", {}).get("name", "Sem task")
            description = entry.get("description", "")
            billable = "Sim" if entry.get("billable") else "Não"
            tags = ", ".join(t["name"] for t in entry.get("tags", []))
            location = entry.get("task_location", {})
            space = location.get("space_name", "")
            list_name = location.get("list_name", "")

            writer.writerow([
                start_dt.strftime("%d/%m/%Y %H:%M"),
                task_name,
                f"{duration_h:.2f}",
                description,
                billable,
                tags,
                space,
                list_name
            ])

    print(f"✓ Exportado para {filename}")

# Uso
export_time_entries_csv(client, "minhas_horas.csv")
```

---

## 📊 Relatórios e Análises

### Análise 1: Tempo por Task

```python
def analyze_by_task(entries):
    """Agrupa e analisa tempo por task"""
    from collections import defaultdict

    by_task = defaultdict(lambda: {"total_ms": 0, "entries": []})

    for entry in entries["data"]:
        task = entry.get("task")
        task_id = task["id"] if task else "no_task"
        task_name = task["name"] if task else "Sem task"

        duration = abs(int(entry["duration"]))
        by_task[task_id]["total_ms"] += duration
        by_task[task_id]["entries"].append(entry)
        by_task[task_id]["name"] = task_name

    # Ordenar por tempo (maior primeiro)
    sorted_tasks = sorted(
        by_task.items(),
        key=lambda x: x[1]["total_ms"],
        reverse=True
    )

    print("TEMPO POR TASK")
    print("=" * 60)
    for task_id, data in sorted_tasks[:10]:  # Top 10
        hours = data["total_ms"] / 1000 / 3600
        count = len(data["entries"])
        print(f"{data['name']:40} {hours:6.2f}h ({count} registros)")

# Uso
entries = client.get_time_entries()
analyze_by_task(entries)
```

### Análise 2: Tempo por Dia da Semana

```python
def analyze_by_weekday(entries):
    """Analisa padrões de trabalho por dia da semana"""
    from datetime import datetime
    from collections import defaultdict

    by_weekday = defaultdict(int)
    weekday_names = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

    for entry in entries["data"]:
        start_dt = datetime.fromtimestamp(int(entry["start"]) / 1000)
        weekday = start_dt.weekday()
        duration = abs(int(entry["duration"]))

        by_weekday[weekday] += duration

    print("\nTEMPO POR DIA DA SEMANA")
    print("=" * 40)
    for i in range(7):
        hours = by_weekday[i] / 1000 / 3600
        bar = "█" * int(hours / 2)
        print(f"{weekday_names[i]}: {hours:5.2f}h {bar}")

# Uso
analyze_by_weekday(entries)
```

### Análise 3: Produtividade (Billable vs Non-Billable)

```python
def productivity_report(entries):
    """Relatório de produtividade billable vs non-billable"""

    billable_ms = 0
    non_billable_ms = 0
    billable_count = 0
    non_billable_count = 0

    for entry in entries["data"]:
        duration = abs(int(entry["duration"]))

        if entry.get("billable"):
            billable_ms += duration
            billable_count += 1
        else:
            non_billable_ms += duration
            non_billable_count += 1

    total_ms = billable_ms + non_billable_ms
    billable_h = billable_ms / 1000 / 3600
    non_billable_h = non_billable_ms / 1000 / 3600
    total_h = total_ms / 1000 / 3600

    print("\nRELATÓRIO DE PRODUTIVIDADE")
    print("=" * 50)
    print(f"Total: {total_h:.2f}h ({billable_count + non_billable_count} registros)")
    print(f"\nFaturável: {billable_h:.2f}h ({billable_count} registros)")
    print(f"  {billable_h/total_h*100:.1f}% do tempo total")
    print(f"\nNão-faturável: {non_billable_h:.2f}h ({non_billable_count} registros)")
    print(f"  {non_billable_h/total_h*100:.1f}% do tempo total")

    # Gráfico ASCII
    billable_bar = "█" * int(billable_h / 2)
    non_billable_bar = "░" * int(non_billable_h / 2)
    print(f"\n{billable_bar}{non_billable_bar}")
    print(f"{'Faturável':^{len(billable_bar)}}{'Não-faturável':^{len(non_billable_bar)}}")

# Uso
productivity_report(entries)
```

---

## 🔧 Troubleshooting

### Problema: "Duration deve ser em milissegundos"

```python
# ❌ ERRADO: segundos
duration = 3600

# ✅ CORRETO: milissegundos
duration = 3600000

# ✅ OU: converter de segundos
duration_seconds = 3600
duration_ms = duration_seconds * 1000
```

### Problema: Timer não para

```python
# Verificar se há timer rodando
timer = client.get_running_timer()

if timer:
    print(f"Timer encontrado: {timer.get('id')}")
    client.stop_timer()
else:
    print("Nenhum timer em execução")
```

### Problema: Time entries não aparecem

```python
# Verificar período de busca
from datetime import datetime, timedelta

# Expandir período
end = datetime.now()
start = end - timedelta(days=90)  # 90 dias

entries = client.get_time_entries(
    start_date=int(start.timestamp() * 1000),
    end_date=int(end.timestamp() * 1000)
)

print(f"Encontrados: {len(entries.get('data', []))} registros")
```

### Problema: Não consegue ver time entries de outros usuários

```python
# Precisa especificar assignee
entries = client.get_time_entries(
    assignee=[123456, 789012]  # IDs dos usuários
)

# Verificar permissões no workspace
# Pode ser necessário permissão de admin
```

### Problema: Duration negativa

```python
# Duration negativa = timer ainda rodando!
for entry in entries["data"]:
    duration = int(entry["duration"])

    if duration < 0:
        print(f"⏱ Timer em execução: {entry.get('description')}")
        print(f"  Iniciado há {abs(duration) / 1000 / 60:.0f} minutos")
    else:
        hours = duration / 1000 / 3600
        print(f"✓ Concluído: {hours:.2f}h")
```

---

**Autor:** Sistema Kaloi
**Data:** 2025-10-31
**Versão:** 1.0
