# Importa biblioteca para envio de e-mail SMTP
import smtplib

# Importa estrutura para montar corpo do e-mail
from email.mime.text import MIMEText

# Importa estrutura para criar e-mail completo
from email.mime.multipart import MIMEMultipart


# Função responsável por enviar e-mail com código de recuperação
def enviar_codigo(destinatario, codigo):

    # E-mail que enviará as mensagens
    EMAIL_REMETENTE = "maggot335L@gmail.com"

    # Senha de app gerada no Google
    SENHA_APP = "ewld uyhq imcc rnnr"

    # Assunto do e-mail
    assunto = "Recuperação de Senha - Sistema Ferramentaria"

    # Corpo da mensagem
    corpo = f"""
Olá,

Seu código de recuperação é:

{codigo}

Se você não solicitou esta recuperação, ignore este e-mail.
"""

    try:
        # Monta estrutura do e-mail
        mensagem = MIMEMultipart()
        mensagem["From"] = EMAIL_REMETENTE
        mensagem["To"] = destinatario
        mensagem["Subject"] = assunto

        # Adiciona texto no corpo
        mensagem.attach(MIMEText(corpo, "plain"))

        # Conecta ao servidor SMTP do Gmail
        servidor = smtplib.SMTP("smtp.gmail.com", 587)

        # Inicia conexão segura TLS
        servidor.starttls()

        # Faz login no Gmail
        servidor.login(EMAIL_REMETENTE, SENHA_APP)

        # Envia e-mail
        servidor.sendmail(
            EMAIL_REMETENTE,
            destinatario,
            mensagem.as_string()
        )

        # Fecha conexão
        servidor.quit()

        return True

    except Exception as erro:
        print("Erro ao enviar e-mail:", erro)
        return False