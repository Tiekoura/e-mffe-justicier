"""
agent.py — Noyau de raisonnement de l'agent e-MFFE justicier.

Fonctionnalités :
- Reçoit une question de l'usager
- Pose des questions de clarification (sans données nominatives)
- Recherche les textes de loi applicables dans la base de connaissances
- Génère une réponse structurée (attitude, textes, sanctions, explications, sources)
- Applique la règle de non-invention
- Génère un rapport Word complet
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path

# Chemins du projet
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
KB_FILES = {
    "enfant": DATA_DIR / "loi_child.json",
    "femme": DATA_DIR / "loi_female.json",
    "famille": DATA_DIR / "loi_family.json",
    "donnees": DATA_DIR / "loi_donnees.json",
    "succession": DATA_DIR / "loi_family.json",  # reuse family for succession
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("emffe-justicier")


class KBNotFoundError(Exception):
    """Raised when no knowledge base records match the query."""


class Agent:
    """Agent juridique e-MFFE justicier."""

    # Questions à poser pour clarifier la situation
    CLARIFICATION_QUESTIONS = [
        "Quel est le problème principal que vous rencontrez ?",
        "Depuis quand ce problème est-il présent ?",
        "Avez-vous déjà déposé une plainte ou saisi la justice ?",
        "Quelles sont les personnes impliquées ? (mère, père, enfant, conjoint...)",
        "Y a-t-il des preuves (bilans médicaux, messages, courriers...) ?",
        "Êtes-vous dans une urgence ? (danger imminent, enfant en danger...)",
    ]

    # Champs personnels interdits (sauf autorisation explicite)
    PERSONAL_DATA_FIELDS = ["nom", "prénom", "téléphone", "email", "adresse", "numéro de casier"]

    def __init__(self, kb_dir: Path = None):
        self.kb_dir = kb_dir or DATA_DIR
        self.records = []
        self._loaded_ids = set()
        self.load_knowledge_base()

    def load_knowledge_base(self):
        """Charge tous les fichiers de connaissances."""
        all_records = []
        for domaine, path in KB_FILES.items():
            if not path.exists():
                logger.warning(f"Fichier KB introuvable : {path}")
                continue
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                for rec in data.get("enregistrements", []):
                    rec["domaine"] = domaine
                    rec_id = rec.get("id", "")
                    # Évite les doublons (ex: loi_family.json est chargé 2x)
                    if rec_id not in self._loaded_ids:
                        self.records.append(rec)
                        self._loaded_ids.add(rec_id)
            except Exception as e:
                logger.error(f"Erreur lecture {path}: {e}")
        self._dedupe()
        logger.info(f"KB chargée : {len(self.records)} enregistrements")

    def _is_personal_data(self, text: str) -> bool:
        """Détecte si le texte contient potentiellement des données nominatives."""
        for field in self.PERSONAL_DATA_FIELDS:
            if field in text.lower():
                return True
        return False

    def clarify(self, question: str, conversation_history: list = None) -> list:
        """
        Pose des questions de clarification pour comprendre la situation.
        Ne collecte PAS de données personnelles nominatives.
        """
        if conversation_history is None:
            conversation_history = []

        # Poser 3 à 8 questions ciblées
        questions = []
        for q in self.CLARIFICATION_QUESTIONS[:8]:
            if len(questions) >= 8:
                break
            if q not in conversation_history:
                questions.append(q)

        # Si l'usager donne des informations, valider qu'il n'y a pas de données personnelles
        for item in conversation_history:
            if self._is_personal_data(item):
                logger.warning("Données personnelles détectées, les filtrer")
                break

        return questions

    def retrieve(self, question: str, num_results: int = 5, num: int = None) -> list:
        """
        Recherche les textes de loi applicables à la question.
        La récupération se fait par correspondance de mots-clés.
        """
        if num is not None:
            num_results = num
        q_lower = question.lower()
        keywords = q_lower.split()

        scored = []
        for rec in self.records:
            score = 0
            text = (rec["titre"] + " " + rec["reference"] + " " + rec["contenu"]).lower()
            for kw in keywords:
                if len(kw) > 3:
                    if kw in text:
                        score += 1
                    # Porte-mots
                    for part in ["enfant", "femme", "famille", "succession", "violence", "mariage", "paternité"]:
                        if part in kw and part in text:
                            score += 0.5
            if score > 0:
                scored.append((score, rec))

        # Trier par score décroissant
        scored.sort(key=lambda x: x[0], reverse=True)
        return [rec for _, rec in scored[:num_results]]

    def answer(self, question: str, conversation_history: list = None) -> dict:
        """
        Génère une réponse structurée à la question de l'usager.
        Retourne un dictionnaire avec :
        - questions_de_clarification : listes de questions à poser
        - texts_applicables : les textes retenus avec citations complètes
        - attitude_recommandee : la démarche à suivre
        - sanctions : les sanctions applicables
        - explications : comment le texte s'applique
        - sources : références
        - orientation_juriste : si l'agent ne peut pas répondre
        """
        if conversation_history is None:
            conversation_history = []

        # 1. D'abord poser des questions de clarification (si pas encore fait)
        if not conversation_history:
            questions = self.clarify(question, conversation_history)
            return {
                "questions_de_clarification": questions,
                "etat": "needs_clarification",
                "contexte": "L'usager doit d'abord décrire sa situation avant analyse.",
            }

        # 2. Rechercher les textes applicables
        matching = self.retrieve(question, num_results=5)

        if not matching:
            return {
                "orientation_juriste": True,
                "message": "Je ne dispose pas de cette information dans ma base de connaissances. "
                          "Veuillez consulter un juriste pour un conseil précis.",
                "detected_topic": "incertain",
                "questions_a_poser": [
                    "Pouvez-vous préciser le domaine (enfant, femme, famille, succession, données) ?",
                    "Depuis quand ce problème existe-t-il ?",
                    "Avez-vous déjà contacté un professionnel de la justice ?",
                ],
            }

        # 3. Construire la réponse
        texts_applicables = []
        for rec in matching:
            texts_applicables.append({
                "id": rec["id"],
                "domaine": rec["domaine"],
                "titre": rec["titre"],
                "reference": rec["reference"],
                "niveau_vérité": rec["niveau_vérité"],
                "contenu": rec["contenu"],
                "attitude_recommandee": rec["attitude_recommandee"],
                "sanctions": rec["sanctions"],
            })

        # 4. Vérifier si l'usager a fourni des informations exprimant un aveu
        #    ou des éléments nécessitant une expertise
        has_assertion = any(kw in question.lower() for kw in [
            "je suis", "mon enfant", "mon mari", "mon père", "mon fils",
            "j'ai", "mauvais", "jure", "droit"
        ])

        return {
            "etat": "answered",
            "questions_de_clarification": [],
            "texts_applicables": texts_applicables,
            "attitude_recommandee": self._synthesize_attitude(question, texts_applicables),
            "sanctions": self._synthesize_sanctions(matchings := texts_applicables),
            "explications": self._synthesize_explications(question, texts_applicables),
            "sources": self._synthesize_sources(texts_applicables),
            "orientation_juriste": False,
            "detected_topic": self._detect_topic(question),
        }

    def _synthesize_attitude(self, question: str, texts: list) -> str:
        """Synthétise l'attitude à tenir à partir des textes retrouvés."""
        if not texts:
            return (
                "Cette situation nécessite une analyse par un juriste. "
                "Consultez un avocat ou un notaire pour un état des lieux précis."
            )

        # Construire une recommandation de base
        rec = "Basez-vous sur les textes cités ci-dessous. "
        if any("pension" in t["contenu"].lower() for t in texts):
            rec += "En cas de non-paiement de pension alimentaire, "
            rec += "consignez par écrit la décision et saisissez le juge des affaires familiales."
        if any("violence" in t["contenu"].lower() or "danger" in t["contenu"].lower() for t in texts):
            rec += "Signalez les faits immédiatement au policier judiciaire et saisissez les autorités de protection."
        if any("mariage" in t["contenu"].lower() and "âge" in t["contenu"].lower() for t in texts):
            rec += "Vérifiez l'âge de tous les intéressés avant toute célébration de mariage."
        if any("filiation" in t["contenu"].lower() for t in texts):
            rec += "Pour les contestations de filiation, rassemblez les preuves et saisissez le juge aux affaires familiales."

        rec += " Pour un diagnostic précis et une défense légale, consultez un juriste."
        return rec

    def _synthesize_sanctions(self, texts: list) -> str:
        """Récupère les sanctions déclarées dans les textes."""
        sanctions = []
        for t in texts:
            if t.get("sanctions"):
                sanctions.append(f"({t['titre']}) {t['sanctions']}")
        if sanctions:
            return " ; ".join(sanctions)
        return "Aucune sanction spécifique ne s'applique à cette situation. Consultez un juriste."

    def _synthesize_explications(self, question: str, texts: list) -> str:
        """Explication synthétique de la situation en fonction du contexte."""
        if not texts:
            return "Je ne dispose pas assez d'informations pour répondre précisément."

        expl = f"Votre question concernant « {question} » est analysée ci-dessous.\n\n"
        for t in texts:
            expl += f"• {t['titre']} :\n"
            expl += f"  {t['contenu'][:400]}...\n\n"
        return expl

    def _synthesize_sources(self, texts: list) -> list:
        """Récupère les références sources complètes."""
        sources = set()
        for t in texts:
            sources.add(t["reference"])
        return list(sources)

    def _detect_topic(self, question: str) -> str:
        """Détecte le domaine de la question."""
        q = question.lower()
        if any(k in q for k in ["enfant", "enfance"]):
            return "enfant"
        if any(k in q for k in ["femme", "mariage", "famille"]):
            return "femme"
        if any(k in q for k in ["mariage", "famille", "paternité"]):
            return "famille"
        if any(k in q for k in ["données", "confidentialité", "RGPD"]):
            return "donnees"
        if any(k in q for k in ["succession", "héritage"]):
            return "succession"
        return "inconnu"

    def _dedupe(self):
        """Supprime les doublons en conservant l'ordre."""
        seen = set()
        unique = []
        for rec in self.records:
            rid = rec.get("id", "")
            if rid not in seen:
                seen.add(rid)
                unique.append(rec)
        self.records = unique

    def generate_report(self, question: str, answer_data: dict, filename: str = None) -> str:
        """
        Génère un rapport Word complet de la situation juridique.
        Retourne le chemin du fichier généré.
        """
        from docx import Document
        from docx.shared import Pt, Mm, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH

        if filename is None:
            filename = f"rapport_emffe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"

        output_path = PROJECT_ROOT / "output" / filename

        doc = Document()

        # Styles de base
        style = doc.styles['Normal']
        style.font.name = 'Calibri'
        style.font.size = Pt(11)

        # Titre
        title = doc.add_heading('RAPPORT DE SITUATION JURIDIQUE', level=0)
        doc.add_paragraph()

        # En-tête
        doc.add_heading('Rapport généré par e-MFFE justicier', level=1)
        doc.add_paragraph(
            f"Date de génération : {datetime.now().strftime('%d/%m/%Y à %H:%M')}"
        )
        doc.add_paragraph(
            "Outil d'information — ne constitue pas un avis juridique professionnel."
        )
        doc.add_paragraph(
            "Cette réponse est générée automatiquement à partir des textes de loi "
            "disponibles dans la base de connaissances de l'agent e-MFFE justicier."
        )
        doc.add_paragraph()
        doc.add_paragraph(
            "Cette réponse est informative et ne constitue pas un conseil juridique définitif. "
            "Pour un état des lieux précis ou une défense, consultez un juriste agréé."
        )
        doc.add_paragraph()

        # Question de l'usager
        doc.add_heading('Question de l\'usager', level=2)
        doc.add_paragraph(question)
        doc.add_paragraph()

        # Contexte
        if answer_data.get("questions_de_clarification"):
            doc.add_heading('Questions de clarification', level=2)
            for q in answer_data["questions_de_clarification"]:
                doc.add_paragraph(q, style='List Bullet')
            doc.add_paragraph()

        # Domaines détectés
        if answer_data.get("detected_topic"):
            doc.add_heading('Domaines concernés', level=2)
            doc.add_paragraph(answer_data["detected_topic"], style='List Bullet')
            doc.add_paragraph()

        # Analyse juridique
        doc.add_heading('Analyse juridique', level=2)
        if answer_data.get("texts_applicables"):
            for i, t in enumerate(answer_data["texts_applicables"], 1):
                doc.add_heading(f'{i}. {t["titre"]}', level=3)
                doc.add_paragraph(f'**Référence :** {t["reference"]}')
                doc.add_paragraph(f'**Niveau de vérification :** {t["niveau_vérité"]}')
                doc.add_paragraph(f'**Texte :** {t["contenu"]}')
                doc.add_paragraph(f'**Attitude recommandée :** {t["attitude_recommandee"]}')
                doc.add_paragraph(f'**Sanctions :** {t["sanctions"]}')
                doc.add_paragraph()
        else:
            doc.add_paragraph(
                "Aucun texte de loi applicable n'a été retrouvé dans la base de connaissances. "
                "Il est possible que la loi n'existe pas encore en Côte d'Ivoire ou que la question "
                "depasse le périmètre de cet outil. Veuillez consulter un juriste."
            )
        doc.add_paragraph()

        # Dispositions générales
        doc.add_heading('Disposition générale', level=2)
        doc.add_paragraph(
            "Cette réponse est générée automatiquement par l'agent e-MFFE justicier. "
            "Elle est informative et ne constitue pas un conseil juridique définitif. "
            "Pour un état des lieux précis, une défense ou un dossier juridique, "
            "il est recommandé de consulter un juriste agréé."
        )
        doc.add_paragraph(
            "L'agent e-MFFE justicier ne se responsabilise pas des interprétations "
            "données par cette réponse."
        )

        # Signatures
        doc.add_paragraph()
        doc.add_paragraph("Signatures indicielles :")
        doc.add_paragraph("Généré par e-MFFE justicier — Outil d'information")
        doc.add_paragraph("Direction : Agent juridique ivoirien spécialisé en droit de l'enfant, de la femme et de la famille")

        # S'assurer que le répertoire existe
        output_path.parent.mkdir(parents=True, exist_ok=True)

        doc.save(str(output_path))
        logger.info(f"Rapport généré : {output_path}")
        return str(output_path)
