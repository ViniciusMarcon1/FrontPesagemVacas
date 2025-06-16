import streamlit as st
import pandas as pd
from api import get_vacas, delete_vaca

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
    st.markdown('## Adicionar Vacas')
    st.info("Funcionalidade de adição ainda não implementada.")

# TAB 3 – Remover Vacas
with tab3:
    st.markdown('## Remover Vacas')

    with st.form("remover_vaca"):
        df_vacas = get_vacas()
        if not df_vacas.empty:
            nomes_vacas = df_vacas['nome'].tolist()
            selected_vaca = st.selectbox("Selecione uma vaca para remover", nomes_vacas)
            submitted = st.form_submit_button("Remover")

            if submitted:
                sucesso = delete_vaca(selected_vaca)
                if sucesso:
                    st.success(f'Vaca "{selected_vaca}" removida com sucesso.')
                else:
                    st.error("Erro ao remover vaca. Verifique se o backend está rodando.")
        else:
            st.info("Sem vacas cadastradas para remover.")
