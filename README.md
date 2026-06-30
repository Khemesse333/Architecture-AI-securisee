# Architecture AI Sécurisée - Plateforme d'Intelligence Informatique Distribuée

Ce projet présente la conception et le déploiement d'une architecture **Zero Trust** sécurisée pour la gouvernance et l'audit d'agents d'IA distribués.

## La Vitrine du Projet : Le Dashboard de Gouvernance
Pour apporter une crédibilité opérationnelle à cette architecture, un **Dashboard de Gouvernance en temps réel** a été conçu et déployé dans un conteneur cloud isolé. Il sert de centre de contrôle (SIEM) pour monitorer la sécurité de la plateforme.

👉 **[Accéder au Dashboard Public en Plein Écran] https://kdiouf-architecture-ai-securisee.hf.space**

### 📊 Fonctionnalités clés visibles sur le Dashboard :
* **Détection des Shadow Agents** : Identification visuelle immédiate des agents non enregistrés ou suspects.
* **Suivi du Cycle de Vie** : Graphiques dynamiques montrant la mise en quarantaine et la suspension automatique des entités malveillantes.
* **Télémétrie Déterministe** : Évaluation continue et reproductible des scores de confiance de la flotte d'IA.

## 📂 Architecture Logicielle
Le dépôt est structuré de manière professionnelle pour séparer la logique métier de l'interface :
* `src/dashboard/` : Interface de restitution visuelle et monitoring (Frontend Streamlit).
* `src/backend/` : Kernel de sécurité, évaluation des règles et simulation des menaces.
* `config/` : Politiques de sécurité au format YAML (`production-policy.yaml`).
* `tests/` : Suite de tests unitaires automatisés validant le Kernel de gouvernance.
