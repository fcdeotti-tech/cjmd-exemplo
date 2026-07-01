import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E BRANDING ROUTE
# ==========================================
st.set_page_config(page_title="Simulador de Precificação - Route Automotive", layout="wide", page_icon="🛵")

# CSS Fiel ao Layout da ROUTE Automotive (Fundo claro, Tons Terrosos, Marrom e Cinza)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp { background-color: #FAFAFA; color: #333333; font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4, h5 { color: #4A4A4A !important; font-family: 'Inter', sans-serif; font-weight: 600; }
    
    /* Cabeçalho ROUTE */
    .header-container { border-bottom: 2px solid #A44C3A; padding-bottom: 15px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center;}
    .header-title { font-size: 24px; font-weight: 800; color: #333333; margin: 0; }
    .header-subtitle { font-size: 14px; color: #777777; margin: 0; }
    .route-logo { font-size: 28px; font-weight: 800; color: #A44C3A; text-align: right; letter-spacing: 2px; line-height: 1.1;}
    .route-logo span { font-size: 14px; font-weight: 600; letter-spacing: 4px; display: block; color: #666666;}
    
    /* Caixas de Texto (Insights) */
    .insight-box { background-color: #FFFFFF; border-left: 4px solid #A44C3A; padding: 15px 20px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .insight-title { font-weight: 800; color: #A44C3A; font-size: 14px; margin-bottom: 5px; display: block; text-transform: uppercase;}
    
    /* Customização das Abas */
    .stTabs [data-baseweb="tab-list"] { background-color: #FFFFFF; border-bottom: 2px solid #E0E0E0; padding: 0 10px;}
    .stTabs [data-baseweb="tab"] { color: #666666; font-weight: 600; padding: 12px 20px; }
    .stTabs [aria-selected="true"] { color: #A44C3A !important; border-bottom-color: #A44C3A !important; border-bottom-width: 3px !important;}
    
    /* Tabela do Simulador */
    .sim-header { font-weight: 800; color: #4A4A4A; text-align: center; margin-bottom: 10px; font-size: 16px; }
</style>
""", unsafe_allow_html=True)

# Cabeçalho da Página
st.markdown("""
<div class="header-container">
    <div>
        <h1 class="header-title">Método de precificação: Modelos & Versões</h1>
        <p class="header-subtitle">YAMAHA BRASIL | Simulador de Decisões e Relatórios Analíticos</p>
    </div>
    <div class="route-logo">ROUTE<span>AUTOMOTIVE</span></div>
</div>
""", unsafe_allow_html=True)

# Paleta de Cores Fiel ao PDF
PALETTE = {
    'brown_dark': '#A44C3A',
    'brown_light': '#D27D60',
    'gray_dark': '#4A4A4A',
    'gray_light': '#BDBDBD',
    'bg_card': '#FDF9F6'
}

# ==========================================
# 2. DADOS MOCKADOS (Baseados nas Páginas do PDF)
# ==========================================
def get_maxdiff_data():
    # Ref: Página 7 do PDF
    return pd.DataFrame({
        'Atributo': ['Freios ABS', 'Painel Digital', 'Faróis de LED', 'Chave presencial', 'Botão de START', 'Suspensão a gás', 'Baú traseiro', 'Bagageiro 2 capacetes'],
        'Score (%)': [22, 18, 15, 12, 11, 9, 8, 5],
        'Cor': [PALETTE['brown_dark'], PALETTE['brown_dark'], PALETTE['brown_light'], PALETTE['brown_light'], PALETTE['brown_light'], PALETTE['gray_light'], PALETTE['gray_light'], PALETTE['gray_light']]
    }).sort_values('Score (%)', ascending=True)

def get_conjoint_importance():
    # Ref: Página 10 do PDF
    return pd.DataFrame({
        'Fator': ['Preço', 'Potência', 'Característica', 'Modelo', 'Painel'],
        'Importância (%)': [41, 23, 16, 12, 8],
        'Cor': [PALETTE['brown_dark'], PALETTE['brown_light'], PALETTE['brown_dark'], PALETTE['gray_dark'], PALETTE['gray_light']]
    }).sort_values('Importância (%)', ascending=True)

def get_mwtp_data():
    # Ref: Página 11 do PDF
    return pd.DataFrame({
        'Feature': ['Potência 300cc', 'Freios ABS', 'Potência 160cc', 'Painel Digital', 'Faróis de LED', 'Chave presencial', 'Botão de START', 'Baú traseiro'],
        'MWTP (R$)': [2340, 1450, 1120, 980, 760, 540, 320, 280],
        'Cor': [PALETTE['brown_dark'], PALETTE['brown_dark'], PALETTE['brown_dark'], PALETTE['brown_light'], PALETTE['brown_light'], PALETTE['brown_light'], PALETTE['brown_light'], PALETTE['brown_light']]
    }).sort_values('MWTP (R$)', ascending=True)

# Dicionários de Opções para o Simulador (Ref: Página 15 do PDF)
OPCOES = {
    'Potência': ['125 cc', '160 cc', '300 cc'],
    'Painel': ['Analóg.', 'Digital'],
    'Destaque': ['Baú', 'ABS', 'Chave pres.', 'LED', 'Susp. gás'],
    'Preço': ['R$ 12.990', 'R$ 13.990', 'R$ 14.990', 'R$ 15.990', 'R$ 16.990']
}

# ==========================================
# 3. RENDERIZAÇÃO DAS ABAS
# ==========================================
tab_mxd, tab_conj, tab_mwtp, tab_elas, tab_sim = st.tabs([
    "📊 03. MaxDiff", 
    "⚖️ 04. Conjoint (Importância)", 
    "💰 04. Conjoint (MWTP)",
    "📈 04. Conjoint (Elasticidade)",
    "🎮 05. Simulador"
])

# --- ABA 1: MAXDIFF ---
with tab_mxd:
    st.markdown("### O que o MaxDiff entrega")
    st.write("Um ranking claro de importância - pronto para orientar a precificação.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        df_mxd = get_maxdiff_data()
        fig_mxd = px.bar(df_mxd, x='Score (%)', y='Atributo', orientation='h', text_auto='.0f')
        fig_mxd.update_traces(marker_color=df_mxd['Cor'], textposition='outside', textfont=dict(color='#4A4A4A'))
        fig_mxd.update_layout(
            plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF',
            xaxis_title="Share of Preference (importância relativa)", yaxis_title=None, height=450,
            xaxis=dict(range=[0, 26], gridcolor='#E0E0E0')
        )
        st.plotly_chart(fig_mxd, use_container_width=True)
        
    with col2:
        st.markdown("""
        <div class="insight-box">
            <span class="insight-title">Análise ROUTE</span>
            <p>Cada atributo recebe um <i>Share of Preference</i> — sua importância relativa dentro do conjunto avaliado.</p>
            <p>No exemplo, <b>Freios ABS</b>, <b>Painel Digital</b> e <b>Faróis de LED</b> concentram a maior parte da importância — enquanto itens como o bagageiro pesam pouco na decisão.</p>
            <p>É esse ranking que define quais atributos entram — e como — na etapa de Conjoint Analysis.</p>
        </div>
        """, unsafe_allow_html=True)

# --- ABA 2: CONJOINT IMPORTANCE ---
with tab_conj:
    st.markdown("### Análise de importância")
    st.write("Quanto cada atributo pesa e como cada nível performa na decisão de compra.")
    
    c1, c2 = st.columns([1, 1.5])
    with c1:
        df_imp = get_conjoint_importance()
        fig_imp = px.bar(df_imp, x='Importância (%)', y='Fator', orientation='h', text_auto='.0f')
        fig_imp.update_traces(marker_color=df_imp['Cor'], textposition='outside')
        fig_imp.update_layout(plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF', xaxis_title="Importância relativa dos atributos na decisão", yaxis_title=None, height=400)
        st.plotly_chart(fig_imp, use_container_width=True)
        
    with c2:
        st.markdown("""
        <div style="background-color: #FFFFFF; padding: 20px; border: 1px solid #E0E0E0; border-radius: 4px;">
            <h4 style="color: #A44C3A !important; text-align: center; margin-bottom: 20px;">Valor relativo por nível (utilidade)</h4>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #EEEEEE; padding: 10px 0;">
                <span style="width: 30%; font-weight: 600; color: #4A4A4A;">POTÊNCIA 300 cc</span>
                <div style="width: 60%; background-color: #F0F0F0; height: 20px; border-radius: 2px; position: relative;">
                    <div style="background-color: #A44C3A; height: 100%; width: 70%; position: absolute; left: 50%; border-radius: 0 2px 2px 0;"></div>
                </div>
                <span style="width: 10%; text-align: right; font-weight: 600;">+14%</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #EEEEEE; padding: 10px 0;">
                <span style="width: 30%; font-weight: 600; color: #4A4A4A;">PREÇO R$ 12.990</span>
                <div style="width: 60%; background-color: #F0F0F0; height: 20px; border-radius: 2px; position: relative;">
                    <div style="background-color: #A44C3A; height: 100%; width: 90%; position: absolute; left: 50%; border-radius: 0 2px 2px 0;"></div>
                </div>
                <span style="width: 10%; text-align: right; font-weight: 600;">+18%</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0;">
                <span style="width: 30%; font-weight: 600; color: #4A4A4A;">PREÇO R$ 18.990</span>
                <div style="width: 60%; background-color: #F0F0F0; height: 20px; border-radius: 2px; position: relative;">
                    <div style="background-color: #BDBDBD; height: 100%; width: 100%; position: absolute; right: 50%; border-radius: 2px 0 0 2px;"></div>
                </div>
                <span style="width: 10%; text-align: right; font-weight: 600;">-22%</span>
            </div>
            <p style="text-align: center; font-size: 12px; color: #777777; margin-top: 20px;">Valor (utilidade) de cada nível — o sinal mostra o que puxa a escolha para cima ou para baixo.</p>
        </div>
        """, unsafe_allow_html=True)

# --- ABA 3: MWTP ---
with tab_mwtp:
    st.markdown("### Disposição marginal a pagar")
    st.write("Quanto cada feature vale em reais, frente à versão base.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        df_mwtp = get_mwtp_data()
        fig_mwtp = px.bar(df_mwtp, x='MWTP (R$)', y='Feature', orientation='h', text_auto='R$ .0f')
        fig_mwtp.update_traces(marker_color=df_mwtp['Cor'], textposition='outside')
        fig_mwtp.update_layout(plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF', xaxis_title="Disposição marginal a pagar — em relação à versão base (R$)", yaxis_title=None, height=450, xaxis=dict(range=[0, 2700]))
        st.plotly_chart(fig_mwtp, use_container_width=True)
        
    with col2:
        st.markdown("""
        <div class="insight-box">
            <span class="insight-title">Precificação por Atributo</span>
            <p>Quando o preço é um dos atributos, calculamos quanto cada nível vale em R$ para o cliente.</p>
            <p>No exemplo, subir a potência para 300 cc vale <b>~R$ 2.340</b>, e os Freios ABS <b>~R$ 1.450</b> — insumos diretos para definir o preço de cada versão.</p>
        </div>
        """, unsafe_allow_html=True)

# --- ABA 4: ELASTICIDADE ---
with tab_elas:
    st.markdown("### Elasticidade de preço")
    st.write("Para cada simulação: share de preferência e projeção de receita.")
    
    c1, c2 = st.columns(2)
    # Mock Data para Elasticidade
    precos_elas = np.arange(13, 20, 1)
    share_elas = [46, 41, 36, 30, 24, 18, 13]
    receita_elas = [60, 58, 54, 48, 41, 32, 25]
    
    with c1:
        fig_s = go.Figure()
        fig_s.add_trace(go.Scatter(x=precos_elas, y=share_elas, mode='lines+markers', line=dict(color=PALETTE['brown_dark'], width=3), marker=dict(size=8), fill='tozeroy', fillcolor='rgba(164, 76, 58, 0.2)'))
        fig_s.update_layout(title="Share de preferência", xaxis_title="Preço (R$ mil)", yaxis_title="Share (%)", plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF', yaxis=dict(range=[0, 50]), height=350)
        st.plotly_chart(fig_s, use_container_width=True)
        st.caption("À medida que o preço sobe, o share cai...")
        
    with c2:
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatter(x=precos_elas, y=receita_elas, mode='lines+markers', line=dict(color='#4A4A4A', width=3), marker=dict(size=8), fill='tozeroy', fillcolor='rgba(230, 230, 230, 0.5)'))
        fig_r.add_annotation(x=13, y=60, text="Receita máx.", showarrow=True, arrowhead=1, ax=30, ay=-20, font=dict(color=PALETTE['brown_dark']))
        fig_r.update_layout(title="Projeção de receita", xaxis_title="Preço (R$ mil)", yaxis_title="Receita (R$ mi)", plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF', yaxis=dict(range=[0, 65]), height=350)
        st.plotly_chart(fig_r, use_container_width=True)
        st.caption("...e a receita tem um ponto ótimo. O modelo encontra o preço que maximiza o resultado.")

# --- ABA 5: SIMULADOR DINÂMICO (PÁGINA 15) ---
with tab_sim:
    st.markdown("### Simulador de decisões")
    st.write("Configure produtos e leia o share de preferência em tempo real. Inclua / exclua produtos e ajuste cada atributo — o modelo recalcula instantaneamente.")
    
    # 1. Criação do "Grid" de configuração igual à tabela da página 15
    st.markdown("<div style='background-color: #FFFFFF; padding: 20px; border-radius: 8px; border: 1px solid #E0E0E0; margin-bottom: 20px;'>", unsafe_allow_html=True)
    
    col_labels, col_A, col_B, col_C, col_D, col_E = st.columns([1, 1.5, 1.5, 1.5, 1.5, 1.5])
    
    with col_labels:
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True) # Spacer
        st.markdown("**Potência**")
        st.markdown("**Painel**")
        st.markdown("**Destaque**")
        st.markdown("**Preço**")
        
    # Inicializando com os valores exatos da tabela do PDF (Pg 15)
    with col_A:
        st.markdown("<div class='sim-header'>A. PCX</div>", unsafe_allow_html=True)
        p_A = st.selectbox("Pot_A", OPCOES['Potência'], index=0, label_visibility="collapsed") # 125cc
        pa_A = st.selectbox("Pai_A", OPCOES['Painel'], index=0, label_visibility="collapsed") # Analóg
        d_A = st.selectbox("Des_A", OPCOES['Destaque'], index=0, label_visibility="collapsed") # Baú
        pr_A = st.selectbox("Pre_A", OPCOES['Preço'], index=0, label_visibility="collapsed") # 12.990
        
    with col_B:
        st.markdown("<div class='sim-header'>B. Nmax</div>", unsafe_allow_html=True)
        p_B = st.selectbox("Pot_B", OPCOES['Potência'], index=1, label_visibility="collapsed") # 160cc
        pa_B = st.selectbox("Pai_B", OPCOES['Painel'], index=1, label_visibility="collapsed") # Digital
        d_B = st.selectbox("Des_B", OPCOES['Destaque'], index=1, label_visibility="collapsed") # ABS
        pr_B = st.selectbox("Pre_B", OPCOES['Preço'], index=1, label_visibility="collapsed") # 13.990
        
    with col_C:
        st.markdown("<div class='sim-header'>C. SH</div>", unsafe_allow_html=True)
        p_C = st.selectbox("Pot_C", OPCOES['Potência'], index=2, label_visibility="collapsed") # 300cc
        pa_C = st.selectbox("Pai_C", OPCOES['Painel'], index=1, label_visibility="collapsed") # Digital
        d_C = st.selectbox("Des_C", OPCOES['Destaque'], index=2, label_visibility="collapsed") # Chave pres.
        pr_C = st.selectbox("Pre_C", OPCOES['Preço'], index=2, label_visibility="collapsed") # 14.990
        
    with col_D:
        st.markdown("<div class='sim-header'>D. Vespa</div>", unsafe_allow_html=True)
        p_D = st.selectbox("Pot_D", OPCOES['Potência'], index=0, label_visibility="collapsed") # 125cc
        pa_D = st.selectbox("Pai_D", OPCOES['Painel'], index=0, label_visibility="collapsed") # Analóg.
        d_D = st.selectbox("Des_D", OPCOES['Destaque'], index=3, label_visibility="collapsed") # LED
        pr_D = st.selectbox("Pre_D", OPCOES['Preço'], index=3, label_visibility="collapsed") # 15.990
        
    with col_E:
        st.markdown("<div class='sim-header'>E. ADV</div>", unsafe_allow_html=True)
        p_E = st.selectbox("Pot_E", OPCOES['Potência'], index=2, label_visibility="collapsed") # 300cc
        pa_E = st.selectbox("Pai_E", OPCOES['Painel'], index=1, label_visibility="collapsed") # Digital
        d_E = st.selectbox("Des_E", OPCOES['Destaque'], index=4, label_visibility="collapsed") # Susp. Gás
        pr_E = st.selectbox("Pre_E", OPCOES['Preço'], index=4, label_visibility="collapsed") # 16.990
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 2. Lógica Fictícia de Cálculo (Logit Mockado) reativa aos inputs
    def calc_util(pot, pai, des, pre):
        u = 10
        if pot == '300 cc': u += 15
        elif pot == '160 cc': u += 8
        if pai == 'Digital': u += 5
        if des == 'ABS' or des == 'Susp. gás': u += 8
        elif des == 'Chave pres.': u += 6
        # Penalidade de preço simples
        idx_preco = OPCOES['Preço'].index(pre)
        u -= (idx_preco * 5)
        return np.exp(u / 5)

    u_A = calc_util(p_A, pa_A, d_A, pr_A)
    u_B = calc_util(p_B, pa_B, d_B, pr_B)
    u_C = calc_util(p_C, pa_C, d_C, pr_C)
    u_D = calc_util(p_D, pa_D, d_D, pr_D)
    u_E = calc_util(p_E, pa_E, d_E, pr_E)
    u_Nenhum = np.exp(12/5) # Cerca de 12% no cenário base
    
    total_u = u_A + u_B + u_C + u_D + u_E + u_Nenhum
    
    df_sim_share = pd.DataFrame({
        'Modelo': ['A. PCX', 'B. Nmax', 'C. SH', 'D. Vespa', 'E. ADV', 'Nenhuma'],
        'Share (%)': [(u_A/total_u)*100, (u_B/total_u)*100, (u_C/total_u)*100, (u_D/total_u)*100, (u_E/total_u)*100, (u_Nenhum/total_u)*100],
        'Cor': [PALETTE['brown_dark'], PALETTE['brown_light'], PALETTE['brown_dark'], PALETTE['brown_light'], PALETTE['gray_dark'], PALETTE['gray_light']]
    })
    
    # Gráfico Shares of Preference (Visual exato do PDF Pg 15)
    st.markdown("<div style='background-color: #FDF9F6; padding: 20px; border-radius: 8px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-bottom: 0;'>Shares of Preference</h3>", unsafe_allow_html=True)
    
    fig_sim = px.bar(df_sim_share, x='Modelo', y='Share (%)', text_auto='.1f')
    fig_sim.update_traces(marker_color=df_sim_share['Cor'], textposition='outside', textfont=dict(color='#4A4A4A', weight='bold'), texttemplate='%{text}%')
    fig_sim.update_layout(
        plot_bgcolor='#FDF9F6', paper_bgcolor='#FDF9F6',
        yaxis_title="Share of Preference", xaxis_title=None, height=350,
        yaxis=dict(range=[0, 45], gridcolor='#E0E0E0'),
        margin=dict(t=20, b=0, l=0, r=0)
    )
    st.plotly_chart(fig_sim, use_container_width=True)
    st.caption("Exemplo real do simulador de scooters Yamaha")
    st.markdown("</div>", unsafe_allow_html=True)

# Footer ROUTE
st.markdown("<hr style='border-color: #E0E0E0; margin-top: 50px;'>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #9E9E9E; font-size: 12px;'>
    Material confidencial ROUTE | Exclusivo para YAMAHA DO BRASIL<br>
    routeautomotive.com.br
</div>
""", unsafe_allow_html=True)