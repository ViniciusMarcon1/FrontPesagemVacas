import streamlit as st
import pandas as pd
from api import get_vacas, delete_vaca
import requests

st.title('Vacas')
st.markdown('Painel de vacas e suas informações')
st.sidebar.markdown('- Aqui podemos verificar as vacas cadastradas, suas informações e quando elas foram cadastradas.')

tab1, tab2, tab3 = st.tabs(['Vacas', 'Adicionar Vacas', 'Remover Vacas'])

# TAB 1 – Listar Vacas
with tab1:
    st.markdown('## Vacas Cadastradas')
    df_vacas = get_vacas()
    if not df_vacas.empty:
        st.dataframe(df_vacas)
    else:
        st.info("Sem vacas cadastradas")

# TAB 2 – Adicionar Vacas (placeholder)
with tab2:
    st.markdown('## Adicionar vacas')

    with st.form("adicionar_vacas"):
        st.write("Adicionar Vacas")
        nome = st.text_input('Nome da vaca')
        data_nascimento = st.date_input('Data de Nascimento')
        rfid = st.text_input("RFID da Tag da Vaca")
        submitted = st.form_submit_button('Adicionar')

        if submitted:
            if nome and data_nascimento and rfid:
                response = requests.post("http://localhost:8080/api/add_vaca", json={
                    "nome": nome,
                    "data_nascimento": data_nascimento.isoformat(), 
                    "rfid": rfid
                })

                if response.status_code == 201:
                    st.success("Vaca adicionada com sucesso!")
                    st.rerun()
                elif response.status_code == 409:
                    st.warning("Uma vaca com este RFID já existe.")
                else:
                    st.error(f"Erro ao adicionar: {response.json().get('error', 'Erro desconhecido')}")
            else:
                st.warning("Preencha todos os campos para adicionar a vaca.")

with tab3: 
    st.markdown('## Remover vacas')

    with st.form("remover_vaca"):
        st.write("Remover Vaca")
        df_vacas = get_vacas()

        if not df_vacas.empty:
            vacas_dict = dict(zip(df_vacas['nome'], df_vacas['id_vaca']))
            selected_vaca_name = st.selectbox("Selecione uma vaca para remover", list(vacas_dict.keys()))
            submitted = st.form_submit_button("Remover")

            if submitted:
                vaca_id = vacas_dict[selected_vaca_name]

                response = requests.post("http://localhost:8080/api/delete_vaca", json={"id_vaca": vaca_id})

                if response.status_code == 200:
                    st.success(f'Vaca "{selected_vaca_name}" removida com sucesso.')
                else:
                    try:
                        error_msg = response.json().get('error', 'Erro desconhecido')
                    except ValueError:
                        error_msg = response.text or 'Erro desconhecido'
                    st.error(f"Erro ao remover: {error_msg}")
        else:
            st.info("Sem vacas cadastradas para remover.")
            st.form_submit_button("Remover", disabled=True)