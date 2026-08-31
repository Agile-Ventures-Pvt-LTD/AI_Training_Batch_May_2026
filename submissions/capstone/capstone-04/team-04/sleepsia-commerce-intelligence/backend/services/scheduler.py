"""
Daily Executive Report Scheduler & State Manager in Python.
"""

import os
import uuid
import datetime
from typing import Dict, Any, List, Optional
from .email_service import execute_reporting_pipeline

initial_recipients = [
    r.strip() for r in os.getenv('SMTP_RECIPIENTS', 'itzanonymousag@gmail.com,acedavkhills@gmail.com').split(',') if r.strip()
]

# In-memory Schedules Store
schedule_jobs: List[Dict[str, Any]] = [
    {
        'id': 'sched-daily-exec',
        'name': 'Daily 09:00 AM Executive Briefing',
        'recipients': initial_recipients,
        'ccRecipients': ['analytics@sleepsia.com'],
        'reportTime': '09:00',
        'timezone': 'Asia/Kolkata',
        'frequency': 'Daily',
        'enabled': True,
        'subjectTemplate': 'Sleepsia Daily Executive Commerce Intelligence Report - {date}',
        'includeVisualAttachment': True,
        'includeAnomalyAlerts': True,
        'includeKpiSummary': True,
        'includeStockoutRisks': True,
        'createdDate': datetime.datetime.now().isoformat(),
        'lastRunTimestamp': None,
        'lastRunStatus': None,
        'nextRunEstimated': 'Tomorrow at 09:00 AM IST',
    },
    {
        'id': 'sched-weekly-digest',
        'name': 'Weekly Leadership Roundup (Monday 08:30 AM)',
        'recipients': initial_recipients,
        'ccRecipients': ['analytics@sleepsia.com'],
        'reportTime': '08:30',
        'timezone': 'Asia/Kolkata',
        'frequency': 'Weekly',
        'weeklyDay': 'Monday',
        'enabled': True,
        'subjectTemplate': 'Sleepsia Weekly Executive Digest & Channel Breakdown - {date}',
        'includeVisualAttachment': True,
        'includeAnomalyAlerts': True,
        'includeKpiSummary': True,
        'includeStockoutRisks': True,
        'createdDate': datetime.datetime.now().isoformat(),
        'lastRunTimestamp': None,
        'lastRunStatus': None,
        'nextRunEstimated': 'Next Monday at 08:30 AM IST',
    },
]

execution_history: List[Dict[str, Any]] = []

current_settings: Dict[str, Any] = {
    'recipients': initial_recipients,
    'ccRecipients': ['analytics@sleepsia.com'],
    'reportTime': '09:00',
    'timezone': 'Asia/Kolkata',
    'frequency': 'Daily',
    'autoSendEnabled': True,
    'lastSentTimestamp': None,
    'lastSentStatus': None,
    'lastSentMessage': None,
}

def get_email_settings() -> Dict[str, Any]:
    return {
        **current_settings,
        'schedules': list(schedule_jobs),
    }

def update_email_settings(new_settings: Dict[str, Any]) -> Dict[str, Any]:
    global current_settings, schedule_jobs
    current_settings.update(new_settings)
    if 'schedules' in new_settings and isinstance(new_settings['schedules'], list):
        schedule_jobs = list(new_settings['schedules'])
    return get_email_settings()

def get_schedules() -> List[Dict[str, Any]]:
    return list(schedule_jobs)

def get_execution_history() -> List[Dict[str, Any]]:
    return list(execution_history)

def create_schedule(job_data: Dict[str, Any]) -> Dict[str, Any]:
    job_id = f"sched-{uuid.uuid4().hex[:8]}"
    new_job = {
        'id': job_id,
        'name': job_data.get('name', 'Custom Executive Report'),
        'recipients': job_data.get('recipients', initial_recipients),
        'ccRecipients': job_data.get('ccRecipients', []),
        'reportTime': job_data.get('reportTime', '09:00'),
        'timezone': job_data.get('timezone', 'Asia/Kolkata'),
        'frequency': job_data.get('frequency', 'Daily'),
        'weeklyDay': job_data.get('weeklyDay', 'Monday'),
        'monthlyDay': job_data.get('monthlyDay', 1),
        'enabled': job_data.get('enabled', True),
        'subjectTemplate': job_data.get('subjectTemplate', 'Sleepsia Commerce Report - {date}'),
        'includeVisualAttachment': job_data.get('includeVisualAttachment', True),
        'includeAnomalyAlerts': job_data.get('includeAnomalyAlerts', True),
        'includeKpiSummary': job_data.get('includeKpiSummary', True),
        'includeStockoutRisks': job_data.get('includeStockoutRisks', True),
        'createdDate': datetime.datetime.now().isoformat(),
        'nextRunEstimated': 'Configured schedule',
    }
    schedule_jobs.append(new_job)
    return new_job

def update_schedule(job_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    for idx, job in enumerate(schedule_jobs):
        if job['id'] == job_id:
            schedule_jobs[idx] = {**job, **updates, 'id': job_id}
            return schedule_jobs[idx]
    return None

def delete_schedule(job_id: str) -> bool:
    global schedule_jobs
    initial_len = len(schedule_jobs)
    schedule_jobs = [j for j in schedule_jobs if j['id'] != job_id]
    return len(schedule_jobs) < initial_len

def toggle_schedule_enabled(job_id: str) -> Optional[Dict[str, Any]]:
    for idx, job in enumerate(schedule_jobs):
        if job['id'] == job_id:
            job['enabled'] = not job.get('enabled', True)
            schedule_jobs[idx] = job
            return job
    return None

def run_schedule_now(job_id: str, google_token: Optional[str] = None) -> Dict[str, Any]:
    job = next((j for j in schedule_jobs if j['id'] == job_id), None)
    if not job:
        raise ValueError(f"Schedule job {job_id} not found")

    date_str = datetime.date.today().isoformat()
    subject = (job.get('subjectTemplate') or 'Sleepsia Executive Report - {date} [Manual Trigger]').replace('{date}', date_str)

    result = execute_reporting_pipeline({
        'recipients': job.get('recipients', initial_recipients),
        'ccRecipients': job.get('ccRecipients', []),
        'subject': subject,
        'googleAccessToken': google_token,
    })

    job['lastRunTimestamp'] = result['timestamp']
    job['lastRunStatus'] = 'Success' if result.get('success') else 'Failed'

    history_entry = {
        'id': f"exec-{uuid.uuid4().hex[:8]}",
        'scheduleId': job_id,
        'scheduleName': job.get('name', 'Executive Report'),
        'timestamp': result['timestamp'],
        'recipients': result.get('recipients', []),
        'status': 'Success' if result.get('success') else 'Failed',
        'message': result.get('message', ''),
        'messageId': result.get('messageId'),
        'previewUrl': result.get('previewUrl'),
        'attachedFiles': result.get('attachedFiles', []),
    }
    execution_history.insert(0, history_entry)
    return result
