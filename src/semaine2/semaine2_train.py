from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

print("1. Chargement du modèle de base...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Dataset d'entraînement enrichi (plusieurs triplets pour ancrer l'apprentissage)
train_examples = [
    InputExample(
        texts=[
            "Quelle est la date validée pour le projet Phoenix ?", 
            "Le lancement du projet Phoenix est reporté au 15 novembre.", 
            "On pourrait peut-être envisager de reporter le projet Phoenix au mois de novembre."
        ]
    ),
    InputExample(
        texts=[
            "Quand sort le projet Phoenix ?", 
            "On a officiellement validé de décaler la sortie de Phoenix au 15/11.", 
            "On pourrait peut-être envisager de reporter le projet Phoenix au mois de novembre."
        ]
    ),
    InputExample(
        texts=[
            "Est-ce qu'on a une date fixe pour le projet Phoenix ?", 
            "Le lancement du projet Phoenix est reporté au 15 novembre.", 
            "On discute d'éventuellement repousser le projet Phoenix à plus tard."
        ]
    )
]

# 3. Préparation du DataLoader (batch_size adapté au nombre d'exemples)
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=3)

# 4. Fonction de perte (Loss) adaptée
train_loss = losses.MultipleNegativesRankingLoss(model)

print("2. Lancement du fine-tuning renforcé (10 époques)...")
# 5. Entraînement sur 10 époques pour donner le temps au modèle d'ajuster ses vecteurs
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=10,
    show_progress_bar=True
)

# 6. Sauvegarde du modèle mis à jour
model.save("models/semaine2_modele_affine")
print("3. Entraînement terminé ! Modèle mis à jour dans 'models/semaine2_modele_affine'.")