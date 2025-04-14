import streamlit as st
from database import criar_usuario, listar_usuarios, alterar_status_usuario

st.set_page_config(page_title="Painel Admin", layout="centered")
st.title("🔐 Painel de Administração de Usuários")

st.sidebar.header("👤 Criar Novo Usuário")
novo_usuario = st.sidebar.text_input("Usuário")
nova_senha = st.sidebar.text_input("Senha", type="password")
if st.sidebar.button("Criar Usuário"):
    if novo_usuario and nova_senha:
        criar_usuario(novo_usuario, nova_senha)
        st.sidebar.success("Usuário criado com sucesso.")
    else:
        st.sidebar.warning("Preencha os campos.")

st.subheader("📋 Lista de Usuários")
usuarios = listar_usuarios()
for usuario in usuarios:
    col1, col2, col3 = st.columns([3, 2, 2])
    col1.write(usuario["usuario"])
    status_str = "Ativo ✅" if usuario["status"] else "Inativo ❌"
    col2.write(status_str)
    
    novo_status = not usuario["status"]
    if col3.button("Ativar" if not usuario["status"] else "Inativar", key=f"{usuario['id']}"):
        alterar_status_usuario(usuario["id"], novo_status)
        st.success(f"Status alterado para {'Ativo' if novo_status else 'Inativo'}.")
        st.rerun()
