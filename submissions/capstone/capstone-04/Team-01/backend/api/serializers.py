from rest_framework import serializers
from .models import EmailLog, ScheduledEmail, StockTransfer, ExecutedAction


class EmailLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailLog
        fields = [
            'id',
            'recipient_email',
            'sender_email',
            'subject',
            'report_type',
            'sent_at',
            'delivery_status',
            'summary_preview',
            'follow_up_actions_count',
            'created_at',
        ]


class ScheduledEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledEmail
        fields = [
            'id',
            'recipient_email',
            'sender_email',
            'report_type',
            'cron',
            'status',
            'next_run',
            'created_at',
            'updated_at',
        ]


class StockTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransfer
        fields = [
            'transfer_id',
            'source',
            'destination',
            'sku',
            'units',
            'priority',
            'status',
            'courier_partner',
            'tracking_number',
            'dispatched_at',
            'updated_at',
        ]


class ExecutedActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutedAction
        fields = [
            'action_id',
            'action_code',
            'title',
            'status',
            'channel',
            'execution_log',
            'executed_at',
        ]
