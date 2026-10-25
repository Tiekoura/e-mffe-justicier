# e-MFFE justicier — Agent juridique ivoirien

Agent d'information juridique spécialisé dans le **droit de l'enfant**, le **droit de la femme** et le **droit de la famille** en Côte d'Ivoire.

## Principes

- **Ne rien inventer** : si la réponse n'est pas dans la base de connaissances, l'agent oriente vers un juriste.
- **Se baser sur la législation ivoirienne** : lois, articles, décrets, politiques publiques.
- **Citier complètement** : chaque texte est cité avec sa référence complète (loi n°..., date, article).
- **Respecter la protection des données personnelles** : conformément au Règlement (UE) 2016/679 (RGPD) et à la Loi n°2014-483 du 21 juillet 2014 relative à la protection des données personnelles en Côte d'Ivoire.
- **Indiquer quand une loi n'existe pas encore** : si la loi n'existe pas en Côte d'Ivoire, l'agent le signale explicitement.

## Architecture

```
e-mffe-justicier/
├── SKILL.md                  # Définition du comportement de l'agent
├── config.yaml               # Configuration (sections légales, avertissements)
├── requirements.txt
├── README.md
├── data/
│   ├── loi_child.json        # Droit de l'enfant (10 enregistrements)
│   ├── loi_female.json       # Droit de la femme (5 enregistrements)
│   ├── loi_family.json       # Droit de la famille (8 enregistrements)
│   ├── loi_donnees.json      # Protection des données (3 enregistrements)
│   ├── schema.yaml           # Schéma de la base de connaissances
│   └── loi_family.yaml       # Version YAML (documentation)
├── src/
│   ├── __init__.py
│   ├── main.py               # API FastAPI (endpoints REST)
│   ├── agent.py              # Noyau de raisonnement
│   ├── retriever.py          # Récupération de textes de loi
│   ├── report_generator.py   # Générateur de rapports Word
│   └── prompts.py            # Prompts système
├── tests/
│   └── test_agent.py         # Tests (8 tests, tous passés)
└── output/                   # Rapports Word générés
```

## Fonctionnalités

### 1. Découverte de la situation
- L'agent reçoit une question écrite de l'usager.
- Il pose 3 à 8 questions ciblées pour comprendre la situation.
- Ne collecte PAS de données nominatives (nom, téléphone, email...).

### 2. Récuperation des textes
- Pour chaque élément de la situation, recherche la ou les lois applicables.
- Chaque texte cité est accompagné de sa référence complète.
- Affiche la date de "dernière actualisation" des informations.
- Précise explicitement si un texte n'existe pas encore en ivoirien.

### 3. Production de la réponse
La réponse contient :
- **Attitude à tenir** : démarches et comportement recommandés, étape par étape.
- **Textes applicables** : cités mot pour mot avec leur référence complète.
- **Sanctions / pénalités** : les peines ou astreintes applicables.
- **Explications** : comment le texte s'applique à la situation.
- **Sources officielles** : références.
- **Avertissement** : "Cette réponse est informative et ne constitue pas un conseil juridique définitif."

### 4. Génération du rapport Word
Quand l'usager demande un rapport, l'agent produit un document Word avec :
- En-tête (titre, date, référence de session)
- Questions de clarification
- Analyse juridique (textes cités, citations, sanctions)
- Dispositions générales et avertissements
- Mention de non-responsabilité
- Signature indicielle

### 5. Règle de non-invention
- Si l'agent ne connaît pas la réponse : "Je ne dispose pas de cette information. Veuillez consulter un juriste."
- Si la loi n'existe pas encore : "La loi n'existe pas encore en Côte d'Ivoire. Veuillez consulter un juriste."

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

### Interface CLI
```python
from src.agent import Agent

agent = Agent()
response = agent.answer("Quel est l'âge minimum pour se marier en Côte d'Ivoire ?")
print(response["attitude_recommandee"])
```

### API FastAPI
```bash
uvicorn src.main:app --reload
```

Endpoints :
- `POST /api/chat` — Envoyer une question
- `POST /api/report` — Générer un rapport Word
- `GET /api/health` — État de santé
- `GET /api/kb` — Statistiques de la base de connaissances

### Génération de rapport
```python
from src.report_generator import ReportGenerator

rg = ReportGenerator(output_dir="output")
path = rg.generate(
    question="Mon mari ne paie pas la pension alimentaire",
    answer_data=response,
    filename="rapport_femme.docx"
)
```

## Architecture du projet

### Base de connaissances
Les fichiers JSON dans `data/` contiennent les enregistrements législatifs avec :
- `id` : identifiant unique
- `domaine` : enfant, femme, famille, donnees
- `titre` : nom court du texte
- `reference` : référence complète (loi, date, article)
- `source` : source officielle
- `niveau_vérité` : niveau de vérification (page_extracted, source_only, verified)
- `contenu` : texte du texte
- `attitude_recommandee` : démarche recommandée
- `sanctions` : sanctions applicables
- `questions_clés` : tags pour la recherche
- `questions_non_repondues` : limites connues

### Workflow de l'agent
1. **Découverte** : la première question est suivie de questions de clarification
2. **Recherche** : recherche des textes par mots-clés et correspondance
3. **Synthèse** : construction de la réponse (attitude, sanctions, explications, sources)
4. **Report** : génération du document Word

## Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

## Conformité RGPD / Loi ivoirienne

- Le service ne stocke pas de données nominatives sans consentement explicite.
- Une mention de confidentialité est affichée en permanence.
- L'usager peut demander la suppression de ses données.
- Conforme au Règlement (UE) 2016/679 et à la Loi n°2014-483 du 21 juillet 2014.

## Développement

### Ajouter un nouveau texte légal
1. Créer un enregistrement JSON dans `data/loi_<domaine>.json`
2. Ajouter les champs requis (id, domaine, titre, reference, contenu, etc.)
3. Lancer les tests : `python -m pytest tests/ -v`

### Ajouter un domaine légal
1. Créer `data/loi_<domaine>.json`
2. Ajouter l'entrée dans `config.yaml` et `src/agent.py` `KB_FILES`
3. Mettre à jour `src/main.py` si nécessaire

## Remerciements

Référence inspirante : Mon Recours CI (https://161-97-152-13.sslip.io/)

---

**Avertissement légal** : Cet outil est informatif et ne constitue pas un avis juridique définitif. Il ne se responsabilise pas des interprétations données. Pour un état des lieux précis, une défense ou un dossier juridique, consultez un juriste agréé.
