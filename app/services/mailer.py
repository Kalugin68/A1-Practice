import smtplib
from email.message import EmailMessage


class EmailService:
    """Класс, отвечающий за работу с SMTP-сервером"""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def send_email(self, to, subject, template):
        """Метод отправки сообщения на SMTP-сервер"""

        msg = EmailMessage()

        msg["subject"] = subject
        msg["from"] = "sashakalugin74@gmail.com"
        msg["to"] = to

        msg.add_alternative(template, subtype="html")

        with smtplib.SMTP(self.host, self.port) as smtp:
            smtp.send_message(msg)

    def healthcheck(self):
        """Короткий пинг до smtp-сервера"""

        try:
            with smtplib.SMTP(self.host, self.port, timeout=5) as smtp:
                smtp.noop()

        except Exception as e:
            raise ConnectionError(
                "Service Unavailable"
            ) from e