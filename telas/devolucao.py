# Importa interface gráfica
import customtkinter as ctk

# Importa caixas de mensagem
from tkinter import messagebox

# Importa conexão com banco
from banco import conectar

# Importa data e hora atual
from datetime import datetime


def abrir_devolucao(app, limpar_tela):

    # Limpa a tela atual
    limpar_tela()

    # Função para voltar ao sistema principal
    def voltar():
        from telas.sistema import abrir_sistema
        abrir_sistema(app, limpar_tela)

    # Função para devolver ferramenta
    def devolver():

        # Captura código digitado
        codigo = entry_codigo.get()

        # Verifica se o campo foi preenchido
        if not codigo:
            messagebox.showerror("Erro", "Digite o código da ferramenta.")
            return

        # Conecta ao banco
        conn = conectar()
        cursor = conn.cursor()

        # Busca ferramenta pelo código
        cursor.execute("""
        SELECT * FROM ferramentas
        WHERE codigo=?
        """, (codigo,))

        ferramenta = cursor.fetchone()

        # Verifica se ferramenta existe
        if not ferramenta:
            conn.close()
            messagebox.showerror("Erro", "Ferramenta não encontrada.")
            return

        # Pega status atual
        status = ferramenta[7]

        # Verifica se está em uso
        if status != "Em uso":
            conn.close()
            messagebox.showerror("Erro", "Ferramenta não está em uso.")
            return

        # Atualiza status para disponível
        cursor.execute("""
        UPDATE ferramentas
        SET status=?
        WHERE codigo=?
        """, ("Disponível", codigo))

        # Captura data atual
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

        # Registra no histórico
        cursor.execute("""
        INSERT INTO historico (
            codigo_ferramenta,
            nome_ferramenta,
            tipo_movimentacao,
            colaborador,
            setor,
            observacao,
            data_movimentacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            ferramenta[1],   # Código
            ferramenta[2],   # Nome
            "DEVOLUÇÃO",
            "-",
            "-",
            "Ferramenta devolvida",
            data_atual
        ))

        # Salva alterações
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Ferramenta devolvida com sucesso.")

        voltar()

    # Título da tela
    ctk.CTkLabel(
        app,
        text="Devolução de Ferramenta",
        font=("Arial", 24)
    ).pack(pady=20)

    # Campo código
    ctk.CTkLabel(app, text="Código da Ferramenta").pack()
    entry_codigo = ctk.CTkEntry(app, width=300)
    entry_codigo.pack(pady=10)

    # Botão devolver
    ctk.CTkButton(
        app,
        text="Confirmar Devolução",
        command=devolver
    ).pack(pady=10)

    # Botão voltar
    ctk.CTkButton(
        app,
        text="Voltar",
        command=voltar
    ).pack(pady=5)