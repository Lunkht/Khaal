"""
██╗  ██╗██╗  ██╗ █████╗ ██╗
██║ ██╔╝██║  ██║██╔══██╗██║
█████╔╝ ███████║███████║██║
██╔═██╗ ██╔══██║██╔══██║██║
██║  ██╗██║  ██║██║  ██║███████╗
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
Khaal — Intelligence Artificielle Générale
"""

import json
import re
import random
import datetime
from typing import Optional


# ============================================================
# MODULE 1 : MÉMOIRE CONVERSATIONNELLE
# ============================================================

class MemoireConversation:
    """Gère le contexte et l'historique de la conversation."""

    def __init__(self, taille_max: int = 20):
        self.historique = []          # Liste des échanges
        self.taille_max = taille_max  # Nombre max de tours mémorisés
        self.contexte_global = {}     # Infos persistantes (nom user, préférences...)
        self.session_debut = datetime.datetime.now()

    def ajouter(self, role: str, contenu: str):
        """Ajoute un message à l'historique."""
        self.historique.append({
            "role": role,
            "contenu": contenu,
            "timestamp": datetime.datetime.now().isoformat()
        })
        # Garder seulement les N derniers échanges
        if len(self.historique) > self.taille_max * 2:
            self.historique = self.historique[-self.taille_max * 2:]

    def get_contexte_recent(self, n: int = 5) -> list:
        """Retourne les N derniers échanges."""
        return self.historique[-n*2:] if len(self.historique) >= n*2 else self.historique

    def memoriser_info(self, cle: str, valeur):
        """Mémorise une information sur l'utilisateur."""
        self.contexte_global[cle] = valeur

    def get_info(self, cle: str, defaut=None):
        """Récupère une information mémorisée."""
        return self.contexte_global.get(cle, defaut)

    def effacer(self):
        """Efface l'historique de la session."""
        self.historique = []
        self.session_debut = datetime.datetime.now()

    def duree_session(self) -> str:
        delta = datetime.datetime.now() - self.session_debut
        minutes = int(delta.total_seconds() / 60)
        return f"{minutes} min" if minutes > 0 else "< 1 min"

    def sauvegarder(self, fichier: str = "khaal_memoire.json"):
        data = {
            "historique": self.historique,
            "contexte_global": self.contexte_global,
        }
        with open(fichier, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def charger(self, fichier: str = "khaal_memoire.json"):
        try:
            with open(fichier, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.historique = data.get("historique", [])
            self.contexte_global = data.get("contexte_global", {})
        except FileNotFoundError:
            pass


# ============================================================
# MODULE 2 : MOTEUR DE RÉPONSE
# ============================================================

class MoteurReponse:
    """
    Moteur de réponse basé sur des règles et patterns.
    Peut être remplacé/augmenté par une vraie API LLM.
    """

    def __init__(self):
        self.regles = self._charger_regles()
        self.personnalite = {
            "nom": "Khaal",
            "ton": "intelligent, direct, légèrement mystérieux",
            "style": "concis mais profond"
        }

    def _charger_regles(self) -> list:
        """Définit les règles de réponse par patterns."""
        return [
            # Salutations
            {
                "patterns": ["bonjour", "salut", "hello", "hey", "bonsoir", "coucou"],
                "reponses": [
                    "Bonjour. Je suis Khaal. Comment puis-je vous être utile ?",
                    "Salut. Khaal à votre service. Que souhaitez-vous ?",
                    "Bonsoir. Je vous écoute.",
                ]
            },
            # Identité
            {
                "patterns": ["qui es-tu", "qui êtes-vous", "tu es quoi", "c'est quoi khaal", "présente-toi"],
                "reponses": [
                    "Je suis Khaal — une intelligence artificielle générale. Je peux répondre à vos questions, générer du contenu, analyser des textes et mémoriser notre conversation.",
                    "Khaal. Une IA conçue pour raisonner, générer et analyser. Posez-moi n'importe quelle question.",
                ]
            },
            # Capacités
            {
                "patterns": ["que sais-tu faire", "tes capacités", "qu'est-ce que tu peux", "tes fonctions"],
                "reponses": [
                    "Mes capacités principales :\n• **Répondre** à vos questions sur divers sujets\n• **Générer** du texte, articles, résumés\n• **Analyser** et résumer des textes\n• **Mémoriser** le contexte de notre conversation\n\nQue voulez-vous explorer ?",
                ]
            },
            # Au revoir
            {
                "patterns": ["au revoir", "bye", "à bientôt", "ciao", "bonne nuit", "bonne journée"],
                "reponses": [
                    "À bientôt. Notre conversation a été mémorisée.",
                    "Au revoir. N'hésitez pas à revenir.",
                    "Bonne continuation. Je serai là si besoin.",
                ]
            },
            # Merci
            {
                "patterns": ["merci", "thanks", "parfait", "super", "excellent", "génial"],
                "reponses": [
                    "Avec plaisir.",
                    "C'est ce pour quoi je suis là.",
                    "Toujours disponible.",
                ]
            },
            # Questions sur la météo (exemple de question contextuelle)
            {
                "patterns": ["météo", "temps qu'il fait", "il pleut", "température"],
                "reponses": [
                    "Je n'ai pas accès aux données météo en temps réel. Pour cela, consultez météo.fr ou Google Météo.",
                ]
            },
            # Heure / Date
            {
                "patterns": ["quelle heure", "quel jour", "quelle date", "on est le"],
                "reponses": ["__DATETIME__"]
            },
            # Blague
            {
                "patterns": ["blague", "raconte une blague", "fais-moi rire", "humour"],
                "reponses": [
                    "Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon ils tomberaient dans le bateau.",
                    "Un électron entre dans un bar. Le barman demande : 'Qu'est-ce que vous prenez ?' L'électron répond : 'Je ne sais pas encore, ça dépend de l'observation.'",
                    "C'est l'histoire d'un algorithme qui entre dans un bar. Il commande une bière, puis une bière, puis une bière... jusqu'à ce que le bar soit vide.",
                ]
            },
            # Génération de texte
            {
                "patterns": ["génère", "écris", "rédige", "crée un texte", "écris-moi"],
                "reponses": ["__GENERER__"]
            },
            # Résumé / Analyse
            {
                "patterns": ["résume", "analyse", "explique", "c'est quoi", "définition de", "qu'est-ce que"],
                "reponses": ["__ANALYSER__"]
            },
        ]

    def trouver_regle(self, message: str) -> Optional[dict]:
        """Trouve la règle correspondant au message."""
        message_lower = message.lower()
        for regle in self.regles:
            for pattern in regle["patterns"]:
                if pattern in message_lower:
                    return regle
        return None

    def generer_reponse_intelligente(self, message: str, memoire: MemoireConversation) -> str:
        """Génère une réponse contextuelle basée sur le message et la mémoire."""

        # Détecter le prénom de l'utilisateur
        match_prenom = re.search(r"je m'appelle (\w+)|mon nom est (\w+)|je suis (\w+)", message.lower())
        if match_prenom:
            prenom = next(g for g in match_prenom.groups() if g)
            prenom = prenom.capitalize()
            memoire.memoriser_info("prenom", prenom)
            return f"Bien, {prenom}. Je m'en souviendrai. Comment puis-je vous aider ?"

        regle = self.trouver_regle(message)

        if regle:
            reponse = random.choice(regle["reponses"])

            # Traitement spécial pour certaines réponses
            if reponse == "__DATETIME__":
                now = datetime.datetime.now()
                reponse = f"Nous sommes le **{now.strftime('%A %d %B %Y')}** à **{now.strftime('%H:%M')}**."

            elif reponse == "__GENERER__":
                reponse = self._generer_contenu(message)

            elif reponse == "__ANALYSER__":
                reponse = self._analyser_contenu(message)

        else:
            reponse = self._reponse_generique(message, memoire)

        # Personnaliser avec le prénom si connu
        prenom = memoire.get_info("prenom")
        if prenom and random.random() < 0.2:  # 20% de chance d'utiliser le prénom
            reponse = f"{prenom}, " + reponse[0].lower() + reponse[1:]

        return reponse

    def _generer_contenu(self, message: str) -> str:
        """Génère du contenu selon la demande."""
        sujets_detectes = re.findall(r"sur ([\w\s]+)|à propos de ([\w\s]+)|un texte ([\w\s]+)", message.lower())
        sujet = "un sujet général"
        if sujets_detectes:
            sujet = next((g for groupe in sujets_detectes for g in groupe if g), sujet).strip()

        templates = [
            f"**{sujet.title()}**\n\nC'est un domaine fascinant qui mérite qu'on s'y attarde. Les fondements théoriques s'articulent autour de concepts clés qui évoluent constamment. Les praticiens du domaine s'accordent sur l'importance d'une approche rigoureuse et méthodique.\n\nEn définitive, explorer {sujet} ouvre des perspectives nouvelles et enrichit notre compréhension du monde.",
            f"Voici un texte sur **{sujet}** :\n\nLa question de {sujet} est au cœur des réflexions contemporaines. Entre tradition et innovation, ce sujet nous invite à repenser nos certitudes. Les experts divergent sur les méthodes, mais convergent sur les objectifs fondamentaux.\n\nL'avenir de {sujet} dépendra de notre capacité collective à innover avec intelligence.",
        ]
        return random.choice(templates)

    def _analyser_contenu(self, message: str) -> str:
        """Analyse ou explique un concept."""
        # Extraction du concept à expliquer
        match = re.search(r"(?:c'est quoi|qu'est-ce que|définition de|explique|résume)\s+(?:le |la |les |l'|un |une )?([\w\s'-]+)", message.lower())
        concept = match.group(1).strip() if match else "ce concept"

        return (
            f"**{concept.title()}** est un terme/concept qui mérite une analyse structurée.\n\n"
            f"Pour vous donner une réponse précise, je vous recommande de me fournir plus de contexte "
            f"ou un texte à analyser. Je pourrai alors :\n"
            f"• Identifier les idées principales\n"
            f"• Dégager la structure logique\n"
            f"• Proposer un résumé concis\n\n"
            f"Partagez-moi un texte et j'analyserai pour vous."
        )

    def _reponse_generique(self, message: str, memoire: MemoireConversation) -> str:
        """Réponse de fallback intelligente."""
        # Analyser le type de question
        if "?" in message:
            if any(w in message.lower() for w in ["comment", "pourquoi", "quand", "où", "combien"]):
                return (
                    f"C'est une question pertinente. Pour y répondre précisément, "
                    f"j'aurais besoin de plus de contexte. Pouvez-vous développer votre question ?"
                )
            return (
                "Je traite votre question. Pour une réponse optimale, "
                "pourriez-vous reformuler ou donner plus de détails ?"
            )

        # Si c'est une affirmation
        historique = memoire.get_contexte_recent(3)
        if historique:
            return (
                "Je comprends. Souhaitez-vous que j'approfondisse ce point, "
                "que je génère du contenu à ce sujet, ou autre chose ?"
            )

        return (
            "Intéressant. Je suis Khaal — posez-moi une question, "
            "demandez-moi de générer ou d'analyser du contenu."
        )

    def analyser_sentiment(self, message: str) -> str:
        """Détecte le ton émotionnel du message."""
        positifs = ["super", "génial", "excellent", "parfait", "merci", "bravo", "bien", "cool"]
        negatifs = ["nul", "mauvais", "terrible", "horrible", "déçu", "frustré", "problème", "erreur"]

        msg_lower = message.lower()
        score_pos = sum(1 for m in positifs if m in msg_lower)
        score_neg = sum(1 for m in negatifs if m in msg_lower)

        if score_pos > score_neg:
            return "positif"
        elif score_neg > score_pos:
            return "negatif"
        return "neutre"

    def compter_mots(self, texte: str) -> dict:
        """Analyse basique d'un texte."""
        mots = texte.split()
        phrases = texte.split(".")
        return {
            "mots": len(mots),
            "phrases": len([p for p in phrases if p.strip()]),
            "caracteres": len(texte),
            "mots_uniques": len(set(m.lower() for m in mots)),
        }


# ============================================================
# MODULE 3 : KHAAL — L'IA PRINCIPALE
# ============================================================

class Khaal:
    """
    Khaal — Intelligence Artificielle Générale
    Point d'entrée principal du système.
    """

    VERSION = "1.0.0"

    def __init__(self):
        self.memoire = MemoireConversation(taille_max=50)
        self.moteur = MoteurReponse()
        self.actif = True
        self.stats = {
            "messages_recus": 0,
            "messages_envoyes": 0,
            "session_debut": datetime.datetime.now().isoformat()
        }
        # Charger la mémoire précédente si elle existe
        self.memoire.charger()

    def repondre(self, message: str) -> dict:
        """
        Traite un message et retourne une réponse complète.
        Retourne un dict avec la réponse et des métadonnées.
        """
        if not message.strip():
            return {"reponse": "...", "sentiment": "neutre", "type": "vide"}

        # Enregistrer le message utilisateur
        self.memoire.ajouter("user", message)
        self.stats["messages_recus"] += 1

        # Analyser le sentiment
        sentiment = self.moteur.analyser_sentiment(message)

        # Commandes spéciales
        if message.lower().strip() in ["clear", "effacer", "reset", "/reset"]:
            self.memoire.effacer()
            reponse = "Mémoire effacée. Nouvelle session démarrée."
            type_reponse = "systeme"

        elif message.lower().strip() in ["stats", "/stats", "statistiques"]:
            reponse = self._get_stats()
            type_reponse = "stats"

        elif message.lower().startswith("analyse:") or message.lower().startswith("analyse :"):
            texte = message[8:].strip()
            stats_texte = self.moteur.compter_mots(texte)
            reponse = (
                f"**Analyse du texte :**\n\n"
                f"• Mots total : **{stats_texte['mots']}**\n"
                f"• Mots uniques : **{stats_texte['mots_uniques']}**\n"
                f"• Phrases : **{stats_texte['phrases']}**\n"
                f"• Caractères : **{stats_texte['caracteres']}**\n"
                f"• Richesse lexicale : **{stats_texte['mots_uniques']/max(stats_texte['mots'],1)*100:.1f}%**"
            )
            type_reponse = "analyse"

        else:
            reponse = self.moteur.generer_reponse_intelligente(message, self.memoire)
            type_reponse = "conversation"

        # Enregistrer la réponse
        self.memoire.ajouter("khaal", reponse)
        self.stats["messages_envoyes"] += 1

        # Sauvegarder périodiquement
        if self.stats["messages_envoyes"] % 5 == 0:
            self.memoire.sauvegarder()

        return {
            "reponse": reponse,
            "sentiment": sentiment,
            "type": type_reponse,
            "tour": self.stats["messages_recus"]
        }

    def _get_stats(self) -> str:
        return (
            f"**Statistiques de session :**\n\n"
            f"• Messages reçus : **{self.stats['messages_recus']}**\n"
            f"• Réponses générées : **{self.stats['messages_envoyes']}**\n"
            f"• Durée session : **{self.memoire.duree_session()}**\n"
            f"• Échanges mémorisés : **{len(self.memoire.historique)}**\n"
            f"• Version Khaal : **{self.VERSION}**"
        )

    def get_historique(self) -> list:
        """Retourne l'historique formaté pour l'interface."""
        return self.memoire.historique
