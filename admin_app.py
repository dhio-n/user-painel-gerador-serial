import streamlit as st
from database import listar_usuarios, criar_usuario, alterar_status_usuario, verificar_login
import bcrypt
import base64
import os

# =========================
# FUNÇÕES DE AUTENTICAÇÃO
# =========================
def verificar_login(usuario, senha):
    # Conectar ao banco e verificar a senha (já implementada)
    pass

# =========================
# TELA DE LOGIN
# =========================
def tela_login():
    caminho_logo = os.path.join(os.path.dirname(__file__), "LOGO2.png")
    
    if os.path.exists(caminho_logo):
        with open(caminho_logo, "rb") as image_file:
            encoded_logo = base64.b64encode(image_file.read()).decode()
        st.markdown(f"""
            <style>
                .stApp {{
                    background-image: url("data:image/png;base64,{encoded_logo}");
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                }}
                .block-container {{
                    background-color: rgba(255, 255, 255, 0.85);
                    padding: 2rem;
                    border-radius: 10px;
                    max-width: 400px;
                    margin: auto;
                    margin-top: 100px;
                }}
            </style>
        """, unsafe_allow_html=True)

    st.subheader("🔐 Painel de Administração de Usuários - Login")
    usuario = st.text_input("Usuário", key="login_usuario")
    senha = st.text_input("Senha", type="password", key="login_senha")

    if st.button("Entrar"):
        if verificar_login(usuario, senha):
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.success("✅ Login realizado com sucesso!")
            st.experimental_rerun()  # Reinicia para carregar o painel admin
        else:
            st.error("❌ Usuário ou senha incorretos.")

# =========================
# TELA DE ADMIN (PANEL)
# =========================
def painel_admin():
    st.set_page_config(page_title="Painel Admin", layout="centered")

    st.title("🔐 Painel de Administração de Usuários")

    # ---------- CRIAÇÃO DE NOVO USUÁRIO ----------
    st.header("👥 Criar novo usuário")
    novo_usuario = st.text_input("Nome de usuário")
    nova_senha = st.text_input("Senha", type="password")
    tipo_usuario = st.selectbox("Tipo de usuário", options=["Comum", "Admin"])

    if st.button("Criar usuário"):
        if novo_usuario and nova_senha:
            # Definindo se o usuário será admin ou comum
            admin = tipo_usuario == "Admin"
            criar_usuario(novo_usuario, nova_senha, admin)
            st.success(f"Usuário {tipo_usuario} criado com sucesso!")
        else:
            st.warning("Preencha todos os campos.")

    st.markdown("---")

    # ---------- LISTA DE USUÁRIOS ----------
    st.header("📋 Lista de usuários")

    # Carregar os usuários da base de dados ou do estado atual
    if 'usuarios' not in st.session_state:
        st.session_state.usuarios = listar_usuarios()

    # Atualizar a lista de usuários após alterações no status
    for usuario in st.session_state.usuarios:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        with col1:
            st.write(f"👤 {usuario['usuario']}")
        with col2:
            status_label = "✅ Ativo" if usuario["ativo"] else "❌ Inativo"
            st.write(f"Status: {status_label}")
        with col3:
            tipo_label = "Admin" if usuario["admin"] else "Comum"
            st.write(f"Tipo: {tipo_label}")
        with col4:
            # Alterando o status
            novo_status = not usuario["ativo"]
            label_botao = "Inativar" if usuario["ativo"] else "Ativar"
            if st.button(label_botao, key=f"status_{usuario['id']}"):
                alterar_status_usuario(usuario["id"], novo_status)
                # Atualizando a lista de usuários no session_state
                st.session_state.usuarios = listar_usuarios()
                st.success(f"Status do usuário {usuario['usuario']} alterado!")
                break  # Impede múltiplos cliques seguidos

# =========================
# INICIALIZA ESTADO DE SESSÃO
# =========================
if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = ""

# =========================
# SE NÃO LOGADO, MOSTRA TELA DE LOGIN
# =========================
if not st.session_state.logado:
    tela_login()

# =========================
# SE LOGADO, MOSTRA O PAINEL ADMIN
# =========================
else:
    painel_admin()
