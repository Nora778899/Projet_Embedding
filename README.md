# Embedding Lab : De la mémoire sémantique à l'agent intelligent

Projet individuel réalisé dans le cadre de la piscine de l'Intelligence Lab.  
**Étudiante :** Nora BOUKAL (B2 IA & Data, ECE Paris)

---

## Semaine 1 : Fondations et Base Sémantique

### Objectifs & Réalisations
* **Modèle de base** : Implémentation et test du modèle d'embeddings `all-MiniLM-L6-v2` via Hugging Face pour capturer le sens global des textes.
* **Baseline lexicale** : Mise en place d'une recherche par mots-clés (BM25) pour évaluer la complémentarité avec l'approche dense.
* **Mémoire sémantique** : Structuration initiale des données au format JSON (`data/memoire_simple.json`).

### Installation & Exécution
1. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
2. Lancer la mémoire sémantique :
   ```bash
   python src/semaine1_memoire.py
   ```

---

## Semaine 2 : Entraînement et Ajustement du Modèle (Contrastive Learning)

### Objectif
Affiner la capacité de l'outil de recherche à distinguer des nuances sémantiques fines (par exemple, différencier une simple proposition d'une décision officielle validée utilisant un vocabulaire similaire).

### Réalisations & Analyse
* **Apprentissage contrastif** : Utilisation de triplets (ancre, positif, négatif difficile) pour spécialiser l'encodeur.
* **Bilan expérimental** : 
  * Les scores initiaux restent proches (~0.75 pour la décision vs ~0.73 pour la proposition) car le modèle de base est déjà robuste.
  * *Leçon clé* : Le fine-tuning avec un petit volume de données ne suffit pas à inverser des nuances logiques complexes sans un dataset massif et diversifié, démontrant que les embeddings seuls ont des limites structurelles.

---

## Semaine 3 : Moteur d'Agent Sémantique (`SemanticAgentEngine`)

### Objectifs
Développer un agent intelligent capable d'exploiter une mémoire multi-personnages (Léa, Karim, Marc), d'assurer la traçabilité des auteurs, de gérer l'obsolescence des informations et d'arbitrer les contradictions.

### Architecture du Projet
```text
src/
└── semaine3/
    ├── semaine3_agent.py      # Moteur principal de l'agent sémantique
    ├── semaine3_memory.json   # Base de données structurée des unités de connaissance
    └── test_agent.py          # Suite de tests unitaires validant les scénarios
```

### Fonctionnalités Clés & Scénarios Validés
1. **Chargement & Parsing Sécurisé** : Lecture d'un fichier JSON structuré en unités (`speaker`, `statement`, `status`, `source_date`).
2. **Recherche Contextuelle & Filtrage** : Recherche par mots-clés dans les déclarations avec filtrage par locuteur et par statut (`active` vs `obsolete`).
3. **Gestion de l'Obsolescence** : Écartement automatique des propositions périmées pour ne retenir que la version la plus récente et active (`run_scenario_obsolescence`).
4. **Arbitrage des Contradictions** : Récupération exhaustive des perspectives divergentes pour comparaison et prise de décision éclairée (`run_scenario_arbitration`).

### Lancer les tests unitaires (Semaine 3)
```bash
python src/semaine3/test_agent.py
```

---
## Documentation des Datasets & Protocole Expérimental

### Structure et Annotation des Données
* **Provenance & Licence :** Corpus synthétique créé sur mesure pour simuler des échanges professionnels d'équipe (projet interne ECE Paris, libre de droits pour usage académique).
* **Préparation & Schéma JSON :** Chaque conversation est découpée en unités atomiques structurées contenant les métadonnées suivantes : `unit_id` (identifiant unique), `speaker` (Léa, Karim, Marc), `statement` (contenu textuel), `status` (`active` ou `obsolete`) et `source_date` (horodatage ISO).
* **Splits (Séparation des jeux) :** 
  * *Jeu d'entraînement (Semaine 2) :* Paires et triplets (ancre, positif, négatif difficile) dédiés à l'apprentissage contrastif.
  * *Jeu d'évaluation et d'arbitrage (Semaine 3) :* Scénarios multi-tours indépendants testant l'obsolescence temporelle et les contradictions entre intervenants.

### Rapport Expérimental & Étude d'Ablation

| Approche / Configuration | Précision sur l'obsolescence | Gestion des contradictions | Coût & Latence (CPU local) | Limite principale observée |
| :--- | :---: | :---: | :---: | :--- |
| **Baseline Lexicale (BM25)** | Faible | Aucune | Très faible (< 10 ms) | Échoue sur les synonymes et reformulations. |
| **Embeddings Bruts (`all-MiniLM-L6-v2`)** | Faible | Aucune | Faible (~30 ms) | Confond une proposition avec une décision (~0.73 vs ~0.75). |
| **Embeddings Affinés (Semaine 2)** | Moyenne | Aucune | Faible (~30 ms) | Surapprentissage rapide sur un petit volume de triplets. |
| **Architecture Hybride (`SemanticAgentEngine`)** | **100 % (Validé)** | **100 % (Validé)** | Faible (~35 ms) | Dépend de la qualité initiale de l'annotation des métadonnées. |

#### Analyse d'Ablation et Exemple d'Erreur Typique
* **Impact du filtrage structuré (Ablation) :** Lorsqu'on désactive le contrôle des attributs `status` et `source_date` dans le `SemanticAgentEngine` pour ne garder que la similarité cosinus, l'agent restitue l'information périmée dans **100 % des scénarios de mise à jour** dès lors que l'ancien message partage plus de mots-clés avec la question que le nouveau.
* **Cas d'erreur vectoriel :** Sur la requête *« Quelle est la date retenue pour le projet ? »*, un encodeur dense seul attribue un score quasi identique à *« On pourrait proposer de reporter au 12 novembre »* (Marc, proposition obsolète) et *« Le projet est officiellement reporté au 15 novembre »* (Karim, décision active), illustrant l'incapacité du vecteur à modéliser l'autorité et la temporalité sans règles déterministes.

## Conclusion & Réflexion Personnelle : Peut-on confier la logique à un simple embedding ?

Au terme de ces trois semaines d'exploration intensive, de tests, de doutes et de questionnements sur le "pourquoi du comment" des modèles, la réponse à notre problématique s'est clarifiée : **non, un modèle d'embeddings ne suffit pas à lui seul, et c'est précisément ce qui rend l'intelligence artificielle agentique passionnante.**

Si l'on s'en remet uniquement à la similarité vectorielle, le système est aveugle : il confond une simple idée lancée en réunion par Marc ("*On pourrait peut-être...*") avec une décision officielle actée par Karim ("*Le projet est reporté au 15 novembre*"). Le vecteur comprend le sujet, mais il ne comprend ni l'autorité, ni la temporalité, ni la valeur logique.

C'est pourquoi notre `SemanticAgentEngine` démontre qu'une architecture hybride est indispensable. Les embeddings excellent pour le *retrieval* (retrouver les bons fragments de texte malgré les reformulations), mais c'est le couplage avec des métadonnées explicites (`status`, `source_date`, `speaker`) et des règles d'arbitrage déterministes qui insuffle une véritable fiabilité à l'agent. 

Plutôt qu'un chatbot illusionniste qui invente des réponses, nous avons construit un agent rigoureux, capable de tracer ses sources, d'écarter l'obsolescence et d'admettre quand une information manque. C'est cette exigence de vérité et de traçabilité qui pose les bases d'une IA réellement utile et digne de confiance pour l'entreprise.