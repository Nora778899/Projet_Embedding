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
            return []
        # J'ouvre le fichier en lecture avec l'encodage utf-8 pour éviter les problèmes d'accents
        with open(self.memory_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def search(self, query, speaker=None, active_only=True):
        """Je recherche par mots-clés dans les 'statement' et je filtre par locuteur ('speaker') et statut actif."""
        results = []
        
        # Je m'assure que la mémoire est bien une liste d'unités
        if not isinstance(self.memory, list):
            return results
        
        # Je parcours chaque unité de mémoire de la liste
        for unit in self.memory:
            # Si on exige des unités actives, j'écarte celles dont le statut est obsolète
            if active_only and unit.get("status") != "active":
                continue
                
            # Si un locuteur est spécifié (ex: Marc, Karim) et qu'il ne correspond pas, je passe au suivant
            if speaker and unit.get("speaker") != speaker:
                continue
                
            # Je vérifie si mon mot-clé (query) est présent dans le champ 'statement'
            statement = unit.get("statement", "")
            if query.lower() in statement.lower():
                results.append(unit) # J'ajoute l'unité trouvée à mes résultats
                
        return results

    def run_scenario_obsolescence(self, topic):
        """Je gère l'obsolescence en filtrant les unités actives et en cherchant la plus récente par 'source_date'."""
        active_units = [u for u in self.memory if u.get("status") == "active"]
        relevant = [u for u in active_units if topic.lower() in u.get("statement", "").lower()]
        
        if not relevant:
            return None
            
        # Je trie par 'source_date' pour extraire la version la plus récente
        latest = max(relevant, key=lambda x: x.get("source_date", ""))
        return latest

    def run_scenario_arbitration(self, topic):
        """J'arbitre les contradictions en récupérant toutes les versions (actives et obsolètes) pour comparaison."""
        return [u for u in self.memory if topic.lower() in u.get("statement", "").lower()]

if __name__ == "__main__":
    # Je crée une instance de mon moteur d'agent sémantique avec les clés adaptées
    agent = SemanticAgentEngine()
    print("Agent initialisé avec succès et synchronisé avec les clés exactes du JSON !")