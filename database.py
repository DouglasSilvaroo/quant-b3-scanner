
import sqlite3

# ==========================================
# CONEXÃO
# ==========================================

def conectar():

    conn = sqlite3.connect("users.db")

    return conn

# ==========================================
# CRIAR TABELA
# ==========================================

def criar_tabela_usuarios():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS usuarios (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE,

            password TEXT

        )

    """)

    conn.commit()

    conn.close()

# ==========================================
# ADICIONAR USUÁRIO
# ==========================================

def adicionar_usuario(username, password):

    conn = conectar()

    cursor = conn.cursor()

    try:

        cursor.execute(

            """

            INSERT INTO usuarios (

                username,
                password

            )

            VALUES (?, ?)

            """,

            (username, password)

        )

        conn.commit()

        sucesso = True

    except:

        sucesso = False

    conn.close()

    return sucesso

# ==========================================
# VALIDAR LOGIN
# ==========================================

def validar_usuario(username, password):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT *

        FROM usuarios

        WHERE username=?

        AND password=?

        """,

        (username, password)

    )

    usuario = cursor.fetchone()

    conn.close()

    return usuario
