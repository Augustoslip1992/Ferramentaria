import sqlite3


def conectar():
    conn = sqlite3.connect("ferramentas.db")
    return conn


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # TABELA DE USUÁRIOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        usuario TEXT UNIQUE,
        email TEXT UNIQUE,
        senha TEXT
    )
    """)

    # TABELA DE FERRAMENTAS
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
