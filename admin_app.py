import streamlit as st
from database import listar_usuarios, criar_usuario, alterar_status_usuario

st.set_page_config(page_title="Painel Admin", layout="centered")

st.title("🔐 Painel de Administração de Usuários")

st.header("👥 Criar novo usuário")
novo_usuario = st.text_input("Nome de usuário")
nova_senha = st.text_input("Senha", type="password")

if st.button("Criar usuário"):
    if novo_usuario and nova_senha:
        criar_usuario(novo_usuario, nova_senha)
        st.success("Usuário criado com sucesso!")
    else:
        st.warning("Preencha todos os campos.")

st.markdown("---")

st.header("📋 Lista de usuários")

usuarios = listar_usuarios()

for usuario in usuarios:
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        st.write(f"👤 {usuario['usuario']}")
    with col2:
        status_label = "✅ Ativo" if usuario["status"] else "❌ Inativo"
        st.write(f"Status: {status_label}")
    with col3:
        novo_status = not usuario["status"]
        label_botao = "Inativar" if usuario["status"] else "Ativar"
        if st.button(label_botao, key=usuario["id"]):
            alterar_status_usuario(usuario["id"], novo_status)
            st.experimental_rerun()
