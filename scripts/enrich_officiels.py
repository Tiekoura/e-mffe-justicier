import json

# Read current files
data_dir = 'data'

child = json.load(open(data_dir + '/loi_child.json', encoding='utf-8'))
family = json.load(open(data_dir + '/loi_family.json', encoding='utf-8'))
female = json.load(open(data_dir + '/loi_female.json', encoding='utf-8'))
donnees = json.load(open(data_dir + '/loi_donnees.json', encoding='utf-8'))

# ==================== ENFANT ====================
# Add official consolidated references
child['metadata']['date_mise_a_jour'] = '2026-10-25'
child['metadata']['sources'] = [
    'famille.gouv.ci (Loi n2019-571 du 26 juin 2019)',
    'famille.gouv.ci (Loi n2019-570 du 26 juin 2019)',
    'LEXCI (Code de la Famille, 545 articles)',
    'gouv.ci (Portail officiel du Gouvernement)',
    'Code civil Ivoirien (Droit des personnes et de la famille)'
]

# Add official records with consolidated references
new_child = [
    {
        "id": "enc-enfant-013",
        "domaine": "enfant",
        "titre": "Filiation : plein exercice des droits",
        "reference": "Loi n2019-571 du 26 juin 2019 relative à la filiation (Code civil I, Livre Ier : Droit des personnes et de la famille), articles 1, 9, 11, 19, 22, 26, 28",
        "source": "famille.gouv.ci",
        "niveau_vérité": "source_only",
        "contenu": "Tout enfant a droit à l'établissement de sa filiation à l'égard de ses auteurs. La filiation des enfants nés dans le mariage se prouve par les actes de naissance inscrits sur les registres de l'état civil. En défaut de ce titre, la possession d'état d'enfant né dans le mariage suffit. La filiation des enfants nés hors mariage résulte à l'égard de la mère, du seul fait de la naissance.",
        "contexte": "Protection de la filiation dans tous les cas de figure.",
        "sanctions": "N/A (réglementation de la filiation)",
        "attitude_recommandee": "Pour un enfant né dans le mariage : consulter le service de l'état civil pour les actes de naissance. Pour un enfant hors mariage : demander la reconnaissance ou une décision de justice.",
        "questions_clés": ["filiation", "enfant", "droits", "mariage"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    },
    {
        "id": "enc-enfant-014",
        "domaine": "enfant",
        "titre": "Domicile de l'enfant mineur",
        "reference": "Code civil Ivoirien, Livre I (Droit des personnes et de la famille), articles 102 à 111 (Domicile) ; Loi n2019-570 du 26 juin 2019",
        "source": "famille.gouv.ci",
        "niveau_vérité": "source_only",
        "contenu": "Le domicile de tout Ivoirien, quant à l'exercice de ses droits civils, est au lieu où il a son principal établissement. Le mineur non émancipé aura son domicile chez ses père et mère ou tuteur. Par exception, le mineur peut avoir son domicile séparé de celui de ses père et mère.",
        "contexte": "Détermination du domicile de l'enfant mineur.",
        "sanctions": "N/A (règles de domicile)",
        "attitude_recommandee": "Le mineur a son domicile chez ses père et mère ou tuteur. En cas de désaccord, le tribunal peut fixer le domicile.",
        "questions_clés": ["domicile", "mineur", "foyer"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    },
    {
        "id": "enc-enfant-015",
        "domaine": "enfant",
        "titre": "Protection des enfants en situation de famille d'accueil",
        "reference": "Décret 90 de 2023 portant Règlementation des Familles d'Accueil ; Loi n2019-571 du 26 juin 2019 relative à la filiation",
        "source": "famille.gouv.ci",
        "niveau_vérité": "source_only",
        "contenu": "La famille d'accueil est constituée d'un couple formé d'un homme et d'une femme vivant ensemble, d'un homme vivant seul ou d'une femme vivant seule. La famille d'accueil ne doit pas avoir plus de six enfants à son domicile, enfants accueillis y compris, pour un couple, et plus de quatre enfants pour une femme vivant seule ou un homme vivant seul. Le placement dans une famille d'accueil est une mesure de protection prise par le juge des tutelles.",
        "contexte": "Protection de l'enfant en situation de placement.",
        "sanctions": "N/A (mesures de protection)",
        "attitude_recommandee": "Le placement dans une famille d'accueil est pris par le juge des tutelles. La famille d'accueil accepte de recevoir l'enfant dans le respect des conditions fixées par le décret.",
        "questions_clés": ["placement", "famille d'accueil", "enfant", "protection"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    }
]
child['enregistrements'].extend(new_child)

# ==================== FAMILLE ====================
family['metadata']['date_mise_a_jour'] = '2026-10-25'
family['metadata']['sources'] = [
    'famille.gouv.ci (Loi n2019-570 du 26 juin 2019)',
    'famille.gouv.ci (Loi n2019-571 du 26 juin 2019)',
    'LEXCI (Code de la Famille, 545 articles)',
    'familles.gouv.ci (Journaux officiels 2022)',
    'Code civil Ivoirien (Droit des personnes et de la famille)'
]

new_family = [
    {
        "id": "fam-civil-012",
        "domaine": "famille",
        "titre": "Domicile de la famille",
        "reference": "Code civil Ivoirien, Livre I, Titre II (De la famille), articles 56 à 60 ; Loi n2019-570 du 26 juin 2019",
        "source": "famille.gouv.ci",
        "niveau_vérité": "source_only",
        "contenu": "Le domicile de la famille est choisi d'un commun accord par les époux. En cas de désaccord, le domicile de la famille est fixé par le tribunal en tenant compte de l'intérêt de la famille. La femme mariée a l'usage du nom du mari.",
        "contexte": "Règles du domicile familial.",
        "sanctions": "N/A (règles de domicile)",
        "attitude_recommandee": "Conseiller un accord conjoint pour le domicile. En cas de désaccord, saisir le tribunal en tenant compte de l'intérêt de la famille.",
        "questions_clés": ["domicile", "foyer", "conflit"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    },
    {
        "id": "fam-civil-013",
        "domaine": "famille",
        "titre": "Régime matrimonial : communauté de biens",
        "reference": "Loi n2019-570 du 26 juin 2019 relative au mariage ; Code civil I (Droit des personnes et de la famille)",
        "source": "famille.gouv.ci",
        "niveau_vérité": "source_only",
        "contenu": "Le régime matrimonial est l'ensemble des règles régissant les effets pécuniaires du mariage dans les rapports des époux entre eux. Par défaut, le régime est la communauté de biens. Les acquêts acquis durant le mariage appartiennent à la communauté.",
        "contexte": "Protection des biens dans le mariage.",
        "sanctions": "N/A (règles de régime matrimonial)",
        "attitude_recommandee": "En l'absence de contrat de mariage, le régime est la communauté de biens. Consulter un notaire pour un régime matrimonial particulier.",
        "questions_clés": ["régime matrimonial", "communauté", "biens"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    },
    {
        "id": "fam-civil-014",
        "domaine": "famille",
        "titre": "Succession : droits de l'enfant",
        "reference": "Code civil Ivoirien, Livre III (De la succession), articles 733 à 874 ; Loi n2019-570 du 26 juin 2019",
        "source": "famille.gouv.ci",
        "niveau_vérité": "source_only",
        "contenu": "Les enfants ont droit à une part de la succession, égale entre eux. Le conjoint survivant a droit à une part selon le régime de la succession. L'égalité des droits entre enfants est garantie. Pour accepter une succession, il y a trois formes : acceptation simple, acceptation sous bénéfice d'inventaire, renonciation.",
        "contexte": "Protection de l'héritage et de l'enfant dans les successions.",
        "sanctions": "Révocation de l'acte de partage en cas de dol ou de violation des réserves",
        "attitude_recommandee": "Prendre connaissance du testament ou de l'acte de notoriété. Faire constater l'état des biens. Pour l'enfant, demander le respect de la réserve héréditaire.",
        "questions_clés": ["succession", "héritage", "réserve", "partage", "part des enfants"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    },
    {
        "id": "fam-civil-015",
        "domaine": "famille",
        "titre": "Divorce : séparation de corps",
        "reference": "Code civil Ivoirien, Livre I, Titre II, articles 346 à 380 ; Loi n2019-570 du 26 juin 2019",
        "source": "famille.gouv.ci",
        "niveau_vérité": "source_only",
        "contenu": "La séparation de corps est une mesure de protection qui permet à l'un des époux de résider séparément de l'autre en raison de danger au foyer, de violence conjugale ou de comportement tourmenteur. Le juge peut ordonner à l'époux agresseur de quitter le foyer commun, sans préjudice de ses droits de visite et d'hébergement pour l'enfant.",
        "contexte": "Protection de la victime de violence conjugale.",
        "sanctions": "Violences conjugales : sanctions pénales",
        "attitude_recommandee": "Saisir immédiatement le juge des libérations conditionnelles ou le procureur de la République pour une mesure de protection.",
        "questions_clés": ["séparation", "danger", "violence", "résidence"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    }
]
family['enregistrements'].extend(new_family)

# ==================== FEMME ====================
female['metadata']['date_mise_a_jour'] = '2026-10-25'
female['metadata']['sources'] = [
    'famille.gouv.ci (Loi n2021-894 du 22 décembre 2021)',
    'famille.gouv.ci (Loi n2019-680 du 14 septembre 2019)',
    'Code pénal Ivoirien (Loi n°95-90 du 24 février 1995)',
    'LEXCI (Code de la Famille)',
    "OHADA / CEDAW (Convention sur l'élimination de toutes les formes de discrimination à l'égard des femmes)"
]

new_female = [
    {
        "id": "fem-female-008",
        "domaine": "femme",
        "titre": "Violences domestiques : protection spéciale",
        "reference": "Loi n2021-894 du 22 décembre 2021 relative aux mesures de protection des victimes de violences domestiques, de viol et de violences sexuelles autres que domestiques",
        "source": "famille.gouv.ci",
        "niveau_vérité": "source_only",
        "contenu": "Loi n2021-894 du 22 décembre 2021 accorde des mesures de protection spéciales aux victimes de violences domestiques, de viol et de violences sexuelles. Les victimes peuvent saisir les juridictions compétentes pour obtenir des mesures de protection immédiate. Le tribunal territorialement compétent est celui du domicile réel ou élu du défendeur.",
        "contexte": "Protection renforcée des femmes victimes de violences.",
        "sanctions": "Condamnation pénale pour violences, viol, violences sexuelles",
        "attitude_recommandee": "Signaler immédiatement la violence. Saisir le tribunal pour obtenir des mesures de protection immédiate.",
        "questions_clés": ["violence", "violences domestiques", "protection"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    },
    {
        "id": "fem-female-009",
        "domaine": "femme",
        "titre": "Egalité professionnelle et familial",
        "reference": "Loi n2019-680 du 14 septembre 2019 portant égalité entre les femmes et les hommes ; Code du travail Ivoirien (Loi n95-673 du 24 septembre 1995)",
        "source": "famille.gouv.ci",
        "niveau_vérité": "source_only",
        "contenu": "La loi n2019-680 du 14 septembre 2019 portant égalité entre les femmes et les hommes vise à éliminer les discriminations fondées sur le sexe et à garantir l'égalité de droits et de chances entre les femmes et les hommes en Côte d'Ivoire. Le Code du travail garantit la protection de la femme au travail : interdépendance des horaires, protection pendant la grossesse, après l'accouchement et pendant l'allaitement.",
        "contexte": "Égalité des chances dans la vie professionnelle et familiale.",
        "sanctions": "Discrimination sexiste : action en justice, obtenir des dommages et intérêts",
        "attitude_recommandee": "Toute discrimination à raison du sexe est réprimée. Saisir les tribunaux ou les autorités compétentes si la discrimination est constatée.",
        "questions_clés": ["égalité", "professionnelle", "discrimination"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    },
    {
        "id": "fem-female-010",
        "domaine": "femme",
        "titre": "Protection de la femme enceinte et de l'enfant à naître",
        "reference": "Loi n2019-680 du 14 septembre 2019 ; Loi n2019-571 du 26 juin 2019 ; Code de l'enfant (Loi n2013-665 du 29 octobre 2013)",
        "source": "familles.gouv.ci",
        "niveau_vérité": "source_only",
        "contenu": "La femme enceinte et l'enfant à naître bénéficient d'une protection spéciale. L'accouchement et le suivi médical prénatal sont des droits de la femme et de l'enfant. Toute violence portant sur la femme enceinte ou les soins à l'enfant à naître est sanctionnée. Le Code de l'enfant garantit la protection de l'enfant à naître.",
        "contexte": "Protection spéciale de la mère et de l'enfant pendant la grossesse et l'enfance précoce.",
        "sanctions": "Violences sur une femme enceinte : peines accrues",
        "attitude_recommandee": "Assurer les soins prénatals. Signaler toute violence envers la femme enceinte. Demander l'accouchement à l'hôpital.",
        "questions_clés": ["femme enceinte", "protection maternelle", "accouchement"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    }
]
female['enregistrements'].extend(new_female)

# ==================== DONNÉES ====================
donnees['metadata']['date_mise_a_jour'] = '2026-10-25'
donnees['metadata']['sources'] = [
    'Loi n2014-483 du 21 juillet 2014 relative à la protection des données personnelles',
    'Règlement (UE) 2016/679 (RGPD)',
    'Loi n2019-680 du 14 septembre 2019',
    "Code de l'enfant (Loi n2013-665 du 29 octobre 2013)"
]

new_donnees = [
    {
        "id": "dp-rgpd-005",
        "domaine": "donnees",
        "titre": "Données des victimes de violences : protection renforcée",
        "reference": "Loi n2014-483 du 21 juillet 2014 relative à la protection des données personnelles ; Loi n2021-894 du 22 décembre 2021 ; Règlement (UE) 2016/679 (RGPD)",
        "source": "Loi 2014-483, Loi 2021-894, RGPD",
        "niveau_vérité": "source_only",
        "contenu": "Les données des victimes de violences domestiques, de viol et de violences sexuelles sont des données à sensibilité spéciale et sont soumises à une protection renforcée. Le traitement de ces données doit respecter les principes de licéité, de minimisation et de confidentialité. Les victimes ont droit à l'information, à l'accès, à la rectification et à la suppression de leurs données.",
        "contexte": "Protection des données des victimes de violences (population vulnérable).",
        "sanctions": "Sanctions administratives et pénales pour non-respect du cadre légal",
        "attitude_recommandee": "Obtenir le consentement explicite de la victime. Restreindre l'accès aux données. Supprimer les données à la fin de la procédure.",
        "questions_clés": ["données", "protection", "violences", "confidentialité"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    },
    {
        "id": "dp-rgpd-006",
        "domaine": "donnees",
        "titre": "Conformité des services d'information juridique",
        "reference": "Loi n2014-483 du 21 juillet 2014 ; Règlement (UE) 2016/679 (RGPD), articles 5, 6, 17, 34",
        "source": "Loi 2014-483, RGPD",
        "niveau_vérité": "source_only",
        "contenu": "Les services d'information juridique (comme e-MFFE justicier) doivent respecter les principes de licéité et de minimisation lors du traitement des données des usagers. Le consentement explicite est requis avant le traitement de données personnelles. Les usagers ont droit à l'information, à l'accès, à la rectification et à la suppression de leurs données. Le service doit mettre en place une politique de confidentialité et un système de gestion des données.",
        "contexte": "Conformité des services d'information juridique en matière de données personnelles.",
        "sanctions": "Sanctions administratives et pénales pour non-respect du cadre légal",
        "attitude_recommandee": "Établir une politique de confidentialité, obtenir le consentement explicite, mettre en place un système de gestion des données, fournir les informations d'obtention des droits aux usagers.",
        "questions_clés": ["données", "protection", "confidentialité", "service"],
        "questions_non_repondues": [],
        "creation_date": "2026-10-25"
    }
]
donnees['enregistrements'].extend(new_donnees)

# Write back
json.dump(child, open(data_dir + '/loi_child.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(family, open(data_dir + '/loi_family.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(female, open(data_dir + '/loi_female.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(donnees, open(data_dir + '/loi_donnees.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print("Enrichissement terminé!")
print(f"Enfant: {len(child['enregistrements'])} records")
print(f"Famille: {len(family['enregistrements'])} records")
print(f"Femme: {len(female['enregistrements'])} records")
print(f"Données: {len(donnees['enregistrements'])} records")
