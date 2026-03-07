"""
🤖 Générateur de Texte / Contenu - Base IA
==========================================
Une IA modulaire capable de générer différents types de contenu
en utilisant des modèles de langage et des règles personnalisées.
"""

import random
import json
import re
from typing import Optional


# ============================================================
# MODULE 1 : CERVEAU DE L'IA - Modèle de Markov simple
# ============================================================

class ModeleMarkov:
    """
    Génère du texte en apprenant les enchaînements de mots
    à partir d'un corpus d'entraînement.
    """

    def __init__(self, ordre: int = 2):
        self.ordre = ordre  # Nombre de mots utilisés comme contexte
        self.chaines = {}   # Dictionnaire des transitions

    def entrainer(self, texte: str):
        """Apprend les patterns depuis un texte d'entraînement."""
        mots = texte.lower().split()
        print(f"  → Entraînement sur {len(mots)} mots...")

        for i in range(len(mots) - self.ordre):
            cle = tuple(mots[i:i + self.ordre])
            suivant = mots[i + self.ordre]

            if cle not in self.chaines:
                self.chaines[cle] = []
            self.chaines[cle].append(suivant)

        print(f"  → {len(self.chaines)} patterns appris ✓")

    def generer(self, longueur: int = 50, debut: Optional[str] = None) -> str:
        """Génère un texte de la longueur souhaitée."""
        if not self.chaines:
            return "❌ Modèle non entraîné. Appelez d'abord entrainer()."

        # Choisir un point de départ
        if debut:
            mots_debut = debut.lower().split()
            cle_actuelle = tuple(mots_debut[-self.ordre:])
            if cle_actuelle not in self.chaines:
                cle_actuelle = random.choice(list(self.chaines.keys()))
        else:
            cle_actuelle = random.choice(list(self.chaines.keys()))

        resultat = list(cle_actuelle)

        for _ in range(longueur):
            if cle_actuelle in self.chaines:
                prochain = random.choice(self.chaines[cle_actuelle])
                resultat.append(prochain)
                cle_actuelle = tuple(resultat[-self.ordre:])
            else:
                break

        texte = " ".join(resultat)
        # Capitaliser la première lettre
        return texte[0].upper() + texte[1:] if texte else ""


# ============================================================
# MODULE 2 : GÉNÉRATEUR DE CONTENU STRUCTURÉ
# ============================================================

class GenerateurContenu:
    """
    Génère du contenu structuré (articles, histoires, descriptions)
    en utilisant des templates et des banques de mots.
    """

    def __init__(self):
        # Banques de mots par catégorie
        self.banques = {
            "adjectifs_positifs": [
                "magnifique", "extraordinaire", "brillant", "fascinant",
                "innovant", "puissant", "élégant", "remarquable"
            ],
            "adjectifs_negatifs": [
                "complexe", "difficile", "mystérieux", "obscur",
                "incertain", "controversé", "ambigu", "redoutable"
            ],
            "verbes_action": [
                "transformer", "révolutionner", "créer", "développer",
                "explorer", "découvrir", "construire", "imaginer"
            ],
            "domaines": [
                "technologie", "science", "art", "musique",
                "littérature", "nature", "philosophie", "histoire"
            ]
        }

        # Templates de phrases
        self.templates = {
            "introduction": [
                "Dans le monde de {domaine}, il existe quelque chose de {adj_pos}.",
                "La {domaine} est une discipline {adj_pos} qui nous invite à {verbe}.",
                "Chaque jour, des esprits {adj_pos} cherchent à {verbe} la {domaine}.",
            ],
            "developpement": [
                "Pour {verbe} dans ce domaine {adj_pos}, il faut comprendre ses aspects {adj_neg}.",
                "Les experts {adj_pos} s'accordent à dire qu'il faut {verbe} avec méthode.",
                "Cette approche {adj_pos} nous permet de {verbe} de façon structurée.",
            ],
            "conclusion": [
                "En conclusion, la {domaine} reste un domaine {adj_pos} à {verbe}.",
                "L'avenir de la {domaine} dépend de notre capacité à {verbe} ensemble.",
                "Ainsi, {verbe} devient une nécessité dans notre monde {adj_pos}.",
            ]
        }

    def _remplir_template(self, template: str) -> str:
        """Remplace les variables d'un template par des mots aléatoires."""
        substitutions = {
            "{adj_pos}": random.choice(self.banques["adjectifs_positifs"]),
            "{adj_neg}": random.choice(self.banques["adjectifs_negatifs"]),
            "{verbe}": random.choice(self.banques["verbes_action"]),
            "{domaine}": random.choice(self.banques["domaines"]),
        }
        for cle, valeur in substitutions.items():
            template = template.replace(cle, valeur)
        return template

    def generer_article(self, sujet: str = "", nb_paragraphes: int = 3) -> str:
        """Génère un article structuré avec introduction, développement et conclusion."""
        parties = ["introduction"] + ["developpement"] * (nb_paragraphes - 2) + ["conclusion"]
        article = []

        if sujet:
            article.append(f"# {sujet.title()}\n")

        for partie in parties:
            templates_partie = self.templates.get(partie, self.templates["developpement"])
            phrase = self._remplir_template(random.choice(templates_partie))
            article.append(phrase)

        return "\n\n".join(article)

    def ajouter_mots(self, categorie: str, mots: list):
        """Ajoute des mots personnalisés à une catégorie."""
        if categorie not in self.banques:
            self.banques[categorie] = []
        self.banques[categorie].extend(mots)
        print(f"  → {len(mots)} mots ajoutés à '{categorie}' ✓")

    def ajouter_template(self, type_section: str, template: str):
        """Ajoute un nouveau template de phrase."""
        if type_section not in self.templates:
            self.templates[type_section] = []
        self.templates[type_section].append(template)
        print(f"  → Template ajouté à '{type_section}' ✓")


# ============================================================
# MODULE 3 : MÉMOIRE ET CONTEXTE
# ============================================================

class MemoireIA:
    """
    Gère la mémoire de l'IA : historique des générations,
    préférences apprises, et sauvegarde/chargement.
    """

    def __init__(self, fichier: str = "memoire_ia.json"):
        self.fichier = fichier
        self.historique = []
        self.preferences = {}
        self.stats = {"total_genere": 0, "mots_generes": 0}

    def enregistrer(self, type_contenu: str, contenu: str, note: int = 0):
        """Enregistre une génération dans l'historique."""
        entree = {
            "type": type_contenu,
            "contenu": contenu,
            "note": note,
            "longueur": len(contenu.split())
        }
        self.historique.append(entree)
        self.stats["total_genere"] += 1
        self.stats["mots_generes"] += entree["longueur"]

    def sauvegarder(self):
        """Sauvegarde la mémoire dans un fichier JSON."""
        data = {
            "historique": self.historique,
            "preferences": self.preferences,
            "stats": self.stats
        }
        with open(self.fichier, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  → Mémoire sauvegardée dans '{self.fichier}' ✓")

    def charger(self):
        """Charge la mémoire depuis un fichier JSON."""
        try:
            with open(self.fichier, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.historique = data.get("historique", [])
            self.preferences = data.get("preferences", {})
            self.stats = data.get("stats", self.stats)
            print(f"  → Mémoire chargée : {len(self.historique)} entrées ✓")
        except FileNotFoundError:
            print("  → Aucune mémoire précédente trouvée, démarrage vierge.")

    def afficher_stats(self):
        """Affiche les statistiques de génération."""
        print("\n📊 Statistiques :")
        print(f"   Générations totales : {self.stats['total_genere']}")
        print(f"   Mots générés        : {self.stats['mots_generes']}")
        if self.historique:
            notes = [e["note"] for e in self.historique if e["note"] > 0]
            if notes:
                print(f"   Note moyenne        : {sum(notes)/len(notes):.1f}/5")


# ============================================================
# MODULE 4 : INTERFACE PRINCIPALE - L'IA Assemblée
# ============================================================

class Khal:
    """
    L'IA principale qui assemble tous les modules.
    C'est le point d'entrée de ton générateur de texte.
    """

    def __init__(self, nom: str = "Khal"):
        self.nom = nom
        self.markov = ModeleMarkov(ordre=2)
        self.generateur = GenerateurContenu()
        self.memoire = MemoireIA()
        print(f"\n🤖 {self.nom} initialisé avec succès !")
        print("=" * 50)

    def apprendre(self, texte: str):
        """Entraîne le modèle Markov sur un texte."""
        print(f"\n📚 Apprentissage en cours...")
        self.markov.entrainer(texte)

    def generer_texte_libre(self, longueur: int = 40, debut: str = "") -> str:
        """Génère du texte libre basé sur l'apprentissage Markov."""
        print(f"\n✍️  Génération de texte libre ({longueur} mots)...")
        texte = self.markov.generer(longueur, debut if debut else None)
        self.memoire.enregistrer("markov", texte)
        return texte

    def generer_article(self, sujet: str = "", paragraphes: int = 3) -> str:
        """Génère un article structuré."""
        print(f"\n📄 Génération d'article{' sur : ' + sujet if sujet else ''}...")
        article = self.generateur.generer_article(sujet, paragraphes)
        self.memoire.enregistrer("article", article)
        return article

    def personnaliser(self, categorie: str, mots: list):
        """Ajoute des mots personnalisés au vocabulaire."""
        print(f"\n🎨 Personnalisation du vocabulaire...")
        self.generateur.ajouter_mots(categorie, mots)

    def sauvegarder(self):
        """Sauvegarde l'état de l'IA."""
        print(f"\n💾 Sauvegarde...")
        self.memoire.sauvegarder()

    def stats(self):
        """Affiche les statistiques."""
        self.memoire.afficher_stats()


# ============================================================
# DÉMONSTRATION - Lance ce fichier pour tester ton IA !
# ============================================================

if __name__ == "__main__":

    # 1. Créer ton IA
    ia = Khal("Khal_v1")

    # 2. Lui apprendre un texte (corpus d'entraînement)
    corpus = """
    L'intelligence artificielle est une technologie fascinante qui transforme notre monde.
    Les machines apprennent à partir des données pour résoudre des problèmes complexes.
    La programmation permet de créer des systèmes intelligents capables d'analyser et de générer du texte.
    Les algorithmes de traitement du langage naturel analysent les structures linguistiques.
    Le deep learning utilise des réseaux de neurones pour apprendre des représentations complexes.
    Les modèles de langage génèrent du texte cohérent grâce à des milliards de paramètres.
    L'intelligence artificielle révolutionne les domaines de la médecine, de l'éducation et de l'art.
    Les chercheurs développent de nouvelles architectures pour améliorer les capacités des modèles.
    """

    ia.apprendre(corpus)

    # 3. Personnaliser le vocabulaire
    ia.personnaliser("adjectifs_positifs", ["révolutionnaire", "avant-gardiste", "prometteur"])

    print("\n" + "="*50)
    print("🎯 RÉSULTATS DE GÉNÉRATION")
    print("="*50)

    # 4. Générer du texte libre
    texte = ia.generer_texte_libre(longueur=30, debut="L'intelligence artificielle")
    print(f"\n📝 Texte libre :\n{texte}")

    # 5. Générer un article
    article = ia.generer_article(sujet="Intelligence Artificielle", paragraphes=3)
    print(f"\n📰 Article généré :\n{article}")

    # 6. Afficher les stats
    ia.stats()

    # 7. Sauvegarder
    ia.sauvegarder()

    print("\n✅ Démonstration terminée ! Modifie ce fichier pour personnaliser ton IA.")
