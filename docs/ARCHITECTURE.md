# Architecture du projet

Cette base représente une conception d’architecture sécurisée Zero Trust pour une plateforme d’intelligence informatique distribuée, basée sur le cadre de simulation **Microsoft Agent Governance Toolkit (MIT)**.

## Structure et Synergie du Projet

Le projet découple de manière stricte le moteur distribué de simulation et l'interface de contrôle et de surveillance (Frontend) :

- **src/dashboard/** : Composants graphiques (`app.py`) et moteur de télémétrie déterministe (`demo_data.py`) sous Streamlit. Il centralise la gouvernance de la flotte.
- **src/detection/** : Cœur d'exécution distribué (`main.py`, `agent_simulated.py`, `governance_demo.py`) simulant les comportements des agents et l'interception des menaces.
- **config/** : Fichiers de politiques de sécurité au format YAML (`dev-policy.yaml`, `production-policy.yaml`, `security-policy.yaml`).
- **docs/** : Cartographie des risques, ressources visuelles (`screenshots/`) et spécifications techniques.
- **tests/** : Suite de tests unitaires automatisés (`test_governance.py`, `test_policies.py`) validant le moteur d'interception.

## Répartition Fonctionnelle et Centralisation sur le Dashboard

Le **Agent Governance Dashboard** fait office de vitrine opérationnelle en matérialisant visuellement les concepts Zero Trust à travers 5 matrices de navigation :

1. **Aperçu de la flotte** : Centre de contrôle (SIEM) affichant les métriques clés (Agents totaux : 30, Instances actives : 10, Agents de l'ombre : 6, Nœuds Orphelins : 9, Risques Critiques : 8), l'allocation par type principal et le "Registre du périmètre central de la flotte".
2. **Agents de l'ombre** : Identification des instances d'exécution actives fonctionnant sans enregistrement cryptographique (Bannière d'anomalie rouge), avec prescription d'actions de remédiation (Signatures JWT, intercepteurs AGT).
3. **Moniteur du cycle de vie** : Entonnoir (Funnel) d'approvisionnement des états de la topologie du système (`pending_approval`, `provisioned`, `active`, `suspended`, `orphaned`, `decommissioned`).
4. **Flux de politiques** : Registre d'audit immuable des décisions d'interception au runtime (`allow`, `deny`, `escalate`), affichant la latence moyenne d'évaluation (1,25 ms).
5. **Carte au Trust** : Matrice de confiance cryptographique bidimensionnelle mesurant le score de confiance dynamique des communications inter-agents (0 à 1000).