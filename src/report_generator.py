"""
report_generator.py — Générateur de rapports Word pour e-MFFE justicier.

Produit un document Word complet avec :
- En-tête, date, référence de session
- Questions de clarification
- Analyse juridique (textes cités, citations, sanctions)
- Dispositions générales et avertissements
- Mention de non-responsabilité
"""

import logging
from datetime import datetime
from pathlib import Path
from docx import Document
from docx.shared import Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

logger = logging.getLogger("emffe-justicier")

# Couleur d'accent pour le rapport (la couleur de l'agent "e-MFFE")
ACCENT_COLOR = RGBColor(0x0F, 0x2A, 0x22)   # vert foncé (teinte du thème)
ALERT_COLOR = RGBColor(0xCC, 0x00, 0x00)    # rouge pour les avertissements


class ReportGenerator:
    """Génère un rapport Word de la situation juridique."""

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path("output")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _add_heading(self, doc, text, level=1):
        """Ajoute un titre stylisé."""
        h = doc.add_heading(text, level=level)
        for run in h.runs:
            run.font.color.rgb = ACCENT_COLOR
        return h

    def _add_warning(self, doc, text):
        """Ajoute un avertissement en rouge."""
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.font.color.rgb = ALERT_COLOR
        run.bold = True
        return p

    def generate(
        self,
        question: str,
        answer_data: dict,
        filename: str = None,
        output_dir: Path = None,
    ) -> str:
        """
        Génère un rapport Word complet.

        Args:
            question: La question de l'usager.
            answer_data: Le dictionnaire de réponse de l'agent.
            filename: Nom du fichier (sans extension). Dossier par défaut 'output'.
            output_dir: Répertoire de sortie. Si None, utilise self.output_dir.

        Returns:
            Chemin absolu du fichier .docx généré.
        """
        if output_dir is not None:
            self.output_dir = output_dir
            self.output_dir.mkdir(parents=True, exist_ok=True)

        if filename is None:
            filename = f"rapport_emffe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"

        output_path = self.output_dir / filename

        doc = Document()

        # Configuration des marges
        for section in doc.sections:
            section.top_margin = Mm(20)
            section.bottom_margin = Mm(20)
            section.left_margin = Mm(25)
            section.right_margin = Mm(25)

        # Titre principal
        title = doc.add_heading("RAPPORT DE SITUATION JURIDIQUE", level=0)
        for run in title.runs:
            run.font.color.rgb = ACCENT_COLOR

        # Sous-titre
        subtitle = doc.add_paragraph()
        run = subtitle.add_run("Agent e-MFFE justicier — Outil d'information juridique ivoirien")
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

        doc.add_paragraph()

        # Informations de la session
        self._add_section_info(doc)

        # Question de l'usager
        self._add_question(doc, question)

        # Contexte de la situation (questions de clarification)
        self._add_context(doc, answer_data)

        # Analyse juridique
        self._add_legal_analysis(doc, answer_data)

        # Dispositions générales
        self._add_disclaimers(doc)

        # Signature indicielle
        self._add_signature(doc)

        # Sauvegarde
        doc.save(str(output_path))
        logger.info(f"Rapport Word généré : {output_path}")
        return str(output_path)

    def _add_section_info(self, doc):
        """Ajoute les informations de la session."""
        p = doc.add_paragraph()
        p.add_run("Date de génération : ").bold = True
        p.add_run(datetime.now().strftime("%d/%m/%Y à %H:%M"))

        p2 = doc.add_paragraph()
        p2.add_run("Agent : ").bold = True
        p2.add_run("e-MFFE justicier v0.1.0")

        p3 = doc.add_paragraph()
        p3.add_run("Domaines couverts : ").bold = True
        p3.add_run("Droit de l'enfant, Droit de la femme, Droit de la famille, "
                   "Succession, Protection des données personnelles")

    def _add_question(self, doc, question):
        """Ajoute la question de l'usager."""
        self._add_heading(doc, "Question de l'usager", level=2)
        p = doc.add_paragraph()
        p.add_run(question)
        doc.add_paragraph()

    def _add_context(self, doc, answer_data):
        """Ajoute le contexte de la situation."""
        if answer_data.get("questions_de_clarification"):
            self._add_heading(doc, "Contexte et questions de clarification", level=2)
            for q in answer_data["questions_de_clarification"]:
                doc.add_paragraph(q, style="List Bullet")
            doc.add_paragraph()

    def _add_legal_analysis(self, doc, answer_data):
        """Ajoute l'analyse juridique avec les textes cités."""
        self._add_heading(doc, "Analyse juridique", level=2)

        if answer_data.get("texts_applicables"):
            for i, t in enumerate(answer_data["texts_applicables"], 1):
                self._add_heading(doc, f"{i}. {t['titre']}", level=3)

                # Zone de citation
                p = doc.add_paragraph()
                p.add_run("Référence : ").bold = True
                p.add_run(t.get("reference", "N/A"))

                p2 = doc.add_paragraph()
                p2.add_run("Niveau de vérification : ").bold = True
                p2.add_run(t.get("niveau_vérité", "N/A"))

                p3 = doc.add_paragraph()
                p3.add_run("Texte : ").bold = True
                p3.add_run(t.get("contenu", ""))

                p4 = doc.add_paragraph()
                p4.add_run("Attitude recommandée : ").bold = True
                p4.add_run(t.get("attitude_recommandee", ""))

                p5 = doc.add_paragraph()
                p5.add_run("Sanctions : ").bold = True
                p5.add_run(t.get("sanctions", "N/A"))

                doc.add_paragraph()
        else:
            self._add_warning(doc,
                "⚠ Aucun texte de loi applicable n'a été retrouvé dans la base de "
                "connaissances. La loi n'existe peut-être pas encore en Côte d'Ivoire, "
                "ou la question dépasse le périmètre de cet outil. "
                "Consultez un juriste pour un état des lieux précis.")

    def _add_disclaimers(self, doc):
        """Ajoute les avertissements légaux."""
        self._add_heading(doc, "Dispositions générales et avertissements", level=2)

        self._add_warning(doc,
            "CETTE RÉPONSE EST INFORMATIVE ET NE CONSTITUE PAS UN CONSEIL JURIDIQUE DÉFINITIF. "
            "Pour un état des lieux précis, une défense ou un dossier juridique, "
            "il est recommandé de consulter un juriste agréé.")

        self._add_warning(doc,
            "e-MFFE justicier ne se responsabilise pas des interprétations données "
            "dans ce rapport. Ces informations sont basées sur les textes de loi "
            "disponibles dans sa base de connaissances au moment de la génération.")

        # Mention de conformité RGPD
        p = doc.add_paragraph()
        p.add_run("Conformité RGPD / Loi n°2014-483 : ").bold = True
        p.add_run("Ce rapport a été généré conformément au Règlement (UE) 2016/679 "
                  "et à la Loi n°2014-483 du 21 juillet 2014 relative à la protection "
                  "des données personnelles en Côte d'Ivoire. Aucune donnée "
                  "nominative n'a été stockée.")

    def _add_signature(self, doc):
        """Ajoute la mention de signature indicielle."""
        doc.add_paragraph()
        p = doc.add_paragraph()
        p.add_run("Signatures indicielles : ").bold = True
        p.add_run("Généré par e-MFFE justicier — Outil d'information juridique")
        doc.add_paragraph()

        p2 = doc.add_paragraph()
        p2.add_run("Direction : ").bold = True
        p2.add_run("Agent juridique ivoirien spécialisé en droit de l'enfant, de la femme et de la famille")
        doc.add_paragraph()

        p3 = doc.add_paragraph()
        p3.add_run("Nan tant que a toujours été une question de jurisprudence et non de droit.").italic = True
