import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from datetime import datetime

class EmailService:
    def __init__(self, smtp_server, smtp_port, smtp_user, smtp_password, sender_email, use_ssl=False):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.sender_email = sender_email
        self.use_ssl = use_ssl

    def send_alert_email(self, subject, body, recipient_emails=None):
        if recipient_emails is None:
            recipient_emails = ["gusousaa1@gmail.com"]

        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = ", ".join(recipient_emails)
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            if self.use_ssl:
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            else:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.ehlo()
                server.starttls()
                server.ehlo()

            print("Conexao estabelecida | Comecando login")
            server.login(self.smtp_user, self.smtp_password)

            print(f"Enviando e-mail para: {recipient_emails}...")
            server.sendmail(self.sender_email, recipient_emails, msg.as_string())

            print("E-mail enviado")
            server.quit()

        except smtplib.SMTPConnectError as e:
            print(f"🚨 Erro de Conexão SMTP: {e}")
            with open("report.log", "a") as my_file:
                my_file.write(f"-{datetime.now()} | 🚨 Erro de Conexão SMTP: {e}")
        except smtplib.SMTPAuthenticationError as e:
            print(f"🚨 Erro de Autenticação SMTP: {e}")
            with open("report.log", "a") as my_file:
                my_file.write(f"-{datetime.now()} | 🚨 Erro de Autenticação SMTP: {e}")
        except smtplib.SMTPException as e:
            print(f"🚨 Erro SMTP Geral: {e}")
            with open("report.log", "a") as my_file:
                my_file.write(f"-{datetime.now()} | 🚨 Erro SMTP Geral: {e}")
        except Exception as e:
            print(f"🚨 Erro inesperado: {e}")
            with open("report.log", "a") as my_file:
                my_file.write(f"-{datetime.now()} | 🚨 Erro inesperado: {e}")
