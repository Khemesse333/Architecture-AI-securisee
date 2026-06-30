"""Agent Governance Dashboard - Real-time agent fleet visibility."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from demo_data import generate_fleet, generate_policy_events, generate_trust_matrix, generate_lifecycle_events

# ─── Configuration de la Page ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Agent Governance Dashboard", 
    page_icon="🛡️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# ─── Style Épuré Lumineux (Blanc & Beige) ─────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #FCFBF9 !important;
        color: #1E293B !important;
    }
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }
    .dashboard-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.03em;
        margin-bottom: 0.25rem;
    }
    .dashboard-subtitle {
        font-size: 0.88rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 1rem 1.25rem !important;
    }
    div[data-testid="stMetricLabel"] p {
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: #64748B !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetricValue"] div {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #0F172A !important;
    }
    .chart-container {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
    }
    .chart-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 1rem;
    }
    .badge-error {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        border: 1px solid #FCA5A5;
        font-size: 0.9rem;
        font-weight: 500;
    }
    .badge-success {
        background-color: #DCFCE7;
        color: #166534;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        border: 1px solid #BBF7D0;
        font-size: 0.9rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ─── Chargement Global Déterministe des Données ───────────────────────────────
@st.cache_data
def load_deterministic_data():
    agents = generate_fleet(30)
    return agents, generate_policy_events(300), generate_trust_matrix(agents), generate_lifecycle_events(agents, 150)

agents, policy_events, trust_matrix, lifecycle_events = load_deterministic_data()
adf = pd.DataFrame(agents)
pdf = pd.DataFrame(policy_events)
tdf = pd.DataFrame(trust_matrix)
ldf = pd.DataFrame(lifecycle_events)

# ─── Barre Latérale Épurée ────────────────────────────────────────────────────
st.sidebar.markdown("<div style='padding: 0.5rem 0;'><b style='font-size:1.2rem; color:#0F172A;'>Gouvernance des agents</b></div>", unsafe_allow_html=True)
st.sidebar.markdown("---")
page = st.sidebar.radio("Matrice de navigation", ["Aperçu de la flotte", "Agents de l'ombre", "Moniteur du cycle de vie", "Flux de politiques", "Carte thermique Trust"])
st.sidebar.markdown("---")
st.sidebar.markdown("<span style='color:#64748B; font-size:0.8rem;'>Mis à jour : 23:44 UTC</span>", unsafe_allow_html=True)
st.sidebar.markdown("<span style='color:#94A3B8; font-size:0.75rem;'>Bac à sable du cadre de simulation</span>", unsafe_allow_html=True)

# Le bouton rafraîchit mais charge la même graine, assurant la stabilité requise par l'IA
if st.sidebar.button("Rafraîchir la télémétrie", use_container_width=True):
    st.rerun()

# Configurations Graphiques communes
RISK_COLORS = {"critical": "#EF4444", "high": "#F97316", "medium": "#F59E0B", "low": "#10B981", "info": "#64748B"}
STATE_COLORS = {"active": "#10B981", "provisioned": "#3B82F6", "suspended": "#F59E0B", "orphaned": "#EF4444", "decommissioned": "#94A3B8", "pending_approval": "#8B5CF6"}
PLOT_THEME = {"paper_bgcolor": "rgba(0,0,0,0)", "plot_bgcolor": "rgba(0,0,0,0)", "margin": dict(l=20, r=20, t=30, b=20)}

# ─── PAGE 1: APERÇU DE LA FLOTTE ──────────────────────────────────────────────
if page == "Aperçu de la flotte":
    st.markdown('<div class="dashboard-title">Aperçu de la flotte</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-subtitle">Microsoft Agent Governance Toolkit (MIT) — Contrôle de découverte des actifs</div>', unsafe_allow_html=True)
    
    total = len(adf)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Agents", total)
    c2.metric("Instances Actives", len(adf[adf["state"]=="active"]))
    c3.metric("Agents de l'ombre", len(adf[~adf["has_identity"]]))
    c4.metric("Nœuds Orphelins", len(adf[adf["state"]=="orphaned"]))
    c5.metric("Risques Critiques", len(adf[adf["risk_level"]=="critical"]))
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-container"><div class="chart-title">Allocations des agents par type principal</div>', unsafe_allow_html=True)
        tc = adf["type"].value_counts().reset_index(); tc.columns = ["type", "count"]
        fig = px.bar(tc, x="type", y="count", color="type", color_discrete_sequence=px.colors.sequential.YlGnBu_r).update_layout(**PLOT_THEME, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="chart-container"><div class="chart-title">États globaux du cycle de vie</div>', unsafe_allow_html=True)
        sc = adf["state"].value_counts().reset_index(); sc.columns = ["state", "count"]
        fig = px.pie(sc, values="count", names="state", color="state", color_discrete_map=STATE_COLORS).update_layout(**PLOT_THEME)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.subheader("Registre du périmètre central de la flotte")
    st.dataframe(adf[["name","type","state","owner","risk_level","risk_score","trust_score","has_identity","heartbeat_count"]].sort_values("risk_score", ascending=False), use_container_width=True, height=350)

# ─── PAGE 2: AGENTS DE L'OMBRE ────────────────────────────────────────────────
elif page == "Agents de l'ombre":
    st.markdown('<div class="dashboard-title">Incidents d\'agents de l\'ombre</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-subtitle">Environnements d\'exécution actifs isolés fonctionnant sans enregistrement cryptographique.</div>', unsafe_allow_html=True)
    
    sdf = adf[~adf["has_identity"]].sort_values("risk_score", ascending=False)
    if sdf.empty:
        st.markdown('<div class="badge-success">Objectif de conformité atteint : 0 charge de travail fantôme détectée.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="badge-error">Anomalies relevées : {len(sdf)} instances actives non enregistrées contournant les couches d\'authentification.</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        for _, a in sdf.iterrows():
            with st.expander(f"Alerte sécurité : {a['name']} ({a['type']}) — Pondération du risque : {a['risk_score']}/100"):
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"**État actuel :** <span style='color:{STATE_COLORS.get(a['state'], '#000')}; font-weight:bold;'>{a['state']}</span>", unsafe_allow_html=True)
                c2.markdown(f"**Sous-réseau latent / Domaine :** <br><span style='color:#10B981; font-size:0.85rem;'>{a['owner']}</span>", unsafe_allow_html=True)
                c3.markdown(f"**Événements observés :** {a['evidence_count']} <br>entrée de télémétrie", unsafe_allow_html=True)
                st.markdown(f'<div class="chart-container" style="background-color:#EFF6FF; border:1px solid #BFDBFE; margin-top:1rem; color:#1E40AF; padding:10px 15px; border-radius:6px; font-size:0.9rem;"><b>Actions de remédiation requises :</b> 1) Attacher la signature JWT signée, 2) Définir la propriété de l\'administrateur d\'entreprise, 3) Déploiement local d\'un intercepteur de politique AGT.</div>', unsafe_allow_html=True)

# ─── PAGE 3: MONITEUR DU CYCLE DE VIE ──────────────────────────────────────────
elif page == "Moniteur du cycle de vie":
    st.markdown('<div class="dashboard-title">Pipeline des opérations du cycle de vie</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-subtitle">Mesures indiquant les latences de déploiement depuis les environnements de test jusqu\'à la production.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container"><div class="chart-title">Agrégations du pipeline d\'approvisionnement</div>', unsafe_allow_html=True)
    states = ["pending_approval", "provisioned", "active", "suspended", "orphaned", "decommissioned"]
    counts = [len(adf[adf["state"]==s]) for s in states]
    fig = go.Figure(go.Funnel(y=states, x=counts, textinfo="value+percent initial", marker=dict(color=["#E2E8F0","#CBD5E1","#94A3B8","#64748B","#475569","#334155"]))).update_layout(**PLOT_THEME)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.subheader("Transitions récentes de l'état de la topologie du système")
    st.dataframe(ldf.head(50), use_container_width=True, height=350)

# ─── PAGE 4: FLUX DE POLITIQUES ───────────────────────────────────────────────
elif page == "Flux de politiques":
    st.markdown('<div class="dashboard-title">Audit d\'interception des politiques au moment de l\'exécution</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-subtitle">Journaux complets suivant les boucles de validation évaluées par le moteur de politique AGT.</div>', unsafe_allow_html=True)
    
    total = len(pdf)
    allows = len(pdf[pdf["decision"]=="allow"])
    denies = len(pdf[pdf["decision"]=="deny"])
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Évaluations", total)
    c2.metric("Décisions : Approuvées", allows)
    c3.metric("Décisions : Interceptées", denies)
    c4.metric("Latence moyenne", f"{pdf['latency_ms'].mean():.2f} ms")
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, col2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-container"><div class="chart-title">Assertions d\'atténuation par type d\'appel</div>', unsafe_allow_html=True)
        ad = pdf.groupby(["action","decision"]).size().reset_index(name="count")
        fig = px.bar(ad, x="action", y="count", color="decision", color_discrete_map={"allow":"#10B981","deny":"#EF4444","escalate":"#F59E0B"}, barmode="stack").update_layout(**PLOT_THEME)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="chart-container"><div class="chart-title">Répartition globale de l\'application</div>', unsafe_allow_html=True)
        dc = pdf["decision"].value_counts().reset_index(); dc.columns = ["decision","count"]
        fig = px.pie(dc, values="count", names="decision", color="decision", color_discrete_map={"allow":"#10B981","deny":"#EF4444","escalate":"#F59E0B"}).update_layout(**PLOT_THEME)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.subheader("Registre d'audit immuable du grand livre SIEM")
    st.dataframe(pdf.head(50), use_container_width=True, height=350)

# ─── PAGE 5: CARTE THERMIQUE TRUST ────────────────────────────────────────────
elif page == "Carte thermique Trust":
    st.markdown('<div class="dashboard-title">Matrice de confiance cryptographique des interactions</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-subtitle">Matrices d\'évaluation du score de confiance dynamique analysant les boucles d\'exécution actives.</div>', unsafe_allow_html=True)
    
    if tdf.empty:
        st.info("Aucun pipeline de messagerie inter-agents actuellement ouvert.")
    else:
        st.markdown('<div class="chart-container"><div class="chart-title">Score de confiance dynamique des communications inter-agents</div>', unsafe_allow_html=True)
        pivot = tdf.pivot_table(values="trust_score", index="from_agent", columns="to_agent", fill_value=0)
        fig = px.imshow(pivot, color_continuous_scale="YlGnBu", zmin=0, zmax=1000, labels={"color":"Valeur de confiance"}).update_layout(**PLOT_THEME)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)