"""
main.py — API FastAPI pour l'agent e-MFFE justicier.

Endpoints :
- POST /api/chat      : Envoyer une question, obtenir une réponse structurée
- POST /api/report    : Générer un rapport Word complet
- GET  /api/health    : État de santé de l'agent
- GET  /api/kb        : Statistiques de la base de connaissances
"""

import logging
from pathlib import Path
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from .agent import Agent
from .retriever import Retriever
from .report_generator import ReportGenerator

app = FastAPI(
    title="e-MFFE justicier — Agent juridique ivoirien",
    description="Agent d'information juridique sur le droit de l'enfant, de la femme et de la famille en Côte d'Ivoire",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Initialisation
KB_DIR = Path(__file__).parent.parent / "data"
agent = Agent(kb_dir=KB_DIR)
retriever = Retriever(kb_dir=KB_DIR)
report_generator = ReportGenerator(output_dir=Path(__file__).parent.parent / "output")

logger = logging.getLogger("emffe-justicier")
logging.basicConfig(level=logging.INFO)


# ── Modèles Pydantic ──────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=5000,
                           description="La question de l'usager (3+ caractères)")
    conversation_history: list = Field(default=None,
                                       description="Historique des échanges")


class ChatResponse(BaseModel):
    etat: str = Field(..., description="état de la réponse (needs_clarification / answered)")
    questions_de_clarification: list = Field(default=[], description="Questions à poser")
    texts_applicables: list = Field(default=[], description="Textes de loi retrouvés")
    attitude_recommandee: str = Field(..., description="Attitude à tenir")
    sanctions: str = Field(..., description="Sanctions applicables")
    explications: str = Field(..., description="Explications synthétiques")
    sources: list = Field(default=[], description="Références sources")
    orientation_juriste: bool = Field(default=False, description="Si orientation vers un juriste")
    detected_topic: str = Field(default="inconnu", description="Domaine détecté")
    message: str = Field(default="", description="Message d'orientation")


class ReportRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=5000)
    conversation_history: list = Field(default=None)
    filename: str = Field(default=None, description="Nom du fichier (sans extension)")


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    kb_records: int
    kb_domains: list


# ── Endpoints ──────────────────────────────────────────────────────────────

@app.get("/", tags=["Root"])
async def root():
    return {
        "service": "e-MFFE justicier",
        "version": "0.1.0",
        "status": "opérationnel",
        "documentation": "/docs",
    }


@app.get("/api/health", response_model=HealthResponse, tags=["API"])
async def health_check():
    """Retourne l'état de santé de l'agent."""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "kb_records": len(agent.records),
        "kb_domains": list({r["domaine"] for r in agent.records}),
    }


@app.post("/api/chat", response_model=ChatResponse, tags=["API"])
async def chat(request: ChatRequest):
    """
    Traite une question de l'usager.
    Retourne une réponse structurée (questions de clarification, textes de loi, etc.)
    """
    if len(request.question) < 3:
        raise HTTPException(status_code=400,
                            detail="La question doit contenir au moins 3 caractères")

    if request.conversation_history is None:
        request.conversation_history = []

    # 1. Si c'est la première question, poser des questions de clarification
    if not request.conversation_history:
        questions = agent.clarify(request.question, request.conversation_history)
        if questions:
            return {
                "etat": "needs_clarification",
                "questions_de_clarification": questions,
                "attitude_recommandee": "",
                "sanctions": "",
                "explications": "",
                "sources": [],
                "orientation_juriste": False,
                "detected_topic": "inconnu",
                "message": "Quelques précisions s'imposent pour analyser votre situation.",
            }

    # 2. Répondre à la question
    answer = agent.answer(request.question, request.conversation_history)

    # 3. Générer un rapport si demandé
    report_path = None
    if request.conversation_history and isinstance(request.conversation_history, list):
        # Si l'historique contient un indicateur de demande de rapport
        if any("rapport" in str(h).lower() for h in request.conversation_history):
            report_path = report_generator.generate(
                question=request.question,
                answer_data=answer,
                filename=request.filename
            )
            answer["report_path"] = report_path

    return answer


@app.post("/api/report", tags=["API"])
async def generate_report(request: ReportRequest):
    """
    Génère un rapport Word complet à partir de la question et de l'analyse.
    """
    if len(request.question) < 3:
        raise HTTPException(status_code=400,
                            detail="La question doit contenir au moins 3 caractères")

    answer = agent.answer(request.question, request.conversation_history or [])

    report_path = report_generator.generate(
        question=request.question,
        answer_data=answer,
        filename=request.filename
    )

    return {
        "status": "ok",
        "report_path": report_path,
        "filename": Path(report_path).name,
        "size_kb": round(Path(report_path).stat().st_size / 1024, 1),
    }


@app.get("/api/kb", tags=["API"])
async def kb_stats():
    """Statistiques de la base de connaissances."""
    domains = {}
    for r in agent.records:
        d = r.get("domaine", "inconnu")
        domains[d] = domains.get(d, 0) + 1

    return {
        "total_records": len(agent.records),
        "domains": domains,
        "sources": list({r.get("source", "N/A") for r in agent.records}),
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/suggest/{topic}", tags=["API"])
async def suggest_questions(topic: str):
    """Suggère des questions types pour clarifier une situation."""
    q = Retriever(kb_dir=KB_DIR)
    suggestions = q.suggest_questions(topic)
    return {
        "topic": topic if topic else "inconnu",
        "questions": suggestions,
    }


# ── Gestion des fichiers statiques (pour l'interface) ─────────────────────

@app.get("/reports/{filename}", tags=["Fichiers"])
async def get_report(filename: str):
    """Télécharge un rapport Word généré."""
    report_path = Path(__file__).parent.parent / "output" / filename
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Rapport non trouvé")
    return FileResponse(
        report_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=filename,
    )
