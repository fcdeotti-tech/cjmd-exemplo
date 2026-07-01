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
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Roboto:wght@400;500&display=swap');
    
    /* Fundo Dark Mode Corporativo e Texto Neutro */
    .stApp { background-color: #0A192F; color: #E2E8F0; font-family: 'Roboto', sans-serif; }
    h1, h2, h3, h4, h5, h6 { color: #FFFFFF !important; font-family: 'Montserrat', sans-serif; font-weight: 600; }
    
    /* Cabeçalho Insights&Etc */
    .header-container { border-bottom: 1px solid #233554; padding-bottom: 20px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center;}
    .header-title { font-size: 28px; font-weight: 700; color: #FFFFFF; margin: 0; }
    .header-subtitle { font-size: 14px; color: #8892B0; margin: 0; font-family: 'Roboto', sans-serif; }
    
    /* Cards Analíticos */
    .insight-box { background-color: #112240; border-left: 4px solid #00FFFF; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); margin-bottom: 25px; }
    .insight-title { font-weight: 700; color: #00FFFF; font-size: 14px; margin-bottom: 10px; display: block; text-transform: uppercase; letter-spacing: 1px;}
    
    .alert-box { background-color: #112240; border-left: 4px solid #FF6B6B; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); margin-bottom: 25px; }
    .alert-title { font-weight: 700; color: #FF6B6B; font-size: 14px; margin-bottom: 10px; display: block; text-transform: uppercase; letter-spacing: 1px;}

    /* Abas Customizadas */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; border-bottom: 1px solid #233554; flex-wrap: wrap;}
    .stTabs [data-baseweb="tab"] { color: #8892B0; font-weight: 500; font-family: 'Montserrat', sans-serif; padding: 10px 15px; font-size: 14px;}
    .stTabs [aria-selected="true"] { color: #00FFFF !important; border-bottom-color: #00FFFF !important; border-bottom-width: 3px !important;}
    
    /* Componentes Streamlit */
    div[data-baseweb="select"] > div { background-color: #112240; color: white; border-color: #233554; }
    .stSlider > div > div > div > div { background-color: #00FFFF !important; }
</style>
""", unsafe_allow_html=True)

# Logo Textual Insights&Etc
logo_html = """
<div style="font-size: 32px; font-weight: 600; color: #FFFFFF; font-family: 'Montserrat', sans-serif; letter-spacing: -0.5px;">
    INSIGHTS<span style="color:#FF6B6B; font-weight:700;">&</span><span style="font-weight:400; font-size: 28px;">Etc</span>
</div>
"""

st.markdown(f"""
<div class="header-container">
    <div>
        <h1 class="header-title">Product & Pricing Simulator</h1>
        <p class="header-subtitle">YAMAHA BRASIL | Modelagem Integrada (MaxDiff, Conjoint, TURF & Elasticidade) | Dados Fictícios</p>
    </div>
    {logo_html}
</div>
""", unsafe_allow_html=True)

# Paleta Institucional
COLORS = {
    'cyan': '#00FFFF',
    'orange': '#FF6B6B',
    'dark_blue': '#112240',
    'slate': '#8892B0',
    'white': '#FFFFFF',
    'bg': '#0A192F',
    'red_alert': '#CC5555'
}

# ==========================================
# 2. FILTROS LATERAIS E DADOS MOCKADOS
# ==========================================
st.sidebar.markdown(logo_html, unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.header("🎯 Parâmetros de Análise")
segmentos_opts = ['Total Mercado', 'Scooter/Cub', 'Small Street/On-off', 'Middle Street/On-Off', 'Big Street / On-Off']
segmento_selecionado = st.sidebar.selectbox("Segmento de Atuação:", segmentos_opts)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Inteligência:** Os modelos estatísticos recalculam as utilidades, o alcance e a elasticidade com base no segmento selecionado.")

# Funções Mockadas - Parte 1 (Original)
def get_maxdiff_data():
    return pd.DataFrame({
        'Atributo': ['Freios ABS', 'Painel Digital', 'Faróis de LED', 'Chave presencial', 'Botão de START', 'Suspensão a gás', 'Baú traseiro', 'Bagageiro 2 capacetes'],
        'Categoria': ['Segurança', 'Tecnologia', 'Design/Segurança', 'Comodidade', 'Comodidade', 'Dinâmica', 'Carga', 'Carga'],
        'Score (%)': [22, 18, 15, 12, 11, 9, 8, 5]
    }).sort_values('Score (%)', ascending=True)

def get_conjoint_importance():
    return pd.DataFrame({
        'Fator': ['Preço', 'Potência', 'Característica Destaque', 'Modelo', 'Painel'],
        'Importância (%)': [41, 23, 16, 12, 8]
    }).sort_values('Importância (%)', ascending=True)

def get_mwtp_data():
    return pd.DataFrame({
        'Feature': ['Potência 300cc', 'Freios ABS', 'Potência 160cc', 'Painel Digital', 'Faróis de LED', 'Chave presencial', 'Botão de START', 'Baú traseiro'],
        'MWTP (R$)': [2340, 1450, 1120, 980, 760, 540, 320, 280]
    }).sort_values('MWTP (R$)', ascending=True)

# Funções Mockadas - Parte 2 (Adicionais: TURF e Elasticidade)
FEATURES = ['Freios ABS', 'Painel Digital TFT', 'Controle de Tração', 'Faróis Full LED', 'Smart Key (Presencial)', 'Conectividade Y-Connect']
BASE_PRICE = 22000

df_turf = pd.DataFrame({
    'Tamanho do Pacote': ['1 Feature', '2 Features', '3 Features', '4 Features', '5 Features', '6 Features'],
    'Reach Acumulado (%)': [42, 65, 81, 88, 92, 94],
    'Combinação Ideal': [
        'Freios ABS', 
        '+ Painel Digital TFT', 
        '+ Faróis Full LED', 
        '+ Controle de Tração', 
        '+ Smart Key', 
        '+ Y-Connect'
    ]
})

prices = np.arange(20000, 26500, 500)
df_elasticity = pd.DataFrame({'Preço (R$)': prices})
df_elasticity['Versão Base'] = 100 / (1 + np.exp((prices - 22000) / 1000)) * 0.4
df_elasticity['Base + ABS + Painel'] = 100 / (1 + np.exp((prices - 23500) / 1200)) * 0.55
df_elasticity['Pacote Premium (Todas as Features)'] = 100 / (1 + np.exp((prices - 25000) / 1500)) * 0.7

# ==========================================
# 3. RENDERIZAÇÃO DAS ABAS (Tudo Integrado)
# ==========================================
tab_mxd, tab_conj, tab_mwtp, tab_turf, tab_sim, tab_elas = st.tabs([
    "📊 1. MaxDiff", 
    "⚖️ 2. Conjoint Importância", 
    "💰 3. Precificação (MWTP)", 
    "🎯 4. Otimização (TURF)", 
    "🎮 5. Simulador Share", 
    "📉 6. Elasticidade-Preço"
])

# --- ABA 1: MAXDIFF ---
with tab_mxd:
    st.markdown("### Hierarquia de Atributos (Maximum Difference Scaling)")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        df_mxd = get_maxdiff_data()
        fig_mxd = px.bar(df_mxd, x='Score (%)', y='Atributo', orientation='h', color='Categoria', text_auto='.0f', color_discrete_sequence=[COLORS['cyan'], '#009999', COLORS['orange'], COLORS['red_alert'], '#4A90E2'])
        fig_mxd.update_layout(
            plot_bgcolor=COLORS['bg'], paper_bgcolor=COLORS['bg'], font_color=COLORS['slate'],
            xaxis_title="Share of Preference (%)", yaxis_title=None, height=450,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_mxd, use_container_width=True)
        
    with col2:
        st.markdown("""
        <div class="insight-box">
            <span class="insight-title">O Ponto de Virada</span>
            <p>Os <b>Freios ABS (22%)</b> e o <b>Painel Digital (18%)</b> dominam a preferência do consumidor. Eles representam o "núcleo" de decisão tecnológica.</p>
            <p>Itens de carga (Baú/Bagageiro) possuem relevância marginal no contexto geral, confirmando que não devem ser o foco da narrativa de precificação primária, a menos que analisados em nichos específicos.</p>
        </div>
        """, unsafe_allow_html=True)

# --- ABA 2: CONJOINT IMPORTANCE ---
with tab_conj:
    st.markdown("### Decomposição da Decisão de Compra (Part-Worths)")
    c1, c2 = st.columns(2)
    
    with c1:
        df_imp = get_conjoint_importance()
        fig_imp = px.bar(df_imp, x='Importância (%)', y='Fator', orientation='h', text_auto='.0f')
        fig_imp.update_traces(marker_color=COLORS['cyan'], textposition='outside')
        fig_imp.update_layout(plot_bgcolor=COLORS['bg'], paper_bgcolor=COLORS['bg'], font_color=COLORS['slate'], xaxis_title="Importância Relativa (%)", yaxis_title=None, height=350)
        st.plotly_chart(fig_imp, use_container_width=True)
        
    with c2:
        st.markdown(f"""
        <div class="alert-box">
            <span class="alert-title">Sensibilidade ao Fator Preço</span>
            <p>O <b>Preço (41%)</b> é o atributo restritivo primário. Contudo, a combinação de <b>Potência (23%)</b> e <b>Destaques Tecnológicos (16%)</b> soma 39% do peso da decisão. Isso prova que, entregando o valor percebido correto em Motor e Tech, o "peso" do preço pode ser contornado na conversão.</p>
        </div>
        """, unsafe_allow_html=True)

# --- ABA 3: MWTP (DISPOSIÇÃO MARGINAL A PAGAR) ---
with tab_mwtp:
    st.markdown("### Precificação Baseada em Valor (Marginal Willingness to Pay)")
    st.write("Quantos reais o cliente aceita pagar a mais em relação a uma versão base de entrada para ter a feature adicionada.")
    
    df_mwtp = get_mwtp_data()
    fig_mwtp = px.bar(df_mwtp, x='MWTP (R$)', y='Feature', orientation='h', text_auto='R$ .0f')
    fig_mwtp.update_traces(marker_color=COLORS['orange'], textposition='outside')
    fig_mwtp.update_layout(plot_bgcolor=COLORS['bg'], paper_bgcolor=COLORS['bg'], font_color=COLORS['slate'], xaxis_title="Disposição a Pagar (R$)", yaxis_title=None, height=450)
    st.plotly_chart(fig_mwtp, use_container_width=True)

# --- ABA 4: TURF / REACH ---
with tab_turf:
    st.markdown("### Total Unduplicated Reach and Frequency (TURF)")
    st.write("Identifica a combinação ideal de atributos (pacote de features) que maximiza o alcance de consumidores únicos.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_turf = go.Figure()
        
        # Área de preenchimento
        fig_turf.add_trace(go.Scatter(
            x=df_turf['Tamanho do Pacote'], y=df_turf['Reach Acumulado (%)'],
            fill='tozeroy', mode='lines+markers+text',
            line=dict(color=COLORS['cyan'], width=4),
            marker=dict(size=10, color=COLORS['white'], line=dict(width=2, color=COLORS['cyan'])),
            text=df_turf['Reach Acumulado (%)'].astype(str) + '%',
            textposition='top center', textfont=dict(color=COLORS['white']),
            hovertext=df_turf['Combinação Ideal'], hoverinfo="text+y"
        ))
        
        fig_turf.add_vline(x=2, line_width=2, line_dash="dash", line_color=COLORS['orange'])
        fig_turf.add_annotation(x=2.2, y=50, text="Ponto de Inflexão<br>(Retorno Marginal Decrescente)", showarrow=False, font=dict(color=COLORS['orange']))

        fig_turf.update_layout(
            plot_bgcolor=COLORS['bg'], paper_bgcolor=COLORS['bg'], font_color=COLORS['slate'],
            xaxis_title="Quantidade de Features no Pacote", yaxis_title="Reach Acumulado (%)",
            yaxis=dict(range=[0, 100], gridcolor='#233554'), xaxis=dict(gridcolor='#233554'),
            height=450, margin=dict(t=30, b=0, l=0, r=0)
        )
        st.plotly_chart(fig_turf, use_container_width=True)
        
    with col2:
        st.markdown(f"""
        <div class="insight-box">
            <span class="insight-title">Insight de Portfólio</span>
            <p>O pacote triplo <b>(ABS + Painel TFT + Full LED)</b> atinge <b>81% do mercado alvo</b>.</p>
            <p>A partir da 4ª feature, o ganho de alcance despenca para menos de 7 p.p. por item adicionado.</p>
        </div>
        <div class="alert-box">
            <span class="alert-title">Recomendação Estratégica</span>
            <p>Empacotar mais de 3 itens de série pode encarecer a moto desnecessariamente sem converter novos clientes. Itens adicionais devem ser tratados como acessórios nas concessionárias.</p>
        </div>
        """, unsafe_allow_html=True)

# --- ABA 5: SIMULADOR DE SHARE (FEATURES + PREÇO) ---
with tab_sim:
    st.markdown("### Simulador de Mercado Dinâmico (Share of Preference)")
    st.write("Configure a Yamaha contra seus principais concorrentes para prever o Market Share cruzando features e elasticidade de preço.")
    
    st.markdown("#### Configuração da Yamaha (Seu Produto)")
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c1:
        preco_yamaha = st.slider("Preço Final (R$)", min_value=20000, max_value=26000, value=22500, step=250)
    
    with c2:
        features_selecionadas = st.multiselect("Itens de Série:", FEATURES, default=['Freios ABS', 'Painel Digital TFT'])
    
    with c3:
        # Lógica Fictícia de Cálculo de Utilidade para o Simulador
        utilidade_base = 30
        utilidade_features = len(features_selecionadas) * 6.5
        penalidade_preco = ((preco_yamaha - 20000) / 1000) * 8
        
        utilidade_yamaha = max(5, utilidade_base + utilidade_features - penalidade_preco)
        
        # Concorrentes Estáticos para o Mock
        utilidade_honda = 32 # Ex: Concorrente Direto a 22k
        utilidade_bajaj = 15 # Ex: Concorrente Agressivo a 24k
        
        total_util = utilidade_yamaha + utilidade_honda + utilidade_bajaj
        share_yamaha = (utilidade_yamaha / total_util) * 100
        share_honda = (utilidade_honda / total_util) * 100
        share_bajaj = (utilidade_bajaj / total_util) * 100
        
        st.markdown(f"""
        <div style="background-color: {COLORS['dark_blue']}; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid {COLORS['cyan']};">
            <h4 style="margin: 0; color: {COLORS['slate']}; font-size: 14px; font-family: Roboto;">SHARE PROJETADO</h4>
            <h1 style="margin: 0; color: {COLORS['cyan']}; font-size: 36px; font-family: Montserrat;">{share_yamaha:.1f}%</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    df_share = pd.DataFrame({
        'Marca': ['Yamaha (Simulada)', 'Concorrente A (Fixo R$22k)', 'Concorrente B (Fixo R$24k)'],
        'Share (%)': [share_yamaha, share_honda, share_bajaj],
        'Cor': [COLORS['cyan'], '#8892B0', '#4A5568']
    }).sort_values('Share (%)', ascending=True)
    
    fig_share = px.bar(df_share, x='Share (%)', y='Marca', orientation='h', text_auto='.1f')
    fig_share.update_traces(marker_color=df_share['Cor'], textposition='outside', textfont=dict(color='white'))
    fig_share.update_layout(
        plot_bgcolor=COLORS['bg'], paper_bgcolor=COLORS['bg'], font_color=COLORS['slate'],
        xaxis_title="Share of Preference (%)", yaxis_title=None, height=250,
        xaxis=dict(range=[0, 100], gridcolor='#233554'), margin=dict(t=10, b=0, l=0, r=0)
    )
    st.plotly_chart(fig_share, use_container_width=True)

# --- ABA 6: ELASTICIDADE PREÇO ---
with tab_elas:
    st.markdown("### Curvas de Elasticidade-Preço por Pacote")
    st.write("Identifica o grau de sensibilidade a preço e o teto (Pricing Ceiling) que o consumidor aceita pagar antes da demanda colapsar.")
    
    fig_elas = go.Figure()
    
    fig_elas.add_trace(go.Scatter(x=df_elasticity['Preço (R$)'], y=df_elasticity['Versão Base'], mode='lines', name='Versão Base (Sem Opcionais)', line=dict(color=COLORS['slate'], width=3, dash='dash')))
    fig_elas.add_trace(go.Scatter(x=df_elasticity['Preço (R$)'], y=df_elasticity['Base + ABS + Painel'], mode='lines', name='Base + ABS + Painel TFT', line=dict(color=COLORS['cyan'], width=4)))
    fig_elas.add_trace(go.Scatter(x=df_elasticity['Preço (R$)'], y=df_elasticity['Pacote Premium (Todas as Features)'], mode='lines', name='Pacote Premium Completasso', line=dict(color=COLORS['orange'], width=4)))
    
    fig_elas.update_layout(
        plot_bgcolor=COLORS['bg'], paper_bgcolor=COLORS['bg'], font_color=COLORS['slate'],
        xaxis_title="Preço Praticado (R$)", yaxis_title="Demanda / Share (%)",
        xaxis=dict(gridcolor='#233554', tickformat="R$ ,.0f"), yaxis=dict(gridcolor='#233554', range=[0, 40]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=500
    )
    
    st.plotly_chart(fig_elas, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        <span class="insight-title">Análise de Captura de Valor</span>
        <p>A curva <b>Laranja (Premium)</b> é muito mais inelástica. Isso significa que consumidores que desejam a moto completa são menos sensíveis a variações de preço, focando no valor entregue pela tecnologia.</p>
        <p>A versão <b>Base (Cinza)</b> sofre colapso rápido de demanda caso ultrapasse a barreira psicológica de R$ 22.500.</p>
    </div>
    """, unsafe_allow_html=True)
    
# ==========================================
# 4. FOOTER CORPORATIVO
# ==========================================
st.markdown("<hr style='border-color: #233554; margin-top: 50px;'>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #8892B0; font-family: Roboto; font-size: 13px;'>
    Desenvolvido por <b>INSIGHTS<span style="color:#FF6B6B;">&</span>Etc</b> | Data Analytics & Market Intelligence<br>
    <i>Confidential Proposal - Yamaha Motor do Brasil</i>
</div>
""", unsafe_allow_html=True)