import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. CONFIGURAÇÃO DA PÁGINA (Tema Corporativo)
st.set_page_config(
    page_title="Target Finance - Simulador",
    page_icon="🎯",
    layout="wide"
)

# Estilização visual dos blocos de resultado (KPIs)
st.markdown("""
    <style>
    .kpi-box { 
        padding: 20px; 
        border-radius: 8px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); 
        margin-bottom: 20px; 
    }
    </style>
""", unsafe_allow_html=True)

# Topo do Aplicativo
st.title("🎯 Target Finance | Simulador de Projeção Real")
st.caption("Projete o crescimento do seu patrimônio de longo prazo expurgando o efeito da inflação.")

st.divider()

# 2. BARRA LATERAL (SIDEBAR) - Onde as pessoas inserem as informações delas
st.sidebar.header("⚙️ Suas Informações")

patrimonio_inicial = st.sidebar.number_input(
    "Patrimônio Inicial Atual (R$)", 
    min_value=0.0, value=10000.0, step=1000.0, format="%.2f"
)

aporte_mensal = st.sidebar.number_input(
    "Aporte Mensal Estimado (R$)", 
    min_value=0.0, value=1500.0, step=100.0, format="%.2f"
)

taxa_nominal_ano = st.sidebar.slider(
    "Taxa de Juros Nominal (% ao ano)", 
    min_value=0.0, max_value=30.0, value=10.5, step=0.1
) / 100

inflacao_ano = st.sidebar.slider(
    "Inflação Estimada (% ao ano - IPCA)", 
    min_value=0.0, max_value=20.0, value=4.0, step=0.1
) / 100

anos_projecao = st.sidebar.number_input(
    "Tempo Alvo da Projeção (Anos)", 
    min_value=1, max_value=50, value=15, step=1
)

# 3. O CÉREBRO MATEMÁTICO (Fórmula de Fisher e Equivalência de Juros)
taxa_real_ano = ((1 + taxa_nominal_ano) / (1 + inflacao_ano)) - 1
taxa_real_mes = ((1 + taxa_real_ano) ** (1/12)) - 1
total_meses = anos_projecao * 12

# Gerando a linha do tempo (Dataframe) mês a mês
meses = np.arange(1, total_meses + 1)
anos_linha = np.ceil(meses / 12).astype(int)

patr_inicial_lista = []
aportes_lista = []
rendimentos_lista = []
patr_final_lista = []

saldo_atual = patrimonio_inicial

for m in meses:
    p_ini = saldo_atual
    apo = aporte_mensal
    rend = (p_ini + apo) * taxa_real_mes
    p_fin = p_ini + apo + rend
    
    patr_inicial_lista.append(p_ini)
    aportes_lista.append(apo)
    rendimentos_lista.append(rend)
    patr_final_lista.append(p_fin)
    
    saldo_atual = p_fin

df = pd.DataFrame({
    "Mês": meses,
    "Ano": anos_linha,
    "Patrimônio Inicial": patr_inicial_lista,
    "Aporte": aportes_lista,
    "Rendimento Real": rendimentos_lista,
    "Patrimônio Final": patr_final_lista
})

# 4. EXIBIÇÃO DOS RESULTADOS (Cards de Destaque)
patrimonio_final_num = df["Patrimônio Final"].iloc[-1]
total_aportado_num = patrimonio_inicial + (aporte_mensal * total_meses)
total_juros_num = patrimonio_final_num - total_aportado_num

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"<div class='kpi-box' style='background-color: #E6F4EA; border-left: 5px solid #10B981;'>"
        f"<p style='margin:0; color:#555; font-size:14px;'><b>PATRIMÔNIO REAL PROJETADO</b></p>"
        f"<h2 style='margin:0; color:#10B981;'>R$ {patrimonio_final_num:,.2f}</h2>"
        f"</div>", unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"<div class='kpi-box' style='background-color: #F4F7FC; border-left: 5px solid #0B1B3D;'>"
        f"<p style='margin:0; color:#555; font-size:14px;'><b>TOTAL QUE SAIU DO SEU BOLSO</b></p>"
        f"<h2 style='margin:0; color:#0B1B3D;'>R$ {total_aportado_num:,.2f}</h2>"
        f"</div>", unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"<div class='kpi-box' style='background-color: #FFF9E6; border-left: 5px solid #F59E0B;'>"
        f"<p style='margin:0; color:#555; font-size:14px;'><b>GANHO EM JUROS REAIS</b></p>"
        f"<h2 style='margin:0; color:#F59E0B;'>R$ {total_juros_num:,.2f}</h2>"
        f"</div>", unsafe_allow_html=True
    )

# 5. GRÁFICO INTERATIVO (Plotly)
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df["Mês"], y=df["Patrimônio Final"],
    mode='lines', name='Patrimônio Líquido',
    line=dict(color='#10B981', width=3)
))

fig.update_layout(
    title="Curva de Crescimento Patrimonial Exponencial (Descontada a Inflação)",
    xaxis_title="Tempo (Meses)",
    yaxis_title="Valor Acumulado (R$)",
    template="plotly_white",
    height=450,
    hovermode="x"
)
st.plotly_chart(fig, use_container_width=True)

# 6. TABELA DE DADOS BRUTOS (Expansível para quem quiser analisar os números)
with st.expander("🔍 Visualizar Tabela de Evolução Mês a Mês"):
    st.dataframe(
        df.style.format({
            "Patrimônio Inicial": "R$ {:.2f}",
            "Aporte": "R$ {:.2f}",
            "Rendimento Real": "R$ {:.2f}",
            "Patrimônio Final": "R$ {:.2f}"
        }), use_container_width=True
    )