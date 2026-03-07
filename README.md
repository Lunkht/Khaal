# 🤖 KHAL — Intelligence Artificielle Générale

## Structure du projet

```
khal/
├── app.py              ← Serveur Flask (point d'entrée)
├── khal_core.py        ← Cerveau de Khal (modules IA)
├── requirements.txt    ← Dépendances Python
├── khal_memoire.json   ← Créé automatiquement (mémoire persistante)
└── templates/
    └── index.html      ← Interface web
```

---

## 🚀 Lancement en local

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer Khal
python app.py

# 3. Ouvrir dans le navigateur
# → http://localhost:5000
```

---

## ☁️ Hébergement gratuit

### Replit (le plus simple)
1. Va sur https://replit.com
2. Crée un projet Python
3. Upload les fichiers
4. Lance avec `python app.py`

### PythonAnywhere
1. Va sur https://pythonanywhere.com
2. Upload les fichiers dans `/home/user/khal/`
3. Configure une Web App Flask
4. WSGI file : `from app import app as application`

---

## 🧩 Capacités de Khal

| Capacité | Commande |
|---|---|
| Conversation générale | Écrire naturellement |
| Génération de texte | "Génère un texte sur..." |
| Analyse de texte | "analyse: [ton texte ici]" |
| Statistiques session | Taper `stats` |
| Réinitialiser | Bouton RESET ou taper `reset` |
| Export conversation | Bouton EXPORT |

---

## 📈 Prochaines évolutions

- [ ] Connecter l'API Anthropic/OpenAI pour une vraie IA
- [ ] Ajouter un système d'authentification
- [ ] Base de données pour la mémoire long terme
- [ ] Mode multi-utilisateurs
- [ ] Synthèse vocale (text-to-speech)
