import streamlit as st
import pandas as pd
from api import get_usuarios

st.title('Usuários')
st.markdown('Painel de usuários e suas permissões')
st.sidebar.markdown('- Aqui podemos verificar os usuários cadastrados, suas permissões e quando eles foram cadastrados.')
    
tab1, tab2 = st.tabs(['Usuários', 'Remover Usuários'])

with tab1:
    st.markdown('## Usuários Cadastrados')
    df_usuarios = get_usuarios()
    if not df_usuarios.empty:
        # Formatando a data de criação
        df_usuarios['data_criacao'] = df_usuarios['data_criacao'].dt.strftime('%d/%m/%Y %H:%M')
        st.dataframe(
            df_usuarios[['nome', 'nivel_usuario', 'data_criacao']]
            .sort_values('data_criacao', ascending=False)
        )
    else:
        st.info("Sem usuários cadastrados")

with tab2:
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