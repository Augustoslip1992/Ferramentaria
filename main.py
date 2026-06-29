import customtkinter as ctk
from banco import criar_tabelas
from telas.login import abrir_login

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Ferramentaria Mili")
app.geometry("900x700")


def limpar_tela():
    for widget in app.winfo_children():
        widget.destroy()


criar_tabelas()
abrir_login(app, limpar_tela)

app.mainloop()
