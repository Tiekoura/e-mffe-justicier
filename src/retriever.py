"""
retriever.py — Récupération de textes de loi applicables à une question.

La récupération se fait par correspondance sémantique simple (mots-clés + scores)
sur la base de connaissances structurée. Le but est de trouver les textes qui
s'appliquent le plus à la question de l'usager.
"""

import logging
from pathlib import Path

from .agent import Agent

logger = logging.getLogger("emffe-justicier")


class Retriever:
    """
    Récupère les textes de loi applicables à une question de l'usager.

    Usage:
        retriever = Retriever(kb_dir=Path("data"))
        matching = retriever.find("quel est l'âge pour se marier ?", num=5)
    """

    def __init__(self, kb_dir: Path = None):
        self.agent = Agent(kb_dir=kb_dir)
        self.records = self.agent.records

    def find(self, question: str, num: int = 5) -> list:
        """
        Trouve les textes de loi applicables à la question.

        Args:
            question: La question de l'usager.
            num: Nombre maximal de résultats.

        Returns:
            Liste des enregistrements (dicts) les plus pertinents.
        """
        if not self.records:
            return []

        # Utilise la méthode retrieve du Agent
        results = self.agent.retrieve(question, num)
        return results

    def find_by_domain(self, domaine: str, num: int = 5) -> list:
        """
        Trouve les textes dans un domaine spécifique.
        """
        return [r for r in self.records if r.get("domaine") == domaine][:num]

    def suggest_questions(self, topic: str = None) -> list:
        """
        Suggère des questions types pour clarifier.
        """
        suggestions = [
            "Quel est le problème principal que vous rencontrez ?",
            "Depuis quand ce problème est-il présent ?",
            "Avez-vous déjà déposé une plainte ou saisi la justice ?",
            "Quelles sont les personnes impliquées ?",
            "Y a-t-il des preuves (bilans, messages, courriers) ?",
            "Êtes-vous dans une urgence ? (danger imminent, enfant en danger)",
        ]
        if topic:
            if topic in ["enfant", "enfance"]:
                suggestions.insert(0, "S'agit-il d'un enfant mineur de 18 ans ?")
            elif topic in ["femme", "famille"]:
                suggestions.insert(0, "S'agit-il d'une situation de violence ou de divorce ?")
        return suggestions

    def get_context_for_question(self, question: str) -> dict:
        """
        Retourne le contexte de la question avec les textes les plus pertinents.
        """
        matching = self.find(question, num=5)
        return {
            "question": question,
            "contexte": f"{len(matching)} texte(s) de loi trouvé(s) pour cette question.",
            "matching": matching,
        }
