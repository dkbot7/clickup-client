# -*- coding: utf-8 -*-
"""
Templates de tasks para o Sistema Kaloi.
"""

from .crm_lead import CRMLeadTemplate
from .project_scrumban import ProjectScrumbanTemplate
from .meeting import MeetingTemplate
from .onboarding import OnboardingTemplate

__all__ = [
    "CRMLeadTemplate",
    "ProjectScrumbanTemplate",
    "MeetingTemplate",
    "OnboardingTemplate"
]
