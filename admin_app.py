import streamlit as st
from database import listar_usuarios, criar_usuario, alterar_status_usuario

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

usuarios = listar_usuarios()

for usuario in usuarios:
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
            st.experimental_rerun()  # Reinicia a execução após mudança
