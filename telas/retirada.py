# Importa interface gráfica
import customtkinter as ctk

# Importa caixas de mensagem
from tkinter import messagebox

# Importa conexão com banco
from banco import conectar

# Importa data e hora atual
from datetime import datetime


def abrir_retirada(app, limpar_tela):
    
    # Limpa tela atual
    limpar_tela()

    # Função para voltar ao sistema principal
    def voltar():
        from telas.sistema import abrir_sistema
        abrir_sistema(app, limpar_tela)

    # Função de retirada
    def retirar():

        # Captura valores digitados
        codigo = entry_codigo.get()
        colaborador = entry_colaborador.get()
        setor = entry_setor.get()
        observacao = entry_obs.get()

        # Valida campos obrigatórios
        if not codigo or not colaborador or not setor:
            messagebox.showerror("Erro", "Preencha os campos obrigatórios.")
            return

        # Conecta ao banco
        conn = conectar()
        cursor = conn.cursor()

        # Busca ferramenta
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

        # Verifica status
        status = ferramenta[7]

        if status != "Disponível":
            conn.close()
            messagebox.showerror("Erro", "Ferramenta indisponível.")
            return

        # Atualiza status para Em uso
        cursor.execute("""
        UPDATE ferramentas
        SET status=?
        WHERE codigo=?
        """, ("Em uso", codigo))

        # Gera data/hora atual
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
            ferramenta[1],   # código
            ferramenta[2],   # nome
            "RETIRADA",
            colaborador,
            setor,
            observacao,
            data_atual
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Retirada realizada com sucesso.")

        voltar()

    # Título da tela
    ctk.CTkLabel(
        app,
        text="Retirada de Ferramenta",
        font=("Arial", 24)
    ).pack(pady=20)

    # Código ferramenta
    ctk.CTkLabel(app, text="Código da Ferramenta").pack()
    entry_codigo = ctk.CTkEntry(app, width=300)
    entry_codigo.pack(pady=5)

    # Colaborador
    ctk.CTkLabel(app, text="Colaborador").pack()
    entry_colaborador = ctk.CTkEntry(app, width=300)
    entry_colaborador.pack(pady=5)

    # Setor
    ctk.CTkLabel(app, text="Setor").pack()
    entry_setor = ctk.CTkEntry(app, width=300)
    entry_setor.pack(pady=5)

    # Observação
    ctk.CTkLabel(app, text="Observação").pack()
    entry_obs = ctk.CTkEntry(app, width=300)
    entry_obs.pack(pady=5)

    # Botão retirar
    ctk.CTkButton(
        app,
        text="Confirmar Retirada",
        command=retirar
    ).pack(pady=10)

    # Botão voltar
    ctk.CTkButton(
        app,
        text="Voltar",
        command=voltar
    ).pack(pady=5)