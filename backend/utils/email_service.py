import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL

logger = logging.getLogger(__name__)

async def send_complaint_notification(
    complaint_id: int,
    title: str,
    description: str,
    category: str,
    location: str,
    severity: float,
    image_url: str = None
):
    """
    Send email notification when a new complaint is submitted
    """
    try:
        subject = f"New Complaint Report: {title} (ID: {complaint_id})"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>New Complaint Report</h2>
                <p><strong>Complaint ID:</strong> {complaint_id}</p>
                <p><strong>Title:</strong> {title}</p>
                <p><strong>Category:</strong> {category}</p>
                <p><strong>Location:</strong> {location}</p>
                <p><strong>Severity Score:</strong> {severity:.2f}</p>
                <hr>
                <p><strong>Description:</strong></p>
                <p>{description}</p>
                {'<p><strong>Image:</strong> ' + image_url + '</p>' if image_url else ''}
                <hr>
                <p>Please review and take appropriate action.</p>
            </body>
        </html>
        """
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = SENDER_EMAIL
        message["To"] = RECEIVER_EMAIL
        
        # Attach HTML body
        message.attach(MIMEText(html_body, "html"))
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
        
        logger.info(f"Email sent for complaint {complaint_id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

async def send_verification_email(
    user_email: str,
    verification_link: str
):
    """
    Send email verification link
    """
    try:
        subject = "Verify Your Email - Local Problem Reporter"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Email Verification</h2>
                <p>Thank you for registering with Local Problem Reporter!</p>
                <p>Click the link below to verify your email:</p>
                <p><a href="{verification_link}">Verify Email</a></p>
                <p>This link will expire in 24 hours.</p>
            </body>
        </html>
        """
        
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = SENDER_EMAIL
        message["To"] = user_email
        
        message.attach(MIMEText(html_body, "html"))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, user_email, message.as_string())
        
        logger.info(f"Verification email sent to {user_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send verification email: {str(e)}")
        return False

async def send_status_update_email(
    complaint_id: int,
    title: str,
    old_status: str,
    new_status: str,
    user_email: str
):
    """
    Send email when complaint status is updated
    """
    try:
        subject = f"Your Complaint Status Updated - {title}"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Complaint Status Update</h2>
                <p><strong>Complaint ID:</strong> {complaint_id}</p>
                <p><strong>Title:</strong> {title}</p>
                <p><strong>Previous Status:</strong> {old_status}</p>
                <p><strong>New Status:</strong> {new_status}</p>
                <p>Your complaint has been updated. Thank you for reporting!</p>
            </body>
        </html>
        """
        
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = SENDER_EMAIL
        message["To"] = user_email
        
        message.attach(MIMEText(html_body, "html"))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, user_email, message.as_string())
        
        logger.info(f"Status update email sent to {user_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send status update email: {str(e)}")
        return False
