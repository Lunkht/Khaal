# 🧠 Guide : Entraîner Khaal avec du vrai Machine Learning

## Vue d'ensemble

```
DONNÉES  →  TOKENISATION  →  MODÈLE GPT-2  →  ENTRAÎNEMENT  →  KHAAL ML
```

Khaal utilise **GPT-2** (le précurseur de ChatGPT), un vrai modèle de génération
de texte de 117 millions de paramètres, via HuggingFace Transformers.

---

## 📁 Fichiers du projet

| Fichier | Rôle |
|---|---|
| `khal_generer_donnees.py` | Génère le dataset d'entraînement |
| `khal_entrainer.py` | Lance l'entraînement ML |
| `Khaal_Entrainement.ipynb` | Notebook Google Colab (recommandé) |
| `khaal_dataset.jsonl` | Dataset généré (créé automatiquement) |
| `khal_modele_entraine/` | Modèle entraîné (créé automatiquement) |

---

## 🚀 Option 1 : Google Colab (RECOMMANDÉ — GPU gratuit)

**Pourquoi Colab ?** L'entraînement ML nécessite un GPU.
Colab t'en donne un gratuitement.

### Étapes

1. Va sur **https://colab.research.google.com**
2. Upload `Khaal_Entrainement.ipynb`
3. Active le GPU : `Exécution > Modifier le type d'exécution > GPU T4`
4. Exécute les cellules une par une
5. Télécharge le modèle entraîné à la fin

**Durée estimée :** 10-20 minutes pour 3 epochs sur GPU Colab gratuit.

---

## 💻 Option 2 : En local

```bash
# 1. Installer les dépendances
pip install torch transformers datasets accelerate

# 2. Générer le dataset
python khal_generer_donnees.py

# 3. Entraîner (avec options)
python khal_entrainer.py --epochs 3 --batch 2

# 4. Tester uniquement (après entraînement)
python khal_entrainer.py --test-seulement
```

> ⚠️ Sans GPU, l'entraînement peut prendre plusieurs heures sur CPU.

---

## 🎨 Personnaliser les données d'entraînement

Le plus important pour avoir une bonne IA : **la qualité des données**.

### Ajouter tes propres exemples dans `khal_generer_donnees.py`

```python
PAIRES_QA = [
    # Ajoute tes paires personnalisées ici !
    {
        "prompt": "Ta question ou phrase d'entrée",
        "completion": "La réponse que tu veux que Khaal donne"
    },
    {
        "prompt": "Khaal, parle-moi de mon entreprise",
        "completion": "Votre entreprise est spécialisée dans..."
    },
    # ... ajoute autant d'exemples que possible
]
```

### Règle d'or
- **+ d'exemples = meilleur modèle**
- Vise minimum **500 exemples** pour de bons résultats
- **1000-5000 exemples** pour un modèle vraiment personnalisé

---

## 🔧 Paramètres d'entraînement

| Paramètre | Valeur conseillée | Impact |
|---|---|---|
| `--epochs` | 3-5 | Plus d'epochs = mieux appris (mais risque de surapprentissage) |
| `--batch` | 2-4 (CPU) / 8-16 (GPU) | Plus grand = plus rapide |
| `--modele` | `gpt2` (117M) ou `gpt2-medium` (345M) | Medium = meilleur mais plus lent |

---

## 📈 Étapes suivantes après l'entraînement

### Intégrer le modèle ML dans Khaal (app Flask)

Dans `khal_core.py`, remplace le `MoteurReponse` par :

```python
from transformers import pipeline

class MoteurML:
    def __init__(self, dossier_modele="khal_modele_entraine"):
        self.generateur = pipeline(
            "text-generation",
            model=dossier_modele,
        )

    def generer_reponse(self, message: str) -> str:
        prompt = f"<|prompt|>{message}<|completion|>"
        resultat = self.generateur(
            prompt,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=self.generateur.tokenizer.eos_token_id
        )[0]["generated_text"]

        if "<|completion|>" in resultat:
            return resultat.split("<|completion|>")[1].split("<|end|>")[0].strip()
        return resultat[len(prompt):]
```

### Aller encore plus loin

- **Fine-tuner Mistral 7B** : modèle open-source bien plus puissant (nécessite plus de RAM)
- **Utiliser l'API Anthropic** : brancher Claude directement dans Khaal
- **Collecter tes propres conversations** : chaque échange avec Khaal peut devenir une donnée d'entraînement
