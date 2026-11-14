import json
import os
from semaine3_agent import SemanticAgentEngine  # J'importe notre classe d'agent mise à jour

def test_updated_agent():
    """Je teste les nouvelles méthodes de recherche et de gestion de l'obsolescence de l'agent."""
    
    # 1. J'initialise mon agent
    agent = SemanticAgentEngine()
    print(f"-> Mémoire chargée. Nombre total d'unités : {len(agent.memory)}")
    
    # 2. Je teste la recherche par mot-clé et par locuteur (speaker) avec filtre actif
    results_karim = agent.search("projet Phoenix", speaker="Karim", active_only=True)
    print(f"-> Unités actives trouvées pour Karim concernant 'projet Phoenix' : {len(results_karim)}")
    assert len(results_karim) == 1, "Karim doit avoir exactement une unité active sur le projet Phoenix."
    
    # 3. Je teste la gestion de l'obsolescence
    latest_info = agent.run_scenario_obsolescence("projet Phoenix")
    print(f"-> Information la plus récente trouvée : '{latest_info.get('statement')}' par {latest_info.get('speaker')}")
    assert latest_info.get("speaker") == "Karim", "L'information la plus récente et active doit provenir de Karim."
    
    # 4. Je teste l'arbitrage (qui récupère toutes les versions, y compris obsolètes)
    all_versions = agent.run_scenario_arbitration("projet Phoenix")
    print(f"-> Nombre total de versions (actives + obsolètes) pour arbitrage : {len(all_versions)}")
    assert len(all_versions) >= 2, "L'arbitrage doit lister toutes les versions pour comparaison."
    
    print("\n🎉 Tous les tests des nouvelles méthodes ont réussi avec succès !")

if __name__ == "__main__":
    test_updated_agent()