# Embedding Lab : De la mémoire sémantique à l'agent intelligent

Projet individuel réalisé dans le cadre de la piscine de l'Intelligence Lab.
Étudiante : Nora BOUKAL (B2 IA & Data)

##    Objectif de la Semaine 1

   - Implémentation et test d'un modèle d'embeddings de base (`all-MiniLM-L6-v2` via Hugging Face).

   - Mise en place d'une baseline lexicale (BM25).

   - Structuration de la mémoire sémantique au format JSON (`data/memoire_simple.json`).

## Installation & Exécution

1. Installer les dépendances :
   ```bash
   pip install -r requirements.txt

2. Lancer la mémoire sémantique :
   ```bash
   python src/semaine1_memoire.py

##  Semaine 2 : Entraînement et ajustement du modèle

### Objectif
Améliorer notre outil de recherche pour qu'il ne se trompe plus entre une vraie **décision officielle** et une simple **proposition** qui utilisent les mêmes mots.


### Les réalisations:

1. **Entraînement du modèle** : 
   - Utilisation d'un modèle de base et d'une technique d'apprentissage par comparaison (triplets : question, bonne réponse, piège).
2. **Tests et essais** :
   - Un premier test rapide pour valider le code (1 époque), puis un entraînement sur plusieurs tours (10 époques) avec plus d'exemples.
   - Les fichiers du modèle entraîné ont été stockés localement et exclus de GitHub grâce au fichier `.gitignore` pour garder un dépôt propre.


###  Bilan
* **Observation** : Même avec plusieurs tours d'entraînement, les scores bougent très peu face aux pièges (~0.75 pour la décision vs ~0.73 pour la proposition). 
* **Pourquoi ?** : Le modèle de base est déjà très fort, et avec un tout petit nombre d'exemples, il ne peut pas tout changer. 
* **Constat** : Pour avoir de vrais meilleurs résultats, il faudrait surtout un **plus grand volume de données** d'entraînement. 

## Semaine 3 : Moteur d'Agent Sémantique (SemanticAgentEngine)

### Objectifs
Développer un agent intelligent capable de gérer une mémoire multi-personnages (Léa, Karim, Marc), d'assurer la traçabilité des auteurs, de gérer l'obsolescence des informations et d'arbitrer les contradictions.

### Architecture du Projet
src/
└── semaine3/
    ├── semaine3_agent.py      # Moteur principal de l'agent sémantique
    ├── semaine3_memory.json   # Base de données structurée des mémoires (JSON)
    └── test_agent.py          # Suite de tests unitaires validant les scénarios

### Fonctionnalités Clés

* **Chargement de la Mémoire Sémantique** : Parsing sécurisé d'un fichier JSON structuré en unités (speaker, statement, status, source_date).

* **Recherche Contextuelle & Filtrage** : Recherche par mots-clés dans les déclarations (statement), filtrage par locuteur (speaker) et gestion des statuts actifs.

* **Gestion de l'Obsolescence** : Écartement automatique des propositions périmées pour ne retenir que la version active la plus récente (run_scenario_obsolescence).

* **Arbitrage des Contradictions** : Récupération de l'ensemble des perspectives divergentes pour comparaison ou prise de décision (run_scenario_arbitration).

### Lancer les tests de la Semaine 3
python src/semaine3/test_agent.py
