# auth.py
import streamlit as st
from database import autenticar_usuario

def login_form():
    st.title("🔐 Login Administrativo")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    login_btn = st.button("Entrar")
    if st.session_state.get("logged_in"):
        # Limpa os campos após login
        st.session_state["usuario_login"] = ""
        st.session_state["senha_login"] = ""

    if login_btn:
        if autenticar_usuario(usuario, senha):
            st.session_state.logged_in = True
            st.session_state.usuario = usuario
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos, ou acesso não autorizado.")

def check_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
