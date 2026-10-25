import json

# Paths
child_path = 'data/loi_child.json'
family_path = 'data/loi_family.json'
female_path = 'data/loi_female.json'
donnees_path = 'data/loi_donnees.json'

# Read current files
child = json.load(open(child_path, encoding='utf-8'))
family = json.load(open(family_path, encoding='utf-8'))
female = json.load(open(female_path, encoding='utf-8'))
donnees = json.load(open(donnees_path, encoding='utf-8'))

# 1. Child law enrichment
new_child = [
    {
        "id": "enc-enfant-011",
        "domaine": "enfant",
        "titre": "Filiation : rapport a l'enfant ne dans le mariage",
        "reference": "Loi n°2019-571 du 26 juin 2019 relative a la filiation ; Code civil I (Droit des personnes et de la famille)",
        "source": "famille.gouv.ci",
        "niveau_vérité": "source_only",
        "contenu": "Tout enfant a droit à l'établissement de sa filiation à l'égard de ses auteurs. L'enfant conçu pendant le mariage ou né moins de 300 jours après la dissolution du mariage a pour père le mari de sa mère.",
        "contexte": "Protection de la filiation dans le mariage.",
        "sanctions": "N/A (réglementation de la filiation)",
        "attitude_recommandee": "Prouver la filiation par les actes de naissance inscrits sur les registres de l'état civil.",
        "questions_clés": ["filiation", "enfant mariage", "paternité"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    },
    {
        "id": "enc-enfant-012",
        "domaine": "enfant",
        "titre": "Filiation : enfants nés hors mariage",
        "reference": "Loi n°2019-571 du 26 juin 2019 relative a la filiation ; Code civil I (Droit des personnes et de la famille)",
        "source": "famille.gouv.ci",
        "niveau_vérité": "source_only",
        "contenu": "La filiation des enfants nés hors mariage résulte à l'égard de la mère, du seul fait de la naissance. La reconnaissance est faite dans l'acte de naissance.",
        "contexte": "Protection spéciale de l'enfant né hors mariage.",
        "sanctions": "N/A",
        "attitude_recommandee": "Pour l'enfant hors mariage, la filiation à l'égard de la mère est automatique. Pour le père, il faut la reconnaissance ou une décision de justice.",
        "questions_clés": ["hors mariage", "reconnaissance", "filiation"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    }
]
child['enregistrements'].extend(new_child)

# 2. Family law enrichment
new_family = [
    {
        "id": "fam-civil-009",
        "domaine": "famille",
        "titre": "Mariage : reconnaissance par l'acte de naissance",
        "reference": "Loi n°2019-570 du 26 juin 2019 relative au mariage ; Code civil I (Droit des personnes et de la famille)",
        "source": "famille.gouv.ci",
        "niveau_vérité": "source_only",
        "contenu": "Le mariage est l'union d'un homme et d'une femme célébrée par devant l'officier de l'état civil. Il crée la famille légitime. Les époux s'obligent à la communauté de vie, se doivent mutuellement respect, fidélité, secours et assistance.",
        "contexte": "Règles du mariage et de ses effets personnels.",
        "sanctions": "Mariage nul : nullité de l'union",
        "attitude_recommandee": "Le mariage doit être célébré devant l'officier de l'état civil. Chaque époux doit contribuer aux charges du ménage.",
        "questions_clés": ["mariage", "célébration", "effets"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    },
    {
        "id": "fam-civil-010",
        "domaine": "famille",
        "titre": "Domicile de la famille",
        "reference": "Loi n°2019-570 du 26 juin 2019 relative au mariage ; Code civil I (Droit des personnes et de la famille)",
        "source": "famille.gouv.ci",
        "niveau_vérité": "source_only",
        "contenu": "Le domicile de la famille est choisi d'un commun accord par les époux. En cas de désaccord, le domicile de la famille est fixé par le tribunal en tenant compte de l'intérêt de la famille.",
        "contexte": "Règles de domicile familial.",
        "sanctions": "N/A",
        "attitude_recommandee": "Conseiller un accord conjoint pour le domicile. En cas de désaccord, saisir le tribunal.",
        "questions_clés": ["domicile", "foyer", "conflit"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    },
    {
        "id": "fam-civil-011",
        "domaine": "famille",
        "titre": "Obligations des époux envers les enfants",
        "reference": "Loi n°2019-570 du 26 juin 2019 relative au mariage ; Code civil I (Droit des personnes et de la famille)",
        "source": "famille.gouv.ci",
        "niveau_vérité": "source_only",
        "contenu": "Les époux assurent ensemble la direction morale et matérielle de la famille, pourvoient à l'éducation des enfants et préparent leur avenir. Ils contribuent aux charges du ménage à proportion de leurs facultés respectives.",
        "contexte": "Rôle parental conjoint.",
        "sanctions": "Violations : responsabilité des parents, suppression des droits",
        "attitude_recommandee": "Partage égal des responsabilités parentales et des charges du ménage.",
        "questions_clés": ["obligations", "éducation", "ménage"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    }
]
family['enregistrements'].extend(new_family)

# 3. Women's rights enrichment
new_female = [
    {
        "id": "fem-female-006",
        "domaine": "femme",
        "titre": "Violences domestiques : protection de la femme",
        "reference": "Loi n°202l-894 du 22 décembre 202l relative aux mesures de protection des victimes de violences domestiques, de viol et de violences sexuelles autres que domestiques",
        "source": "famille.gouv.ci",
        "niveau_vérité": "source_only",
        "contenu": "Loi n°2021-894 accorde des mesures de protection spéciales aux victimes de violences domestiques, de viol et de violences sexuelles. Les victimes peuvent saisir les juridictions compétentes pour obtenir des mesures de protection immédiate.",
        "contexte": "Protection des femmes victimes de violences.",
        "sanctions": "Condamnation pénale pour violences, viol, violences sexuelles",
        "attitude_recommandee": "Signaler immédiatement la violence. Saisir le tribunal pour obtenir des mesures de protection.",
        "questions_clés": ["violence", "violences domestiques", "protection"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    },
    {
        "id": "fem-female-007",
        "domaine": "femme",
        "titre": "Carrière et famille : conciliation",
        "reference": "Code civil Ivoirien, Livre I (Droit des personnes et de la famille) ; Loi n°2019-680 du 14 septembre 2019",
        "source": "LEXCI, Loi 2019-680",
        "niveau_vérité": "source_only",
        "contenu": "La loi 2019-680 du 14 septembre 2019 renforce l'égalité entre les femmes et les hommes, notamment dans l'accès à la carrière et la conciliation vie professionnelle et vie familiale.",
        "contexte": "Égalité des chances dans la vie professionnelle et familiale.",
        "sanctions": "Discrimination sexiste : action en justice",
        "attitude_recommandee": "Si discrimination, saisir le tribunal. Exiger une conciliation entre vie pro et vie familiale.",
        "questions_clés": ["carrière", "famille", "conciliation", "égalité"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    }
]
female['enregistrements'].extend(new_female)

# 4. Data protection enrichment
new_donnees = [
    {
        "id": "dp-rgpd-004",
        "domaine": "donnees",
        "titre": "Données des usagers : protection spéciale",
        "reference": "Loi n°2014-483 du 21 juillet 2014 relative à la protection des données personnelles ; Règlement (UE) 2016/679 (RGPD)",
        "source": "Loi 2014-483, RGPD",
        "niveau_vérité": "source_only",
        "contenu": "Les données des usagers des services juridiques (dossiers, dossiers d'enfants, dossiers de femmes victimes de violences) sont des données à sensibilité spéciale et sont soumises à une protection renforcée.",
        "contexte": "Protection des données des populations vulnérables (enfants, femmes victimes).",
        "sanctions": "Sanctions administratives et pénales pour non-respect du cadre légal",
        "attitude_recommandee": "Obtenir le consentement explicite. Restreindre l'accès aux données. Supprimer à la fin de la procédure.",
        "questions_clés": ["données", "protection", "usagers", "confidentialité"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    }
]
donnees['enregistrements'].extend(new_donnees)

# Write back
json.dump(child, open(child_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(family, open(family_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(female, open(female_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(donnees, open(donnees_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print("Updated: %d child, %d family, %d female, %d donnees" % (
    len(child['enregistrements']), len(family['enregistrements']),
    len(female['enregistrements']), len(donnees['enregistrements']))
)
