"""
Django REST Framework API Views for Sleepsia Commerce Intelligence Platform.
"""

import base64
import datetime
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from rest_framework import status

from backend.services.dataset_service import (
    get_active_dataset,
    reset_to_default_dataset,
    parse_sleepsia_workbook,
    set_active_dataset,
)
from backend.services.kpi_engine import calculate_kpis
from backend.services.multi_agent_supervisor import (
    run_deterministic_multi_agent_analysis,
    build_daily_executive_report,
    record_agent_feedback,
    get_agent_feedback_store,
    run_orchestrated_agent_pipeline,
)
from backend.services.agent_graph_engine import execute_multi_agent_graph
from backend.services.gemini_service import run_gemini_supervisor_agent, query_gemini_chat_bi
from backend.services.report_image_generator import generate_dashboard_svg
from backend.services.scheduler import (
    get_email_settings,
    update_email_settings,
    get_schedules,
    create_schedule,
    update_schedule,
    delete_schedule,
    toggle_schedule_enabled,
    run_schedule_now,
    get_execution_history,
)
from backend.services.email_service import (
    set_stored_google_access_token,
    get_stored_google_access_token,
    get_stored_google_user_email,
    is_stored_google_token_valid,
    execute_reporting_pipeline,
)

# 1. Health check
@api_view(['GET'])
def health_check(request):
    return Response({
        'status': 'ok',
        'engine': 'Python Django Backend',
        'timestamp': datetime.datetime.now().isoformat(),
    })

# 2. Dataset Endpoints
@api_view(['GET'])
def dataset_summary(request):
    data = get_active_dataset()
    return Response({
        'metadata': data.get('metadata', {}),
        'productCount': len(data.get('products', [])),
        'salesCount': len(data.get('sales', [])),
        'marketplaceCount': len(data.get('marketplaceMasters', [])),
        'dateRange': data.get('metadata', {}).get('dateRange', {}),
    })

@api_view(['POST'])
def dataset_reset_default(request):
    data = reset_to_default_dataset()
    return Response({
        'success': True,
        'metadata': data.get('metadata', {}),
    })

@api_view(['POST'])
@parser_classes([JSONParser, MultiPartParser, FormParser, FileUploadParser])
def dataset_upload(request):
    try:
        file_bytes = None
        file_name = 'Uploaded_Sleepsia_Workbook.xlsx'

        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            file_bytes = uploaded_file.read()
            file_name = uploaded_file.name
        elif request.data and 'fileBase64' in request.data:
            base64_str = request.data['fileBase64']
            if ',' in base64_str:
                base64_str = base64_str.split(',')[1]
            file_bytes = base64.b64decode(base64_str)
            file_name = request.data.get('fileName', file_name)
        elif request.body:
            file_bytes = request.body

        if not file_bytes:
            return Response({'success': False, 'error': 'No file content provided'}, status=status.HTTP_400_BAD_REQUEST)

        result = parse_sleepsia_workbook(file_bytes, file_name)
        if not result.get('success'):
            return Response({'success': False, 'errors': result.get('errors', [])}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': True,
            'metadata': result.get('data', {}).get('metadata', {}),
            'warnings': result.get('warnings', []),
        })
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 3. Dynamic KPI Endpoint
@api_view(['GET'])
def kpis_view(request):
    date_val = request.query_params.get('date')
    channel_val = request.query_params.get('channel', 'All')
    cat_val = request.query_params.get('category', 'All')
    sku_val = request.query_params.get('sku', 'All')

    data = get_active_dataset()
    kpis = calculate_kpis(data, {
        'date': date_val,
        'channel': channel_val,
        'category': cat_val,
        'sku': sku_val,
    })
    return Response({'success': True, 'kpis': kpis})

# 4. Multi-Agent Analysis Endpoint
@api_view(['POST'])
def agents_analyze(request):
    try:
        date_val = request.data.get('date')
        use_gemini = request.data.get('useGemini', True)
        data = get_active_dataset()
        target_date = date_val or data.get('metadata', {}).get('dateRange', {}).get('end', '2026-08-07')

        orchestrated = run_orchestrated_agent_pipeline(data, target_date)
        findings = orchestrated.get('findings', [])

        if use_gemini:
            try:
                gemini_findings = run_gemini_supervisor_agent(data, target_date)
                if gemini_findings:
                    findings = gemini_findings
            except Exception as gemini_err:
                print(f"[API] Gemini enhanced interpretation fallback: {gemini_err}")

        return Response({
            'success': True,
            'findings': findings,
            'pipeline': orchestrated.get('pipeline', []),
            'state': orchestrated.get('state', {}),
            'report': orchestrated.get('report', {}),
            'date': target_date,
        })
    except Exception as e:
        print(f"[API] /api/agents/analyze error: {e}")
        data = get_active_dataset()
        orchestrated = run_orchestrated_agent_pipeline(data, request.data.get('date'))
        return Response({
            'success': True,
            'findings': orchestrated.get('findings', []),
            'pipeline': orchestrated.get('pipeline', []),
            'state': orchestrated.get('state', {}),
            'report': orchestrated.get('report', {}),
            'fallback': True,
        })

# 4b. Explicit Multi-Agent Graph Endpoint
@api_view(['GET'])
def agents_graph(request):
    try:
        date_val = request.query_params.get('date')
        data = get_active_dataset()
        target_date = date_val or data.get('metadata', {}).get('dateRange', {}).get('end', '2026-08-07')
        graph_result = run_orchestrated_agent_pipeline(data, target_date)
        return Response({
            'success': True,
            'pipeline': graph_result.get('pipeline', []),
            'state': graph_result.get('state', {}),
            'findings': graph_result.get('findings', []),
            'report': graph_result.get('report', {}),
        })
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 5. Chat BI Endpoint
@api_view(['POST'])
def agents_chat(request):
    try:
        msg = request.data.get('message')
        date_val = request.data.get('date')
        if not msg:
            return Response({'success': False, 'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

        data = get_active_dataset()
        res = query_gemini_chat_bi(msg, data, date_val)
        return Response({'success': True, 'answer': res.get('answer'), 'sources': res.get('sources', [])})
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 6. Recommendation Feedback
@api_view(['POST'])
def agents_feedback(request):
    finding_id = request.data.get('findingId')
    feedback = request.data.get('feedback')
    note = request.data.get('note')

    if not finding_id or not feedback:
        return Response({'success': False, 'error': 'findingId and feedback are required'}, status=status.HTTP_400_BAD_REQUEST)

    record_agent_feedback(finding_id, feedback, note)
    return Response({'success': True, 'allFeedback': get_agent_feedback_store()})

# 7. Daily Executive Report
@api_view(['GET'])
def report_generate(request):
    date_val = request.query_params.get('date')
    data = get_active_dataset()
    report = build_daily_executive_report(data, date_val)
    return Response({'success': True, 'report': report})

# 8. Dashboard SVG / Image Generator
@api_view(['GET'])
def report_dashboard_image(request):
    date_val = request.query_params.get('date')
    data = get_active_dataset()
    report = build_daily_executive_report(data, date_val)
    svg = generate_dashboard_svg(report)

    response = HttpResponse(svg, content_type='image/svg+xml')
    response['Content-Disposition'] = f'inline; filename="sleepsia_daily_dashboard_{report.get("reportDate")}.svg"'
    return response

# 9. Email Settings & Schedules
@api_view(['GET', 'POST'])
def settings_view(request):
    if request.method == 'GET':
        return Response({'success': True, 'settings': get_email_settings()})
    elif request.method == 'POST':
        new_settings = update_email_settings(request.data)
        return Response({'success': True, 'settings': new_settings})

@api_view(['GET', 'POST'])
def schedules_view(request):
    if request.method == 'GET':
        return Response({
            'success': True,
            'schedules': get_schedules(),
            'history': get_execution_history(),
            'settings': get_email_settings(),
        })
    elif request.method == 'POST':
        try:
            new_job = create_schedule(request.data)
            return Response({'success': True, 'schedule': new_job, 'schedules': get_schedules()})
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def schedule_detail_view(request, job_id):
    if request.method == 'PUT':
        updated = update_schedule(job_id, request.data)
        if not updated:
            return Response({'success': False, 'error': 'Schedule job not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'schedule': updated, 'schedules': get_schedules()})
    elif request.method == 'DELETE':
        deleted = delete_schedule(job_id)
        return Response({'success': True, 'deleted': deleted, 'schedules': get_schedules()})

@api_view(['POST'])
def schedule_toggle_view(request, job_id):
    job = toggle_schedule_enabled(job_id)
    if not job:
        return Response({'success': False, 'error': 'Schedule job not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'success': True, 'schedule': job, 'schedules': get_schedules()})

@api_view(['POST'])
def schedule_run_now_view(request, job_id):
    try:
        bearer_token = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            bearer_token = auth_header[7:]
        google_token = request.data.get('googleAccessToken') or bearer_token or get_stored_google_access_token()

        if google_token:
            set_stored_google_access_token(google_token)

        result = run_schedule_now(job_id, google_token)
        return Response({
            'success': True,
            'message': result.get('message'),
            'messageId': result.get('messageId'),
            'previewUrl': result.get('previewUrl'),
            'timestamp': result.get('timestamp'),
            'schedule': next((s for s in get_schedules() if s['id'] == job_id), None),
            'history': get_execution_history(),
        })
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 10. Simple Email Authentication
@api_view(['POST'])
def auth_verify_email(request):
    """Simple email-based authentication (no Firebase required)"""
    try:
        email = request.data.get('email', '').strip().lower()

        if not email:
            return Response({
                'success': False,
                'error': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Basic email validation
        import re
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, email):
            return Response({
                'success': False,
                'error': 'Invalid email format'
            }, status=status.HTTP_400_BAD_REQUEST)

        print(f"[Auth] Email verified: {email}")

        return Response({
            'success': True,
            'email': email,
            'authenticated': True,
            'message': f'Session created for {email}'
        })

    except Exception as e:
        print(f"[Auth] Email verification error: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 10. Google Auth Endpoints
@api_view(['POST'])
def auth_sync_google_token(request):
    try:
        access_token = request.data.get('accessToken')
        email = request.data.get('email')
        auth_header = request.headers.get('Authorization')
        bearer_token = auth_header[7:] if (auth_header and auth_header.startswith('Bearer ')) else None
        token = access_token or bearer_token

        if token and isinstance(token, str) and token.strip():
            set_stored_google_access_token(token, email)
            return Response({
                'success': True,
                'connected': True,
                'email': get_stored_google_user_email(),
                'message': f"Google Account ({get_stored_google_user_email()}) synced with automated scheduler.",
            })
        return Response({'success': False, 'error': 'No valid access token provided.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def auth_google_status(request):
    has_token = bool(get_stored_google_access_token())
    is_valid = is_stored_google_token_valid()
    return Response({
        'success': True,
        'connected': has_token and is_valid,
        'hasToken': has_token,
        'isValid': is_valid,
        'email': get_stored_google_user_email(),
    })

# 11. Send Report via Email
@api_view(['POST'])
def email_send_report(request):
    try:
        date_val = request.data.get('date')
        recipients = request.data.get('recipients')
        cc_recipients = request.data.get('ccRecipients')
        custom_subject = request.data.get('customSubject')
        body_token = request.data.get('googleAccessToken')

        auth_header = request.headers.get('Authorization')
        bearer_token = auth_header[7:] if (auth_header and auth_header.startswith('Bearer ')) else None
        google_token = bearer_token or body_token or get_stored_google_access_token()

        if google_token:
            set_stored_google_access_token(google_token)

        result = execute_reporting_pipeline({
            'date': date_val,
            'recipients': recipients,
            'ccRecipients': cc_recipients,
            'subject': custom_subject,
            'isTestEmail': False,
            'googleAccessToken': google_token,
        })

        return Response({
            'success': True,
            'message': result.get('message'),
            'messageId': result.get('messageId'),
            'previewUrl': result.get('previewUrl'),
            'timestamp': result.get('timestamp'),
            'details': {
                'to': result.get('recipients'),
                'cc': result.get('ccRecipients'),
                'subject': result.get('subject'),
                'attachedFiles': result.get('attachedFiles'),
                'imageAttachmentGenerated': result.get('imageAttachmentGenerated'),
            },
            'warnings': result.get('warnings'),
        })
    except Exception as e:
        print(f"[API] /api/email/send-report error: {e}")
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 12. Send Test Diagnostic Email
@api_view(['POST'])
def email_send_test(request):
    try:
        date_val = request.data.get('date')
        recipients = request.data.get('recipients')
        cc_recipients = request.data.get('ccRecipients')
        body_token = request.data.get('googleAccessToken')

        auth_header = request.headers.get('Authorization')
        bearer_token = auth_header[7:] if (auth_header and auth_header.startswith('Bearer ')) else None
        google_token = bearer_token or body_token or get_stored_google_access_token()

        if google_token:
            set_stored_google_access_token(google_token)

        result = execute_reporting_pipeline({
            'date': date_val,
            'recipients': recipients,
            'ccRecipients': cc_recipients,
            'isTestEmail': True,
            'googleAccessToken': google_token,
        })

        return Response({
            'success': True,
            'message': result.get('message'),
            'messageId': result.get('messageId'),
            'previewUrl': result.get('previewUrl'),
            'timestamp': result.get('timestamp'),
            'details': {
                'to': result.get('recipients'),
                'cc': result.get('ccRecipients'),
                'subject': result.get('subject'),
                'attachedFiles': result.get('attachedFiles'),
                'imageAttachmentGenerated': result.get('imageAttachmentGenerated'),
            },
            'warnings': result.get('warnings'),
        })
    except Exception as e:
        print(f"[API] /api/email/send-test error: {e}")
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 13. Cron Daily Report
@api_view(['POST'])
def cron_daily_report(request):
    try:
        print(f"[Scheduler] Manual/Cloud daily report trigger received at: {datetime.datetime.now().isoformat()}")
        result = execute_reporting_pipeline()
        return Response({
            'success': True,
            'schedulerJob': 'sleepsia-daily-report-cron',
            'executedAt': result.get('timestamp'),
            'message': result.get('message'),
            'messageId': result.get('messageId'),
            'previewUrl': result.get('previewUrl'),
            'recipients': result.get('recipients'),
            'attachedFiles': result.get('attachedFiles'),
        })
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
