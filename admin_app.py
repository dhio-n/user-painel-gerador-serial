import streamlit as st
from auth import login_form, check_login
from database import listar_usuarios, criar_usuario, alterar_status_usuario, usuario_existe, alterar_tipo_usuario

st.set_page_config(page_title="Painel Admin", layout="centered")

# Verifica se está logado
check_login()

if not st.session_state.logged_in:
    login_form()
    st.stop()

st.title("🔐 Painel de Administração de Usuários")

# ---------- CRIAÇÃO DE NOVO USUÁRIO ----------
st.header("👥 Criar novo usuário")
novo_usuario = st.text_input("Nome de usuário", key="novo_usuario")
nova_senha = st.text_input("Senha", type="password", key="nova_senha")
tipo_usuario = st.selectbox("Tipo de usuário", options=["Comum", "Admin"], key="tipo_usuario")

if st.button("Criar usuário"):
    if novo_usuario and nova_senha:
        if usuario_existe(novo_usuario):
            st.warning("⚠️ Este nome de usuário já existe. Deseja alterar o tipo de usuário?")
        else:
            admin = tipo_usuario == "Admin"
            criar_usuario(novo_usuario, nova_senha, admin)
            st.success(f"Usuário {tipo_usuario} criado com sucesso!")
            # Limpar os campos após criação
            st.session_state.novo_usuario = ""
            st.session_state.nova_senha = ""
    else:
        st.warning("Preencha todos os campos.")

st.markdown("---")

# ---------- LISTA DE USUÁRIOS ----------
st.header("📋 Lista de usuários")

if 'usuarios' not in st.session_state:
    st.session_state.usuarios = listar_usuarios()

for usuario in st.session_state.usuarios:
    col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])
    with col1:
        st.write(f"👤 {usuario['usuario']}")
    with col2:
        status_label = "✅ Ativo" if usuario["ativo"] else "❌ Inativo"
        st.write(f"Status: {status_label}")
    with col3:
        tipo_atual = "Admin" if usuario["admin"] else "Comum"
        novo_tipo = "Comum" if usuario["admin"] else "Admin"
        if st.button(f"➡️ {novo_tipo}", key=f"tipo_{usuario['id']}"):
            alterar_tipo_usuario(usuario["id"], not usuario["admin"])
            st.success(f"Papel do usuário {usuario['usuario']} alterado para {novo_tipo}!")
            st.session_state.usuarios = listar_usuarios()
            break
        else:
            st.write(f"Tipo: {tipo_atual}")
    with col4:
        novo_status = not usuario["ativo"]
        label_botao = "Inativar" if usuario["ativo"] else "Ativar"
        if st.button(label_botao, key=f"status_{usuario['id']}"):
            alterar_status_usuario(usuario["id"], novo_status)
            st.session_state.usuarios = listar_usuarios()
            st.success(f"Status do usuário {usuario['usuario']} alterado!")
            break

# ---------- BOTÃO DE LOGOUT ----------
st.markdown("---")
if st.button("🚪 Sair"):
    st.session_state.logged_in = False
    st.experimental_rerun()
