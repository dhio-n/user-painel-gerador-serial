import psycopg2
from psycopg2.extras import RealDictCursor
import os
import bcrypt

def conectar():
    try:
        conn = psycopg2.connect(
            user="postgres.qsqajbcsbuezstvnaofj",
            password=os.environ["SENHA"],
            host="aws-0-sa-east-1.pooler.supabase.com",
            port="6543",
            dbname="postgres",
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        raise

# ---------- USUÁRIOS ----------

def criar_usuario(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
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
