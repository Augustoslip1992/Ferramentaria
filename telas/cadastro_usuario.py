import customtkinter as ctk
from tkinter import messagebox
from banco import conectar


def abrir_cadastro_usuario(app, limpar_tela):
    limpar_tela()

    def voltar():
        from telas.login import abrir_login

        abrir_login(app, limpar_tela)

    def cadastrar():
        nome = campo_nome.get()
        usuario = campo_usuario.get()
        email = campo_email.get()
        senha = campo_senha.get()

        if not nome or not usuario or not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos")
            return

        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
            INSERT INTO usuarios (nome, usuario, email, senha)
            VALUES (?, ?, ?, ?)
            """,
                (nome, usuario, email, senha),
            )

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

            from telas.login import abrir_login

            abrir_login(app, limpar_tela)

        except Exception as e:
            conn.close()
            print("ERRO REAL:", e)
            messagebox.showerror("Erro", str(e))

    ctk.CTkLabel(app, text="Cadastro de Usuário", font=("Arial", 24)).pack(pady=20)

    ctk.CTkLabel(app, text="Nome").pack()
    campo_nome = ctk.CTkEntry(app, width=250)
    campo_nome.pack(pady=5)

    ctk.CTkLabel(app, text="Usuário").pack()
    campo_usuario = ctk.CTkEntry(app, width=250)
    campo_usuario.pack(pady=5)

    ctk.CTkLabel(app, text="E-mail").pack()
    campo_email = ctk.CTkEntry(app, width=250)
    campo_email.pack(pady=5)

    ctk.CTkLabel(app, text="Senha").pack()
    campo_senha = ctk.CTkEntry(app, show="*", width=250)
    campo_senha.pack(pady=5)

    ctk.CTkButton(app, text="Cadastrar", command=cadastrar).pack(pady=15)

    ctk.CTkButton(app, text="Voltar", command=voltar).pack(pady=5)
