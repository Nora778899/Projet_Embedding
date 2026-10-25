from rank_bm25 import BM25Okapi

# 1. Définition de notre mini-mémoire sémantique 
corpus_unites = [
    {"unit_id": "u-001", "type": "decision", "statement": "Le lancement du projet Phoenix est reporté au 15 novembre."},
    {"unit_id": "u-002", "type": "decision", "statement": "On a officiellement validé de décaler la sortie de Phoenix au 15/11."},
    {"unit_id": "u-003", "type": "proposal", "statement": "On pourrait peut-être envisager de reporter le projet Phoenix au mois de novembre."},
    {"unit_id": "u-004", "type": "action", "statement": "Léa doit absolument envoyer le compte-rendu financier avant ce soir."}
]

# 2. Préparation pour BM25
corpus_textes = [unite["statement"] for unite in corpus_unites]
tokenized_corpus = [doc.lower().split(" ") for doc in corpus_textes]

# Initialisation de l'algorithme BM25
bm25 = BM25Okapi(tokenized_corpus)

# 3. Simulation d'une requête utilisateur
requete = "Quelle est la date officielle du projet Phoenix ?"
print(f"Requête utilisateur : '{requete}'\n")
tokenized_query = requete.lower().split(" ")

# 4. Calcul des scores BM25
scores = bm25.get_scores(tokenized_query)

print("--- Résultats de la recherche lexicale (BM25) ---")
for idx, score in enumerate(scores):
    unite = corpus_unites[idx]
    print(f"Score : {score:.4f} | Type : {unite['type']} | Texte : '{unite['statement']}'")