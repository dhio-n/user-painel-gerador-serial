import os
import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt

def conectar():
    return psycopg2.connect(
        user="postgres.qsqajbcsbuezstvnaofj",
        password=os.environ["SENHA"],
        host="aws-0-sa-east-1.pooler.supabase.com",
        port="6543",
        dbname="postgres",
        cursor_factory=RealDictCursor
    )

def criar_usuario(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    cursor.execute("""
        INSERT INTO usuarios (usuario, senha, status)
        VALUES (%s, %s, TRUE)
        ON CONFLICT (usuario) DO NOTHING
    """, (usuario, senha_hash))
    conn.commit()
    conn.close()

def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, usuario, status FROM usuarios ORDER BY id")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def alterar_status_usuario(usuario_id, novo_status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET status = %s WHERE id = %s", (novo_status, usuario_id))
    conn.commit()
    conn.close()

def autenticar_usuario(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
    user = cursor.fetchone()
    conn.close()
    
    if user and bcrypt.checkpw(senha.encode('utf-8'), user['senha'].encode('utf-8')):
        return user
    return None
