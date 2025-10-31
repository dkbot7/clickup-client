# 📊 Resumo Executivo: Funcionalidades Avançadas (C-H)

**TL;DR - 6 funcionalidades em 5 minutos**

---

## ⚡ Quick Reference

| Feature | Endpoint Principal | Complexidade | Status |
|---------|-------------------|--------------|--------|
| **Attachments** | `POST /task/{id}/attachment` | 🟢 Baixa | ✅ Pesquisado |
| **Checklists** | `POST /task/{id}/checklist` | 🟢 Baixa | ✅ Pesquisado |
| **Goals** | `POST /team/{id}/goal` | 🟡 Média | ✅ Pesquisado |
| **Members** | `GET /list/{id}/member` | 🟢 Baixa | ✅ Pesquisado |
| **Webhooks** | `POST /team/{id}/webhook` | 🟡 Média | ✅ Pesquisado |
| **Views** | `GET /list/{id}/view` | 🔴 Alta | ✅ Pesquisado |

---

## 📎 C. Attachments (Anexos)

### O Que É
Upload de arquivos para tasks.

### Quick Facts
- **Tamanho máximo:** 1 GB
- **Content-Type:** `multipart/form-data`
- **Limitação:** Apenas arquivos locais (não cloud)

### Código Básico
```python
file = {"attachment": ('file.png', open('file.png', 'rb'))}
response = requests.post(
    f'https://api.clickup.com/api/v2/task/{task_id}/attachment',
    files=file,
    headers={'Authorization': token}
)
```

### Principais Armadilhas
- ❌ Esquecer `multipart/form-data`
- ❌ Arquivos > 1GB
- ❌ Tentar usar URLs de cloud

---

## ✅ D. Checklists (Listas de Verificação)

### O Que É
Listas de tarefas dentro de tasks.

### Quick Facts
- **Criar checklist:** Nome simples
- **Adicionar items:** Nome + assignee opcional
- **Marcar concluído:** `resolved: true`

### Código Básico
```python
# Criar checklist
checklist = client.create_checklist(task_id, "Deploy Checklist")

# Adicionar items
client.add_checklist_item(
    checklist["id"],
    "Rodar testes",
    assignee=123456
)

# Marcar como feito
client.complete_checklist_item(checklist["id"], item_id)
```

### Principais Armadilhas
- ❌ Esquecer checklist_id vs task_id
- ❌ Tentar editar checklist sem item_id

---

## 🎯 E. Goals (Objetivos/Metas)

### O Que É
Metas quantitativas com targets e progresso.

### Quick Facts
- **Múltiplos owners:** Sim
- **Due dates:** Timestamp Unix ms
- **Targets:** Key results com progresso
- **Cores:** Hex (#RRGGBB)

### Código Básico
```python
goal = client.create_goal(
    name="Aumentar Vendas Q1",
    due_date=1735689600000,
    owners=[123456, 789012],
    description="Meta trimestral"
)
```

### Principais Armadilhas
- ❌ Confundir goal com task
- ❌ Esquecer multiple_owners quando > 1 owner

---

## 👥 F. Members (Gerenciamento de Membros)

### O Que É
Listar e gerenciar membros em tasks/lists.

### Quick Facts
- **Listar:** Por list ou task
- **Assignees:** Array de user IDs
- **Limitação:** Não assign teams (apenas usuários)

### Código Básico
```python
# Listar membros
members = client.get_list_members(list_id)

# Adicionar assignees
client.add_assignees(task_id, [123456, 789012])

# Remover assignees
client.remove_assignees(task_id, [123456])
```

### Principais Armadilhas
- ❌ Tentar assignar teams (não suportado)
- ❌ User IDs são integers, team IDs são GUIDs

---

## 📣 G. Webhooks (Notificações)

### O Que É
Receber eventos do ClickUp em tempo real.

### Quick Facts
- **Eventos:** 20+ tipos (taskCreated, taskUpdated, etc)
- **IP:** Dinâmico (não dedicado)
- **Security:** HMAC SHA256 signature
- **Timeout:** Responder em < 30s

### Código Básico
```python
# Criar webhook
webhook = client.create_webhook(
    endpoint_url="https://meu-servidor.com/webhook",
    events=["taskCreated", "taskUpdated"],
    space_id="901234567"
)

# Listener (Flask)
@app.route('/webhook', methods=['POST'])
def webhook_listener():
    data = request.json
    event = data.get('event')

    if event == 'taskCreated':
        # Processar task criada
        pass

    return jsonify({"status": "ok"}), 200
```

### Principais Armadilhas
- ❌ Esquecer verificação de signature
- ❌ Endpoint > 30s timeout
- ❌ Usar HTTP em vez de HTTPS

---

## 📊 H. Views (Visualizações Customizadas)

### O Que É
Views com filtros, agrupamentos e ordenação.

### Quick Facts
- **Tipos:** list, board, calendar, gantt
- **Níveis:** Workspace, Space, Folder, List
- **Limitação:** Page views não suportadas (Docs, Whiteboards)

### Código Básico
```python
# Listar views
views = client.get_list_views(list_id)

# Buscar tasks de uma view
tasks = client.get_view_tasks(view_id)

# Atualizar view
client.update_view(
    view_id,
    name="Tasks Urgentes",
    filters={
        "op": "AND",
        "fields": [{"field": "priority", "operator": "=", "value": 1}]
    }
)
```

### Principais Armadilhas
- ❌ Tentar criar page views (não suportado)
- ❌ Confundir view_id com list_id

---

## 📋 Comparação de Complexidade

### 🟢 Fácil (< 1h implementação)
- **Attachments** - Upload simples
- **Checklists** - CRUD básico
- **Members** - Listar e assignar

### 🟡 Médio (1-2h implementação)
- **Goals** - Estrutura mais complexa
- **Webhooks** - Requer servidor listener

### 🔴 Avançado (2-4h implementação)
- **Views** - Filtros, grouping, sorting complexos

---

## 🚀 Priorização de Implementação

### Fase 1 (Essencial)
1. **Checklists** - Muito usado em tasks
2. **Members** - Gerenciar assignees
3. **Attachments** - Upload de arquivos

### Fase 2 (Importante)
4. **Webhooks** - Automação em tempo real
5. **Goals** - Tracking de metas

### Fase 3 (Avançado)
6. **Views** - Dashboards customizados

---

## 💡 Receitas Rápidas

### Upload de Arquivo
```python
client.upload_attachment("task_id", "/path/to/file.pdf")
```

### Criar Checklist Completo
```python
checklist = client.create_checklist("task_id", "Deploy")
client.add_checklist_item(checklist["id"], "Testes")
client.add_checklist_item(checklist["id"], "Build")
client.add_checklist_item(checklist["id"], "Deploy")
```

### Configurar Webhook
```python
webhook = client.create_webhook(
    "https://myapp.com/webhook",
    ["taskCreated", "taskUpdated"]
)
```

---

## 📚 Documentação Completa

### Pesquisa Técnica Detalhada
📖 **[ADVANCED_FEATURES_RESEARCH.md](ADVANCED_FEATURES_RESEARCH.md)**
- 6 funcionalidades documentadas
- Endpoints completos
- Código de implementação
- Limitações e armadilhas

---

## 🆚 Comparativo: Básico vs Avançado

| Feature | Custom Fields | Time Tracking | **Checklists** | **Webhooks** |
|---------|---------------|---------------|----------------|--------------|
| **Uso** | Dados custom | Horas | Tarefas | Eventos |
| **Freq** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Compl** | 🟡 Média | 🟢 Baixa | 🟢 Baixa | 🟡 Média |

---

**Criado em:** 2025-10-31
**Autor:** Sistema Kaloi
**Tempo de leitura:** 5 minutos
