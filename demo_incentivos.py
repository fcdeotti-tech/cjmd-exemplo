import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E CSS CORPORATIVO
# ==========================================
st.set_page_config(page_title="Incentives Clinic - Route Automotive", layout="wide", page_icon="📈")

st.markdown("""
<style>
    /* Tema Claro Corporativo (Estilo PDF Route Automotive) */
    .stApp { background-color: #F8FAFC; color: #0F172A; font-family: 'Segoe UI', Arial, sans-serif; }
    h1, h2, h3, h4 { color: #002060 !important; font-family: 'Segoe UI', Arial, sans-serif; font-weight: 700; }
    
    /* Cabeçalho Customizado */
    .header-container { border-bottom: 3px solid #002060; padding-bottom: 10px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: flex-end;}
    .header-title { font-size: 28px; font-weight: 800; color: #002060; margin: 0; }
    .header-subtitle { font-size: 16px; color: #64748B; margin: 0; }
    .route-logo { font-size: 22px; font-weight: 900; color: #002060; letter-spacing: 1px; text-align: right; line-height: 1.2;}
    .route-logo span { color: #00B0F0; font-weight: 400; font-size: 14px; letter-spacing: 3px; display: block;}

    /* Cards de Insight e Metodologia */
    .insight-box { background-color: #FFFFFF; border-left: 6px solid #00B0F0; padding: 20px; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 25px; }
    .insight-title { font-weight: 800; color: #002060; font-size: 16px; margin-bottom: 8px; display: block; text-transform: uppercase;}
    
    .alert-box { background-color: #FFF5F5; border-left: 6px solid #E53E3E; padding: 20px; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 25px; }
    .alert-title { font-weight: 800; color: #E53E3E; font-size: 16px; margin-bottom: 8px; display: block; text-transform: uppercase;}

    /* Customização de Tabs */
    .stTabs [data-baseweb="tab-list"] { background-color: #FFFFFF; padding: 10px 10px 0 10px; border-radius: 8px 8px 0 0; border-bottom: 2px solid #E2E8F0;}
    .stTabs [data-baseweb="tab"] { color: #64748B; font-weight: 600; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { color: #002060 !important; border-bottom-color: #00B0F0 !important; border-bottom-width: 3px !important;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CABEÇALHO GLOBAL
# ==========================================
st.markdown("""
<div class="header-container">
    <div>
        <h1 class="header-title">Incentives Clinic</h1>
        <p class="header-subtitle">DADOS FICTÍCIOS | ILUSTRATIVO | Simulador Integrado MaxDiff + Conjoint</p>
    </div>
    <div class="route-logo">
        ROUTE
        <span>AUTOMOTIVE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 3. DADOS FAKE (BASEADOS NO PDF)
# ==========================================
BENEFICIOS = [
    "Taxa de Juros Subsidiada",
    "Desconto Direto (Bônus Varejo)",
    "Supervalorização do Usado",
    "Seguro Grátis",
    "IPVA Grátis",
    "Manutenção Grátis",
    "Documentação Grátis",
    "Brindes / Acessórios"
]

def get_maxdiff_ranking():
    # Baseado na página 2 do PDF
    scores = [82, 76, 68, 55, 45, 30, 22, 15]
    return pd.DataFrame({'Incentivo': BENEFICIOS, 'Score (0-100)': scores}).sort_values('Score (0-100)', ascending=True)

def get_maxdiff_heatmap():
    # Baseado na página 14 do PDF (Consenso vs Polarizado)
    np.random.seed(42)
    data = {
        'Apostadores': [85, 78, 70, 50, 42, 25, 18, 10],
        'Potenciais':  [80, 75, 65, 58, 48, 30, 22, 18],
        'Indecisos':   [81, 74, 69, 45, 40, 35, 28, 20],
        'Refratários': [83, 76, 68, 62, 55, 28, 20, 15]
    }
    df = pd.DataFrame(data, index=BENEFICIOS)
    # Calculando desvio padrão para definir Consenso
    df['Desvio Padrão'] = df.std(axis=1)
    df['Diagnóstico'] = df['Desvio Padrão'].apply(lambda x: 'Consenso' if x < 6 else 'Polarizado')
    return df

def get_turf_data():
    # Baseado na página 14 do PDF
    steps = ["1", "2", "3", "4", "5"]
    reach_acumulado = [42, 61, 74, 81, 85]
    incremento_texto = ["+42pp", "+19pp", "+13pp", "+7pp", "+4pp"]
    incentivos = [
        "1. Taxa Subsidiada",
        "2. + Bônus Varejo",
        "3. + Super do Usado",
        "4. + Seguro Grátis",
        "5. + IPVA Grátis"
    ]
    return pd.DataFrame({
        'Nº de Incentivos': steps,
        'Reach Acumulado (%)': reach_acumulado,
        'Incremento': incremento_texto,
        'Combinação': incentivos
    })

# ==========================================
# 4. RENDERIZAÇÃO: MÓDULO MAXDIFF
# ==========================================
st.markdown("### Módulo 1: Otimização e Triagem de Incentivos (MaxDiff)")

tab1, tab2, tab3 = st.tabs(["📊 1. Ranking Geral", "🗺️ 2. Heatmap por Persona", "📈 3. Análise TURF (Reach)"])

with tab1:
    col_text, col_chart = st.columns([1, 2])
    with col_text:
        st.markdown("""
        <div class="insight-box">
            <span class="insight-title">Principais Insights</span>
            <p><b>#1 Taxa Subsidiada (82)</b><br>Incentivo mais valorizado. Ativa tanto financiadores quanto clientes à vista.</p>
            <p><b>#2 Bônus de Varejo (76)</b><br>Alta percepção de 'dinheiro real'; mais eficaz para fechar o negócio.</p>
            <p><b>#3 Super do Usado (68)</b><br>Forte 'pull' para quem tem carro a dar na troca; sensível ao valor FIPE.</p>
        </div>
        <div class="alert-box">
            <span class="alert-title">Benefícios Extras (22-55)</span>
            <p>Seguro, IPVA e Documentação atraem leads, mas raramente fecham negócio sozinhos se os 3 pilares financeiros acima não estiverem ajustados.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_chart:
        df_rank = get_maxdiff_ranking()
        fig_rank = px.bar(df_rank, x='Score (0-100)', y='Incentivo', orientation='h', text_auto='.0f')
        fig_rank.update_traces(marker_color='#002060', textposition='outside')
        fig_rank.update_layout(
            title="Ranking de Importância dos Incentivos (0-100)",
            xaxis_title="Score MaxDiff", yaxis_title=None,
            template="plotly_white", height=450,
            xaxis=dict(range=[0, 100])
        )
        st.plotly_chart(fig_rank, use_container_width=True)

with tab2:
    st.markdown("Avaliamos se um benefício é amado por todos (Consenso) ou se ele agrada apenas um nicho específico (Polarizado).")
    df_heat = get_maxdiff_heatmap()
    
    colA, colB = st.columns([2, 1])
    with colA:
        # Extrai apenas as colunas numéricas para o gráfico
        heat_data = df_heat[['Apostadores', 'Potenciais', 'Indecisos', 'Refratários']]
        fig_heat = px.imshow(
            heat_data, 
            text_auto=True, 
            aspect="auto",
            color_continuous_scale="Blues",
            title="MaxDiff Score Médio por Persona"
        )
        fig_heat.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig_heat, use_container_width=True)
        
    with colB:
        st.markdown("<br><br>", unsafe_allow_html=True) # Espaçamento
        st.dataframe(df_heat[['Diagnóstico']], use_container_width=True, height=350)
        st.caption("🚨 **Dica Route:** Evite incentivos *Polarizados* (como Seguro Grátis) em campanhas de TV amplas. Use-os apenas em ativações de CRM 1:1.")

with tab3:
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        df_turf = get_turf_data()
        fig_turf = go.Figure()
        
        # Barras de Incremento
        fig_turf.add_trace(go.Bar(
            x=df_turf['Nº de Incentivos'], 
            y=df_turf['Reach Acumulado (%)'],
            text=df_turf['Incremento'],
            textposition='inside',
            marker_color='#E2E8F0',
            name='Reach'
        ))
        
        # Linha de Acumulado
        fig_turf.add_trace(go.Scatter(
            x=df_turf['Nº de Incentivos'], 
            y=df_turf['Reach Acumulado (%)'],
            mode='lines+markers+text',
            text=df_turf['Reach Acumulado (%)'].astype(str) + '%',
            textposition='top center',
            line=dict(color='#00B0F0', width=4),
            marker=dict(size=12, color='#002060'),
            name='Acumulado'
        ))
        
        # Ponto de inflexão
        fig_turf.add_vline(x=2, line_dash="dash", line_color="#E53E3E", annotation_text="Ponto de Inflexão")
        
        fig_turf.update_layout(
            title="Reach Acumulado por Combinação de Incentivos",
            xaxis_title="Quantidade de Incentivos no Pacote",
            yaxis_title="Reach (%)",
            yaxis=dict(range=[0, 100]),
            template="plotly_white",
            height=450,
            showlegend=False
        )
        st.plotly_chart(fig_turf, use_container_width=True)
        
    with col2:
        st.markdown("""
        <div class="insight-box" style="margin-top: 50px;">
            <span class="insight-title">Sugestão Route Automotive</span>
            <h3 style="color: #00B0F0; margin-top: 10px;">74% de Alcance</h3>
            <p><b>Combinação Ótima:</b><br>Taxa Subsidiada + Bônus Varejo + Supervalorização do Usado.</p>
            <p style="color: #E53E3E;"><b>O Ponto de Inflexão ocorre em 3 incentivos.</b> O 4º e o 5º incentivos (Seguro e IPVA) trazem menos de 8 p.p. de alcance adicional e geram custo-benefício negativo para a montadora.</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ==========================================
# 5. RENDERIZAÇÃO: MÓDULO CONJOINT
# ==========================================
st.markdown("### Módulo 2: Simulador Financeiro (Conjoint Analysis)")
st.markdown("Combinamos os pacotes campeões do MaxDiff com o Preço de Tabela do veículo para prever a conversão real na loja.")

col_sim1, col_sim2, col_sim3 = st.columns(3)

tiers = ["Preço Cheio (+2%)", "Preço Sugerido (Tabela)", "Desconto Tático (-3%)", "Desconto Agressivo (-6%)"]

with col_sim1:
    st.markdown("**Pacote A: Taxa 0% (24x)**")
    t1 = st.selectbox("Selecione o Preço (Pacote A)", tiers, index=1)
with col_sim2:
    st.markdown("**Pacote B: Bônus Usado (R$ 5k)**")
    t2 = st.selectbox("Selecione o Preço (Pacote B)", tiers, index=2)
with col_sim3:
    st.markdown("**Pacote C: Sem Benefícios**")
    t3 = st.selectbox("Selecione o Preço (Pacote C)", tiers, index=3)

# Lógica matemática fake simplificada para ilustrar o share
base_shares = np.array([45, 35, 20])
modifiers = np.array([
    1 - (tiers.index(t1) * 0.15),
    1 - (tiers.index(t2) * 0.15),
    1 - (tiers.index(t3) * 0.25)
])
raw_scores = base_shares * (2 - modifiers)
final_shares = (raw_scores / raw_scores.sum()) * 100

df_share = pd.DataFrame({
    'Oferta na Concessionária': ['Pacote A (Taxa 0%)', 'Pacote B (Bônus Usado)', 'Pacote C (Apenas Desconto N.F.)'],
    'Share de Escolha (%)': final_shares
}).sort_values('Share de Escolha (%)', ascending=False)

fig_conjoint = px.bar(df_share, x='Share de Escolha (%)', y='Oferta na Concessionária', orientation='h', text_auto='.1f')
fig_conjoint.update_traces(marker_color='#00B0F0')
fig_conjoint.update_layout(template="plotly_white", height=300)

st.plotly_chart(fig_conjoint, use_container_width=True)

st.markdown("""
<div class="insight-box" style="border-color: #002060;">
    <span class="insight-title">Análise de Elasticidade Comercial</span>
    <p>O simulador demonstra como a <b>percepção psicológica do benefício</b> (ex: Taxa Zero) muitas vezes supera o <b>desconto real em dinheiro</b> na nota fiscal (Pacote C). Isso permite que a montadora proteja sua margem de lucro mantendo o preço de tabela, financiando apenas a taxa através do banco da montadora.</p>
</div>
""", unsafe_allow_html=True)