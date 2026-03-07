# 🤖 Khal - Générateur de Texte Personnel

## Structure du projet

```
khal/
├── generateur_texte.py   ← Fichier principal (ton IA)
└── memoire_ia.json       ← Créé automatiquement à l'exécution
```

---

## 🧩 Les 4 modules

| Module | Rôle |
|---|---|
| `ModeleMarkov` | Apprend les enchaînements de mots depuis un texte |
| `GenerateurContenu` | Crée du contenu structuré avec templates |
| `MemoireIA` | Sauvegarde l'historique et les stats |
| `Khal` | Assemble tout — c'est ton point d'entrée |

---

## 🚀 Démarrage rapide

```python
from generateur_texte import Khal

ia = Khal("Khal_v1")

# Entraîner avec ton propre texte
ia.apprendre("Ton texte ici. Plus il est long, mieux c'est !")

# Générer du texte libre
texte = ia.generer_texte_libre(longueur=50)
print(texte)

# Générer un article
article = ia.generer_article(sujet="Mon Sujet", paragraphes=4)
print(article)
```

---

## 🎨 Personnalisation

### Ajouter des mots au vocabulaire
```python
ia.personnaliser("adjectifs_positifs", ["incroyable", "sublime"])
ia.personnaliser("verbes_action", ["analyser", "optimiser"])
```

### Entraîner avec un fichier texte
```python
with open("mon_corpus.txt", "r", encoding="utf-8") as f:
    contenu = f.read()
ia.apprendre(contenu)
```

### Ajuster la précision Markov
```python
from generateur_texte import ModeleMarkov

# ordre=1 → plus créatif/aléatoire
# ordre=3 → plus fidèle au corpus
modele = ModeleMarkov(ordre=3)
```

---

## 📈 Prochaines étapes

- [ ] Connecter l'API OpenAI ou Anthropic pour plus de puissance
- [ ] Ajouter une interface web avec Flask
- [ ] Entraîner sur un vrai dataset (livres, articles...)
- [ ] Ajouter un système de scoring pour améliorer les résultats
- [ ] Implémenter un modèle de réseau de neurones simple (avec PyTorch)

---

## 📦 Dépendances

Aucune installation requise — uniquement la bibliothèque standard Python 3.x !

Pour aller plus loin :
```bash
pip install transformers torch  # Pour des modèles IA avancés
pip install flask               # Pour une interface web
```
