from django.db import models
from django.utils import timezone


class EmailLog(models.Model):
    DELIVERY_STATUS_CHOICES = [
        ('Delivered', 'Delivered'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
    ]

    id = models.CharField(max_length=50, primary_key=True)
    recipient_email = models.EmailField()
    sender_email = models.EmailField()
    subject = models.CharField(max_length=500)
    report_type = models.CharField(max_length=200)
    sent_at = models.CharField(max_length=100)
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='Delivered')
    summary_preview = models.TextField()
    follow_up_actions_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.recipient_email}"


class ScheduledEmail(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Paused', 'Paused'),
    ]

    id = models.CharField(max_length=50, primary_key=True)
    recipient_email = models.EmailField()
    sender_email = models.EmailField()
    report_type = models.CharField(max_length=200)
    cron = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    next_run = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.report_type} - {self.recipient_email}"


class StockTransfer(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
        ('Failed', 'Failed'),
    ]

    transfer_id = models.CharField(max_length=50, primary_key=True)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    sku = models.CharField(max_length=100)
    units = models.IntegerField()
    priority = models.CharField(max_length=50, default='Normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    courier_partner = models.CharField(max_length=200)
    tracking_number = models.CharField(max_length=100, unique=True)
    dispatched_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-dispatched_at']

    def __str__(self):
        return f"{self.transfer_id} - {self.sku}"


class ExecutedAction(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Executed', 'Executed'),
        ('Failed', 'Failed'),
    ]

    action_id = models.CharField(max_length=50, primary_key=True)
    action_code = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Executed')
    channel = models.CharField(max_length=100)
    execution_log = models.TextField()
    executed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-executed_at']

    def __str__(self):
        return f"{self.action_code} - {self.title}"
