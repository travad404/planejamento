import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("Programa de Eficiência Energética Residencial")
st.text("DEPLOY por Guilherme Tyba - UNESP ROSANA - Link do github:https://github.com/travad404/planejamento/tree/main")

st.header("Opções de Entrada de Dados")

upload_option = st.radio("Escolha como deseja inserir os dados", 
                         ("Upload de tabela", "Inserir manualmente"))

if upload_option == "Upload de tabela":
    uploaded_file = st.file_uploader("Envie um arquivo CSV contendo os campos nome, potencia_watts, inicio, fim, quantidade", type=["csv"])
    if uploaded_file:
        appliances_df = pd.read_csv(uploaded_file)
        st.subheader("Tabela Carregada")
        st.dataframe(appliances_df)
else:
    if "appliances" not in st.session_state:
        st.session_state["appliances"] = []

    nome = st.text_input("Nome do Eletrodoméstico")
    potencia_watts = st.number_input("Potência (em Watts)", min_value=0, step=10)
    quantidade = st.number_input("Quantidade", min_value=1, step=1)
    inicio = st.number_input("Hora de início (0 a 23)", min_value=0, max_value=23, step=1)
    fim = st.number_input("Hora de término (0 a 23)", min_value=0, max_value=24, step=1)

    if st.button("Adicionar"):
        st.session_state["appliances"].append({
            "nome": nome,
            "potencia_watts": potencia_watts,
            "quantidade": quantidade,
            "inicio": inicio,
            "fim": fim
        })

    appliances_df = pd.DataFrame(st.session_state["appliances"])

    if not appliances_df.empty:
        st.subheader("Tabela de Eletrodomésticos")
        st.dataframe(appliances_df)

if not appliances_df.empty:
    appliances_df["daily_consumption_kwh"] = appliances_df.apply(
        lambda row: (row["potencia_watts"] / 1000) * (row["fim"] - row["inicio"]) * row["quantidade"],
        axis=1,
    )
    appliances_df["monthly_consumption_kwh"] = appliances_df["daily_consumption_kwh"] * 30

    st.header("Consumo Diário por Eletrodoméstico")
    plt.figure(figsize=(10, 6))
    plt.barh(appliances_df["nome"], appliances_df["daily_consumption_kwh"], color="lightgreen")
    plt.xlabel("Consumo (kWh)")
    plt.ylabel("Eletrodoméstico")
    plt.title("Consumo Diário por Eletrodoméstico")
    for index, value in enumerate(appliances_df["daily_consumption_kwh"]):
        plt.text(value, index, f"{value:.2f} kWh", va="center")
    st.pyplot(plt)

    st.header("Consumo Mensal por Eletrodoméstico")
    plt.figure(figsize=(10, 6))
    plt.barh(appliances_df["nome"], appliances_df["monthly_consumption_kwh"], color="skyblue")
    plt.xlabel("Consumo (kWh)")
    plt.ylabel("Eletrodoméstico")
    plt.title("Consumo Mensal por Eletrodoméstico")
    for index, value in enumerate(appliances_df["monthly_consumption_kwh"]):
        plt.text(value, index, f"{value:.2f} kWh", va="center")
    st.pyplot(plt)

    hourly_consumption = np.zeros(24)
    for _, row in appliances_df.iterrows():
        for hour in range(int(row["inicio"]), int(row["fim"])):
            hourly_consumption[hour] += (row["potencia_watts"] / 1000) * row["quantidade"]

    st.header("Consumo Hora a Hora (kWh)")
    plt.figure(figsize=(12, 6))
    plt.bar(range(24), hourly_consumption, color="orange")
    plt.xlabel("Hora do Dia")
    plt.ylabel("Consumo (kWh)")
    plt.title("Consumo de Energia Hora a Hora")
    for hour, value in enumerate(hourly_consumption):
        plt.text(hour, value + 0.01, f"{value:.2f}", ha="center")
    st.pyplot(plt)

    st.header("Cálculo de Custo")
    rate = st.number_input("Informe a taxa de energia em R$/kWh", min_value=0.0, step=0.01)
    if rate > 0:
        total_daily_cost = appliances_df["daily_consumption_kwh"].sum() * rate
        total_monthly_cost = appliances_df["monthly_consumption_kwh"].sum() * rate

        st.metric("Custo Total Diário (R$)", f"{total_daily_cost:.2f}")
        st.metric("Custo Total Mensal (R$)", f"{total_monthly_cost:.2f}")

    st.subheader("Exportar Tabela")
    csv = appliances_df.to_csv(index=False).encode("utf-8")
    st.download_button("Baixar CSV", csv, "consumo_residencial.csv", "text/csv")
