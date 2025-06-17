import streamlit as st
from api import get_usuarios
from werkzeug.security import generate_password_hash, check_password_hash


st.set_page_config(page_title='Fazenda Experimental Gralha Azul', page_icon='🦜', layout='wide')

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    df_usuarios = get_usuarios()
    placeholder = st.empty()

    with placeholder.form("login"):
        st.markdown("#### Digite suas credenciais")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        usuario = df_usuarios[df_usuarios["email"] == email]

        if not usuario.empty:
            hash_armazenado = usuario.iloc[0]["senha"]

            if check_password_hash(hash_armazenado, password):
                placeholder.empty()
                st.success("Login realizado com sucesso!")
                st.session_state.logged_in = True
                st.session_state.usuario = email  
                st.session_state.nivel_usuario = usuario.iloc[0]["nivel_usuario"]  # <- Guarda o nível
                st.rerun()
            else:
                st.error("Senha incorreta.")
                st.session_state.logged_in = False
        else:
            st.error("Usuário não encontrado.")
            st.session_state.logged_in = False
        
    st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.nivel_usuario = None
        st.rerun()

# Páginas
login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
home = st.Page("pages/home.py", title="Home", icon="🦜")
users = st.Page("pages/users.py", title="Usuários", icon="👤")
vacas = st.Page("pages/vacas.py", title="Vacas", icon="🐮")
reports = st.Page("pages/reports.py", title="Relatórios", icon="📑")
config = st.Page("pages/config.py", title="Config", icon="⚙")

# Logo e navegação
sidebar_logo = 'images/n_logo.png'
st.logo(sidebar_logo, icon_image=sidebar_logo, size='large')
st.sidebar.title('Gralha Azul')

if st.session_state.logged_in:
    nivel = st.session_state.get("nivel_usuario", "user")  # Default como 'user' se não definido

    # Páginas padrão para todos
    main_pages = [home, reports]

    # Adiciona páginas restritas se admin
    if nivel == "Admin":
        main_pages.insert(1, users)
        main_pages.insert(2, vacas)

    pg = st.navigation(
        {
            "Páginas Principais": main_pages,
            "Configurações": [config, logout_page]
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()