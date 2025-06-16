import streamlit as st
import pandas as pd
from api import get_usuarios
import requests

st.title('Usuários')
st.markdown('Painel de usuários e suas permissões')
st.sidebar.markdown('- Aqui podemos verificar os usuários cadastrados, suas permissões e quando eles foram cadastrados.')
    
tab1, tab2, tab3 = st.tabs(['Usuários', 'Adicionar Usuários', 'Remover Usuários'])

with tab1:
    st.markdown('## Usuários Cadastrados')
    df_usuarios = get_usuarios()
    if not df_usuarios.empty:
        # Formatando a data de criação
        df_usuarios['criado_em'] = df_usuarios['criado_em'].dt.strftime('%d/%m/%Y %H:%M')
        st.dataframe(
            df_usuarios[['nome', 'nivel_usuario', 'criado_em']]
            .sort_values('criado_em', ascending=False)
        )
    else:
        st.info("Sem usuários cadastrados")

with tab2:
    st.markdown('## Adicionar Usuários')
    niveis = ["Admin", "User"]
    with st.form("adicionar_usuarios"):
        st.write("Adicionar Usuários")
        nome = st.text_input('Nome do Usuário')
        email = st.text_input('Email do Usuário')
        nivel_usuario = st.selectbox("Selecione um nível de permissão", niveis)
        submitted = st.form_submit_button('Adicionar')

        if submitted:
            if nome and email and nivel_usuario:
                response = requests.post("http://localhost:8080/api/add_user", json={
                    "nome": nome,
                    "email": email,
                    "nivel_usuario": nivel_usuario
                })

                if response.status_code == 201:
                    st.success("Usuário adicionado com sucesso!")
                    st.rerun()
                elif response.status_code == 409:
                    st.warning("Um usuário com este e-mail já existe.")
                else:
                    st.error(f"Erro ao adicionar: {response.json().get('error', 'Erro desconhecido')}")
            else:
                st.warning("Preencha todos os campos para adicionar o usuário.")


with tab3:
    st.markdown('## Remover usuários')

    with st.form("remover_usuario"):
        st.write("Remover Usuário")
        df_usuarios = get_usuarios()
        
        if not df_usuarios.empty:
            usuarios_dict = dict(zip(df_usuarios['nome'], df_usuarios['id_usuario']))
            selected_user_name = st.selectbox("Selecione um usuário para apagar", list(usuarios_dict.keys()))
            
            submitted = st.form_submit_button("Remover")
            if submitted:
                user_id = usuarios_dict[selected_user_name]
                
                response = requests.post("http://localhost:8080/api/remove_user", json={"id_usuario": user_id})
                
                if response.status_code == 200:
                    st.success(f"Usuário '{selected_user_name}' removido com sucesso.")
                else:
                    st.error(f"Erro ao remover: {response.json().get('error', 'Erro desconhecido')}")
        else:
            st.info("Sem usuários cadastrados para remover")
            st.form_submit_button("Remover", disabled=True)
