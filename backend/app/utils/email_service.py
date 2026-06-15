import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings


def send_otp_email(to_email: str, otp: str, name: str = "there"):
    """
    Sends OTP via Gmail SMTP.
    In Java → like using JavaMailSender with SMTP config.
    """
    subject = "Your Profit Plus Verification Code"

    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #06060c; padding: 40px;">
            <div style="max-width: 400px; margin: auto; background-color: #0d0d18; 
                        border-radius: 16px; padding: 30px; border: 1px solid #1f1f33;">
                <h2 style="color: #ffffff;">Profit Plus</h2>
                <p style="color: #94a3b8;">Hi {name},</p>
                <p style="color: #94a3b8;">Your verification code is:</p>
                <div style="background-color: #1c1530; padding: 15px; border-radius: 10px; 
                            text-align: center; margin: 20px 0;">
                    <span style="font-size: 32px; font-weight: bold; color: #a78bfa; letter-spacing: 8px;">
                        {otp}
                    </span>
                </div>
                <p style="color: #64748b; font-size: 12px;">
                    This code expires in 5 minutes. If you didn't request this, please ignore this email.
                </p>
            </div>
        </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_EMAIL
    msg["To"] = to_email
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_EMAIL, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False