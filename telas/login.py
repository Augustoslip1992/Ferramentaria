# Importa biblioteca da interface
import customtkinter as ctk

# Importa janelas de alerta
from tkinter import messagebox

# Importa conexão com banco
from banco import conectar

# Importa tela principal do sistema
from telas.sistema import abrir_sistema

# Importa tela cadastro de usuário
from telas.cadastro_usuario import abrir_cadastro_usuario

# Importa serviço de envio de e-mail
from util.email_service import enviar_codigo

# Importa gerador de código aleatório
import random


def abrir_login(app, limpar_tela):

    # Limpa widgets da tela atual
    limpar_tela()

    # Função de login
    def validar_login():
        usuario = campo_usuario.get()
        senha = campo_senha.get()

        print("Tentando login...")
        print("Usuário:", usuario)
        print("Senha:", senha)

        conn = conectar()
        cursor = conn.cursor()

        # Busca usuário no banco
        cursor.execute(
            """
        SELECT * FROM usuarios
        WHERE usuario=? AND senha=?
        """,
            (usuario, senha),
        )

        resultado = cursor.fetchone()
        conn.close()

        print("Resultado banco:", resultado)

        if resultado:
            abrir_sistema(app, limpar_tela)
        else:
            label_resultado.configure(
                text="Usuário ou senha incorretos", text_color="red"
            )

    # Função recuperar senha
    def esqueceu_senha():

        # Pega e-mail digitado
        email = campo_usuario.get()

        if not email:
            messagebox.showwarning("Aviso", "Digite seu e-mail no campo usuário.")
            return

        conn = conectar()
        cursor = conn.cursor()

        # Verifica se e-mail existe
        cursor.execute(
            """
        SELECT * FROM usuarios WHERE email=?
        """,
            (email,),
        )

        usuario = cursor.fetchone()
        conn.close()

        if not usuario:
            messagebox.showerror("Erro", "E-mail não encontrado.")
            return

        # Gera código aleatório
        codigo = str(random.randint(100000, 999999))

        # Envia e-mail
        enviado = enviar_codigo(email, codigo)

        if not enviado:
            messagebox.showerror("Erro", "Falha ao enviar e-mail.")
            return

        messagebox.showinfo("Sucesso", f"Código enviado para {email}")

        abrir_validacao_codigo(email, codigo)

    # Tela validação de código
    def abrir_validacao_codigo(email, codigo_enviado):
        limpar_tela()

        def validar_codigo():
            codigo_digitado = campo_codigo.get()

            if codigo_digitado == codigo_enviado:
                abrir_nova_senha(email)
            else:
                resultado_codigo.configure(text="Código inválido", text_color="red")

        ctk.CTkLabel(app, text="Validação de Código", font=("Arial", 24)).pack(pady=20)

        ctk.CTkLabel(app, text="Digite o código recebido").pack()

        campo_codigo = ctk.CTkEntry(app, width=250)
        campo_codigo.pack(pady=10)

        ctk.CTkButton(app, text="Validar", command=validar_codigo).pack(pady=10)

        resultado_codigo = ctk.CTkLabel(app, text="")
        resultado_codigo.pack()

    # Tela nova senha
    def abrir_nova_senha(email):
        limpar_tela()

        def salvar_nova_senha():
            nova_senha = campo_nova_senha.get()

            if not nova_senha:
                messagebox.showerror("Erro", "Digite uma nova senha")
                return

            conn = conectar()
            cursor = conn.cursor()

            cursor.execute(
                """
            UPDATE usuarios
            SET senha=?
            WHERE email=?
            """,
                (nova_senha, email),
            )

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Senha alterada com sucesso")

            abrir_login(app, limpar_tela)

        ctk.CTkLabel(app, text="Nova Senha", font=("Arial", 24)).pack(pady=20)

        campo_nova_senha = ctk.CTkEntry(app, show="*", width=250)
        campo_nova_senha.pack(pady=10)

        ctk.CTkButton(app, text="Salvar", command=salvar_nova_senha).pack(pady=10)

    # Interface login
    ctk.CTkLabel(app, text="Sistema de Login", font=("Arial", 24)).pack(pady=20)

    ctk.CTkLabel(app, text="Usuário").pack()

    campo_usuario = ctk.CTkEntry(app, width=250)
    campo_usuario.pack(pady=5)

    ctk.CTkLabel(app, text="Senha").pack()

    campo_senha = ctk.CTkEntry(app, show="*", width=250)
    campo_senha.pack(pady=5)

    ctk.CTkButton(app, text="Login", command=validar_login).pack(pady=10)

    ctk.CTkButton(
        app,
        text="Cadastrar Usuário",
        command=lambda: abrir_cadastro_usuario(app, limpar_tela),
    ).pack(pady=5)

    ctk.CTkButton(app, text="Esqueci minha senha", command=esqueceu_senha).pack(pady=5)

    label_resultado = ctk.CTkLabel(app, text="")
    label_resultado.pack(pady=10)
