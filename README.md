# Privacy-First RAG Architecture

Architecture 100% locale, asynchrone et sans appel d'API externe, conçue pour l'ingénierie Machine Learning, le Deep Learning (PyTorch) et la recherche scientifique.

## 🛠 Infrastructure Matérielle et Logicielle

- **OS :** Ubuntu Linux 
- **GPU :** NVIDIA GeForce RTX 5080 (16 Go VRAM)
- **RAM :** 64 Go
- **Moteur d'inférence :** Ollama (Service système Linux natif)
- **Interfaces :** Obsidian (Plugin Copilot) & Open WebUI (Docker)

## 🧠 Modèles et Répartition des Tâches

Pour éviter la saturation matérielle (KV Cache) et le goulot d'étranglement de la RAM système, les modèles sont strictement isolés par interface et par tâche.

### 1. Obsidian (Théorie et RAG Rapide)
- **Modèle :** `qwen2.5:14b`
- **Exécution :** 100% VRAM. Vitesse d'inférence maximale.
- **Rôle :** Synthèse de fiches de cours, requêtes théoriques.
- **Contrainte :** Les modèles de la gamme "Coder" sont exclus de cette interface pour bloquer les boucles de formatage JSON provoquées par les instructions agentiques cachées du plugin.

### 2. Open WebUI (Ingénierie MLOps & Code)
- **Modèle :** `qwen2.5-coder:32b`
- **Exécution :** Débordement partiel de la VRAM vers la RAM système.
- **Rôle :** Conception d'architectures Docker, pipelines scikit-learn, API FastAPI, scripts de validation croisée.

### 3. Open WebUI (Recherche Scientifique)
- **Modèle :** `qwen3.8:27b`
- **Exécution :** Débordement partiel de la VRAM vers la RAM système.
- **Rôle :** Raisonnement profond, analyse multimodale, extraction de méthodologies à partir de la recherche académique.

## ⚙️ Configuration Système (Ollama + Docker)

Pour permettre à Open WebUI (isolé dans son conteneur Docker) de communiquer avec Ollama sur l'hôte Ubuntu, le service Linux est modifié pour écouter sur toutes les interfaces :

1. Édition du service : `sudo systemctl edit ollama.service`
2. Ajout des règles réseau :
```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0"
