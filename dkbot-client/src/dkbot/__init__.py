# -*- coding: utf-8 -*-
"""
dkbot - ClickUp Client Extended
Sistema Kaloi - Funcionalidades Avançadas A-H

Cliente ClickUp com suporte completo para:
- A. Custom Fields (16 tipos)
- B. Time Tracking (timers e registros)
- C. Attachments (upload de arquivos)
- D. Checklists (listas de verificação)
- E. Goals (objetivos e metas)
- F. Members (gerenciamento de membros)
- G. Webhooks (eventos em tempo real)
- H. Views (visualizações customizadas)

Autor: Sistema Kaloi (IA 03 - Claude Code)
Versão: 1.0.0
"""

from .client import KaloiClickUpClient

__version__ = "1.0.0"
__author__ = "Dani Kaloi - Sistema Kaloi"
__license__ = "MIT"

__all__ = ["KaloiClickUpClient"]
