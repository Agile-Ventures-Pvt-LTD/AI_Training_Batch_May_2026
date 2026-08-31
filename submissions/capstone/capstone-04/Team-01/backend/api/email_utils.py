from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_email(subject, recipient_email, template_name=None, context=None, plain_text=None):
    """
    Send an email with optional HTML template support.

    Args:
        subject: Email subject
        recipient_email: Recipient email address or list of emails
        template_name: Path to email template (optional)
        context: Context dict for template rendering (optional)
        plain_text: Plain text email body (used if no template)
    """
    if isinstance(recipient_email, str):
        recipient_email = [recipient_email]

    if template_name:
        html_message = render_to_string(template_name, context or {})
        plain_message = strip_tags(html_message)
    else:
        plain_message = plain_text or ""
        html_message = None

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_email,
        html_message=html_message,
        fail_silently=False,
    )


def send_password_reset_email(user_email, reset_url):
    """Send password reset email."""
    send_email(
        subject="Reset Your Password",
        recipient_email=user_email,
        context={
            'reset_url': reset_url,
            'user_email': user_email,
        },
        template_name='emails/password_reset.html'
    )


def send_welcome_email(user_email, username):
    """Send welcome email to new user."""
    send_email(
        subject="Welcome to Agile Ventures",
        recipient_email=user_email,
        context={
            'username': username,
        },
        template_name='emails/welcome.html'
    )
