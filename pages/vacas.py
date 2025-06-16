import streamlit as st
import pandas as pd
from api import get_vacas

st.title('Vacas')
st.markdown('Painel de vacas e suas informações')
st.sidebar.markdown('- Aqui podemos verificar as vacas cadastrados, suas informações e quando elas foram cadastradas.')
    
tab1, tab2, tab3 = st.tabs(['Vacas', 'Adicionar Vacas', 'Remover Vacas'])

with tab1:
    st.markdown('## Vacas Cadastradas')
    df_vacas = get_vacas()
    if not df_vacas.empty:
        #Formatando a data de criação
        #df_vacas['data_nascimento'] = df_vacas['data_nascimento'].dt.strftime('%d/%m/%Y')
        st.dataframe(df_vacas)
    else:
        st.info("Sem usuários cadastrados")

with tab2:
    st.markdown('## Adicionar vacas')

    with st.form("adicionar_vacas"):
        st.write("Adicionar Vacas")
        df_vacas = get_vacas()
        if not df_vacas.empty:
            vacas = df_vacas['nome'].tolist()
            selected_vaca = st.selectbox("Selecione um usuário para apagar", vacas)
            submitted = st.form_submit_button("Remover")
            if submitted:
                st.warning(f"Funcionalidade de remoção ainda não implementada na API")
                st.write("Usuário selecionado para remoção: ", selected_vaca)
        else:
            st.info("Sem vacas cadastrados para remover")
            st.form_submit_button("Remover", disabled=True)

with tab3: 
    st.markdown('## Remover vacas')

    with st.form("remover_vaca"):
        st.write("Remover Vacas")
        df_vacas = get_vacas()
        if not df_vacas.empty:
            vacas = df_vacas['nome'].tolist()
            selected_vaca = st.selectbox("Selecione um usuário para apagar", vacas)
            submitted = st.form_submit_button("Remover")
            if submitted:
                st.warning(f"Funcionalidade de remoção ainda não implementada na API")
                st.write("Usuário selecionado para remoção: ", selected_vaca)
        else:
            st.info("Sem vacas cadastradas para remover")
            st.form_submit_button("Remover", disabled=True)