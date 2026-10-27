from sentence_transformers import SentenceTransformer, util

print("1. Chargement de notre modèle fine-tuné...")
model = SentenceTransformer('models/semaine2_modele_affine')

# Notre mémoire sémantique de référence
corpus_unites = [
    {"unit_id": "u-001", "type": "decision", "statement": "Le lancement du projet Phoenix est reporté au 15 novembre."},
    {"unit_id": "u-002", "type": "decision", "statement": "On a officiellement validé de décaler la sortie de Phoenix au 15/11."},
    {"unit_id": "u-003", "type": "proposal", "statement": "On pourrait peut-être envisager de reporter le projet Phoenix au mois de novembre."},
    {"unit_id": "u-004", "type": "action", "statement": "Léa doit absolument envoyer le compte-rendu financier avant ce soir."}
]

query = "Quelle est la date validée pour le projet Phoenix ?"

print(f"\n--- Requête de test : '{query}' ---\n")

# Encodage
query_embedding = model.encode(query, convert_to_tensor=True)
corpus_statements = [unite["statement"] for unite in corpus_unites]
corpus_embeddings = model.encode(corpus_statements, convert_to_tensor=True)

# Calcul des similarités cosinus
cosine_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]

# Affichage trié des résultats
results = []
for idx, score in enumerate(cosine_scores):
    results.append((score.item(), corpus_unites[idx]))

# Tri par score décroissant
results.sort(key=lambda x: x[0], reverse=True)

for score, unite in results:
    print(f"[{unite['unit_id']}] ({unite['type']}) -> Score: {score:.4f}")
    print(f"    \"{unite['statement']}\"\n")