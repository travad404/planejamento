import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title(Programa de Eficiência Energética Residencial)
st.text(feito por Guilherme Tyba)

st.header(Opções de Entrada de Dados)

upload_option = st.radio(Escolha como deseja inserir os dados, 
                         (Upload de tabela, Inserir manualmente))

if upload_option == Upload de tabela
    uploaded_file = st.file_uploader(Envie um arquivo CSV contendo os campos name, power_watts, start_hour, end_hour, quantity, type=[csv])
    if uploaded_file
        appliances_df = pd.read_csv(uploaded_file)
        st.subheader(Tabela Carregada)
        st.dataframe(appliances_df)
else
    if appliances not in st.session_state
        st.session_state[appliances] = []

    name = st.text_input(Nome do Eletrodoméstico)
    power_watts = st.number_input(Potência (em Watts), min_value=0, step=10)
    quantity = st.number_input(Quantidade, min_value=1, step=1)
    start_hour = st.number_input(Hora de início (0 a 23), min_value=0, max_value=23, step=1)
    end_hour = st.number_input(Hora de término (0 a 23), min_value=0, max_value=23, step=1)

    if st.button(Adicionar)
        st.session_state[appliances].append({
            name name,
            power_watts power_watts,
            quantity quantity,
            start_hour start_hour,
            end_hour end_hour
        })

    appliances_df = pd.DataFrame(st.session_state[appliances])

    if not appliances_df.empty
        st.subheader(Tabela de Eletrodomésticos)
        st.dataframe(appliances_df)

if not appliances_df.empty
    appliances_df[daily_consumption_kwh] = appliances_df.apply(
        lambda row ((row[power_watts]  1000)  (row[end_hour] - row[start_hour])  row[quantity]),
        axis=1,
    )
    appliances_df[monthly_consumption_kwh] = appliances_df[daily_consumption_kwh]  30

    st.header(Consumo Diário por Eletrodoméstico)
    plt.figure(figsize=(10, 6))
    plt.barh(appliances_df[name], appliances_df[daily_consumption_kwh], color=lightgreen)
    plt.xlabel(Consumo (kWh))
    plt.ylabel(Eletrodoméstico)
    plt.title(Consumo Diário por Eletrodoméstico)
    for index, value in enumerate(appliances_df[daily_consumption_kwh])
        plt.text(value, index, f{value.2f} kWh, va='center')
    st.pyplot(plt)

    st.header(Consumo Mensal por Eletrodoméstico)
    plt.figure(figsize=(10, 6))
    plt.barh(appliances_df[name], appliances_df[monthly_consumption_kwh], color=skyblue)
    plt.xlabel(Consumo (kWh))
    plt.ylabel(Eletrodoméstico)
    plt.title(Consumo Mensal por Eletrodoméstico)
    for index, value in enumerate(appliances_df[monthly_consumption_kwh])
        plt.text(value, index, f{value.2f} kWh, va='center')
    st.pyplot(plt)

    st.header(Cálculo de Custo)
    rate = st.number_input(Informe a taxa de energia em R$kWh, min_value=0.0, step=0.01)
    if rate  0
        total_daily_cost = appliances_df[daily_consumption_kwh].sum()  rate
        total_monthly_cost = appliances_df[monthly_consumption_kwh].sum()  rate

        st.metric(Custo Total Diário (R$), f{total_daily_cost.2f})
        st.metric(Custo Total Mensal (R$), f{total_monthly_cost.2f})

    st.subheader(Exportar Tabela)
    csv = appliances_df.to_csv(index=False).encode('utf-8')
    st.download_button(Baixar CSV, csv, consumo_residencial.csv, textcsv)
