from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

print("1. Chargement du modèle de base...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Définition de notre triplet d'entraînement (Ancrage, Positif, Négatif Dur)
# Ancrage : La question posée par l'utilisateur
# Positif : La vraie décision officielle (u-001)
# Négatif Dur : La proposition piège qui se ressemble (u-003)p
train_examples = [
    InputExample(
        texts=[
            "Quelle est la date validée pour le projet Phoenix ?", 
            "Le lancement du projet Phoenix est reporté au 15 novembre.", 
            "On pourrait peut-être envisager de reporter le projet Phoenix au mois de novembre."
        ]
    )
]

# 3. Préparation du DataLoader
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=1)

# 4. Définition de la fonction de perte (Loss) adaptée aux triplets
train_loss = losses.MultipleNegativesRankingLoss(model)

print("2. Lancement du fine-tuning (apprentissage contrastive)...")
# 5. Entraînement du modèle sur 1 petite époque pour tester
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=1,
    show_progress_bar=True
)

# 6. Sauvegarde du modèle entraîné
model.save("models/semaine2_modele_affine")
print("3. Entraînement terminé ! Modèle sauvegardé dans 'models/semaine2_modele_affine'.")