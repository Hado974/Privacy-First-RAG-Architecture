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

## Pipeline de traitement des données
1. **Ingestion :** Conversion des documents techniques (notebooks, documentations) en fichiers Markdown textuels via scripts Python automatisés.
2. **Indexation :** Le modèle d'embedding génère les vecteurs à la volée sur le GPU pour les documents déposés dans le répertoire cible.
3. **Inférence :** L'interface utilisateur interroge l'endpoint local `http://localhost:11434/v1` via des instructions système prédéfinies.

## Instructions système (Prompt Engineering)
Le comportement du LLM est calibré via un fichier de configuration (voir dossier `prompts/AGENTS.md`). Les directives forcent l'assistant à prioriser le contexte fourni par la recherche vectorielle, à produire du code Python modulaire (PEP 8, typage) et à justifier ses choix algorithmiques en Data Science.
