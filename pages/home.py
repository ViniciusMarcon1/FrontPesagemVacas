import streamlit as st
import pandas as pd
import numpy as np 
from api import get_pesagens, get_vacas, get_alertas

st.title('Dashboard')
st.markdown('Bem vindo ao Dashboard da Fazenda Exprimental Gralha Azul')
st.sidebar.markdown('- Essa página é dedicada para verificar informações gerais de forma rápida e prática!')
st.divider()

# Carregando dados
df_pesagens = get_pesagens()
df_vacas = get_vacas()
df_alertas = get_alertas()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Média de Peso por Vaca")
    if not df_pesagens.empty:
        media_peso = df_pesagens.groupby('id_vaca')['pesagem'].mean().reset_index()
        st.bar_chart(media_peso.set_index('id_vaca'))
    else:
        st.info("Sem dados de pesagem disponíveis")

with col2:
    st.markdown("#### Evolução de Peso")
    if not df_pesagens.empty:
        df_pesagens_sorted = df_pesagens.sort_values('data_hora')
        st.line_chart(df_pesagens_sorted.set_index('data_hora')['pesagem'])
    else:
        st.info("Sem dados de pesagem disponíveis")

with col3:
    st.markdown("#### Alertas Recentes")
    if not df_alertas.empty:
        st.dataframe(
            df_alertas[['tipo_alerta', 'data_hora']]
            .sort_values('data_hora', ascending=False)
            .head(5)
        )
    else:
        st.info("Sem alertas disponíveis")

st.markdown('## Pesagens Recentes')
if not df_pesagens.empty:
    # Juntando com informações das vacas
    df_completo = pd.merge(
        df_pesagens,
        df_vacas[['id_vaca', 'nome', 'rfid']],
        on='id_vaca',
        how='left'
    )
    df_completo['data_hora'] = df_completo['data_hora'].dt.strftime('%H:%M | %d/%m')
    st.dataframe(
        df_completo[['nome', 'rfid', 'pesagem', 'data_hora']]
        .sort_values('data_hora', ascending=False)
    )
else:
    st.info("Sem dados de pesagem disponíveis")