from django.urls import path
from . import views

urlpatterns = [
    path('ai/chat', views.ai_chat, name='ai-chat'),
    path('ai/root-cause', views.ai_root_cause, name='ai-root-cause'),
    path('ai/generate-content', views.generate_content, name='generate-content'),
    path('email/send', views.send_email_api, name='send-email'),
    path('email/send-live', views.send_live_email, name='send-live-email'),
    path('email/test-connection', views.test_email_connection, name='test-connection'),
    path('email/schedule', views.schedule_email, name='schedule-email'),
    path('email/history', views.email_history, name='email-history'),
    path('sheets/fetch-proxy', views.fetch_google_sheets, name='fetch-sheets'),
    path('sheets/push-webhook', views.push_sheets_webhook, name='push-webhook'),
    path('actions/transfer-stock', views.transfer_stock, name='transfer-stock'),
    path('actions/execute', views.execute_action, name='execute-action'),
]
