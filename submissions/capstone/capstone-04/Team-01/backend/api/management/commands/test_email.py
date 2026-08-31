from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Test email configuration'

    def add_arguments(self, parser):
        parser.add_argument('recipient', type=str, help='Recipient email address')

    def handle(self, *args, **options):
        recipient = options['recipient']

        self.stdout.write('=' * 60)
        self.stdout.write('Email Configuration Test')
        self.stdout.write('=' * 60)
        self.stdout.write(f'Backend: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'Host: {settings.EMAIL_HOST}')
        self.stdout.write(f'Port: {settings.EMAIL_PORT}')
        self.stdout.write(f'Use TLS: {settings.EMAIL_USE_TLS}')
        self.stdout.write(f'From Email: {settings.DEFAULT_FROM_EMAIL}')
        self.stdout.write(f'Host User: {settings.EMAIL_HOST_USER}')
        self.stdout.write(f'Recipient: {recipient}')
        self.stdout.write('=' * 60)

        try:
            self.stdout.write('Attempting to send test email...')
            send_mail(
                subject='Test Email from Django SMTP',
                message='This is a test email to verify Django SMTP configuration is working correctly.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS('✓ Email sent successfully!'))
            self.stdout.write(self.style.SUCCESS(f'✓ Check {recipient} for the test email'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Email failed: {str(e)}'))
            self.stdout.write(self.style.ERROR(f'✗ Error type: {type(e).__name__}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
