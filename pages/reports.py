import streamlit as st
import pandas as pd
import numpy as np 
import api

st.title('Relatórios')
st.markdown('Relatórios e dados disponíveis para download')
st.sidebar.markdown('- Adicionar descrição.')

df_vacas = api.get_vacas()
df_pesagens = api.get_pesagens()
df_medidas = api.get_medidas()

tab1, tab2, tab3 = st.tabs(['Vacas', 'Pesagens', 'Medidas'])

with tab1:
    st.markdown('## Tabela Vacas')
    if not df_vacas.empty:
        st.dataframe(df_vacas)
    else:
        st.info("Sem dados de vacas disponíveis")

with tab2:
    st.markdown('## Tabela Pesagens')
    if not df_pesagens.empty:
        st.dataframe(df_pesagens)
    else:
        st.info("Sem dados de pesagens disponíveis")

with tab3:
    st.markdown('## Tabela Medidas')
    if not df_medidas.empty:
        st.dataframe(df_medidas)
    else:
        st.info("Sem dados de medidas disponíveis")