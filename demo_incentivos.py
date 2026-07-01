import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E BRANDING INSIGHTS&ETC
# ==========================================
st.set_page_config(page_title="Product & Pricing Simulator - Insights&Etc", layout="wide", page_icon="🏍️")

# Aplicação do Dark Mode e Cores da Marca (Insights&Etc)
st.markdown("""
<style>
    /* Fundo Dark Mode Corporativo e Texto Neutro */
    .stApp { background-color: #0A192F; color: #E2E8F0; font-family: 'Montserrat', sans-serif; }
    h1, h2, h3, h4 { color: #FFFFFF !important; font-weight: 600; font-family: 'Montserrat', sans-serif; }
    
    /* Cabeçalho Insights&Etc */
    .header-container { border-bottom: 2px solid #00FFFF; padding-bottom: 15px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: flex-end;}
    .header-title { font-size: 26px; font-weight: 700; color: #FFFFFF; margin: 0; }
    .header-subtitle { font-size: 14px; color: #8892B0; margin: 0; font-family: 'Roboto', sans-serif; }
    .brand-logo { font-size: 28px; font-weight: 600; color: #0A192F; text-align: right; line-height: 1; background-color: #FFFFFF; padding: 10px 15px; border-radius: 4px; }
    
    /* Cards Analíticos */
    .insight-box { background-color: #112240; border-left: 4px solid #00FFFF; padding: 20px; border-radius: 6px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); margin-bottom: 25px; font-family: 'Roboto', sans-serif; }
    .insight-title { font-weight: 700; color: #00FFFF; font-size: 16px; margin-bottom: 10px; display: block; text-transform: uppercase; letter-spacing: 1px;}
    
    .alert-box { background-color: #112240; border-left: 4px solid #FF6B6B; padding: 20px; border-radius: 6px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); margin-bottom: 25px; font-family: 'Roboto', sans-serif; }
    .alert-title { font-weight: 700; color: #FF6B6B; font-size: 16px; margin-bottom: 10px; display: block; text-transform: uppercase; letter-spacing: 1px;}

    /* Abas Customizadas */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; border-bottom: 1px solid #233554;}
    .stTabs [data-baseweb="tab"] { color: #8892B0; font-weight: 500; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { color: #00FFFF !important; border-bottom-color: #00FFFF !important; border-bottom-width: 3px !important;}
</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown("""
<div class="header-container">
    <div>
        <h1 class="header-title">Product Features & Pricing Simulator</h1>
        <p class="header-subtitle">YAMAHA BRASIL | Simulador Integrado MaxDiff + Conjoint (Dados Ilustrativos)</p>
    </div>
    <div style="font-size: 28px; font-weight: 600; color: #FFFFFF; font-family: 'Montserrat', sans-serif;">
        INSIGHTS<span style="color:#FF6B6B; font-weight:700;">&</span><span style="font-weight:400;">Etc</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 2. FILTROS LATERAIS (SEGMENTAÇÃO)
# ==========================================
st.sidebar.markdown("""<div style="font-size: 20px; font-weight: 600; color: #FFFFFF; margin-bottom: 20px;">
    INSIGHTS<span style="color:#FF6B6B; font-weight:700;">&</span><span style="font-weight:400;">Etc</span>
</div>""", unsafe_allow_html=True)

st.sidebar.header("🎯 Parâmetros de Análise")
segmentos_opts = ['Total Mercado', 'Scooter/Cub', 'Small Street/On-off', 'Middle Street/On-Off', 'Big Street / On-Off']
segmento_selecionado = st.sidebar.selectbox("Segmento de Atuação:", segmentos_opts)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Dica Analítica:** O filtro acima recalcula dinamicamente as utilidades da Conjoint e os scores da MaxDiff de acordo com a categoria da motocicleta.")

# ==========================================
# 3. DADOS MOCKADOS (Baseados na Proposta da Yamaha)
# ==========================================
def get_maxdiff_data():
    # Ref: Proposta Pg 7 - Share of Preference
    return pd.DataFrame({
        'Atributo': ['Freios ABS', 'Painel Digital', 'Faróis de LED', 'Chave presencial', 'Botão de START', 'Suspensão a gás', 'Baú traseiro', 'Bagageiro 2 capacetes'],
        'Categoria': ['Segurança', 'Tecnologia', 'Design/Segurança', 'Comodidade', 'Comodidade', 'Dinâmica', 'Carga', 'Carga'],
        'Score (%)': [22, 18, 15, 12, 11, 9, 8, 5]
    }).sort_values('Score (%)', ascending=True)

def get_conjoint_importance():
    # Ref: Proposta Pg 10 - Análise de Importância
    return pd.DataFrame({
        'Fator': ['Preço', 'Potência', 'Característica Destaque', 'Modelo', 'Painel'],
        'Importância (%)': [41, 23, 16, 12, 8]
    }).sort_values('Importância (%)', ascending=True)

def get_mwtp_data():
    # Ref: Proposta Pg 11 - Disposição marginal a pagar
    return pd.DataFrame({
        'Feature': ['Potência 300cc', 'Freios ABS', 'Potência 160cc', 'Painel Digital', 'Faróis de LED', 'Chave presencial', 'Botão de START', 'Baú traseiro'],
        'MWTP (R$)': [2340, 1450, 1120, 980, 760, 540, 320, 280]
    }).sort_values('MWTP (R$)', ascending=True)

def get_adoption_curve():
    # Ref: Proposta Pg 13 - Share por segmento e simulações
    return pd.DataFrame({
        'Cenário': ['1. Versão base', '2. + Freios ABS', '3. + Painel Digital', '4. + Potência 300cc'],
        'Yamaha': [36, 44, 49, 58],
        'Concorrência': [52, 46, 42, 34],
        'Nenhuma': [12, 10, 9, 8]
    })

# Paleta de cores da Insights&Etc para gráficos
CHART_COLORS = ['#00FFFF', '#009999', '#FF6B6B', '#CC5555', '#4A90E2']

# ==========================================
# 4. RENDERIZAÇÃO DO DASHBOARD
# ==========================================
tab_mxd, tab_conj, tab_mwtp, tab_sim = st.tabs([
    "📊 1. MaxDiff (Priorização)", 
    "⚖️ 2. Conjoint (Utilidades)", 
    "💰 3. MWTP (Valor em R$)", 
    "📈 4. Simulador Competitivo"
])

# --- ABA 1: MAXDIFF ---
with tab_mxd:
    st.markdown("### Hierarquia de Atributos (Maximum Difference Scaling)")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        df_mxd = get_maxdiff_data()
        fig_mxd = px.bar(df_mxd, x='Score (%)', y='Atributo', orientation='h', color='Categoria', text_auto='.0f', color_discrete_sequence=CHART_COLORS)
        fig_mxd.update_layout(
            plot_bgcolor='#0A192F', paper_bgcolor='#0A192F', font_color='#E2E8F0',
            xaxis_title="Share of Preference (%)", yaxis_title=None, height=450,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_mxd, use_container_width=True)
        
    with col2:
        st.markdown("""
        <div class="insight-box">
            <span class="insight-title">Interpretação do Cliente</span>
            <p>Os <b>Freios ABS (22%)</b> e o <b>Painel Digital (18%)</b> dominam a preferência do consumidor na composição da motocicleta.</p>
            <p>Itens de carga, como o <i>Bagageiro para 2 capacetes</i>, possuem relevância marginal e não devem ser tratados como diferenciais estratégicos de precificação primária.</p>
        </div>
        """, unsafe_allow_html=True)

# --- ABA 2: CONJOINT IMPORTANCE ---
with tab_conj:
    st.markdown("### Decomposição da Decisão de Compra")
    c1, c2 = st.columns(2)
    
    with c1:
        df_imp = get_conjoint_importance()
        fig_imp = px.bar(df_imp, x='Importância (%)', y='Fator', orientation='h', text_auto='.0f')
        fig_imp.update_traces(marker_color='#00FFFF', textposition='outside')
        fig_imp.update_layout(plot_bgcolor='#0A192F', paper_bgcolor='#0A192F', font_color='#E2E8F0', xaxis_title="Importância Relativa (%)", yaxis_title=None, height=350)
        st.plotly_chart(fig_imp, use_container_width=True)
        
    with c2:
        st.markdown("""
        <div class="alert-box">
            <span class="alert-title">Sensibilidade ao Fator Preço</span>
            <p>O <b>Preço (41%)</b> é o atributo mais restritivo. Contudo, a combinação de <b>Potência (23%)</b> e <b>Destaques Tecnológicos (16%)</b> soma 39% do peso da decisão, provando que o consumidor está disposto a fazer trade-offs se a proposta de valor for clara.</p>
        </div>
        """, unsafe_allow_html=True)

# --- ABA 3: MWTP (DISPOSIÇÃO MARGINAL A PAGAR) ---
with tab_mwtp:
    st.markdown("### Precificação Baseada em Valor (Marginal Willingness to Pay)")
    st.write("Quantos reais o cliente aceita pagar a mais em relação a uma versão base de entrada para ter a feature adicionada.")
    
    df_mwtp = get_mwtp_data()
    fig_mwtp = px.bar(df_mwtp, x='MWTP (R$)', y='Feature', orientation='h', text_auto='R$ .0f')
    fig_mwtp.update_traces(marker_color='#FF6B6B', textposition='outside')
    fig_mwtp.update_layout(plot_bgcolor='#0A192F', paper_bgcolor='#0A192F', font_color='#E2E8F0', xaxis_title="Disposição a Pagar (R$)", yaxis_title=None, height=450)
    st.plotly_chart(fig_mwtp, use_container_width=True)

# --- ABA 4: SIMULADOR DE CENÁRIOS E SHARE ---
with tab_sim:
    st.markdown("### Simulador de Curva de Adoção e Share of Preference")
    st.write("Impacto da inserção de pacotes tecnológicos sobre a captura de Share frente à concorrência.")
    
    df_adopt = get_adoption_curve()
    
    fig_adopt = go.Figure()
    fig_adopt.add_trace(go.Bar(x=df_adopt['Cenário'], y=df_adopt['Yamaha'], name='Yamaha', marker_color='#00FFFF', text=df_adopt['Yamaha'].astype(str) + '%', textposition='inside'))
    fig_adopt.add_trace(go.Bar(x=df_adopt['Cenário'], y=df_adopt['Concorrência'], name='Concorrência', marker_color='#4A90E2', text=df_adopt['Concorrência'].astype(str) + '%', textposition='inside'))
    fig_adopt.add_trace(go.Bar(x=df_adopt['Cenário'], y=df_adopt['Nenhuma'], name='Nenhuma', marker_color='#2D3436', text=df_adopt['Nenhuma'].astype(str) + '%', textposition='inside'))
    
    fig_adopt.update_layout(
        barmode='stack', plot_bgcolor='#0A192F', paper_bgcolor='#0A192F', font_color='#E2E8F0',
        yaxis_title="Share of Preference (%)", height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_adopt, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box" style="border-color: #00FFFF;">
        <span class="insight-title">Análise de Elasticidade Comercial</span>
        <p>A simples adição do <b>Painel Digital</b> ao pacote ABS eleva o share de 44% para 49%[cite: 910, 911]. O upgrade de motorização para 300cc consolida a liderança absoluta no cenário simulado (58%)[cite: 909], retirando volume direto do principal concorrente.</p>
    </div>
    """, unsafe_allow_html=True)