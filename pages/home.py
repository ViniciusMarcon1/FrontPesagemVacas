import streamlit as st
import pandas as pd
import numpy as np 
import requests
import json 
from api import get_pesagens, get_vacas, get_alertas, get_medidas

st.title('Dashboard')
st.markdown('Bem vindo ao Dashboard da Fazenda Exprimental Gralha Azul')
st.sidebar.markdown('- Essa página é dedicada para verificar informações gerais de forma rápida e prática!')
st.divider()

# Carregando dados
df_pesagens = get_pesagens()
df_vacas = get_vacas()
df_alertas = get_alertas()
df_medidas = get_medidas()

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

st.markdown('## Medidas')
if not df_medidas.empty:
    edited_df = st.data_editor(df_medidas, num_rows="dynamic", use_container_width=True)

    if st.button("Salvar alterações"):
        st.info("Enviando alterações ao banco de dados...")

        # Verifica alterações linha a linha e envia via POST
        for index, row in edited_df.iterrows():
            original_row = df_medidas.loc[index]
            if not row.equals(original_row):
                payload = row.to_dict()
                #payload = json.loads(row.to_json(date_format='iso'))

                for key, value in payload.items():
                    if isinstance(value, pd.Timestamp):
                        payload[key] = value.strftime('%Y-%m-%d %H:%M:%S')

                try:
                    response = requests.post("http://localhost:8080/api/edit_medida", json=payload)
                    if response.status_code == 200:
                        st.success(f"Medida {payload['id_medida']} atualizada com sucesso!")
                    else:
                        st.error(f"Erro ao atualizar medida {payload['id_medida']}: {response.text}")
                except Exception as e:
                    st.error(f"Erro de conexão ao atualizar medida {payload['id_medida']}: {str(e)}")
else:
    st.info("Sem dados de pesagem disponíveis")