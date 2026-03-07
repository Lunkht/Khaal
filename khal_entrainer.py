"""
khal_entrainer.py
=================
Entraîne un vrai modèle de génération de texte (GPT-2)
sur les données personnalisées de Khal via HuggingFace Transformers.

Prérequis :
    pip install torch transformers datasets accelerate

Usage :
    python khal_entrainer.py
    python khal_entrainer.py --epochs 5 --batch 4
"""

import argparse
import os
import json

# ── Vérification des dépendances ──────────────────────────────────────────────
try:
    import torch
    from transformers import (
        GPT2LMHeadModel, GPT2Tokenizer,
        TextDataset, DataCollatorForLanguageModeling,
        Trainer, TrainingArguments,
        pipeline
    )
    from datasets import Dataset
    DEPS_OK = True
except ImportError:
    DEPS_OK = False


def verifier_deps():
    if not DEPS_OK:
        print("❌ Dépendances manquantes. Installez-les avec :")
        print("   pip install torch transformers datasets accelerate")
        print("\n💡 Sur Google Colab : ces packages sont déjà installés !")
        exit(1)
    print("✅ Dépendances OK")
    print(f"   PyTorch  : {torch.__version__}")
    device = "GPU 🚀" if torch.cuda.is_available() else "CPU (plus lent)"
    print(f"   Device   : {device}\n")


# ── Chargement des données ────────────────────────────────────────────────────

def charger_dataset(fichier: str = "khal_dataset.jsonl") -> list:
    """Charge le dataset JSONL généré par khal_generer_donnees.py"""
    if not os.path.exists(fichier):
        print(f"❌ Fichier introuvable : {fichier}")
        print("   Lance d'abord : python khal_generer_donnees.py")
        exit(1)

    textes = []
    with open(fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            obj = json.loads(ligne.strip())
            textes.append(obj["text"])

    print(f"✅ Dataset chargé : {len(textes)} exemples")
    return textes


# ── Tokenisation ──────────────────────────────────────────────────────────────

def preparer_tokenizer(modele_base: str = "gpt2"):
    """Charge et configure le tokenizer GPT-2."""
    print(f"🔄 Chargement du tokenizer ({modele_base})...")
    tokenizer = GPT2Tokenizer.from_pretrained(modele_base)

    # GPT-2 n'a pas de token de padding par défaut
    tokenizer.pad_token = tokenizer.eos_token

    # Ajouter nos tokens spéciaux
    tokens_speciaux = ["<|prompt|>", "<|completion|>", "<|end|>"]
    tokenizer.add_special_tokens({"additional_special_tokens": tokens_speciaux})

    print(f"✅ Tokenizer prêt (vocab : {len(tokenizer)} tokens)")
    return tokenizer


def tokeniser_dataset(textes: list, tokenizer, longueur_max: int = 256):
    """Tokenise tous les exemples du dataset."""
    print("🔄 Tokenisation du dataset...")

    def tokeniser(batch):
        return tokenizer(
            batch["text"],
            truncation=True,
            max_length=longueur_max,
            padding="max_length",
        )

    dataset_hf = Dataset.from_dict({"text": textes})
    dataset_tok = dataset_hf.map(tokeniser, batched=True, remove_columns=["text"])
    dataset_tok = dataset_tok.train_test_split(test_size=0.1, seed=42)

    print(f"✅ Dataset tokenisé :")
    print(f"   Train : {len(dataset_tok['train'])} exemples")
    print(f"   Test  : {len(dataset_tok['test'])} exemples")
    return dataset_tok


# ── Modèle ────────────────────────────────────────────────────────────────────

def charger_modele(modele_base: str, tokenizer):
    """Charge GPT-2 et l'adapte à notre vocabulaire étendu."""
    print(f"🔄 Chargement du modèle {modele_base}...")
    modele = GPT2LMHeadModel.from_pretrained(modele_base)

    # Redimensionner les embeddings pour nos nouveaux tokens
    modele.resize_token_embeddings(len(tokenizer))

    nb_params = sum(p.numel() for p in modele.parameters()) / 1e6
    print(f"✅ Modèle chargé : {nb_params:.0f}M paramètres")
    return modele


# ── Entraînement ──────────────────────────────────────────────────────────────

def entrainer(modele, tokenizer, dataset_tok, epochs: int, batch_size: int, dossier_sortie: str):
    """Lance l'entraînement avec HuggingFace Trainer."""

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False  # GPT-2 = modèle causal (pas masqué)
    )

    args = TrainingArguments(
        output_dir=dossier_sortie,
        overwrite_output_dir=True,

        # Durée d'entraînement
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,

        # Optimisation
        learning_rate=5e-5,
        warmup_steps=50,
        weight_decay=0.01,
        fp16=torch.cuda.is_available(),  # Utilise FP16 si GPU disponible

        # Évaluation & sauvegarde
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        logging_steps=10,

        # Reproductibilité
        seed=42,
    )

    trainer = Trainer(
        model=modele,
        args=args,
        train_dataset=dataset_tok["train"],
        eval_dataset=dataset_tok["test"],
        data_collator=data_collator,
    )

    print(f"\n🚀 Entraînement démarré !")
    print(f"   Epochs     : {epochs}")
    print(f"   Batch size : {batch_size}")
    print(f"   Device     : {'GPU' if torch.cuda.is_available() else 'CPU'}")
    print(f"   Sortie     : {dossier_sortie}/\n")

    trainer.train()

    print("\n✅ Entraînement terminé !")
    trainer.save_model(dossier_sortie)
    tokenizer.save_pretrained(dossier_sortie)
    print(f"✅ Modèle sauvegardé dans : {dossier_sortie}/")
    return trainer


# ── Test du modèle entraîné ───────────────────────────────────────────────────

def tester_modele(dossier_modele: str):
    """Teste le modèle entraîné avec quelques prompts."""
    print(f"\n🧪 Test du modèle entraîné...")

    generateur = pipeline(
        "text-generation",
        model=dossier_modele,
        tokenizer=dossier_modele,
    )

    prompts_test = [
        "<|prompt|>Bonjour<|completion|>",
        "<|prompt|>Qui es-tu ?<|completion|>",
        "<|prompt|>C'est quoi l'IA ?<|completion|>",
        "<|prompt|>Génère un texte sur la technologie<|completion|>",
    ]

    print("\n" + "="*60)
    print("RÉSULTATS DU MODÈLE KHAL ENTRAÎNÉ")
    print("="*60)

    for prompt in prompts_test:
        question = prompt.replace("<|prompt|>", "").replace("<|completion|>", "")
        print(f"\n❓ {question}")
        try:
            resultat = generateur(
                prompt,
                max_new_tokens=80,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=generateur.tokenizer.eos_token_id,
            )[0]["generated_text"]

            # Extraire uniquement la completion
            if "<|completion|>" in resultat:
                completion = resultat.split("<|completion|>")[1]
                completion = completion.split("<|end|>")[0].strip()
                print(f"🤖 {completion}")
            else:
                print(f"🤖 {resultat[len(prompt):][:100]}")
        except Exception as e:
            print(f"⚠️  Erreur : {e}")


# ── Point d'entrée ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Entraîne Khal sur GPT-2")
    parser.add_argument("--epochs",   type=int, default=3,            help="Nombre d'epochs (défaut: 3)")
    parser.add_argument("--batch",    type=int, default=2,            help="Batch size (défaut: 2)")
    parser.add_argument("--modele",   type=str, default="gpt2",       help="Modèle de base HuggingFace (défaut: gpt2)")
    parser.add_argument("--dataset",  type=str, default="khal_dataset.jsonl")
    parser.add_argument("--sortie",   type=str, default="khal_modele_entraine")
    parser.add_argument("--test-seulement", action="store_true",      help="Tester un modèle déjà entraîné")
    args = parser.parse_args()

    print("\n" + "█"*50)
    print("  KHAL — ENTRAÎNEMENT ML")
    print("█"*50 + "\n")

    verifier_deps()

    if args.test_seulement:
        tester_modele(args.sortie)
        return

    # Pipeline complet
    textes      = charger_dataset(args.dataset)
    tokenizer   = preparer_tokenizer(args.modele)
    dataset_tok = tokeniser_dataset(textes, tokenizer)
    modele      = charger_modele(args.modele, tokenizer)
    entrainer(modele, tokenizer, dataset_tok, args.epochs, args.batch, args.sortie)
    tester_modele(args.sortie)

    print("\n🎯 Intègre le modèle dans Khal avec :")
    print(f'   from transformers import pipeline')
    print(f'   khal_ml = pipeline("text-generation", model="{args.sortie}")')


if __name__ == "__main__":
    main()
