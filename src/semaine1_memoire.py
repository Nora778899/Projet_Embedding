import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi

# 1. Mémoire sémantique simplifiée et logique
memoire_simple = [
    {
        "unit_id": "u-001",
        "type": "decision",
        "statement": "Le lancement du projet Phoenix est reporté au 15 novembre."
    },
    {
        "unit_id": "u-002",
        "type": "decision",
        "statement": "On a officiellement validé de décaler la sortie de Phoenix au 15/11."
    },
    {
        "unit_id": "u-003",
        "type": "proposal",
        "statement": "On pourrait peut-être envisager de reporter le projet Phoenix au mois de novembre."
    },
    {
        "unit_id": "u-004",
        "type": "action",
        "statement": "Léa doit absolument envoyer le compte-rendu financier avant ce soir."
    }
]

# Sauvegarde au format JSON
with open("data/memoire_simple.json", "w", encoding="utf-8") as f:
    json.dump(memoire_simple, f, ensure_ascii=False, indent=4)

print("✅ Mémoire simplifiée exportée avec succès !\n")

# 2. Test rapide de recherche
requete = "Quelle est la date validée pour le projet Phoenix ?"
textes = [u["statement"] for u in memoire_simple]

model = SentenceTransformer('all-MiniLM-L6-v2')
scores_embeddings = cosine_similarity(model.encode([requete]), model.encode(textes))[0]

print(f"Requête : '{requete}'\n")
for i, unite in enumerate(memoire_simple):
    print(f"[{unite['unit_id']}] ({unite['type']}) : {unite['statement']}")
    print(f"   -> Score sémantique : {scores_embeddings[i]:.4f}\n")