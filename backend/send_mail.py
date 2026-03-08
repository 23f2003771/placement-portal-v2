import smtplib
from email.mime.text import MIMEText


SMTP_HOST = "localhost"
SMTP_PORT = 1025
FROM_EMAIL = "admin@gmail.com"

def send_email(to_email, subject, body):

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.sendmail(FROM_EMAIL, [to_email], msg.as_string())
        return True


def get_html_template():

    return """
    <html>
    <body style="font-family: Arial, sans-serif; background:#f4f6f9; margin:0; padding:20px;">
        <div style="max-width:600px; margin:auto; background:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 2px 6px rgba(0,0,0,0.1);">
            <div style="background:#2563eb; color:white; padding:18px;">
                <h2 style="margin:0;">Placement Portal v2</h2>
                <p style="margin:4px 0 0; font-size:14px; opacity:0.9;">College Placement Cell</p>
            </div>
            <div style="padding:22px; color:#333; font-size:15px; line-height:1.5;">
                <p>Hello,</p>
                <p>This is a test email from the <b>Placement Portal v2</b>. Your email notification system is working correctly.</p>
                <p>You will receive updates here about placement drives, interview schedules, and company announcements.</p>
                <div style="text-align:center; margin:20px 0;">
                    <a href="#" style="background:#2563eb; color:white; text-decoration:none; padding:10px 18px; border-radius:6px; font-weight:600;">Open Portal</a>
                </div>
                <p style="font-size:13px; color:#666;">If you did not expect this email, you can safely ignore it.</p>
            </div>
            <div style="background:#f1f5f9; padding:12px 18px; font-size:12px; color:#6b7280;">
                Sent by Placement Cell • Automated Notification
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    from app import app
    from models import User

    with app.app_context():
        print("--- Starting Bulk Email Process ---")
        users = User.query.all()
        html_content = get_html_template()

        for user in users:
            success = send_email(user.email, "Test: Beautiful HTML/CSS Email", html_content)
            if success:
                print(f"SUCCESS: Email sent to {user.email}")
        
        print("--- Process Completed ---")