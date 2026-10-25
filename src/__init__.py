"""
e-mffe-justicier — Agent juridique ivoirien
Droit de l'enfant, de la femme et de la famille.

Version : 0.1.0
"""
__version__ = "0.1.0"
__author__ = "e-MFFE justicier team"

from .agent import Agent, KBNotFoundError
from .retriever import Retriever
from .report_generator import ReportGenerator
from .main import app

__all__ = ["Agent", "Retriever", "ReportGenerator", "app", "__version__"]
