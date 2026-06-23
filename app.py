import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página para o tema escuro/amplo
st.set_page_config(page_title="Target Finance Simulator", layout="wide", initial_sidebar_state="expanded")

# --- TRUQUE DE DESIGN (CSS) ---
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            min-width: 340px;
            max-width: 340px;
            background-color: #1a1c23;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.header("Parâmetros do Simulador")
st.sidebar.markdown("---")

patrimonio_inicial = st.sidebar.number_input("Patrimônio Inicial Atual (R$)", min_value=0.0, value=10000.0, step=1000.0)
aporte_mensal = st.sidebar.number_input("Aporte Mensal Estimado (R$)", min_value=0.0, value=1500.0, step=100.0)
taxa_juros_nominal = st.sidebar.slider("Taxa de Juros Nominal (% ao ano)", min_value=0.0, max_value=30.0, value=10.0, step=0.5)
inflacao_estimada = st.sidebar.slider("Inflação Estimada (% ao ano - IPCA)", min_value=0.0, max_value=20.0, value=4.0, step=0.1)
anos = st.sidebar.number_input("Tempo Alvo da Projeção (Anos)", min_value=1, max_value=50, value=15, step=1)

# --- CÁLCULOS MATEMÁTICOS ---
meses = anos * 12
taxa_mensal_nominal = (1 + taxa_juros_nominal / 100) ** (1 / 12) - 1
taxa_mensal_inflacao = (1 + inflacao_estimada / 100) ** (1 / 12) - 1
taxa_mensal_real = (1 + taxa_mensal_nominal) / (1 + taxa_mensal_inflacao) - 1

patrimonio_real = patrimonio_inicial
total_investido = patrimonio_inicial

dados_evolucao = []

for mes in range(1, meses + 1):
    rendimento_real = patrimonio_real * taxa_mensal_real
    # Corrigido: soma o rendimento e o aporte separadamente
    patrimonio_real += rendimento_real
    patrimonio_real += aporte_mensal
    total_investido += aporte_mensal
    
    dados_evolucao.append({
        "Mês": mes,
        "Ano": int(np.ceil(mes / 12)),
        "Patrimônio Total (Real)": patrimonio_real,
        "Total Investido": total_investido
    })

df = pd.DataFrame(dados_evolucao)
ganho_juros_real = patrimonio_real - total_investido

# --- CORPO PRINCIPAL DO SITE ---
st.title("Target Finance Simulator")
st.markdown("Projete o crescimento do seu patrimônio de longo prazo expurgando o efeito da inflação.")
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="PATRIMÔNIO REAL PROJETADO", value=f"R$ {patrimonio_real:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
with col2:
    st.metric(label="TOTAL QUE SAIU DO SEU BOLSO", value=f"R$ {total_investido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
with col3:
    st.metric(label="GANHO EM JUROS REAIS", value=f"R$ {ganho_juros_real:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

aba_grafico, aba_tabela = st.tabs(["Gráfico de Evolução", "Tabela Detalhada"])

with aba_grafico:
    st.subheader("Curva de Crescimento Patrimonial Exponencial")
    st.line_chart(df.set_index("Mês")[["Patrimônio Total (Real)", "Total Investido"]])

with aba_tabela:
    st.subheader("Evolução Mensal dos Saldos")
    df_formatado = df.copy()
    df_formatado["Patrimônio Total (Real)"] = df_formatado["Patrimônio Total (Real)"].map(lambda x: f"R$ {x:,.2f}")
    df_formatado["Total Investido"] = df_formatado["Total Investido"].map(lambda x: f"R$ {x:,.2f}")
    st.dataframe(df_formatado, use_container_width=True)