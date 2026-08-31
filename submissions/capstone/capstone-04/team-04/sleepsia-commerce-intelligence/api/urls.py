"""
API URL Routing for Sleepsia Commerce Intelligence Platform.
"""

from django.urls import path
from . import views

urlpatterns = [
    # 1. Health check
    path('health', views.health_check, name='health_check'),

    # 2. Dataset Endpoints
    path('dataset/summary', views.dataset_summary, name='dataset_summary'),
    path('dataset/reset-default', views.dataset_reset_default, name='dataset_reset_default'),
    path('dataset/upload', views.dataset_upload, name='dataset_upload'),

    # 3. Dynamic KPIs
    path('kpis', views.kpis_view, name='kpis_view'),

    # 4. Multi-Agent Analysis & Graph
    path('agents/analyze', views.agents_analyze, name='agents_analyze'),
    path('agents/graph', views.agents_graph, name='agents_graph'),

    # 5. Chat BI
    path('agents/chat', views.agents_chat, name='agents_chat'),

    # 6. Recommendation Feedback
    path('agents/feedback', views.agents_feedback, name='agents_feedback'),

    # 7. Daily Executive Report & Visuals
    path('report/generate', views.report_generate, name='report_generate'),
    path('report/dashboard-image', views.report_dashboard_image, name='report_dashboard_image'),

    # 8. Settings & Schedules
    path('settings', views.settings_view, name='settings_view'),
    path('schedules', views.schedules_view, name='schedules_view'),
    path('schedules/<str:job_id>', views.schedule_detail_view, name='schedule_detail_view'),
    path('schedules/<str:job_id>/toggle', views.schedule_toggle_view, name='schedule_toggle_view'),
    path('schedules/<str:job_id>/run-now', views.schedule_run_now_view, name='schedule_run_now_view'),

    # 9. Authentication
    path('auth/verify-email', views.auth_verify_email, name='auth_verify_email'),
    path('auth/sync-google-token', views.auth_sync_google_token, name='auth_sync_google_token'),
    path('auth/google-status', views.auth_google_status, name='auth_google_status'),

    # 10. Email Service
    path('email/send-report', views.email_send_report, name='email_send_report'),
    path('email/send-test', views.email_send_test, name='email_send_test'),

    # 11. Automated Daily Report Cron
    path('cron/daily-report', views.cron_daily_report, name='cron_daily_report'),
]
