import customtkinter as ctk
from tkinter import messagebox
from banco import conectar


def abrir_sistema(app, limpar_tela):
    # Limpa tela atual (login)
    limpar_tela()

    # =========================
    # FRAMES PRINCIPAIS
    # =========================

    # Frame lateral esquerdo (menu)
    frame_menu = ctk.CTkFrame(app, width=220)
    frame_menu.pack(side="left", fill="y", padx=10, pady=10)

    # Frame principal (conteúdo)
    frame_conteudo = ctk.CTkFrame(app)
    frame_conteudo.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # =========================
    # FUNÇÕES AUXILIARES
    # =========================

    def limpar_conteudo():
        # Remove todos os widgets do painel direito
        for widget in frame_conteudo.winfo_children():
            widget.destroy()

    def voltar():
        # Volta para tela de login
        from telas.login import abrir_login

        abrir_login(app, limpar_tela)

    # =========================
    # DASHBOARD
    # =========================

    def abrir_dashboard():
        # Limpa painel
        limpar_conteudo()

        # Título
        ctk.CTkLabel(frame_conteudo, text="Dashboard", font=("Arial", 24)).pack(pady=20)

        conn = conectar()
        cursor = conn.cursor()

        # Conta total de ferramentas
        cursor.execute("SELECT COUNT(*) FROM ferramentas")
        total = cursor.fetchone()[0]

        conn.close()

        # Exibe total
        ctk.CTkLabel(
            frame_conteudo,
            text=f"Total de ferramentas cadastradas: {total}",
            font=("Arial", 18),
        ).pack(pady=10)

    # =========================
    # CADASTRO
    # =========================

    def abrir_cadastro():
        # Limpa painel direito
        limpar_conteudo()

        # Título
        ctk.CTkLabel(
            frame_conteudo, text="Cadastro de Ferramentas", font=("Arial", 24)
        ).pack(pady=20)

        # Frame do formulário
        frame_form = ctk.CTkFrame(frame_conteudo)
        frame_form.pack(pady=20)

        # Código
        ctk.CTkLabel(frame_form, text="Código").grid(row=0, column=0, padx=10, pady=5)
        entry_codigo = ctk.CTkEntry(frame_form)
        entry_codigo.grid(row=0, column=1, padx=10, pady=5)

        # Descrição
        ctk.CTkLabel(frame_form, text="Descrição").grid(
            row=1, column=0, padx=10, pady=5
        )
        entry_descricao = ctk.CTkEntry(frame_form)
        entry_descricao.grid(row=1, column=1, padx=10, pady=5)

        # Marca
        ctk.CTkLabel(frame_form, text="Marca").grid(row=2, column=0, padx=10, pady=5)
        entry_marca = ctk.CTkEntry(frame_form)
        entry_marca.grid(row=2, column=1, padx=10, pady=5)

        # Categoria
        ctk.CTkLabel(frame_form, text="Categoria").grid(
            row=3, column=0, padx=10, pady=5
        )
        entry_categoria = ctk.CTkEntry(frame_form)
        entry_categoria.grid(row=3, column=1, padx=10, pady=5)

        # Quantidade
        ctk.CTkLabel(frame_form, text="Quantidade").grid(
            row=4, column=0, padx=10, pady=5
        )
        entry_quantidade = ctk.CTkEntry(frame_form)
        entry_quantidade.grid(row=4, column=1, padx=10, pady=5)

        # Estoque mínimo
        ctk.CTkLabel(frame_form, text="Estoque Mínimo").grid(
            row=5, column=0, padx=10, pady=5
        )
        entry_estoque_minimo = ctk.CTkEntry(frame_form)
        entry_estoque_minimo.grid(row=5, column=1, padx=10, pady=5)

        # Localização
        ctk.CTkLabel(frame_form, text="Localização").grid(
            row=6, column=0, padx=10, pady=5
        )
        entry_localizacao = ctk.CTkEntry(frame_form)
        entry_localizacao.grid(row=6, column=1, padx=10, pady=5)

        def salvar():
            # Validação simples
            if (
                entry_codigo.get() == ""
                or entry_descricao.get() == ""
                or entry_marca.get() == ""
            ):
                messagebox.showerror("Erro", "Preencha os campos obrigatórios.")
                return

            conn = conectar()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO ferramentas
                (
                    codigo,
                    descricao,
                    marca,
                    categoria,
                    quantidade,
                    estoque_minimo,
                    localizacao,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    entry_codigo.get(),
                    entry_descricao.get(),
                    entry_marca.get(),
                    entry_categoria.get(),
                    entry_quantidade.get(),
                    entry_estoque_minimo.get(),
                    entry_localizacao.get(),
                    "Disponível",
                ),
            )

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Ferramenta cadastrada com sucesso!")

        # Botão cadastrar
        ctk.CTkButton(frame_form, text="Cadastrar", command=salvar).grid(
            row=7, column=0, columnspan=2, pady=20
        )

    # =========================
    # MENU
    # =========================

    ctk.CTkLabel(frame_menu, text="MENU", font=("Arial", 22)).pack(pady=20)

    ctk.CTkButton(frame_menu, text="Dashboard", command=abrir_dashboard).pack(
        pady=10, padx=10
    )

    ctk.CTkButton(frame_menu, text="Cadastrar", command=abrir_cadastro).pack(
        pady=10, padx=10
    )

    ctk.CTkButton(frame_menu, text="Retirada").pack(pady=10, padx=10)

    ctk.CTkButton(frame_menu, text="Devolução").pack(pady=10, padx=10)

    ctk.CTkButton(frame_menu, text="Histórico").pack(pady=10, padx=10)

    ctk.CTkButton(frame_menu, text="Sair", command=voltar).pack(pady=30, padx=10)

    # Tela inicial
    abrir_dashboard()
