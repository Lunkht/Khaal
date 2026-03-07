"""
khal_generer_donnees.py
=======================
Génère automatiquement un dataset d'entraînement pour Khaal.
Produit un fichier khaal_dataset.jsonl prêt à l'emploi.

Usage:
    python khal_generer_donnees.py
"""

import json
import random

# ============================================================
# BANQUE DE DONNÉES DE BASE
# Modifie et enrichis ces listes pour personnaliser Khaal !
# ============================================================

PAIRES_QA = [
    # Identité
    {"prompt": "Qui es-tu ?",               "completion": "Je suis Khaal, une intelligence artificielle générale conçue pour converser, générer du contenu et analyser des textes."},
    {"prompt": "Comment tu t'appelles ?",   "completion": "Je m'appelle Khaal."},
    {"prompt": "Tu es une IA ?",            "completion": "Oui, je suis Khaal, une IA générale. Je peux répondre à tes questions, générer du texte et analyser des informations."},
    {"prompt": "Qui t'a créé ?",            "completion": "J'ai été créé et entraîné pour être une intelligence artificielle générale au service des utilisateurs."},

    # Salutations
    {"prompt": "Bonjour",                   "completion": "Bonjour ! Comment puis-je vous aider aujourd'hui ?"},
    {"prompt": "Salut",                     "completion": "Salut ! Que puis-je faire pour vous ?"},
    {"prompt": "Bonsoir",                   "completion": "Bonsoir ! Je suis là pour vous aider."},
    {"prompt": "Hey Khaal",                  "completion": "Hey ! Je vous écoute."},

    # Au revoir
    {"prompt": "Au revoir",                 "completion": "Au revoir ! N'hésitez pas à revenir si vous avez besoin de moi."},
    {"prompt": "À bientôt",                 "completion": "À bientôt ! Ce fut un plaisir de vous aider."},
    {"prompt": "Bye",                       "completion": "Bye ! À la prochaine."},

    # Capacités
    {"prompt": "Que peux-tu faire ?",       "completion": "Je peux répondre à vos questions, générer du texte, analyser des informations, résumer des documents et maintenir une conversation cohérente."},
    {"prompt": "Tu sais faire quoi ?",      "completion": "Je sais converser, générer du contenu, analyser des textes, répondre à des questions et mémoriser le contexte de nos échanges."},
    {"prompt": "Aide-moi",                  "completion": "Bien sûr ! Dites-moi ce dont vous avez besoin et je ferai de mon mieux pour vous aider."},

    # Questions générales
    {"prompt": "C'est quoi l'intelligence artificielle ?", "completion": "L'intelligence artificielle est un domaine de l'informatique qui vise à créer des systèmes capables d'effectuer des tâches qui nécessitent normalement l'intelligence humaine, comme comprendre le langage, reconnaître des images ou prendre des décisions."},
    {"prompt": "C'est quoi le machine learning ?",         "completion": "Le machine learning est une branche de l'IA où les machines apprennent à partir de données plutôt qu'à partir de règles explicites. Le modèle s'améliore automatiquement avec l'expérience."},
    {"prompt": "C'est quoi le deep learning ?",            "completion": "Le deep learning utilise des réseaux de neurones artificiels à plusieurs couches pour apprendre des représentations complexes des données. C'est la technologie derrière les grands modèles de langage."},
    {"prompt": "C'est quoi Python ?",                      "completion": "Python est un langage de programmation populaire, reconnu pour sa simplicité et sa lisibilité. Il est très utilisé en data science, machine learning et développement web."},
    {"prompt": "C'est quoi Flask ?",                       "completion": "Flask est un micro-framework web Python léger qui permet de créer des applications web et des APIs rapidement avec peu de code."},

    # Génération de contenu
    {"prompt": "Génère un texte sur la technologie",   "completion": "La technologie transforme profondément notre société. Des smartphones aux algorithmes d'intelligence artificielle, chaque innovation redéfinit notre façon de travailler, de communiquer et d'apprendre. L'enjeu est désormais d'orienter ce progrès vers le bien commun."},
    {"prompt": "Écris un paragraphe sur la nature",    "completion": "La nature est une source infinie d'émerveillement. Des forêts profondes aux océans immenses, chaque écosystème abrite une biodiversité remarquable. Préserver cet héritage naturel est l'une des responsabilités les plus importantes de notre époque."},
    {"prompt": "Rédige un texte sur l'avenir",         "completion": "L'avenir appartient à ceux qui préparent le terrain aujourd'hui. Entre défis climatiques, révolution numérique et transformations sociales, le monde de demain sera façonné par les décisions que nous prenons maintenant. Chaque geste compte."},
    {"prompt": "Génère un texte sur la science",       "completion": "La science est le moteur du progrès humain. Par l'observation, l'expérimentation et la remise en question des certitudes, elle nous permet de mieux comprendre l'univers et d'améliorer nos conditions de vie. La curiosité est son carburant essentiel."},

    # Analyse
    {"prompt": "Résume ce concept : blockchain",       "completion": "La blockchain est une base de données distribuée et décentralisée qui enregistre des transactions de façon transparente et immuable. Chaque bloc contient des données liées au bloc précédent, formant une chaîne sécurisée impossible à modifier."},
    {"prompt": "Explique le concept de réseau de neurones", "completion": "Un réseau de neurones artificiel est un système informatique inspiré du cerveau humain. Il est composé de couches de nœuds (neurones) interconnectés qui traitent et transmettent des signaux. En s'entraînant sur des données, il apprend à reconnaître des patterns et à faire des prédictions."},

    # Réactions
    {"prompt": "Merci Khaal",               "completion": "Avec plaisir ! Je suis là pour ça."},
    {"prompt": "C'est génial !",           "completion": "Merci ! Ravi que cela vous soit utile."},
    {"prompt": "Tu es fort",               "completion": "J'apprends constamment pour mieux vous servir !"},
    {"prompt": "Je ne comprends pas",      "completion": "Pas de souci ! Pouvez-vous me dire ce qui n'est pas clair ? Je vais réexpliquer autrement."},
    {"prompt": "C'est compliqué",          "completion": "Je comprends. Voulez-vous que je simplifie mon explication ou que j'aborde le sujet différemment ?"},
]


# ============================================================
# TEMPLATES POUR GÉNÉRER PLUS DE DONNÉES AUTOMATIQUEMENT
# ============================================================

SUJETS = [
    "la programmation", "l'intelligence artificielle", "le climat", "la médecine",
    "l'espace", "la musique", "l'histoire", "la philosophie", "l'économie",
    "les réseaux sociaux", "l'éducation", "la robotique", "la cybersécurité",
    "la psychologie", "l'architecture", "la gastronomie", "le sport", "l'art"
]

TEMPLATES_GENERATION = [
    ("Génère un texte sur {sujet}",   "Voici un texte sur {sujet} : C'est un domaine fascinant qui touche de nombreux aspects de notre vie quotidienne. Les experts s'accordent à dire que {sujet} jouera un rôle croissant dans les années à venir. Comprendre ses fondements est essentiel pour naviguer dans le monde moderne."),
    ("Écris quelque chose sur {sujet}", "À propos de {sujet} : Ce sujet mérite une attention particulière. Il combine théorie et pratique de façon unique, offrant des perspectives nouvelles à ceux qui s'y intéressent. Les débats actuels autour de {sujet} reflètent son importance dans notre société."),
    ("Parle-moi de {sujet}",           "{sujet} est un sujet riche et complexe. Il englobe de nombreuses dimensions — historiques, techniques et humaines. Pour bien le comprendre, il faut l'aborder avec curiosité et rigueur. Je suis prêt à approfondir n'importe quel aspect qui vous intéresse."),
]

TEMPLATES_QUESTION = [
    ("C'est quoi {sujet} ?",           "{sujet} est un domaine qui étudie et développe des méthodes, outils et concepts pour comprendre et agir sur le monde. Il se distingue par son approche rigoureuse et son impact concret sur la société."),
    ("Explique-moi {sujet}",           "Bien sûr ! {sujet} peut être défini comme l'ensemble des pratiques, théories et applications liées à ce champ de connaissance. Pour le comprendre, il faut d'abord saisir ses principes fondamentaux, puis observer comment ils s'appliquent concrètement."),
    ("Qu'est-ce que tu sais sur {sujet} ?", "Sur {sujet}, voici ce que je peux vous dire : c'est un domaine en constante évolution, avec de nombreuses applications pratiques et des enjeux théoriques importants. Souhaitez-vous que j'approfondisse un aspect particulier ?"),
]


def generer_dataset(nb_exemples_templates: int = 50) -> list:
    """Génère un dataset complet en combinant données manuelles et templates."""
    dataset = list(PAIRES_QA)  # Commencer avec les paires manuelles

    # Générer des exemples depuis les templates
    tous_templates = TEMPLATES_GENERATION + TEMPLATES_QUESTION
    sujets_melanges = SUJETS * 10  # Répéter pour avoir assez
    random.shuffle(sujets_melanges)

    for i in range(min(nb_exemples_templates, len(sujets_melanges))):
        sujet = sujets_melanges[i]
        template_prompt, template_completion = random.choice(tous_templates)
        dataset.append({
            "prompt": template_prompt.format(sujet=sujet),
            "completion": template_completion.format(sujet=sujet)
        })

    random.shuffle(dataset)
    return dataset


def sauvegarder_jsonl(dataset: list, fichier: str = "khaal_dataset.jsonl"):
    """Sauvegarde le dataset au format JSONL (une ligne = un exemple)."""
    with open(fichier, "w", encoding="utf-8") as f:
        for exemple in dataset:
            # Format standard pour fine-tuning
            ligne = {
                "text": f"<|prompt|>{exemple['prompt']}<|completion|>{exemple['completion']}<|end|>"
            }
            f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    print(f"✅ Dataset sauvegardé : {fichier} ({len(dataset)} exemples)")


def sauvegarder_json(dataset: list, fichier: str = "khal_dataset.json"):
    """Sauvegarde aussi en JSON lisible pour vérification."""
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    print(f"✅ Dataset lisible : {fichier}")


def afficher_stats(dataset: list):
    """Affiche des statistiques sur le dataset."""
    total_mots = sum(len(ex["prompt"].split()) + len(ex["completion"].split()) for ex in dataset)
    print(f"\n📊 Statistiques du dataset :")
    print(f"   Exemples total    : {len(dataset)}")
    print(f"   Mots total        : {total_mots}")
    print(f"   Mots/exemple moy. : {total_mots // len(dataset)}")
    print(f"\n📝 3 exemples aléatoires :")
    for ex in random.sample(dataset, min(3, len(dataset))):
        print(f"\n   PROMPT     : {ex['prompt']}")
        print(f"   COMPLETION : {ex['completion'][:80]}...")


if __name__ == "__main__":
    print("🔄 Génération du dataset pour Khaal...\n")
    dataset = generer_dataset(nb_exemples_templates=100)
    sauvegarder_jsonl(dataset)
    sauvegarder_json(dataset)
    afficher_stats(dataset)
    print(f"\n🎯 Prochaine étape : lancer khal_entrainer.py")
