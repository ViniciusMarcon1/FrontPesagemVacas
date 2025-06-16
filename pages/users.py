import streamlit as st
import pandas as pd
from api import get_usuarios

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
        nome = st.text_input('Nome da Usuário')
        email = st.text_input('Email da Usuário')
        nivel_usuario = st.selectbox("Selecione um nível de permissão", niveis)
        st.form_submit_button('Adicionar')

with tab3:
    st.markdown('## Remover usuários')

    with st.form("remover_usuario"):
        st.write("Remover Usuário")
        df_usuarios = get_usuarios()
        if not df_usuarios.empty:
            usuarios = df_usuarios['nome'].tolist()
            selected_user = st.selectbox("Selecione um usuário para apagar", usuarios)
            submitted = st.form_submit_button("Remover")
            if submitted:
                st.warning(f"Funcionalidade de remoção ainda não implementada na API")
                st.write("Usuário selecionado para remoção: ", selected_user)
        else:
            st.info("Sem usuários cadastrados para remover")
            st.form_submit_button("Remover", disabled=True)