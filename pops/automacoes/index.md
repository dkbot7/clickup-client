# Banco de Dados - Automações ClickUp

> Base de conhecimento extraída das análises das Aulas 01-04 (Flow Pro - João Pedro Nascimento)
> Ferramenta: ClickUp Nativo (sem Make/n8n nas fases iniciais)

---

## Índice por Departamento

### 💰 Financeiro
| ID | Automação | Ferramenta | Prioridade |
|----|-----------|------------|------------|
| [FIN-01](financeiro/FIN-01-alerta-7-dias.md) | Alerta de vencimento 7 dias antes | ClickUp Nativo | 🔴 ALTA |
| [FIN-02](financeiro/FIN-02-alerta-3-dias.md) | Alerta de vencimento 3 dias antes | ClickUp Nativo | 🔴 ALTA |
| [FIN-03](financeiro/FIN-03-alerta-1-dia.md) | Alerta de vencimento 1 dia antes | ClickUp Nativo | 🔴 ALTA |
| [FIN-04](financeiro/FIN-04-conta-vencida.md) | Conta vencida → Task de revisão | ClickUp Nativo | 🔴 ALTA |

### 📁 Projetos
| ID | Automação | Ferramenta | Prioridade |
|----|-----------|------------|------------|
| [PRJ-01](projetos/PRJ-01-checklist-testes-status.md) | Checklist Testes 100% → Status monitoramento | ClickUp Nativo | 🔴 ALTA |
| [PRJ-02](projetos/PRJ-02-checklist-progresso-fase.md) | Checklist 25/50/75/100% → Atualizar campo Fase | ClickUp Nativo | 🔴 ALTA |
| [PRJ-03](projetos/PRJ-03-auto-assign-gestor.md) | Gestor preenchido → Auto-assign | ClickUp Nativo | 🔴 ALTA |
| [PRJ-04](projetos/PRJ-04-alerta-prazo-vencido.md) | Prazo vencido → Tag + Task revisão | ClickUp Nativo | 🔴 ALTA |
| [PRJ-05](projetos/PRJ-05-alertas-progressivos.md) | Alertas 7/3/1 dias antes do prazo | ClickUp Nativo | 🔴 ALTA |
| [PRJ-06](projetos/PRJ-06-risco-alto-mitigacao.md) | Risco "Alto" → Criar plano de mitigação | ClickUp Nativo | 🟡 MÉDIA |
| [PRJ-07](projetos/PRJ-07-valor-50k-diretoria.md) | Valor > R$50k → Notificar diretoria | ClickUp Nativo | 🟡 MÉDIA |
| [PRJ-08](projetos/PRJ-08-orcamento-overrun.md) | Orçamento excedido → Alerta | ClickUp Nativo | 🟡 MÉDIA |

### 🤝 Comercial
| ID | Automação | Ferramenta | Prioridade |
|----|-----------|------------|------------|
| [COM-01](comercial/COM-01-lembrete-reuniao-24h.md) | Lembrete de reunião 24h antes | Make + WhatsApp | 🔴 ALTA |
| [COM-02](comercial/COM-02-lembrete-reuniao-1h.md) | Lembrete de reunião 1h antes | Make + WhatsApp | 🔴 ALTA |
| [COM-03](comercial/COM-03-lead-negocio-fechado.md) | Lead "Negócio Fechado" → Onboarding | Make + ClickUp | 🟡 MÉDIA |

### 🏷️ Tags & Workflow
| ID | Automação | Ferramenta | Prioridade |
|----|-----------|------------|------------|
| [TAG-01](tags/TAG-01-tag-urgente-prioridade.md) | Tag "urgente" → Prioridade urgente + notificar | ClickUp Nativo | 🔴 ALTA |
| [TAG-02](tags/TAG-02-tag-interno-valor-zero.md) | Tag "interno" → Valor = R$ 0 | ClickUp Nativo | 🟡 MÉDIA |
| [TAG-03](tags/TAG-03-tag-bloqueado-desbloqueio.md) | Tag "bloqueado" → Task de desbloqueio | ClickUp Nativo | 🟡 MÉDIA |
| [TAG-04](tags/TAG-04-tag-aprovado-proxima-fase.md) | Tag "aprovado" → Mover para próxima fase | ClickUp Nativo | 🟡 MÉDIA |

### ⚙️ Workflow Geral
| ID | Automação | Ferramenta | Prioridade |
|----|-----------|------------|------------|
| [WKF-01](workflow/WKF-01-status-concluido-arquivar.md) | Status "concluído" → Arquivar + celebração | ClickUp Nativo | 🟢 BAIXA |
| [WKF-02](workflow/WKF-02-status-em-andamento-notificar.md) | Status "em andamento" → Notificar assignees | ClickUp Nativo | 🟢 BAIXA |
| [WKF-03](workflow/WKF-03-checklist-planejamento-tag.md) | Checklist Planejamento 100% → Tag | ClickUp Nativo | 🟢 BAIXA |

---

## Resumo

| Total | ClickUp Nativo | Make Necessário |
|-------|----------------|-----------------|
| 19 automações | 16 (84%) | 3 (16%) |

**ROI estimado:** 13h de setup → 33h/mês economizadas
