# 📊 Resumo Executivo: Time Tracking

**TL;DR - O que você precisa saber sobre Time Tracking na API ClickUp**

---

## ⚡ Quick Facts

| Aspecto | Informação |
|---------|------------|
| **Endpoints principais** | `POST /team/{id}/time_entries` (criar)<br>`POST /team/{id}/time_entries/start` (timer)<br>`POST /team/{id}/time_entries/stop` (parar) |
| **Campos suportados** | duration, description, billable, tags, start |
| **Timer em tempo real** | ✅ Sim (start/stop automático) |
| **Registro manual** | ✅ Sim (com duração fixa) |
| **Período padrão busca** | Últimos 30 dias |
| **Complexidade** | 🟢 Baixa |

---

## ✅ O Que Funciona

```python
# ✅ Registrar tempo manualmente
client.create_time_entry(
    duration=3600000,  # 1h em ms
    task_id="abc123",
    description="Desenvolvimento",
    billable=True
)

# ✅ Usar timer (start/stop)
client.start_timer(task_id="abc123")
# ... trabalhar ...
client.stop_timer()

# ✅ Buscar time entries
entries = client.get_time_entries(
    start_date=start_ms,
    end_date=end_ms
)
```

---

## ❌ O Que NÃO Funciona

```python
# ❌ Endpoints legacy (descontinuados)
client.track_time(task_id, ...)  # Use create_time_entry

# ❌ Filtrar por tags ou billable status
entries = client.get_time_entries(billable=True)  # NÃO SUPORTADO

# ❌ Múltiplos filtros de localização
entries = client.get_time_entries(
    space_id="123",
    folder_id="456"  # Apenas UM filtro por vez!
)
```

---

## 🎯 2 Formas de Registrar Tempo

### 1. Registro Manual (Tempo Passado)

**Use quando:** Lembrou de registrar depois

```python
# Trabalhei 2 horas ontem
client.create_time_entry(
    duration=7200000,  # 2h em ms
    task_id="abc123",
    description="Desenvolvimento da feature"
)
```

### 2. Timer em Tempo Real (Automático)

**Use quando:** Quer rastrear enquanto trabalha

```python
# Começar a trabalhar
client.start_timer(task_id="abc123")

# Quando terminar
client.stop_timer()  # Registra automaticamente
```

---

## 🔑 3 Conceitos Essenciais

### 1. Duration em MILISSEGUNDOS

```python
# ❌ ERRADO - segundos
duration = 3600  # 1 hora

# ✅ CORRETO - milissegundos
duration = 3600000  # 1 hora (× 1000)

# ✅ Helper
from src.clickup_api.helpers.date_utils import fuzzy_time_to_seconds
duration_ms = fuzzy_time_to_seconds("2 horas") * 1000
```

### 2. Duration Negativa = Timer Rodando

```python
# Timer em execução
{
    "duration": "-3600000",  # Negativo!
    "start": "1701388800000",
    "end": null
}

# Timer parado
{
    "duration": "3600000",   # Positivo
    "start": "1701388800000",
    "end": "1701392400000"
}
```

### 3. Billable vs Non-Billable

```python
# Faturável (cobrar do cliente)
billable=True

# Não-faturável (interno, reunião, etc)
billable=False
```

---

## ⚠️ Principais Armadilhas

### 1. Timestamps em segundos vs milissegundos
```python
# ❌ ERRADO
duration = 3600  # segundos

# ✅ CORRETO
duration = 3600000  # milissegundos (×1000)
```

### 2. Esquecer de parar timer
```python
# Sempre verificar antes de sair
timer = client.get_running_timer()
if timer:
    client.stop_timer()
    print("Timer parado!")
```

### 3. Filtros de busca limitados
```python
# ❌ Não tem filtro nativo
entries = client.get_time_entries(billable=True)  # NÃO EXISTE

# ✅ Filtrar manualmente
entries = client.get_time_entries()
billable_entries = [e for e in entries["data"] if e.get("billable")]
```

### 4. Apenas um filtro de localização
```python
# ❌ ERRADO - múltiplos filtros
params = {"space_id": "123", "list_id": "456"}

# ✅ CORRETO - apenas um
params = {"task_id": "abc123"}  # Mais específico
```

---

## 📝 Receita Básica

### Registrar Tempo Manual

```python
from src.clickup_api.client import KaloiClickUpClient
from src.clickup_api.helpers.date_utils import fuzzy_time_to_seconds

client = KaloiClickUpClient()

# 1 hora e 30 minutos de trabalho
duration_seconds = fuzzy_time_to_seconds("1 hora e 30 minutos")
duration_ms = duration_seconds * 1000

client.create_time_entry(
    duration=duration_ms,
    task_id="abc123",
    description="Desenvolvimento da API",
    billable=True
)
```

### Usar Timer

```python
# Iniciar
client.start_timer(
    task_id="abc123",
    description="Trabalhando na feature"
)

print("⏱ Timer iniciado! Trabalhe na task...")

# ... trabalhar ...

# Parar
client.stop_timer()
print("✓ Tempo registrado!")
```

### Buscar Registros

```python
from datetime import datetime, timedelta

# Última semana
end = datetime.now()
start = end - timedelta(days=7)

entries = client.get_time_entries(
    start_date=int(start.timestamp() * 1000),
    end_date=int(end.timestamp() * 1000)
)

# Calcular total
total_ms = sum(abs(int(e["duration"])) for e in entries["data"])
total_hours = total_ms / 1000 / 3600

print(f"Total da semana: {total_hours:.2f}h")
```

---

## 🚀 Fluxo de Trabalho Recomendado

```python
# 1. Começar o dia - iniciar timer
client.start_timer(
    task_id="task_atual",
    description="Desenvolvimento",
    billable=True
)

# 2. Trocar de task - para e inicia novo
current = client.get_running_timer()
if current:
    client.stop_timer()

client.start_timer(
    task_id="nova_task",
    description="Code review"
)

# 3. Pausa (almoço) - parar timer
client.stop_timer()

# 4. Voltar - reiniciar
client.start_timer(task_id="task_atual")

# 5. Fim do dia - parar timer
client.stop_timer()
```

---

## 📊 Cálculos Comuns

### Total de Horas

```python
entries = client.get_time_entries()

total_ms = sum(
    abs(int(e["duration"]))
    for e in entries["data"]
)

total_hours = total_ms / 1000 / 3600
print(f"Total: {total_hours:.2f}h")
```

### Billable vs Non-Billable

```python
billable_ms = sum(
    abs(int(e["duration"]))
    for e in entries["data"]
    if e.get("billable")
)

non_billable_ms = sum(
    abs(int(e["duration"]))
    for e in entries["data"]
    if not e.get("billable")
)

print(f"Faturável: {billable_ms / 1000 / 3600:.2f}h")
print(f"Não-faturável: {non_billable_ms / 1000 / 3600:.2f}h")
```

### Tempo por Task

```python
from collections import defaultdict

by_task = defaultdict(int)

for entry in entries["data"]:
    task = entry.get("task")
    task_id = task["id"] if task else "no_task"
    duration = abs(int(entry["duration"]))

    by_task[task_id] += duration

# Mostrar top 5
for task_id, total_ms in sorted(
    by_task.items(),
    key=lambda x: x[1],
    reverse=True
)[:5]:
    hours = total_ms / 1000 / 3600
    print(f"{task_id}: {hours:.2f}h")
```

---

## 💡 Dicas Práticas

### 1. Sempre Use Helpers de Tempo

```python
# ✅ BOM: Usar helpers
from src.clickup_api.helpers.date_utils import fuzzy_time_to_seconds

duration_ms = fuzzy_time_to_seconds("2 horas e 30 minutos") * 1000

# ❌ RUIM: Calcular manualmente
duration_ms = 2 * 60 * 60 * 1000 + 30 * 60 * 1000
```

### 2. Verificar Timer Antes de Sair

```python
def cleanup_timers(client):
    """Chamar ao sair do app"""
    timer = client.get_running_timer()
    if timer:
        print("⚠ Você tem um timer rodando!")
        client.stop_timer()
        print("✓ Timer parado automaticamente")

# No final do script
cleanup_timers(client)
```

### 3. Exportar para Análise

```python
# Buscar dados
entries = client.get_time_entries()

# Exportar para CSV/Excel para análise detalhada
import csv

with open("horas.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Data", "Task", "Horas", "Billable"])

    for e in entries["data"]:
        writer.writerow([
            e["start"],
            e.get("task", {}).get("name", "N/A"),
            abs(int(e["duration"])) / 1000 / 3600,
            e.get("billable")
        ])
```

---

## 🔗 Próximos Passos

1. **Ler:** [TIME_TRACKING_RESEARCH.md](TIME_TRACKING_RESEARCH.md) - Pesquisa completa
2. **Praticar:** [TIME_TRACKING_EXAMPLES.md](TIME_TRACKING_EXAMPLES.md) - 15+ exemplos
3. **Implementar:** Ver checklist em TIME_TRACKING_RESEARCH.md

---

## 📚 Recursos

- **Documentação oficial:** https://developer.clickup.com/reference/createatimeentry
- **Start Timer:** https://developer.clickup.com/reference/startatimeentry
- **Get Entries:** https://developer.clickup.com/reference/gettimeentrieswithinadaterange

---

## 🆚 Time Tracking vs Custom Fields

| Aspecto | Time Tracking | Custom Fields |
|---------|---------------|---------------|
| **Complexidade** | 🟢 Baixa | 🟡 Média |
| **Atualização em lote** | ✅ N/A | ❌ Não suportado |
| **Timer em tempo real** | ✅ Sim | ❌ N/A |
| **Filtros de busca** | 🟡 Limitados | ✅ Por lista |
| **Uso comum** | Rastreamento de horas | Dados customizados |

---

**Criado em:** 2025-10-31
**Autor:** Sistema Kaloi
**Tempo de leitura:** 3 minutos
