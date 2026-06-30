# Architecture du projet

Cette base représente une conception d’architecture sécurisée Zero Trust pour une plateforme d’intelligence distribuée.

## Structure retenue

- src/dashboard/: composants du tableau de bord de gouvernance et de visualisation.
- src/detection/: logique de détection et d’évaluation des incidents.
- config/: politiques YAML de gouvernance et de sécurité.
- docs/: documentation technique, cartographie OWASP et captures d’écran.
- tests/: validations unitaires du moteur de gouvernance.

## Répartition fonctionnelle

- Dashboard: visualisation du périmètre, des agents, des politiques et des scores de confiance.
- Moteur de gouvernance: évaluation des actions via des politiques YAML et journalisation d’audit.
- Démonstrations et scénarios: fichiers de simulation pour valider la logique de contrôle sans faire partie du cœur du produit.

## Point de vigilance

Les fichiers de démonstration et de test sont conservés pour illustrer la logique, mais le cœur fonctionnel du projet est centré sur le dashboard, les politiques et le moteur de gouvernance.
