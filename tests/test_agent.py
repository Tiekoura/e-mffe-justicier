"""
Tests pour e-MFFE justicier.

Pour lancer : python -m pytest tests/ -v
"""

import pytest
import json
from pathlib import Path
import sys

# Ajouter le répertoire src au chemin d'import
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agent import Agent


@pytest.fixture
def agent():
    """Fixture pour l'agent."""
    return Agent()


class TestAgentInitialization:
    """Tests d'initialisation de l'agent."""

    def test_agent_creates(self, agent):
        """L'agent doit s'initialiser."""
        assert agent is not None

    def test_kb_loaded(self, agent):
        """La base de connaissances doit être chargée."""
        assert len(agent.records) > 0, "La KB doit contenir des enregistrements"

    def test_kb_has_records(self, agent):
        """La KB doit contenir au moins 20 enregistrements."""
        assert len(agent.records) >= 20, f"Attendu >= 20, trouvé {len(agent.records)}"


class TestKBStructure:
    """Tests sur la structure de la base de connaissances."""

    def test_required_fields(self, agent):
        """Chaque enregistrement doit avoir les champs requis."""
        required = {"id", "domaine", "titre", "reference", "contenu"}
        for rec in agent.records:
            missing = required - set(rec.keys())
            assert not missing, f"Enregistrement {rec.get('id')} manque des champs : {missing}"


class TestRetrieval:
    """Tests de récupération de textes."""

    def test_retrieve_child_law(self, agent):
        """La récupération doit trouver des textes sur l'enfant."""
        results = agent.retrieve("quel âge pour se marier un enfant ?", num=5)
        assert len(results) > 0
        # Vérifier que le domaine enfant est bien atteint
        domains = {r["domaine"] for r in results}
        assert "enfant" in domains

    def test_retrieve_female_law(self, agent):
        """la récupération doit trouver des textes sur la femme."""
        results = agent.retrieve("violences faites à une femme", num=5)
        assert len(results) > 0
        domains = {r["domaine"] for r in results}
        assert "femme" in domains or "enfant" in domains


class TestClarify:
    """Tests de clarification."""

    def test_clarify_returns_questions(self, agent):
        """La méthode clarify doit retourner une liste de questions."""
        questions = agent.clarify("Je me demande si je peux garder mon enfant")
        assert isinstance(questions, list)
        assert len(questions) > 0
        assert all(isinstance(q, str) for q in questions)


class TestGenerateReport:
    """Tests de génération de rapport Word."""

    def test_generate_report_creates_file(self, agent, tmp_path):
        """La génération de rapport doit créer un fichier Word."""
        from report_generator import ReportGenerator
        rg = ReportGenerator(output_dir=tmp_path)

        answer = agent.answer("Quel âge pour se marier un enfant ?")
        path = rg.generate(
            question="Quel âge pour se marier un enfant ?",
            answer_data=answer,
            filename="test_rapport.docx"
        )

        import os
        assert os.path.exists(path), f"File not found: {path}"
        assert path.endswith('.docx')
