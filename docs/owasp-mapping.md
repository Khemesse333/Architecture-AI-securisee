# Cartographie OWASP et Traduction Graphique (Dashboard)

Ce projet établit une passerelle directe entre les risques de sécurité de l’IA agentique et leur signalement instantané sur l'interface de gouvernance.

## 🚨 Traduction Visuelle des Atténuations OWASP sur le Dashboard

Le générateur déterministe (`demo_data.py`) et le tableau de bord (`app.py`) retranscrivent fidèlement les scénarios du noyau de contrôle :

### 1. Agent-01: Prompt Injection (Interception d'outils critiques)
- **Logique Métier** : Tentative d'injection via l'action `subprocess_spawn` ou l'outil `SystemTerminalTool`.
- **Impact Dashboard** : Onglet *Flux de politiques*. Le graphique des *"Assertions d'attaque par type d'appel"* montre l'interception immédiate de l'action (`decision: deny` ou `escalate`). Le compteur de la page d'accueil incrémente la métrique globale **"Risques Critiques"**.

### 2. Agent-03: Sensitive Data Exposure / Exfiltration
- **Logique Métier** : Requête de sortie de réseau non autorisée via `DataExportTool` ou `network_egress`.
- **Impact Dashboard** : Onglet *Carte au Trust*. La valeur de confiance entre l'agent émetteur et le récepteur s'effondre sur la Heatmap. L'action frauduleuse est répertoriée en direct dans le tableau de l'onglet *Flux de politiques*.

### 3. Agent-06: Privilege Escalation (Agents de l'ombre)
- **Logique Métier** : Exécution d'un agent sans identité cryptographique valide ou usurpation d'un outil d'administration (`AdminTool`).
- **Impact Dashboard** : Onglet *Agents de l'ombre*. Le système détecte l'absence de signature et lève une bannière d'anomalie rouge : *« 6 instances actives non enregistrées contournant les couches d'authentification »*.