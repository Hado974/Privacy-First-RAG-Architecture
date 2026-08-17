# Local RAG System for Technical Knowledge Base

## Aperçu du projet
Ce dépôt documente le déploiement d'une architecture RAG (Retrieval-Augmented Generation) 100 % locale, souveraine et gratuite. Elle permet d'interroger une base de connaissances technique personnelle (fichiers Markdown) via des LLMs exécutés en local. 

Ce projet démontre l'intégration de modèles open-source avec accélération matérielle, sans dépendance à des API cloud tierces, garantissant une confidentialité totale des données et une absence de coûts d'inférence.

## Architecture technique
- **Moteur d'inférence :** Ollama (déployé en tant que service `systemd` local).
- **Base de données / Interface :** Obsidian (fichiers `.md` structurés).
- **Orchestration RAG :** Plugin Obsidian Copilot (moteur d'exécution `opencode` via endpoint BYOK OpenAI-compatible).
- **Modèle d'Embedding :** `nomic-embed-text` (Vectorisation de la base documentaire).
- **Modèles de Génération (LLM) :** `llama3.1:8b`, `qwen2.5-coder:32b`, `command-r:35b` (sélection dynamique selon la tâche).

## Prérequis matériels et logiciels
- **OS :** Linux (Ubuntu recommandé).
- **Compute :** GPU NVIDIA avec VRAM suffisante pour le déchargement partiel ou total des modèles (Architecture testée sur NVIDIA GeForce RTX 5080, 64 Go RAM).
- **Dépendances :** `ollama`, `python3`, `jupyter nbconvert`.

## Installation et Dépendances

### 1. Applications système requises
Ce projet s'appuie sur des logiciels indépendants de l'environnement Python. Vous devez les installer manuellement sur votre système d'exploitation :

- **Ollama** : Moteur d'exécution pour les modèles locaux.
  - Installation (Linux) : `curl -fsSL https://ollama.com/install.sh | sh`
- **Obsidian** : Interface utilisateur et gestionnaire de la base de connaissances.
  - Téléchargement : `https://obsidian.md/download`
- **Python 3** : Nécessaire uniquement pour exécuter le script de conversion et d'ingestion (`scripts/ingestion_pipeline.py`).

### 2. Téléchargement des modèles d'IA (Ollama)
Une fois le service système Ollama actif, ouvrez un terminal et exécutez ces commandes pour télécharger les modèles d'embedding et de génération de texte :

```bash
# Modèle d'indexation vectorielle (obligatoire pour le RAG)
ollama pull nomic-embed-text

# Modèle généraliste pour la synthèse des notes et la théorie
ollama pull llama3.1

# Modèle principal pour le code (Rapide avec une VRAM 16 Go)
ollama pull qwen2.5-coder:14b

# Modèle expert MLOps (Plus lent, nécessite de la RAM supplémentaire pour une VRAM de 16 Go)
ollama pull qwen2.5-coder:32b
```
## Stratégie multi-modèles
Le système exploite plusieurs LLMs locaux pour équilibrer la vitesse d'inférence et l'expertise technique, en fonction des limites de la VRAM :
- **`qwen2.5-coder:14b` :** Le modèle par défaut pour la rédaction de scripts Python et l'analyse de données courante. Il se charge intégralement dans la VRAM du GPU (16 Go) pour garantir une vitesse de génération maximale.
- **`qwen2.5-coder:32b` :** Le modèle expert dédié aux architectures MLOps et aux pipelines complexes. Son poids (environ 20 Go) impose un déchargement partiel sur la RAM système, réduisant la vitesse d'inférence en échange d'une précision maximale sur le code.
- **`llama3.1:8b` :** Utilisé spécifiquement pour l'interrogation sémantique de la base de connaissances et la synthèse de notes théoriques.

## Pipeline de traitement des données
1. **Ingestion :** Conversion des documents techniques (notebooks, documentations) en fichiers Markdown textuels via scripts Python automatisés.
2. **Indexation :** Le modèle d'embedding génère les vecteurs à la volée sur le GPU pour les documents déposés dans le répertoire cible.
3. **Inférence :** L'interface utilisateur interroge l'endpoint local `http://localhost:11434/v1` via des instructions système prédéfinies.

## Instructions système (Prompt Engineering)
Le comportement du LLM est calibré via un fichier de configuration (voir dossier `prompts/AGENTS.md`). Les directives forcent l'assistant à prioriser le contexte fourni par la recherche vectorielle, à produire du code Python modulaire (PEP 8, typage) et à justifier ses choix algorithmiques en Data Science.



