# Importa interface gráfica
import customtkinter as ctk

# Importa tabela
from tkinter import ttk

# Importa conexão com banco
from banco import conectar


def abrir_historico(app, limpar_tela):

    # Limpa tela atual
    limpar_tela()

    # Função voltar
    def voltar():
        from telas.sistema import abrir_sistema
        abrir_sistema(app, limpar_tela)

    # Conecta ao banco
    conn = conectar()
    cursor = conn.cursor()

    # Título
    ctk.CTkLabel(
        app,
        text="Histórico de Movimentações",
        font=("Arial", 24)
    ).pack(pady=20)

    # Frame tabela
    frame_tabela = ctk.CTkFrame(app)
    frame_tabela.pack(fill="both", expand=True, padx=20, pady=20)

    # Colunas da tabela
    colunas = (
        "ID",
        "Código",
        "Ferramenta",
        "Tipo",
        "Colaborador",
        "Setor",
        "Data"
    )

    # Cria tabela
    tabela = ttk.Treeview(
        frame_tabela,
        columns=colunas,
        show="headings"
    )

    # Configura colunas
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=130)

    tabela.pack(fill="both", expand=True)

    # Busca histórico no banco
    cursor.execute("""
    SELECT id,
           codigo_ferramenta,
           nome_ferramenta,
           tipo_movimentacao,
           colaborador,
           setor,
           data_movimentacao
    FROM historico
    ORDER BY id DESC
    """)

    dados = cursor.fetchall()

    # Adiciona registros na tabela
    for item in dados:
        tabela.insert("", "end", values=item)

    conn.close()

    # Botão voltar
    ctk.CTkButton(
        app,
        text="Voltar",
        command=voltar
    ).pack(pady=10)