# 🔬 Pesquisa Técnica: Custom Fields (Campos Personalizados)

**Data:** 2025-10-31
**Pesquisador:** Sistema Kaloi (Claude Code)
**Objetivo:** Entender como adicionar e editar custom fields via API ClickUp v2

---

## 📋 Índice

1. [Resumo Executivo](#resumo-executivo)
2. [Documentação Oficial da API](#documentação-oficial-da-api)
3. [Tipos de Custom Fields Suportados](#tipos-de-custom-fields-suportados)
4. [Endpoints da API](#endpoints-da-api)
5. [Estrutura de Dados](#estrutura-de-dados)
6. [Limitações e Restrições](#limitações-e-restrições)
7. [Implementações Existentes em Python](#implementações-existentes-em-python)
8. [Exemplo de Implementação](#exemplo-de-implementação)
9. [Recomendações para o Projeto](#recomendações-para-o-projeto)
10. [Referências](#referências)

---

## 🎯 Resumo Executivo

### Descobertas Principais

✅ **Custom Fields são suportados pela API v2 do ClickUp**
✅ **16 tipos diferentes de campos disponíveis**
✅ **Endpoint específico para atualizar valores: `POST /task/{task_id}/field/{field_id}`**
⚠️ **Limitação crítica: Não é possível atualizar múltiplos custom fields de uma vez**
⚠️ **Planos gratuitos têm limite de 60 usos (não resetam)**
❌ **O endpoint `PUT /task/{task_id}` NÃO suporta atualização de custom fields**

### Complexidade de Implementação

| Aspecto | Complexidade | Justificativa |
|---------|--------------|---------------|
| Obter field_id | 🟡 Média | Requer chamada adicional à API |
| Setar valor simples | 🟢 Baixa | POST direto com JSON |
| Múltiplos campos | 🔴 Alta | Requer loop e múltiplas requisições |
| Validação de tipos | 🟡 Média | Cada tipo tem formato específico |
| Tradução PT/EN | 🟡 Média | Nomes de campos podem estar em PT |

---

## 📚 Documentação Oficial da API

### Links Principais

- **Set Custom Field Value**: https://developer.clickup.com/reference/setcustomfieldvalue
- **Custom Fields Guide**: https://developer.clickup.com/docs/customfields
- **Get Accessible Custom Fields**: https://developer.clickup.com/reference/getaccessiblecustomfields

---

## 🎨 Tipos de Custom Fields Suportados

A API ClickUp v2 suporta **16 tipos de campos personalizados**:

| # | Tipo | Descrição | Formato de Valor |
|---|------|-----------|------------------|
| 1 | `url` | Links/URLs | `"value": "https://example.com"` |
| 2 | `drop_down` | Lista suspensa (seleção única) | `"value": "option_id"` |
| 3 | `labels` | Etiquetas/tags (múltipla seleção) | `"value": {"add": ["id1"], "remove": ["id2"]}` |
| 4 | `email` | Endereço de e-mail | `"value": "user@example.com"` |
| 5 | `phone` | Número de telefone | `"value": "+55 11 99999-9999"` |
| 6 | `date` | Data (com ou sem hora) | `"value": 1701388800000, "time": true` |
| 7 | `short_text` | Texto curto (1 linha) | `"value": "Texto curto"` |
| 8 | `text` | Texto longo (múltiplas linhas) | `"value": "Texto longo..."` |
| 9 | `checkbox` | Checkbox (verdadeiro/falso) | `"value": true` |
| 10 | `number` | Número (inteiro ou decimal) | `"value": 42.5` |
| 11 | `currency` | Moeda | `"value": 1500.00` |
| 12 | `tasks` | Relação com outras tasks | `"value": {"add": ["task_id1"], "remove": []}` |
| 13 | `users` | Usuários | `"value": {"add": ["user_id1"], "remove": []}` |
| 14 | `emoji` | Emoji/reação | `"value": "😀"` |
| 15 | `automatic_progress` | Progresso automático | ⚠️ Somente leitura |
| 16 | `manual_progress` | Progresso manual | `"value": 75` (0-100) |
| 17 | `location` | Localização/endereço | `"value": {"address": "...", "lat": 0, "lng": 0}` |

### ⚠️ Tipos Somente Leitura

- **`automatic_progress`** - Calculado automaticamente pelo ClickUp
- **Voting fields** - Não podem ser definidos via API

---

## 🔌 Endpoints da API

### 1. Obter Custom Fields Acessíveis

**Endpoint:** `GET /list/{list_id}/field`

**Descrição:** Retorna todos os custom fields configurados em uma lista.

**Resposta:**
```json
{
  "fields": [
    {
      "id": "b955c4dc-a6a7-4c05-9051-8d5f7e4f2c55",
      "name": "Priority Level",
      "type": "drop_down",
      "type_config": {
        "default": 0,
        "placeholder": null,
        "options": [
          {
            "id": "uuid-1",
            "name": "High",
            "color": "#ff0000",
            "orderindex": 0
          },
          {
            "id": "uuid-2",
            "name": "Medium",
            "color": "#ffff00",
            "orderindex": 1
          }
        ]
      },
      "date_created": "1622547600000",
      "hide_from_guests": false
    }
  ]
}
```

### 2. Obter Custom Fields de uma Task

**Endpoint:** `GET /task/{task_id}`

**Descrição:** Retorna a task completa, incluindo valores dos custom fields.

**Resposta (trecho):**
```json
{
  "id": "task_id",
  "name": "Task Name",
  "custom_fields": [
    {
      "id": "field_id",
      "name": "Priority Level",
      "type": "drop_down",
      "value": {
        "id": "uuid-1",
        "name": "High",
        "color": "#ff0000"
      }
    }
  ]
}
```

### 3. Setar Valor de Custom Field

**Endpoint:** `POST /task/{task_id}/field/{field_id}`

**Descrição:** Define ou atualiza o valor de um custom field específico.

**Headers:**
```http
Authorization: YOUR_API_TOKEN
Content-Type: application/json
```

**Request Body (exemplos por tipo):**

#### Texto
```json
{
  "value": "Novo valor do campo"
}
```

#### Número
```json
{
  "value": 42
}
```

#### Checkbox
```json
{
  "value": true
}
```

#### Data (com hora)
```json
{
  "value": 1701388800000,
  "time": true
}
```

#### Dropdown
```json
{
  "value": "option_id_from_type_config"
}
```

#### Labels (múltipla seleção)
```json
{
  "value": {
    "add": ["label_id_1", "label_id_2"],
    "remove": ["label_id_3"]
  }
}
```

#### Usuários
```json
{
  "value": {
    "add": [123456, 789012],
    "remove": []
  }
}
```

#### Localização
```json
{
  "value": {
    "formatted_address": "Rua Exemplo, 123 - São Paulo, SP",
    "place_id": "ChIJAbCDeFGH...",
    "lat": -23.5505,
    "lng": -46.6333
  }
}
```

**Resposta de Sucesso:**
```json
{
  "id": "field_id",
  "name": "Priority Level",
  "type": "drop_down",
  "value": {
    "id": "uuid-1",
    "name": "High",
    "color": "#ff0000"
  }
}
```

---

## 📊 Estrutura de Dados

### Objeto Custom Field (retornado pela API)

```python
{
    "id": str,              # UUID único do campo
    "name": str,            # Nome exibido do campo
    "type": str,            # Tipo do campo (ver tabela acima)
    "type_config": dict,    # Configurações específicas do tipo
    "date_created": str,    # Timestamp de criação (ms)
    "hide_from_guests": bool,
    "value": Any            # Valor atual (formato varia por tipo)
}
```

### Type Config (configurações específicas)

Cada tipo de campo tem configurações específicas em `type_config`:

**Dropdown:**
```python
{
    "default": int,        # Índice da opção padrão
    "placeholder": str,
    "options": [
        {
            "id": str,     # UUID da opção
            "name": str,   # Nome da opção
            "color": str,  # Cor hex (#RRGGBB)
            "orderindex": int
        }
    ]
}
```

**Number/Currency:**
```python
{
    "precision": int,      # Casas decimais (0-8)
    "default": float
}
```

**Date:**
```python
{
    "has_time": bool       # Se inclui hora ou apenas data
}
```

---

## ⚠️ Limitações e Restrições

### 1. Atualização Individual Obrigatória

**❌ NÃO FUNCIONA:**
```python
# Tentar atualizar múltiplos custom fields no endpoint PUT /task
client.update_task(task_id, custom_fields=[...])  # NÃO SUPORTADO
```

**✅ FORMA CORRETA:**
```python
# Atualizar cada custom field separadamente
for field_id, value in custom_fields.items():
    client.set_custom_field(task_id, field_id, value)
```

### 2. Limitação de Uso (Planos Gratuitos)

- **Limite:** 60 usos totais de custom fields por workspace
- **Acumulação:** Cada chamada ao endpoint `POST /task/{task_id}/field/{field_id}` conta como 1 uso
- **Reset:** **NÃO RESETAM** - limite permanente
- **Afeta:** Apenas planos "Free Forever"

### 3. Campos Somente Leitura

Não podem ser definidos via API:
- `automatic_progress` (calculado automaticamente)
- Campos de votação (voting fields)

### 4. Necessidade de Field ID

- Não é possível usar o **nome** do campo diretamente
- É necessário obter o **UUID** (`field_id`) antes de atualizar
- Requer chamada adicional à API: `GET /list/{list_id}/field`

### 5. Criação vs Atualização de Tasks

**Ao CRIAR task (POST):**
```python
# Pode passar múltiplos custom fields de uma vez
payload = {
    "name": "Nova Task",
    "custom_fields": [
        {"id": "field_id_1", "value": "valor1"},
        {"id": "field_id_2", "value": 42}
    ]
}
```

**Ao ATUALIZAR task (PUT):**
```python
# NÃO suporta custom_fields no payload
# Deve usar POST /task/{task_id}/field/{field_id} para cada campo
```

---

## 🐍 Implementações Existentes em Python

### 1. **pyclickup** (Stashchen) - ⭐ Mais Completa

**URL:** https://github.com/Stashchen/pyclickup

**Abordagem:** Declarativa/OOP com classes tipadas

**Exemplo:**
```python
from pyclickup import ClickUpList
from pyclickup.custom_fields import ShortTextField, CurrencyField, DateField

class Employee(ClickUpList):
    first_name = ShortTextField(field_name="First Name")
    last_name = ShortTextField(field_name="Last Name")
    salary = CurrencyField(field_name="Current Salary")
    hire_date = DateField(field_name="Hire Date")

# Uso
employee = Employee.get(task_id="abc123")
employee.first_name = "John"
employee.salary = 5000.00
employee.update()  # Envia para API
```

**Prós:**
- ✅ Abstração de alto nível
- ✅ Type hints e validação
- ✅ Sintaxe pythônica
- ✅ Suporte a múltiplos tipos de campos

**Contras:**
- ❌ Requer definição prévia de classes
- ❌ Menos flexível para uso dinâmico

### 2. **clickupython** (Imzachjohnson)

**URL:** https://github.com/Imzachjohnson/clickupython

**Abordagem:** API wrapper direto

**Status:** ⚠️ Não mantido ativamente pelo autor

### 3. **pyclickup** (jpetrucciani)

**URL:** https://github.com/jpetrucciani/pyclickup

**Abordagem:** Wrapper simples da API

**Uso para custom fields:**
```python
from pyclickup import ClickUp

client = ClickUp(api_token)
# Acesso direto aos endpoints da API
```

### 4. **Clickup_API** (SmiNat)

**URL:** https://github.com/SmiNat/Clickup_API

**Recursos:**
- ✅ Endpoint `get_accessible_custom_fields` implementado
- ✅ FastAPI + OOP

---

## 💡 Exemplo de Implementação

### Opção 1: Implementação Simples (Recomendada para o Projeto Atual)

```python
# src/clickup_api/client.py

def get_custom_fields(self, list_id: str) -> Optional[Dict]:
    """
    Obtém todos os custom fields de uma lista.

    Args:
        list_id: ID da lista

    Returns:
        dict com lista de custom fields
    """
    return self._request("GET", f"list/{list_id}/field")


def set_custom_field(
    self,
    task_id: str,
    field_id: str,
    value: Any,
    **kwargs
) -> Optional[Dict]:
    """
    Define valor de um custom field em uma task.

    Args:
        task_id: ID da task
        field_id: UUID do custom field
        value: Valor a ser definido (formato depende do tipo)
        **kwargs: Parâmetros adicionais (ex: time=True para datas)

    Exemplos:
        # Texto
        client.set_custom_field("task_id", "field_id", "Novo valor")

        # Número
        client.set_custom_field("task_id", "field_id", 42)

        # Checkbox
        client.set_custom_field("task_id", "field_id", True)

        # Data com hora
        client.set_custom_field(
            "task_id",
            "field_id",
            1701388800000,
            time=True
        )

        # Labels (adicionar/remover)
        client.set_custom_field(
            "task_id",
            "field_id",
            {"add": ["label1"], "remove": ["label2"]}
        )

    Returns:
        dict com custom field atualizado
    """
    payload = {"value": value}
    payload.update(kwargs)

    result = self._request(
        "POST",
        f"task/{task_id}/field/{field_id}",
        json=payload
    )

    if result:
        print(f"[green]✓ Custom field atualizado![/green]")

    return result


def set_multiple_custom_fields(
    self,
    task_id: str,
    fields: Dict[str, Any]
) -> List[Optional[Dict]]:
    """
    Define múltiplos custom fields de uma task.

    ATENÇÃO: Faz uma requisição API para cada campo!

    Args:
        task_id: ID da task
        fields: Dicionário {field_id: value}

    Exemplo:
        client.set_multiple_custom_fields(
            "task_id",
            {
                "field_id_1": "Texto",
                "field_id_2": 42,
                "field_id_3": True
            }
        )

    Returns:
        Lista com resultados de cada atualização
    """
    results = []

    print(f"[yellow]⚠ Atualizando {len(fields)} custom fields...[/yellow]")

    for field_id, value in fields.items():
        result = self.set_custom_field(task_id, field_id, value)
        results.append(result)

    successful = sum(1 for r in results if r is not None)
    print(f"[green]✓ {successful}/{len(fields)} custom fields atualizados[/green]")

    return results
```

### Opção 2: Helper para Mapear Nomes → IDs

```python
# src/clickup_api/helpers/custom_fields.py

from typing import Dict, Optional

class CustomFieldMapper:
    """
    Helper para mapear nomes de custom fields para IDs.
    """

    def __init__(self, client, list_id: str):
        """
        Inicializa o mapper com uma lista específica.

        Args:
            client: Instância do KaloiClickUpClient
            list_id: ID da lista
        """
        self.client = client
        self.list_id = list_id
        self._fields_cache = None

    def get_field_id(self, field_name: str) -> Optional[str]:
        """
        Obtém field_id a partir do nome do campo.

        Args:
            field_name: Nome do custom field (case insensitive)

        Returns:
            UUID do campo ou None se não encontrado
        """
        if not self._fields_cache:
            self._load_fields()

        field_name_lower = field_name.lower()

        for field in self._fields_cache.get("fields", []):
            if field["name"].lower() == field_name_lower:
                return field["id"]

        return None

    def _load_fields(self):
        """Carrega custom fields da lista e armazena em cache."""
        self._fields_cache = self.client.get_custom_fields(self.list_id)

    def set_by_name(
        self,
        task_id: str,
        field_name: str,
        value: Any
    ) -> Optional[Dict]:
        """
        Define custom field usando o nome em vez do ID.

        Args:
            task_id: ID da task
            field_name: Nome do custom field
            value: Valor a definir

        Returns:
            Resultado da atualização ou None
        """
        field_id = self.get_field_id(field_name)

        if not field_id:
            print(f"[red]✗ Custom field '{field_name}' não encontrado[/red]")
            return None

        return self.client.set_custom_field(task_id, field_id, value)


# Uso:
from src.clickup_api.helpers.custom_fields import CustomFieldMapper

mapper = CustomFieldMapper(client, list_id="123456")
mapper.set_by_name("task_id", "Priority Level", "High")
mapper.set_by_name("task_id", "Due Date", 1701388800000)
```

### Opção 3: Tradução PT/EN para Custom Fields

```python
# src/clickup_api/helpers/translation.py (adicionar)

# Mapeamento de nomes comuns de custom fields PT → EN
CUSTOM_FIELD_NAMES_PT_TO_EN = {
    "prioridade": "priority",
    "prioridade alta": "high priority",
    "nível de prioridade": "priority level",
    "data de entrega": "delivery date",
    "data de vencimento": "due date",
    "responsável": "assignee",
    "departamento": "department",
    "orçamento": "budget",
    "estimativa": "estimate",
    "progresso": "progress",
    "status do projeto": "project status",
}

def translate_custom_field_name(name: str, to_english: bool = True) -> str:
    """
    Traduz nome de custom field PT ↔ EN.

    Args:
        name: Nome do custom field
        to_english: Se True, traduz PT → EN

    Returns:
        Nome traduzido ou original
    """
    name_lower = name.lower()

    if to_english:
        return CUSTOM_FIELD_NAMES_PT_TO_EN.get(name_lower, name)
    else:
        # EN → PT (inverte o dicionário)
        reverse_map = {v: k for k, v in CUSTOM_FIELD_NAMES_PT_TO_EN.items()}
        return reverse_map.get(name_lower, name)
```

---

## 🎯 Recomendações para o Projeto

### 1. Implementação Incremental

**Fase 1 (Básico):**
- ✅ Implementar `get_custom_fields(list_id)`
- ✅ Implementar `set_custom_field(task_id, field_id, value)`
- ✅ Adicionar ao README exemplos de uso

**Fase 2 (Intermediário):**
- ✅ Implementar `set_multiple_custom_fields()`
- ✅ Adicionar helper `CustomFieldMapper`
- ✅ Suporte a tipos comuns (text, number, checkbox, date, dropdown)

**Fase 3 (Avançado):**
- ✅ Validação de tipos antes de enviar
- ✅ Tradução PT/EN de nomes de campos
- ✅ Cache de field IDs
- ✅ Suporte a todos os 16 tipos

### 2. Priorização de Tipos

**Alta prioridade (usar primeiro):**
1. `short_text` / `text` - Mais comum
2. `number` - Muito usado
3. `checkbox` - Simples e útil
4. `date` - Importante para prazos
5. `drop_down` - Seleção de opções

**Média prioridade:**
6. `labels` - Tags/categorias
7. `users` - Atribuição de pessoas
8. `currency` - Valores monetários
9. `email` / `phone` - Contatos

**Baixa prioridade:**
10. `tasks` - Relações entre tasks
11. `location` - Localização
12. `emoji` - Menos crítico
13. `manual_progress` - Casos específicos

### 3. Manter Compatibilidade com Sistema Atual

```python
# Manter API existente intacta
# Adicionar novos métodos sem quebrar o código atual

# ✅ BOM: Adicionar métodos novos
def get_custom_fields(self, list_id: str):
    ...

def set_custom_field(self, task_id: str, field_id: str, value: Any):
    ...

# ✅ BOM: Estender create_task para aceitar custom_fields
def create_task(self, list_id: str, name: str, custom_fields: Optional[Dict] = None, **kwargs):
    # ... código existente ...

    if custom_fields:
        payload["custom_fields"] = [
            {"id": field_id, "value": value}
            for field_id, value in custom_fields.items()
        ]
```

### 4. Documentação Clara de Limitações

```python
def set_custom_field(self, task_id: str, field_id: str, value: Any):
    """
    Define valor de um custom field.

    ⚠️ LIMITAÇÕES:
    - Cada chamada conta como 1 uso (planos gratuitos têm limite de 60)
    - Não é possível atualizar múltiplos campos de uma vez
    - Requer o UUID do campo (use get_custom_fields() para obter)

    ...
    """
```

### 5. Testes com Dados Reais

Antes de finalizar a implementação, testar com:
- ✅ Diferentes tipos de campos
- ✅ Validação de formato de valores
- ✅ Tratamento de erros (campo não existe, valor inválido, etc.)
- ✅ Performance (múltiplas atualizações sequenciais)

---

## 📖 Referências

### Documentação Oficial
1. **Set Custom Field Value**: https://developer.clickup.com/reference/setcustomfieldvalue
2. **Custom Fields Guide**: https://developer.clickup.com/docs/customfields
3. **Get Accessible Custom Fields**: https://developer.clickup.com/reference/getaccessiblecustomfields
4. **Update Task**: https://developer.clickup.com/reference/updatetask

### Repositórios GitHub
1. **pyclickup (Stashchen)**: https://github.com/Stashchen/pyclickup
2. **clickupython**: https://github.com/Imzachjohnson/clickupython
3. **pyclickup (jpetrucciani)**: https://github.com/jpetrucciani/pyclickup
4. **Clickup_API (SmiNat)**: https://github.com/SmiNat/Clickup_API

### Discussões e Feedback
1. **Add custom fields value with API**: https://feedback.clickup.com/public-api/p/put-data-in-task-custom-fields-via-api-update-task-custom-field-via-api
2. **Custom Fields with API**: https://feedback.clickup.com/public-api/p/custom-fields-with-api

---

## ✅ Checklist de Implementação

- [ ] Implementar `get_custom_fields(list_id)`
- [ ] Implementar `set_custom_field(task_id, field_id, value)`
- [ ] Implementar `set_multiple_custom_fields(task_id, fields)`
- [ ] Adicionar suporte para tipos básicos (text, number, checkbox, date)
- [ ] Criar `CustomFieldMapper` helper
- [ ] Adicionar tradução PT/EN de nomes de campos
- [ ] Estender `create_task()` para aceitar custom_fields
- [ ] Criar testes unitários
- [ ] Criar exemplos práticos no README
- [ ] Documentar limitações claramente
- [ ] Testar com workspace real

---

**Próximos Passos:**
1. Implementar métodos básicos em `src/clickup_api/client.py`
2. Criar helper `CustomFieldMapper` em `src/clickup_api/helpers/custom_fields.py`
3. Adicionar testes em `test_custom_fields.py`
4. Atualizar README com exemplos

---

**Autor:** Sistema Kaloi (Claude Code)
**Data:** 2025-10-31
**Versão:** 1.0
