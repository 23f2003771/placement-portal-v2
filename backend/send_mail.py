import smtplib
from email.mime.text import MIMEText


SMTP_HOST = "localhost"
SMTP_PORT = 1025
FROM_EMAIL = "placementportal@gmail.com"

def send_email(to_email, subject, body):

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.sendmail(FROM_EMAIL, [to_email], msg.as_string())
        return True