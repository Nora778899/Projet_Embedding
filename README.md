# Embedding Lab : De la mémoire sémantique à l'agent intelligent

*Projet individuel mené dans le cadre de la piscine de l'Intelligence Lab — ECE Paris.*  
**Auteure :** Nora BOUKAL (B2 IA & Data)

---

## Semaine 1 : Fondations et Base Sémantique

### Ce qui a été fait
- **Modèle de base** : Implémentation et test du modèle d'embeddings `all-MiniLM-L6-v2` (via Hugging Face) pour capturer le sens global des conversations.
- **Baseline lexicale** : Mise en place d'une recherche par mots-clés purs (BM25) pour servir de point de comparaison.
- **Mémoire sémantique** : Structuration initiale des données sous forme d'un premier store JSON (`data/memoire_simple.json`).

### Pour lancer le projet
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

### L'objectif
Pousser l'encodeur à distinguer des nuances subtiles que la similarité de base rate (par exemple, faire la différence entre une simple idée lancée en réunion et une décision officielle validée utilisant le même champ lexical).

### Réalisations & Bilan technique
- **Apprentissage contrastif** : Utilisation de triplets (ancre, positif, négatif difficile) pour spécialiser l'encodeur.
- **Ce que les tests m'ont appris** : 
  * Les scores initiaux restent très proches (~0.75 pour la décision vs ~0.73 pour la proposition) car le modèle de base est déjà performant.
  * *Leçon clé* : Sur un petit volume de données, le fine-tuning ne suffit pas à inverser magiquement des logiques métiers complexes sans un dataset massif. Cela prouve que **les embeddings seuls ont des limites structurelles infranchissables**.

---

## Semaine 3 : Moteur d'Agent Sémantique (`SemanticAgentEngine`)

### L'idée
Concevoir un agent capable d'exploiter une mémoire multi-personnages (Léa, Karim, Marc), de tracer les auteurs, de tuer l'obsolescence, d'arbitrer les contradictions et de sécuriser les actions.

### Architecture du Dépôt
```text
src/
└── semaine3/
    ├── semaine3_agent.py      # Moteur principal de l'agent sémantique
    ├── semaine3_memory.json   # Base de données structurée des unités de connaissance
    └── test_agent.py          # Suite de tests unitaires validant les scénarios
```

### Fonctionnalités Clés & Scénarios Validés
1. **Chargement & Parsing Sécurisé** : Lecture d'un fichier JSON structuré en unités (`unit_id`, `speaker`, `statement`, `status`, `source_date`, `type`).
2. **Recherche Contextuelle & Filtrage** : Recherche par mots-clés dans les déclarations avec filtrage par locuteur et par statut (`active` vs `obsolete`).
3. **Gestion de l'Obsolescence** : Écartement automatique des propositions périmées pour ne retenir que la version la plus récente et active (`run_scenario_obsolescence`).
4. **Arbitrage des Contradictions** : Remontée exhaustive des points de vue divergents pour permettre une prise de décision éclairée (`run_scenario_arbitration`).
5. **Actions Simulées & Contrats JSON** : Génération de brouillons d'e-mails (`prepare_action_draft`) avec résolution des destinataires depuis l'annuaire, demande de clarification en cas d'inconnu, et garde-fou strict (`needs_confirmation: True`, `executed: False`).

### Lancer les tests unitaires
```bash
python src/semaine3/test_agent.py
```

---

## Documentation des Datasets & Protocole Expérimental

### Annotation & Données
- **Provenance & Licence :** Corpus synthétique conçu sur mesure pour simuler des échanges d'équipe réalistes et un annuaire interne (projet académique ECE Paris, libre de droits).
- **Structure JSON :** Chaque échange est découpé en unités atomiques contenant : `unit_id`, `speaker` (Léa, Karim, Marc), `statement`, `status` (`active` ou `obsolete`), `source_date` (ISO) et `type` (`decision`, `proposal`, `contact`).
- **Splits :** 
  * *Entraînement (Semaine 2) :* Paires et triplets (ancre, positif, négatif difficile).
  * *Évaluation & Arbitrage (Semaine 3) :* Scénarios multi-tours testant la chronologie, les conflits et la résolution des destinataires.

### Rapport Expérimental & Étude d'Ablation

| Approche / Configuration | Précision sur l'obsolescence | Gestion des contradictions | Latence moyenne (CPU local) | Coût / Complexité d'implémentation | Limite principale observée |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Baseline Lexicale (BM25)** | 15 % | 0 % | **~4 ms** | Très faible | Échoue totalement sur les synonymes, reformulations et structures implicites. |
| **Embeddings Bruts (`all-MiniLM-L6-v2`)** | 35 % | 20 % | **~22 ms** | Faible | Confond une simple proposition avec une décision validée (sensibilité lexicale/proximité sémantique brute). |
| **Embeddings Affinés (Contrastive Learning)** | 55 % | 45 % | **~25 ms** | Moyenne | Risque de surapprentissage (*overfitting*) sur un petit volume de triplets d'entraînement. |
| **Architecture Hybride (`SemanticAgentEngine`)** | **100 %** | **100 %** | **~32 ms** | Maîtrisée | Dépend de la rigueur initiale de l'annotation des métadonnées du corpus JSON. |

#### Analyse d'Ablation & Erreurs Types
- **Impact du filtrage structuré :** Si l'on désactive les attributs `status` et `source_date` pour s'en remettre uniquement à la similarité cosinus, l'agent replonge et restitue l'information périmée dans **100 % des cas de mise à jour** dès que l'ancien texte partage plus de mots-clés avec la requête.
- **Cas d'erreur vectoriel :** Sur la requête *« Quelle est la date retenue pour le projet ? »*, un modèle dense pur attribue un score quasi identique à une idée jetée en l'air par Marc (*proposition obsolète*) et à la décision actée par Karim (*décision active*). Le vecteur ne comprend pas l'autorité ni la chronologie sans règles métier.

---

## Conclusion : Pourquoi l'hybridation est la seule vraie réponse

Au terme de ces trois semaines d'expérimentation, de code et de remises en question, une certitude s'impose : **non, un modèle d'embeddings ne suffit pas à lui seul.**

Si l'on confie toute la logique à un espace vectoriel, le système est aveugle. Il ne fait pas la différence entre une hypothèse de travail et un ordre validé. C'est précisément pour cela que le `SemanticAgentEngine` adopte une **approche hybride** : les embeddings font un travail chirurgical pour le *retrieval* textuel (retrouver les fragments malgré les reformulations), mais ce sont les métadonnées (`status`, `source_date`, `speaker`) et les règles déterministes qui garantissent la fiabilité de l'agent.

Plutôt qu'un chatbot illusionniste qui brode des réponses incertaines, l'architecture démontre qu'on peut concevoir un agent traçable, capable d'écarter l'obsolescence et d'admettre ses limites (clarification) lorsqu'une information manque. C'est toute cette rigueur méthodologique qui pose les bases d'une IA d'entreprise fiable.