from django.db.models.signals import post_migrate
from django.dispatch import receiver
import os


@receiver(post_migrate)
def create_default_data(sender, **kwargs):
    from .models import EmailLog, ScheduledEmail

    if EmailLog.objects.count() == 0:
        EmailLog.objects.bulk_create([
            EmailLog(
                id='mail-log-1',
                recipient_email='vikashr984@gmail.com',
                sender_email='vikashr984@gmail.com',
                subject='[URGENT] Anomaly & Follow-Up Supply Chain Resolution: Sleepsia Pillow (SKU-SLP-001)',
                report_type='Quick Commerce OOS & Mother Hub Follow-up',
                sent_at='2026-08-17 07:16 AM IST',
                delivery_status='Delivered',
                summary_preview='Blinkit Bengaluru dark stores #HSR-04 and #KRM-06 reported 0 stock. Follow-up: 3,450 units available at Nelamangala Mother Hub. Transfer of 250 units initiated.',
                follow_up_actions_count=2
            ),
            EmailLog(
                id='mail-log-2',
                recipient_email='vikashr984@gmail.com',
                sender_email='vikashr984@gmail.com',
                subject='Weekly Business Review (WBR) - Week 33 Executive Briefing',
                report_type='WBR Executive Report',
                sent_at='2026-08-17 07:30 AM IST',
                delivery_status='Delivered',
                summary_preview='Gross sales ₹78.4L (+8.4% YoY). Quick commerce penetration 36.5%. ROAS 4.22x. Revenue at risk ₹16.2L.',
                follow_up_actions_count=4
            )
        ])

    if ScheduledEmail.objects.count() == 0:
        ScheduledEmail.objects.bulk_create([
            ScheduledEmail(
                id='sched-1',
                recipient_email='vikashr984@gmail.com',
                sender_email='vikashr984@gmail.com',
                report_type='Weekly Business Review (WBR)',
                cron='0 8 * * 1 (Every Monday 08:00 AM IST)',
                status='Active',
                next_run='2026-08-24 08:00 AM IST'
            ),
            ScheduledEmail(
                id='sched-2',
                recipient_email='vikashr984@gmail.com',
                sender_email='vikashr984@gmail.com',
                report_type='Daily Dark Store OOS & Stock Transfer Digest',
                cron='0 7,14,20 * * * (Daily at 07:00, 14:00, 20:00 IST)',
                status='Active',
                next_run='2026-08-18 14:00 PM IST'
            )
        ])
