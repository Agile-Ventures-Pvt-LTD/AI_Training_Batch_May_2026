from django.core.management.base import BaseCommand
from django.core.mail import send_mail, get_connection
from django.conf import settings
import json
from datetime import datetime


class Command(BaseCommand):
    help = 'Comprehensive email configuration debugging'

    def add_arguments(self, parser):
        parser.add_argument('recipient', type=str, help='Recipient email address')
        parser.add_argument('--skip-send', action='store_true', help='Skip actual email send')

    def handle(self, *args, **options):
        recipient = options['recipient']
        skip_send = options.get('skip_send', False)

        self.stdout.write('=' * 70)
        self.stdout.write('COMPREHENSIVE EMAIL DEBUGGING')
        self.stdout.write('=' * 70)

        # 1. Check Configuration
        self.stdout.write('\n[1] CONFIGURATION CHECK')
        self.stdout.write('-' * 70)
        self.stdout.write(f'EMAIL_BACKEND: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'EMAIL_HOST: {settings.EMAIL_HOST}')
        self.stdout.write(f'EMAIL_PORT: {settings.EMAIL_PORT}')
        self.stdout.write(f'EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}')
        self.stdout.write(f'EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}')
        self.stdout.write(f'EMAIL_HOST_PASSWORD: {"*" * len(settings.EMAIL_HOST_PASSWORD)}')
        self.stdout.write(f'DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}')

        # 2. Validate Configuration
        self.stdout.write('\n[2] VALIDATION CHECK')
        self.stdout.write('-' * 70)
        errors = []

        if not settings.EMAIL_HOST_USER:
            errors.append('✗ EMAIL_HOST_USER is empty')
        else:
            self.stdout.write(f'✓ EMAIL_HOST_USER is set: {settings.EMAIL_HOST_USER}')

        if not settings.EMAIL_HOST_PASSWORD:
            errors.append('✗ EMAIL_HOST_PASSWORD is empty')
        else:
            self.stdout.write(f'✓ EMAIL_HOST_PASSWORD is set (length: {len(settings.EMAIL_HOST_PASSWORD)})')

        if settings.DEFAULT_FROM_EMAIL != settings.EMAIL_HOST_USER:
            self.stdout.write(f'⚠ WARNING: DEFAULT_FROM_EMAIL ({settings.DEFAULT_FROM_EMAIL}) does not match EMAIL_HOST_USER ({settings.EMAIL_HOST_USER})')

        if settings.EMAIL_PORT not in [587, 465]:
            errors.append(f'✗ EMAIL_PORT {settings.EMAIL_PORT} is unusual (should be 587 or 465)')
        else:
            self.stdout.write(f'✓ EMAIL_PORT is valid: {settings.EMAIL_PORT}')

        if errors:
            self.stdout.write(self.style.ERROR('\n'.join(errors)))

        # 3. Test Connection
        self.stdout.write('\n[3] CONNECTION TEST')
        self.stdout.write('-' * 70)
        try:
            connection = get_connection()
            connection.open()
            self.stdout.write(self.style.SUCCESS('✓ SMTP connection successful'))
            connection.close()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ SMTP connection failed'))
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            self.stdout.write(self.style.ERROR(f'Error type: {type(e).__name__}'))
            return

        # 4. Test Email Send
        if not skip_send:
            self.stdout.write('\n[4] EMAIL SEND TEST')
            self.stdout.write('-' * 70)
            try:
                send_mail(
                    subject='Django Email Configuration Test',
                    message=f'This is a test email from Django SMTP.\n\nSent at: {datetime.now()}\nFrom: {settings.DEFAULT_FROM_EMAIL}\nTo: {recipient}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS('✓ Email sent successfully!'))
                self.stdout.write(f'✓ Check {recipient} for the test email')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Email send failed'))
                self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
                self.stdout.write(self.style.ERROR(f'Error type: {type(e).__name__}'))
                import traceback
                self.stdout.write(self.style.ERROR(traceback.format_exc()))
        else:
            self.stdout.write('\n[4] EMAIL SEND TEST')
            self.stdout.write('Skipped (use --skip-send=false to enable)')

        # 5. Summary
        self.stdout.write('\n[5] SUMMARY')
        self.stdout.write('-' * 70)
        if not errors:
            self.stdout.write(self.style.SUCCESS('✓ All checks passed!'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ {len(errors)} issues found'))
            for error in errors:
                self.stdout.write(error)

        self.stdout.write('=' * 70)
