# Architecture AI Sécurisée - Plateforme d'Intelligence Informatique Distribuée

Ce dépôt présente la conception d'une architecture **Zero Trust** pour la gouvernance et le contrôle d'actifs d'IA distribués, s'appuyant sur le cadre **Microsoft Agent Governance Toolkit (MIT)**.

## Le Cœur du Projet : Agent Governance Dashboard
Pour valider cette architecture, le projet intègre un centre de surveillance et de gouvernance (SIEM) complet en plein écran :

👉 **Lien pour accéder au Dashboard (https://kdiouf-architecture-ai-securisee.hf.space)**

### Fonctionnalités Centrales Implémentées :
* **Découverte des Actifs & Télémétrie** : Suivi en direct du statut des instances (Actives, Orphelines, Suspendues) et registre du périmètre central.
* **Incidents d'Agents de l'Ombre** : Détection automatique des environnements d'exécution actifs fonctionnant sans enregistrement cryptographique (JWT).
* **Audit d'Interception des Politiques** : Journalisation complète des boucles de validation au runtime (`allow`, `deny`, `escalate`) avec calcul des latences (Moyenne : 1,25 ms).
* **Carte au Trust** : Matrice de confiance cryptographique évaluant le score de confiance dynamique des communications inter-agents (0 à 1000).

##  Stabilité et Simulation Déterministe
Afin de répondre aux exigences académiques de reproductibilité scientifique, le moteur de données (`demo_data.py`) est **strictement déterministe**. L'utilisation d'une graine fixe (`random.seed(42)`) et d'une référence temporelle figée au **30 Juin 2026** garantit que les scénarios de menace, les graphes de cycle de vie et les métriques de risques s'exécutent de façon stable et identique à chaque rafraîchissement.

## 📂 Organisation du Dépôt
- `src/dashboard/` : Visualisation de la flotte, graphes Plotly et interface Streamlit (`app.py`, `demo_data.py`).
- `src/detection/` : Kernel de gouvernance, simulation des agents et gestion des logs (`main.py`, `agent_simulated.py`).
- `config/` : Politiques de sécurité et d'accès au format YAML (`production-policy.yaml`).
- `tests/` : Suite de validation unitaire automatisée (`test_governance.py`).
