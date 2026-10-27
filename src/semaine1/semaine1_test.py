from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


print("Chargement du modèle d'embeddings...")
model = SentenceTransformer('all-MiniLM-L6-v2')


phrases = [
    "Le lancement du projet Phoenix est reporté au 15 novembre.",
    "On a officiellement validé de décaler la sortie de Phoenix au 15/11.",
    "On pourrait peut-être envisager de reporter le projet Phoenix au mois de novembre.",
    "Léa doit absolument envoyer le compte-rendu financier avant ce soir."
]

print("\n--- Génération des embeddings ---")

vecteurs = model.encode(phrases)

print(f"Forme de la matrice des vecteurs : {vecteurs.shape}") 

print("\n--- Calcul des similarités ---")
similarites = cosine_similarity(vecteurs)

for i in range(len(phrases)):
    for j in range(len(phrases)):
        print(f"Sim({i}, {j}) = {similarites[i][j]:.4f}  --> '{phrases[i]}' vs '{phrases[j]}'")