# 🤖 AUTOMAÇÕES NATIVAS DO CLICKUP

**Data:** 2025-10-31
**Custo:** R$ 0 (100% gratuito com plano atual)
**Tempo de Setup:** 30 minutos

---

## ✅ DECISÃO FINAL: USAR AUTOMAÇÕES NATIVAS DO CLICKUP

### Por quê?

✅ **R$ 0/mês** - Incluído no plano atual
✅ **Setup imediato** - Sem precisar MEI ou WhatsApp
✅ **Interface visual** - Sem código
✅ **100% integrado** - Nativo do ClickUp
✅ **Notificações nativas** - Email + in-app

❌ ~~Python + GitHub Actions~~ - Complexo demais
❌ ~~WhatsApp Business API~~ - Precisa MEI + R$123/mês
❌ ~~Interakt~~ - Não necessário

---

## 🎯 AUTOMAÇÕES A IMPLEMENTAR

### 1. 🚨 ALERTAS DE CONTAS A PAGAR

#### Automação 1.1: Alerta 7 Dias Antes
**Gatilho:** Due date chegando em 7 dias
**Ações:**
1. Adicionar tag `vencendo-em-breve`
2. Postar comentário: "⚠️ Esta conta vence em 7 dias!"
3. Notificar assignee

**Como criar:**
```
1. Abra List "Contas a Pagar"
2. Clique em "Automate" (canto superior direito)
3. Clique em "+ Add Automation"
4. Escolha: "When due date arrives"
5. Configure: "7 days before"
6. Adicione ações:
   - Add tag: "vencendo-em-breve"
   - Add comment: "⚠️ Esta conta vence em 7 dias!"
   - Send notification to: Assignees
7. Salve
```

---

#### Automação 1.2: Alerta 3 Dias Antes (Urgente)
**Gatilho:** Due date chegando em 3 dias
**Ações:**
1. Adicionar tag `urgente`
2. Mudar prioridade para "Alta"
3. Postar comentário: "🔥 URGENTE: Esta conta vence em 3 dias!"
4. Notificar assignee + watchers

**Como criar:**
```
1. List "Contas a Pagar" > Automate > + Add
2. When: "due date arrives"
3. Configure: "3 days before"
4. Ações:
   - Add tag: "urgente"
   - Set priority: High
   - Add comment: "🔥 URGENTE: Esta conta vence em 3 dias!"
   - Send notification to: Assignees + Watchers
5. Salve
```

---

#### Automação 1.3: Alerta 1 Dia Antes (Muito Urgente)
**Gatilho:** Due date chegando em 1 dia
**Ações:**
1. Adicionar tag `muito-urgente`
2. Mudar prioridade para "Urgente"
3. Postar comentário: "🚨 MUITO URGENTE: Esta conta vence AMANHÃ!"
4. Notificar assignee + watchers + list watchers

**Como criar:**
```
1. List "Contas a Pagar" > Automate > + Add
2. When: "due date arrives"
3. Configure: "1 day before"
4. Ações:
   - Add tag: "muito-urgente"
   - Set priority: Urgent
   - Add comment: "🚨 MUITO URGENTE: Esta conta vence AMANHÃ!"
   - Send notification to: Everyone watching
5. Salve
```

---

#### Automação 1.4: Conta Vencida
**Gatilho:** Due date passou (vencido)
**Ações:**
1. Adicionar tag `atrasado`
2. Mudar status para "Revisão Necessária" (ou criar status novo)
3. Postar comentário: "🔴 VENCIDO: Possível cobrança de juros!"
4. Criar subtask "Revisar conta vencida"

**Como criar:**
```
1. List "Contas a Pagar" > Automate > + Add
2. When: "due date arrives"
3. Configure: "on the day" (ou criar trigger custom "when overdue")
4. Ações:
   - Add tag: "atrasado"
   - Move to status: "Revisão Necessária"
   - Add comment: "🔴 VENCIDO: Possível cobrança de juros!"
   - Create subtask: "Revisar conta vencida"
5. Salve
```

---

### 2. 📅 LEMBRETES DE REUNIÕES COMERCIAIS

#### Automação 2.1: Lembrete 24h Antes
**Gatilho:** Custom field "Agendamento" chegando em 24h
**Ações:**
1. Adicionar tag `lembrete-24h`
2. Postar comentário com detalhes da reunião
3. Notificar assignee

**Como criar:**
```
1. List "Agenda Comercial" > Automate > + Add
2. When: "custom field changes"
   (Ou use: "due date arrives" se usar due date)
3. Configure: Custom field "Agendamento" - 24 hours before
4. Ações:
   - Add tag: "lembrete-24h"
   - Add comment: "📅 Lembrete: Reunião amanhã!"
   - Send notification to: Assignees
5. Salve
```

**Nota:** Se ClickUp não permitir trigger em custom field date, use Due Date como workaround.

---

#### Automação 2.2: Lembrete 1h Antes
**Gatilho:** Custom field "Agendamento" chegando em 1h
**Ações:**
1. Adicionar tag `lembrete-1h`
2. Postar comentário urgente
3. Notificar assignee

**Como criar:**
```
1. List "Agenda Comercial" > Automate > + Add
2. When: "due date arrives" (ou custom field)
3. Configure: "1 hour before"
4. Ações:
   - Add tag: "lembrete-1h"
   - Add comment: "⏰ REUNIÃO EM 1 HORA!"
   - Send notification to: Assignees
5. Salve
```

---

### 3. 📊 RELATÓRIOS SEMANAIS (Simplificado)

#### Automação 3.1: Lembrete Segunda-feira
**Gatilho:** Toda segunda-feira 9h
**Ações:**
1. Criar task "Relatório Semanal - [DATA]"
2. Template com checklist:
   - [ ] Revisar contas a pagar da semana
   - [ ] Revisar reuniões agendadas
   - [ ] Analisar tasks concluídas
3. Atribuir ao gestor

**Como criar:**
```
1. List "Contas a Pagar" (ou criar list "Relatórios")
2. Automate > + Add
3. When: "on a schedule"
4. Configure: Every Monday at 9:00 AM
5. Ações:
   - Create task: "📊 Relatório Semanal - {{date}}"
   - Set template: [criar template com checklist]
   - Assign to: [seu usuário]
6. Salve
```

---

## 🚀 PLANO DE IMPLEMENTAÇÃO

### HOJE (30 minutos)

#### Fase 1: Contas a Pagar (15 min)
1. Abrir List "Contas a Pagar"
2. Criar 4 automações de alertas
3. Testar com 1 task (mudar due date manualmente)

#### Fase 2: Reuniões Comerciais (10 min)
1. Abrir List "Agenda Comercial"
2. Criar 2 automações de lembretes
3. Testar com 1 reunião

#### Fase 3: Relatórios (5 min)
1. Criar automação de lembrete semanal
2. Configurar template de checklist

---

## ✅ VANTAGENS DAS AUTOMAÇÕES NATIVAS

### vs Python + GitHub Actions

| Aspecto | Nativo ClickUp | Python + GH Actions |
|---------|----------------|---------------------|
| **Custo** | R$ 0 | R$ 123-173/mês |
| **Setup** | 30 min | 3-5 dias |
| **Código** | 0 linhas | 1.100 linhas |
| **Manutenção** | Zero | Média |
| **Pré-requisitos** | Nenhum | MEI + Interakt |
| **Notificações** | Email + in-app | WhatsApp |
| **Confiabilidade** | 99.9% | 95% |

### Desvantagens Aceitáveis

❌ Não envia WhatsApp (mas envia email)
❌ Não gera relatórios automáticos complexos (mas cria task de lembrete)
❌ Menos flexibilidade (mas suficiente para 90% dos casos)

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### Contas a Pagar
- [ ] Automação: 7 dias antes
- [ ] Automação: 3 dias antes
- [ ] Automação: 1 dia antes
- [ ] Automação: Vencido
- [ ] Teste com 1 task

### Reuniões Comerciais
- [ ] Automação: 24h antes
- [ ] Automação: 1h antes
- [ ] Teste com 1 reunião

### Relatórios
- [ ] Automação: Lembrete segunda-feira
- [ ] Template de checklist
- [ ] Teste manual

### Extras Opcionais
- [ ] Auto-assign quando campo "Gestor" preenchido
- [ ] Tag "interno" → Valor = R$ 0
- [ ] Checklist 100% → Mover status
- [ ] Reunião concluída → Criar task de follow-up

---

## 🎓 TUTORIAIS PASSO A PASSO

### Como Criar Automação no ClickUp

```
1. Abra a List onde quer criar automação
2. Clique em "Automate" (ícone de raio, canto superior direito)
3. Clique em "+ Add Automation"
4. Escolha um dos templates prontos OU "Create Custom"
5. Configure o TRIGGER (gatilho):
   - When task status changes
   - When due date arrives
   - When custom field changes
   - On a schedule
   - When tag is added
   - etc.
6. Configure as ACTIONS (ações):
   - Add tag
   - Set priority
   - Move to status
   - Add comment
   - Create task/subtask
   - Send notification
   - Assign to
   - Set custom field
   - etc.
7. Teste a automação
8. Ative
```

### Exemplo Prático: Alerta 3 Dias Antes

```
1. List "Contas a Pagar" > Automate
2. + Add Automation > Create Custom
3. TRIGGER:
   - When: "due date arrives"
   - Time: "3 days before"
4. ACTIONS (adicione uma por uma):
   a) Add tag
      - Tag name: "urgente"

   b) Set priority
      - Priority: "High"

   c) Add comment
      - Comment: "🔥 URGENTE: Esta conta vence em 3 dias! Por favor, providencie o pagamento."

   d) Send notification
      - To: "Assignees"
      - Message: "Conta vencendo em 3 dias!"
5. Name automation: "Alerta 3 dias antes"
6. Save
```

---

## 🔍 TROUBLESHOOTING

### Automação não dispara

**Problema:** Criei automação mas não está funcionando
**Soluções:**
1. Verificar se automação está ATIVA (toggle verde)
2. Verificar se a task atende aos critérios do trigger
3. Testar manualmente mudando due date
4. Verificar permissões (apenas owner/admin podem criar automações)

### Notificações não chegam

**Problema:** Automação dispara mas não recebo notificação
**Soluções:**
1. Verificar configurações de notificações: Settings > Notifications
2. Verificar se está como assignee ou watcher da task
3. Verificar email de spam

### Trigger de custom field não funciona

**Problema:** ClickUp não tem trigger para custom field date
**Solução:**
- Use Due Date como workaround
- Ou use automação de criação: "When task created" → "Add due date based on custom field"

---

## 📊 RESULTADOS ESPERADOS

### Após Implementação

**Contas a Pagar (33 tasks):**
- ✅ 100% monitoradas automaticamente
- ✅ Alertas em 7/3/1 dia + vencimento
- ✅ Tags automáticas para filtrar
- ✅ Comentários automáticos com instruções
- ✅ Notificações via email + in-app

**Reuniões Comerciais (5 reuniões):**
- ✅ Lembretes 24h e 1h antes
- ✅ Notificações automáticas
- ✅ Tags de controle

**Relatórios Semanais:**
- ✅ Task criada toda segunda-feira
- ✅ Checklist padronizado
- ✅ Processo consistente

---

## 💡 EXTRAS: OUTRAS AUTOMAÇÕES ÚTEIS

### Auto-Assign Gestor
**Trigger:** Custom field "Gestor de Projetos" preenchido
**Action:** Adicionar pessoa como assignee

### Tag Interno → Valor Zero
**Trigger:** Tag "interno" adicionada
**Action:** Set custom field "Valor" = R$ 0

### Checklist Completo → Avançar Status
**Trigger:** Checklist item "Testes e Validação" 100% concluído
**Action:** Move to status "Monitoramento"

### Projeto Concluído → Criar Review
**Trigger:** Status mudou para "Concluído"
**Action:** Create task "Review: [nome do projeto]" na list "Revisões"

---

## 🏁 CONCLUSÃO

**Decisão Final:** Usar 100% automações nativas do ClickUp

**Benefícios:**
- ✅ R$ 0/mês (vs R$123-173 com WhatsApp)
- ✅ Setup hoje mesmo (vs 3-5 dias)
- ✅ Zero código (vs 1.100 linhas)
- ✅ Zero manutenção

**Trade-offs Aceitáveis:**
- Email ao invés de WhatsApp (ainda notifica!)
- Menos flexível (mas suficiente)

**Próxima Ação:**
1. Implementar 6 automações principais (30 min)
2. Testar com tasks reais (15 min)
3. Monitorar primeira semana
4. Ajustar se necessário

**Status:** ✅ PRONTO PARA IMPLEMENTAR AGORA!

---

**Criado em:** 2025-10-31
**Custo:** R$ 0
**Tempo:** 30 minutos
**Código:** 0 linhas

🎯 **100% Nativo ClickUp - Simples e Eficaz!**
