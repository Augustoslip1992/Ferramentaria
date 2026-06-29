import sqlite3


# Função que conecta no banco de dados SQLite
def conectar():
    conn = sqlite3.connect("ferramentas.db")
    return conn


# Função que cria as tabelas do sistema
def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # Cria tabela de ferramentas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ferramentas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT,
        descricao TEXT,
        marca TEXT,
        categoria TEXT,
        quantidade INTEGER,
        estoque_minimo INTEGER,
        localizacao TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()
