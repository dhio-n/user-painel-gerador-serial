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

def criar_usuario(usuario, senha, admin=False):
    conn = conectar()
    cursor = conn.cursor()
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
    cursor.execute("""
        INSERT INTO usuarios (usuario, senha, ativo, admin)
        VALUES (%s, %s, TRUE, %s)
        ON CONFLICT (usuario) DO NOTHING
    """, (usuario, senha_hash, admin))
    conn.commit()
    conn.close()

def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, usuario, ativo, admin FROM usuarios ORDER BY id")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def alterar_status_usuario(usuario_id, novo_status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET ativo = %s WHERE id = %s", (novo_status, usuario_id))
    conn.commit()
    conn.close()

# ---------- AUTENTICAÇÃO ----------

def autenticar_usuario(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, usuario, senha, ativo, admin FROM usuarios WHERE usuario = %s", (usuario,))
    usuario_db = cursor.fetchone()
    conn.close()

    if usuario_db and bcrypt.checkpw(senha.encode(), usuario_db['senha'].encode()):
        if usuario_db['ativo'] and usuario_db['admin']:
            return True  # Autenticado como admin
        else:
            return False  # Autenticado, mas não é admin ou não está ativo
    return False  # Dados inválidos ou senha incorreta


def usuario_existe(usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM usuarios WHERE usuario = %s", (usuario,))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe

def alterar_tipo_usuario(usuario_id, novo_admin):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET admin = %s WHERE id = %s", (novo_admin, usuario_id))
    conn.commit()
    conn.close()

