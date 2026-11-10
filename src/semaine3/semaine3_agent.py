import json  # J'importe le module json pour pouvoir lire et manipuler notre fichier de mémoire
import os    # J'importe le module os pour vérifier si le fichier existe sur le disque

class SemanticAgentEngine:
    def __init__(self, memory_path="src/semaine3/semaine3_memory.json"):
        # J'enregistre le chemin du fichier de mémoire dans un attribut de l'objet
        self.memory_path = memory_path
        # Je charge le fichier JSON en mémoire dès que j'initialise mon agent
        self.memory = self.load_memory()

    def load_memory(self):
        """Je définis la fonction pour charger le fichier JSON de mémoire sémantique."""
        # Je vérifie si le fichier existe physiquement avant de l'ouvrir
        if not os.path.exists(self.memory_path):
            print(f"Erreur : Le fichier {self.memory_path} est introuvable.")
            return {}
        # J'ouvre le fichier en lecture avec l'encodage utf-8 pour éviter les problèmes d'accents
        with open(self.memory_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def search(self, query, author=None):
        """Je définis la fonction de recherche par mots-clés et filtrage par auteur."""
        results = []
        # Je récupère la liste des entrées dans le dictionnaire JSON (ou une liste vide par défaut)
        entries = self.memory.get("entries", [])
        
        # Je parcours chaque entrée de mémoire une par une
        for entry in entries:
            # Si un auteur est spécifié (ex: Léa, Karim, Marc) et qu'il ne correspond pas, je passe au suivant
            if author and entry.get("author") != author:
                continue
            # Je vérifie si mon mot-clé (query) est présent dans le contenu, sans me soucier des majuscules
            if query.lower() in entry.get("content", "").lower():
                results.append(entry) # J'ajoute l'entrée trouvée à mes résultats
                
        return results

if __name__ == "__main__":
    # Je crée une instance de mon moteur d'agent sémantique
    agent = SemanticAgentEngine()
    print("Agent initialisé avec succès !")