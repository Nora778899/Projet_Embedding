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
        entries = self.memory.get("entries", [])
        
        for entry in entries:
            if author and entry.get("author") != author:
                continue
            if query.lower() in entry.get("content", "").lower():
                results.append(entry)
                
        return results

    def run_scenario_attribution(self, query, author):
        """Scénario 1 & 2 : Je filtre et récupère spécifiquement les contributions d'un auteur."""
        return self.search(query, author=author)

    def run_scenario_obsolescence(self, topic):
        """Scénario 4 & 7 : Je gère l'obsolescence en extrayant uniquement l'information la plus récente."""
        entries = self.memory.get("entries", [])
        relevant = [e for e in entries if topic.lower() in e.get("content", "").lower()]
        
        if not relevant:
            return None
            
        latest = max(relevant, key=lambda x: x.get("date", ""))
        return latest

    def run_scenario_arbitration(self, topic):
        """Scénario 6 : J'arbitre les contradictions en récupérant toutes les versions des différents auteurs."""
        entries = self.memory.get("entries", [])
        return [e for e in entries if topic.lower() in e.get("content", "").lower()]

if __name__ == "__main__":
    # Je crée une instance de mon moteur d'agent sémantique pour valider les scénarios
    agent = SemanticAgentEngine()
    print("Agent initialisé et prêt pour les 7 scénarios de démonstration !")