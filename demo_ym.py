import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E BRANDING ROUTE
# ==========================================
st.set_page_config(page_title="Simulador de Precificação - Route Automotive", layout="wide", page_icon="🛵")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Montserrat:wght@400;600;700&display=swap');
    
    .stApp { background-color: #FAFAFA; color: #333333; font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4, h5 { color: #4A4A4A !important; font-family: 'Inter', sans-serif; font-weight: 600; }
    
    .header-container { border-bottom: 2px solid #A44C3A; padding-bottom: 15px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: flex-end;}
    .header-title { font-size: 24px; font-weight: 800; color: #333333; margin: 0; }
    .header-subtitle { font-size: 14px; color: #777777; margin: 0; }
    .route-logo { font-size: 28px; font-weight: 800; color: #A44C3A; text-align: right; letter-spacing: 2px; line-height: 1.1;}
    .route-logo span { font-size: 14px; font-weight: 600; letter-spacing: 4px; display: block; color: #666666;}
    
    .insight-box { background-color: #FFFFFF; border-left: 4px solid #A44C3A; padding: 15px 20px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .insight-title { font-weight: 800; color: #A44C3A; font-size: 14px; margin-bottom: 5px; display: block; text-transform: uppercase;}
    
    .stTabs [data-baseweb="tab-list"] { background-color: #FFFFFF; border-bottom: 2px solid #E0E0E0; padding: 0 10px;}
    .stTabs [data-baseweb="tab"] { color: #666666; font-weight: 600; padding: 12px 20px; }
    .stTabs [aria-selected="true"] { color: #A44C3A !important; border-bottom-color: #A44C3A !important; border-bottom-width: 3px !important;}
    
    .sim-header { font-weight: 800; color: #4A4A4A; text-align: center; margin-bottom: 10px; font-size: 16px; border-bottom: 1px solid #E0E0E0; padding-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# Cabeçalho da Página
st.markdown("""
<div class="header-container">
    <div>
        <h1 class="header-title">Modelo de Precificação de Features</h1>
        <p class="header-subtitle">YAMAHA BRASIL | Pesquisa Quantitativa Pricing</p>
    </div>
    <div style="text-align: right;">
        <div style="font-family: 'Montserrat', sans-serif; font-size: 12px; color: #777777; margin-bottom: -5px; letter-spacing: 1px;">POWERED BY</div>
        <div class="route-logo">ROUTE<span>AUTOMOTIVE</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

PALETTE = {
    'brown_dark': '#A44C3A', 'brown_light': '#D27D60',
    'gray_dark': '#4A4A4A', 'gray_light': '#BDBDBD', 'bg_card': '#FDF9F6'
}

# ==========================================
# 2. DADOS EMBUTIDOS (MOCK BASEADO NA PLANILHA)
# ==========================================
MOCK_DATA = [
    ['Powertrain', 'Cilindrada', 'Padrão', 0, 0, 0, 0],
    ['Powertrain', 'Cilindrada', '10 cc a mais', 54, 48, 75, 137],
    ['Powertrain', 'Cilindrada', '50 cc a mais', 0, 0, 377, 683],
    ['Powertrain', 'Potência', 'Padrão', 0, 0, 0, 0],
    ['Powertrain', 'Potência', '1cv a mais', 68, 61, 95, 172],
    ['Powertrain', 'Torque', 'Padrão', 0, 0, 0, 0],
    ['Powertrain', 'Torque', '1kgfm a mais', 656, 588, 917, 1660],
    ['Powertrain', 'Cambio', 'Manual', 0, 0, 0, 0],
    ['Powertrain', 'Cambio', 'Semi automático (DCT)', 387, 389, 650, 1657],
    ['Quadro e Suspensão', 'Suspensão', 'Convencional', 0, 0, 0, 0],
    ['Quadro e Suspensão', 'Suspensão', 'Invertida', 364, 417, 958, 1257],
    ['Quadro e Suspensão', 'Freios', 'Convencional', 0, 0, 0, 0],
    ['Quadro e Suspensão', 'Freios', 'ABS 1 Canal', 621, 671, 0, 0],
    ['Quadro e Suspensão', 'Freios', 'ABS 2 Canais', 0, 0, 893, 1335],
    ['Painel de Instrumentos', 'Painel', 'Analógico', 0, 0, 0, 0],
    ['Painel de Instrumentos', 'Painel', 'Digital TFT', 371, 371, 683, 1031],
    ['Painel de Instrumentos', 'Conectividade', 'Sem conectividade', 0, 0, 0, 0],
    ['Painel de Instrumentos', 'Conectividade', 'Bluetooth (Y-Connect)', 164, 157, 331, 527],
    ['Iluminação', 'Farol dianteiro', 'Halógeno', 0, 0, 0, 0],
    ['Iluminação', 'Farol dianteiro', 'Full LED', 262, 273, 352, 579],
    ['Carenagem e Acabamento', 'Porta capacete', 'Sem Porta capacete', 0, 0, 0, 0],
    ['Carenagem e Acabamento', 'Porta capacete', 'Para capacete fechado', 355, 0, 0, 0],
    ['Serviços', 'Garantia', '1 ano', 0, 0, 0, 0],
    ['Serviços', 'Garantia', '3 anos', 142, 137, 370, 519]
]

SEGMENTOS = ['Scooter', 'Small Street', 'Middle Street', 'Big Street']
df_spec = pd.DataFrame(MOCK_DATA, columns=['Grupo', 'Item', 'Nivel'] + SEGMENTOS)
df_spec['Total'] = df_spec[SEGMENTOS].mean(axis=1)

df_importancia = df_spec.groupby(['Grupo', 'Item'])[SEGMENTOS + ['Total']].max().reset_index()

# ==========================================
# 3. RENDERIZAÇÃO DAS ABAS
# ==========================================
tab_imp, tab_turf, tab_mwtp, tab_elas, tab_sim = st.tabs([
    "📊 Importância", 
    "🎯 TURF", 
    "💰 MWTP",
    "📈 Elasticidade",
    "🎮 Simulador"
])

# --- ABA 1: IMPORTÂNCIA ---
with tab_imp:
    st.markdown("### Importância por Ítem")
    st.write("Calculado com base no valor máximo atribuído a cada ítem (diferença entre o melhor nível e o base).")
    
    col_t, col_s = st.columns([1, 1])
    
    with col_t:
        st.markdown("#### Importância Total (Mercado)")
        df_imp_total = df_importancia.sort_values('Total', ascending=True)
        fig_total = px.bar(df_imp_total, x='Total', y='Item', orientation='h', color='Grupo', 
                           color_discrete_sequence=[PALETTE['brown_dark'], PALETTE['brown_light'], PALETTE['gray_dark'], '#8B5A2B', '#CD853F', '#A9A9A9'])
        fig_total.update_layout(plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF', xaxis_title="Score de Importância", yaxis_title=None, height=500, showlegend=False)
        st.plotly_chart(fig_total, use_container_width=True)
        
    with col_s:
        st.markdown("#### Importância por Segmento")
        df_melt = df_importancia.melt(id_vars=['Grupo', 'Item'], value_vars=SEGMENTOS, var_name='Segmento', value_name='Importância')
        top_itens = df_imp_total.tail(7)['Item'].tolist()
        df_melt = df_melt[df_melt['Item'].isin(top_itens)]
        
        fig_seg = px.bar(df_melt, x='Importância', y='Item', color='Segmento', barmode='group', orientation='h', 
                         color_discrete_sequence=['#4A4A4A', '#A44C3A', '#D27D60', '#BDBDBD'])
        fig_seg.update_layout(plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF', xaxis_title="Score de Importância", yaxis_title=None, height=500, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_seg, use_container_width=True)

# --- ABA 2: TURF (DINÂMICO E COM INSIGHT) ---
with tab_turf:
    st.markdown("### Análise TURF (Combinações Ideais)")
    st.write("As melhores combinações de **Ítem + Nível** para maximizar o alcance de mercado.")
    
    col_sel_turf, _ = st.columns([1, 3])
    with col_sel_turf:
        segmento_turf = st.selectbox("Selecione o Segmento:", ['Total Mercado'] + SEGMENTOS, key="turf_seg")
    
    col_alvo_turf = 'Total' if segmento_turf == 'Total Mercado' else segmento_turf

    df_validos = df_spec[df_spec[col_alvo_turf] > 0].sort_values(col_alvo_turf, ascending=False)
    df_best = df_validos.groupby('Item').first().reset_index().sort_values(col_alvo_turf, ascending=False).head(6)
    df_best['Combo'] = df_best['Item'] + ": " + df_best['Nivel']
    
    mod_reach = 1.15 if segmento_turf == 'Scooter' else 0.95 if 'Small' in segmento_turf else 0.85 if 'Middle' in segmento_turf else 0.75 if 'Big' in segmento_turf else 1.0
    
    reach_base = int(42 * mod_reach)
    reach_vals, inc_vals, inc_puro = [], [], []
    
    for i in range(len(df_best)):
        if i == 0:
            reach_vals.append(reach_base)
            inc_vals.append(f"{reach_base}pp")
            inc_puro.append(reach_base)
        else:
            inc = int((25 / i) * mod_reach)
            reach_base += inc
            reach_vals.append(min(reach_base, 98))
            inc_vals.append(f"+{inc}pp")
            inc_puro.append(inc)
            
    df_best['Reach'] = reach_vals
    df_best['Inc'] = inc_vals
    
    # Caixa de Insight (Corrigida para evitar erros se a lista for muito pequena)
    if len(inc_puro) > 1:
        melhor_inc_idx = np.argmax(inc_puro[1:]) + 1
        item_melhor_inc = df_best.iloc[melhor_inc_idx]['Combo']
        valor_melhor_inc = inc_puro[melhor_inc_idx]

        st.markdown(f"""
        <div class="insight-box">
            <span class="insight-title">Insight de Retorno Marginal</span>
            <p>Analisando o segmento <b>{segmento_turf}</b>, a adição da configuração <b>"{item_melhor_inc}"</b> é a que proporciona o maior salto consecutivo de captura de novos clientes (+{valor_melhor_inc}pp em relação ao passo anterior).</p>
        </div>
        """, unsafe_allow_html=True)

    fig_turf = go.Figure()
    fig_turf.add_trace(go.Bar(
        x=df_best['Combo'], y=df_best['Reach'],
        marker_color='#F0F0F0', name='Incremento Marginal', hoverinfo='none',
        text=df_best['Inc'], textposition='inside'
    ))
    fig_turf.add_trace(go.Scatter(
        x=df_best['Combo'], y=df_best['Reach'],
        mode='lines+markers+text',
        text=df_best['Reach'].astype(str) + '%', textposition='top center',
        textfont=dict(color=PALETTE['brown_dark'], weight='bold'),
        line=dict(color=PALETTE['brown_dark'], width=4),
        marker=dict(size=12, color=PALETTE['brown_dark']),
        name='Reach Acumulado'
    ))
    fig_turf.update_layout(plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF', xaxis_title="Combinações Otimizadas", yaxis_title="Reach Acumulado (%)", yaxis=dict(range=[0, 110], gridcolor='#E0E0E0'), height=400, showlegend=False, margin=dict(t=20))
    st.plotly_chart(fig_turf, use_container_width=True)

# --- ABA 3: MWTP ---
with tab_mwtp:
    st.markdown("### Disposição Marginal a Pagar (MWTP)")
    st.write("Análise do valor financeiro atribuído a cada grupo, item e nível, frente à versão base.")
    
    st.markdown("#### 1. Importância dos Grupos")
    df_grupo = df_importancia.groupby('Grupo')['Total'].sum().reset_index().sort_values('Total', ascending=True)
    
    fig_g = px.bar(df_grupo, x='Total', y='Grupo', orientation='h', text_auto='.0f')
    fig_g.update_traces(marker_color=PALETTE['brown_dark'], textposition='outside', textfont=dict(size=14, color='#4A4A4A'))
    fig_g.update_layout(
        plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF', 
        xaxis_title="Soma MWTP (R$)", yaxis_title=None, height=400, 
        xaxis=dict(gridcolor='#E0E0E0', range=[0, df_grupo['Total'].max() * 1.15]),
        margin=dict(t=20, b=0, l=0, r=0)
    )
    st.plotly_chart(fig_g, use_container_width=True)
    st.markdown("<hr style='border-color: #E0E0E0;'>", unsafe_allow_html=True)

    st.markdown("#### 2. MWTP dos Ítens (Por Grupo)")
    grupos_lista = df_grupo.sort_values('Total', ascending=False)['Grupo'].tolist()
    
    c1, c2, c3 = st.columns(3)
    cols = [c1, c2, c3]
    for idx, grp in enumerate(grupos_lista):
        df_sub = df_importancia[df_importancia['Grupo'] == grp].sort_values('Total', ascending=True)
        if not df_sub.empty:
            fig_sub = px.bar(df_sub, x='Total', y='Item', orientation='h', title=grp, text_auto='.0f')
            fig_sub.update_traces(marker_color=PALETTE['brown_light'], textposition='outside')
            fig_sub.update_layout(
                title=dict(text=grp, font=dict(color=PALETTE['brown_dark'], size=14)),
                plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF', 
                xaxis_title=None, yaxis_title=None, height=220, 
                xaxis=dict(gridcolor='#E0E0E0', range=[0, df_sub['Total'].max() * 1.3]),
                margin=dict(l=0, r=0, t=40, b=0)
            )
            cols[idx % 3].plotly_chart(fig_sub, use_container_width=True)

    st.markdown("<hr style='border-color: #E0E0E0;'>", unsafe_allow_html=True)
    st.markdown("#### 3. Detalhamento por Nível")
    
    col_sel_g, col_sel_i, _ = st.columns([1, 1, 1.5])
    with col_sel_g:
        grupo_selecionado = st.selectbox("Selecione o Grupo:", df_spec['Grupo'].unique())
    with col_sel_i:
        itens_disponiveis = df_spec[df_spec['Grupo'] == grupo_selecionado]['Item'].unique()
        item_selecionado = st.selectbox("Selecione o Ítem:", itens_disponiveis)
        
    df_niveis = df_spec[(df_spec['Grupo'] == grupo_selecionado) & (df_spec['Item'] == item_selecionado)].sort_values('Total', ascending=True)
    
    fig_niveis = px.bar(df_niveis, x='Total', y='Nivel', orientation='h', text_auto='.0f')
    fig_niveis.update_traces(marker_color=PALETTE['gray_dark'], textposition='outside', textfont=dict(size=12))
    fig_niveis.update_layout(
        plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF', 
        xaxis_title="Valor MWTP (R$)", yaxis_title=None, height=300, 
        xaxis=dict(gridcolor='#E0E0E0', range=[0, max(100, df_niveis['Total'].max() * 1.15)]),
        margin=dict(l=0, r=0, t=20, b=0)
    )
    st.plotly_chart(fig_niveis, use_container_width=True)

# --- ABA 4: ELASTICIDADE DINÂMICA ---
with tab_elas:
    st.markdown("### Elasticidade de Preço por Nível")
    st.write("Compare a curva de demanda para cada nível do ítem selecionado.")
    
    # Seletores
    c_sel1, c_sel2, _ = st.columns([1, 1, 2])
    with c_sel1:
        feature_sel = st.selectbox("Selecione o Ítem:", df_spec['Item'].unique().tolist(), key="elas_i")
    with c_sel2:
        segmento_elas = st.selectbox("Segmento:", ['Total'] + SEGMENTOS, key="elas_seg")
    
    # Preparação dos dados para o nível selecionado
    df_item = df_spec[df_spec['Item'] == feature_sel]
    precos_elas = [13000, 15000, 17000, 19000, 21000]
    
    # Criamos colunas lado a lado
    col_grafico, col_tabela = st.columns([1.5, 1])
    
    with col_grafico:
        fig_elas = go.Figure()
        tabela_data = {'Preço': [f"R$ {p/1000:.3f}" for p in precos_elas]}
        
        for _, row in df_item.iterrows():
            nivel = row['Nivel']
            if nivel == 'Padrão': continue
            
            # Cálculo de share dinâmico por segmento
            base_val = row[segmento_elas if segmento_elas != 'Total' else 'Total']
            shares = [max(1.0, (base_val / 20) * (1 - (p-13000)/10000)) for p in precos_elas]
            
            fig_elas.add_trace(go.Scatter(x=precos_elas, y=shares, mode='lines+markers', name=nivel))
            tabela_data[nivel] = [f"{s:.1f}%" for s in shares]
            
        fig_elas.update_layout(
            title=f"Curva de Demanda: {feature_sel}",
            xaxis_title="Preço (R$)", yaxis_title="Share (%)",
            plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF',
            yaxis=dict(gridcolor='#E0E0E0', range=[0, 60]), height=400,
            margin=dict(t=40, b=0, l=0, r=0)
        )
        st.plotly_chart(fig_elas, use_container_width=True)
        
    with col_tabela:
        st.markdown("<div style='margin-bottom: 15px; font-weight: 600; color: #4A4A4A;'>Tabela de Share Projetado</div>", unsafe_allow_html=True)
        st.table(pd.DataFrame(tabela_data))

# --- ABA 5: SIMULADOR 100% REATIVO ---
with tab_sim:
    st.markdown("### Simulador Dinâmico")
    st.write("Teste o share de preferência alterando os atributos. O gráfico reage matematicamente às suas escolhas.")
    
    ITEM_1 = 'Torque'
    ITEM_2 = 'Freios'
    ITEM_3 = 'Painel'
    
    NIVEIS_1 = df_spec[df_spec['Item'] == ITEM_1]['Nivel'].tolist()
    NIVEIS_2 = df_spec[df_spec['Item'] == ITEM_2]['Nivel'].tolist()
    NIVEIS_3 = df_spec[df_spec['Item'] == ITEM_3]['Nivel'].tolist()
    NIVEIS_PRECO = ['R$ 14.990', 'R$ 15.990', 'R$ 16.990', 'R$ 18.990', 'R$ 22.990']

    st.markdown("<div style='background-color: #FFFFFF; padding: 20px; border-radius: 4px; border: 1px solid #E0E0E0; margin-bottom: 20px;'>", unsafe_allow_html=True)
    col_labels, col_A, col_B, col_C, col_D = st.columns([1, 1.5, 1.5, 1.5, 1.5])
    
    with col_labels:
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        st.markdown(f"**{ITEM_1}**")
        st.markdown(f"**{ITEM_2}**")
        st.markdown(f"**{ITEM_3}**")
        st.markdown("**Preço**")
        
    def renderizar_dropdowns(coluna, titulo, pre_selecao):
        with coluna:
            st.markdown(f"<div class='sim-header'>{titulo}</div>", unsafe_allow_html=True)
            v1 = st.selectbox(f"{ITEM_1}_{titulo}", NIVEIS_1, index=pre_selecao[0], label_visibility="collapsed")
            v2 = st.selectbox(f"{ITEM_2}_{titulo}", NIVEIS_2, index=pre_selecao[1], label_visibility="collapsed")
            v3 = st.selectbox(f"{ITEM_3}_{titulo}", NIVEIS_3, index=pre_selecao[2], label_visibility="collapsed")
            vp = st.selectbox(f"Preco_{titulo}", NIVEIS_PRECO, index=pre_selecao[3], label_visibility="collapsed")
            
            # Retorna os Índices selecionados para fazer cálculo matemático real
            return NIVEIS_1.index(v1), NIVEIS_2.index(v2), NIVEIS_3.index(v3), NIVEIS_PRECO.index(vp)

    idxA = renderizar_dropdowns(col_A, "Configuração A", [0, 0, 0, 0])
    idxB = renderizar_dropdowns(col_B, "Configuração B", [min(1, len(NIVEIS_1)-1), min(1, len(NIVEIS_2)-1), 0, 1])
    idxC = renderizar_dropdowns(col_C, "Configuração C", [0, min(2, len(NIVEIS_2)-1), min(1, len(NIVEIS_3)-1), 2])
    idxD = renderizar_dropdowns(col_D, "Configuração D", [0, min(1, len(NIVEIS_2)-1), 0, 0])
    st.markdown("</div>", unsafe_allow_html=True)
    
    # --- CÁLCULO MATEMÁTICO REAL REATIVO AOS DROPDOWNS ---
    def calcular_utilidade(indices):
        # Utilidade Base + (peso do torque * indice) + (peso freio * indice) + (peso painel * indice) - (penalidade preço * indice)
        u = 10.0 + (indices[0] * 3.5) + (indices[1] * 4.2) + (indices[2] * 2.8) - (indices[3] * 5.0)
        return max(0.1, np.exp(u / 5.0)) # Logit model simples
        
    util_A = calcular_utilidade(idxA)
    util_B = calcular_utilidade(idxB)
    util_C = calcular_utilidade(idxC)
    util_D = calcular_utilidade(idxD)
    util_None = np.exp(1.5) # Fator Nenhuma das Opções
    
    total_util = util_A + util_B + util_C + util_D + util_None
    
    df_sim_share = pd.DataFrame({
        'Configurações': ['Configuração A', 'Configuração B', 'Configuração C', 'Configuração D', 'Nenhuma'],
        'Share (%)': [(util_A/total_util)*100, (util_B/total_util)*100, (util_C/total_util)*100, (util_D/total_util)*100, (util_None/total_util)*100],
        'Cor': [PALETTE['brown_dark'], PALETTE['brown_light'], PALETTE['gray_dark'], PALETTE['gray_light'], '#E0E0E0']
    })
    
    # Criando o rótulo corrigido que não gera erro de "NoneType" no Plotly
    df_sim_share['Rotulo'] = df_sim_share['Share (%)'].apply(lambda x: f"{x:.1f}%")
    
    st.markdown("<div style='background-color: #FDF9F6; padding: 20px; border-radius: 4px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-bottom: 0;'>Share of Preference Projetado</h3>", unsafe_allow_html=True)
    
    fig_sim = px.bar(df_sim_share, x='Configurações', y='Share (%)', text='Rotulo')
    fig_sim.update_traces(marker_color=df_sim_share['Cor'], textposition='outside', textfont=dict(color='#4A4A4A', weight='bold'))
    fig_sim.update_layout(plot_bgcolor='#FDF9F6', paper_bgcolor='#FDF9F6', yaxis_title="Share (%)", xaxis_title=None, height=350, yaxis=dict(range=[0, max(50, df_sim_share['Share (%)'].max() * 1.2)], gridcolor='#E0E0E0'), margin=dict(t=20, b=0, l=0, r=0))
    st.plotly_chart(fig_sim, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<hr style='border-color: #E0E0E0; margin-top: 50px;'>", unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align: center; color: #9E9E9E; font-size: 13px; font-family: Inter;'>
    Material confidencial ROUTE | Exclusivo para YAMAHA DO BRASIL<br>
    Dashboard Analytics and Tech dev by <b>INSIGHTS</b><b style='color:#FF6B6B'>&</b><b>Etc</b>
</div>
""", unsafe_allow_html=True)