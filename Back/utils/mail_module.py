import smtplib, ssl
from email.mime.text import MIMEText

from test_data import email_from, password, email_host, email_port


class MailUtil:
    @staticmethod
    def send_message(subject: str, email_to: str, body: str):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = email_from
        msg["To"] = email_to

        context = ssl.create_default_context()

        with smtplib.SMTP(email_host, email_port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(email_from, password)
            server.sendmail(email_from, email_to, msg.as_string())