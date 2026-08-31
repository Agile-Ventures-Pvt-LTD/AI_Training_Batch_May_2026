"""
Email Service in Python - Executive Distribution, Gmail API & Google OAuth Integration.
"""

import os
import re
import smtplib
import base64
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, Any, List, Optional
import requests
import json
from dotenv import load_dotenv

# Load .env file to ensure all environment variables are available
load_dotenv()

from .dataset_service import get_active_dataset
from .multi_agent_supervisor import build_daily_executive_report, fmt_curr, fmt_num
from .report_image_generator import generate_dashboard_svg

# RFC 5322 regex
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$")

# Google access token storage
_stored_google_token: Optional[str] = None
_stored_google_email: str = 'itzanonymousag@gmail.com'
_stored_token_timestamp: Optional[float] = None

def set_stored_google_access_token(token: Optional[str], email: Optional[str] = None):
    global _stored_google_token, _stored_google_email, _stored_token_timestamp
    if token and token.strip():
        _stored_google_token = token.strip()
        _stored_token_timestamp = datetime.datetime.now().timestamp()
        if email and email.strip():
            _stored_google_email = email.strip().lower()
        print(f"[EmailService] Stored Google access token for {_stored_google_email}")
    else:
        _stored_google_token = None
        _stored_token_timestamp = None

def get_stored_google_access_token() -> Optional[str]:
    return _stored_google_token

def get_stored_google_user_email() -> str:
    return _stored_google_email

def is_stored_google_token_valid() -> bool:
    if not _stored_google_token:
        return False
    if not _stored_token_timestamp:
        return True
    # 50 min validity
    return (datetime.datetime.now().timestamp() - _stored_token_timestamp) < (50 * 60)

def validate_recipients(emails: List[str]) -> Dict[str, List[str]]:
    valid = []
    invalid = []
    for raw in emails:
        clean = raw.strip()
        if not clean:
            continue
        if EMAIL_REGEX.match(clean):
            valid.append(clean)
        else:
            invalid.append(clean)
    return {'valid': valid, 'invalid': invalid}

def send_via_gmail_api(gmail_access_token: str, from_email: str, to_emails: List[str],
                       cc_emails: List[str], subject: str, html_body: str, svg_content: str) -> Dict[str, Any]:
    """Send email via Gmail API using OAuth access token."""
    try:
        # Create MIME message
        msg = MIMEMultipart('related')
        msg['From'] = from_email
        msg['To'] = ', '.join(to_emails)
        if cc_emails:
            msg['Cc'] = ', '.join(cc_emails)
        msg['Subject'] = subject

        # Attach HTML body
        msg.attach(MIMEText(html_body, 'html'))

        # Attach SVG dashboard
        if svg_content:
            svg_attach = MIMEBase('image', 'svg+xml')
            svg_attach.set_payload(svg_content.encode('utf-8'))
            encoders.encode_base64(svg_attach)
            svg_attach.add_header('Content-Disposition', 'attachment; filename="sleepsia_daily_dashboard.svg"')
            msg.attach(svg_attach)

        # Encode message
        raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()

        # Send via Gmail API
        send_url = 'https://www.googleapis.com/gmail/v1/users/me/messages/send'
        headers = {
            'Authorization': f'Bearer {gmail_access_token}',
            'Content-Type': 'application/json',
        }

        payload = {'raw': raw_message}
        response = requests.post(send_url, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            return {
                'success': True,
                'messageId': result.get('id'),
                'timestamp': datetime.datetime.now().isoformat(),
                'method': 'Gmail API',
            }
        else:
            error_msg = response.text
            print(f"[EmailService] Gmail API error ({response.status_code}): {error_msg}")
            return {
                'success': False,
                'error': f"Gmail API error: {response.status_code}",
                'details': error_msg,
            }

    except Exception as e:
        print(f"[EmailService] Gmail API send error: {e}")
        return {
            'success': False,
            'error': str(e),
            'method': 'Gmail API',
        }

def compose_html_report(report: Dict[str, Any], is_test: bool = False) -> str:
    kpis = report.get('kpis', {})
    wins = report.get('topWins', [])
    risks = report.get('topRisks', [])
    actions = report.get('actionPlan', [])
    rankings = report.get('marketplaceRankings', [])

    wins_html = ''.join([f"<li style='margin-bottom: 6px;'>{w}</li>" for w in wins])
    risks_html = ''.join([f"<li style='margin-bottom: 6px; color: #ef4444;'>{r}</li>" for r in risks])

    actions_rows = ''.join([
        f"<tr>"
        f"<td style='padding: 8px; border-bottom: 1px solid #334155; font-weight: bold;'>{a.get('priority', 'P2')}</td>"
        f"<td style='padding: 8px; border-bottom: 1px solid #334155;'>{a.get('action', '')}</td>"
        f"<td style='padding: 8px; border-bottom: 1px solid #334155; color: #94a3b8;'>{a.get('expectedImpact', '')}</td>"
        f"</tr>"
        for a in actions[:4]
    ])

    mkt_rows = ''.join([
        f"<tr>"
        f"<td style='padding: 8px; border-bottom: 1px solid #334155;'>{m.get('platform', '')}</td>"
        f"<td style='padding: 8px; border-bottom: 1px solid #334155;'>{fmt_curr(m.get('netRevenue', 0))}</td>"
        f"<td style='padding: 8px; border-bottom: 1px solid #334155; color: #10b981;'>{fmt_curr(m.get('profit', 0))} ({m.get('profitMargin', 0)}%)</td>"
        f"</tr>"
        for m in rankings[:5]
    ])

    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Sleepsia Daily Executive Commerce Report</title>
</head>
<body style="background-color: #0b0f19; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; padding: 24px;">
  <div style="max-width: 800px; margin: 0 auto; background-color: #1e293b; border-radius: 12px; padding: 32px; border: 1px solid #334155;">
    
    <!-- Header -->
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 20px; margin-bottom: 24px;">
      <div>
        <h1 style="color: #38bdf8; margin: 0; font-size: 24px;">Sleepsia Commerce Intelligence</h1>
        <p style="color: #94a3b8; margin: 4px 0 0 0; font-size: 14px;">Daily Executive Automated Briefing</p>
      </div>
      <div style="text-align: right;">
        <span style="background-color: #0f172a; padding: 6px 12px; border-radius: 6px; font-size: 13px; color: #e2e8f0; border: 1px solid #334155;">
          Date: {report.get('reportDate', '')}
        </span>
      </div>
    </div>

    <!-- Executive Summary -->
    <div style="background-color: #0f172a; border-left: 4px solid #38bdf8; padding: 16px; border-radius: 6px; margin-bottom: 24px;">
      <h3 style="margin-top: 0; color: #38bdf8; font-size: 16px;">AI Supervisor Summary</h3>
      <p style="line-height: 1.6; color: #cbd5e1; margin: 0;">{report.get('executiveSummary', '')}</p>
    </div>

    <!-- KPI Grid -->
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;">
      <div style="background-color: #0f172a; padding: 16px; border-radius: 8px; border: 1px solid #334155;">
        <div style="color: #94a3b8; font-size: 12px; font-weight: bold;">NET REVENUE</div>
        <div style="font-size: 22px; font-weight: bold; color: #f8fafc; margin-top: 4px;">{fmt_curr(kpis.get('netRevenue', 0))}</div>
        <div style="font-size: 12px; color: #10b981;">{kpis.get('totalOrders', 0)} Orders | {kpis.get('unitsSold', 0)} Units</div>
      </div>
      <div style="background-color: #0f172a; padding: 16px; border-radius: 8px; border: 1px solid #334155;">
        <div style="color: #94a3b8; font-size: 12px; font-weight: bold;">NET PROFIT</div>
        <div style="font-size: 22px; font-weight: bold; color: #10b981; margin-top: 4px;">{fmt_curr(kpis.get('netProfit', 0))}</div>
        <div style="font-size: 12px; color: #e2e8f0;">Margin: {kpis.get('profitMarginPercent', 0)}%</div>
      </div>
    </div>

    <!-- Top Wins & Risks -->
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;">
      <div style="background-color: #0f172a; padding: 16px; border-radius: 8px; border: 1px solid #334155;">
        <h4 style="color: #10b981; margin-top: 0; font-size: 14px;">Key Wins</h4>
        <ul style="padding-left: 18px; margin: 0; font-size: 13px; line-height: 1.5; color: #cbd5e1;">
          {wins_html}
        </ul>
      </div>
      <div style="background-color: #0f172a; padding: 16px; border-radius: 8px; border: 1px solid #334155;">
        <h4 style="color: #ef4444; margin-top: 0; font-size: 14px;">Operational Risks</h4>
        <ul style="padding-left: 18px; margin: 0; font-size: 13px; line-height: 1.5;">
          {risks_html}
        </ul>
      </div>
    </div>

    <!-- Marketplace Rankings -->
    <div style="margin-bottom: 24px;">
      <h4 style="color: #f8fafc; margin-bottom: 8px; font-size: 15px;">Marketplace Leaderboard</h4>
      <table style="width: 100%; border-collapse: collapse; font-size: 13px; background-color: #0f172a; border-radius: 8px;">
        <thead>
          <tr style="border-bottom: 2px solid #334155; text-align: left; color: #94a3b8;">
            <th style="padding: 8px;">Channel</th>
            <th style="padding: 8px;">Revenue</th>
            <th style="padding: 8px;">Profit</th>
          </tr>
        </thead>
        <tbody>
          {mkt_rows}
        </tbody>
      </table>
    </div>

    <!-- Prioritized Actions -->
    <div style="margin-bottom: 24px;">
      <h4 style="color: #f8fafc; margin-bottom: 8px; font-size: 15px;">Prioritized Action Directives</h4>
      <table style="width: 100%; border-collapse: collapse; font-size: 13px; background-color: #0f172a; border-radius: 8px;">
        <thead>
          <tr style="border-bottom: 2px solid #334155; text-align: left; color: #94a3b8;">
            <th style="padding: 8px;">Priority</th>
            <th style="padding: 8px;">Action Directive</th>
            <th style="padding: 8px;">Expected Impact</th>
          </tr>
        </thead>
        <tbody>
          {actions_rows}
        </tbody>
      </table>
    </div>

    <!-- Footer -->
    <div style="border-top: 1px solid #334155; padding-top: 16px; text-align: center; color: #64748b; font-size: 12px;">
      Confidential • Prepared for Sleepsia Executive Leadership • Sent via Sleepsia Django Intelligence Engine
    </div>
  </div>
</body>
</html>
"""

def execute_reporting_pipeline(options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if options is None:
        options = {}

    dataset = options.get('data') or get_active_dataset()
    date_val = options.get('date') or dataset.get('metadata', {}).get('dateRange', {}).get('end', '2026-08-07')
    recipients = options.get('recipients') or [
        os.getenv('SMTP_RECIPIENTS', 'itzanonymousag@gmail.com,acedavkhills@gmail.com').split(',')[0].strip()
    ]
    cc_recipients = options.get('ccRecipients') or ['analytics@sleepsia.com']
    is_test = options.get('isTestEmail', False)
    custom_subj = options.get('subject')
    gmail_token = options.get('googleAccessToken')

    report = build_daily_executive_report(dataset, date_val)
    svg_content = generate_dashboard_svg(report)

    subject = custom_subj or (
        f"{'[TEST DIAGNOSTIC] ' if is_test else ''}Sleepsia Daily Executive Commerce Intelligence Report - {date_val}"
    )

    val_res = validate_recipients(recipients)
    valid_recipients = val_res['valid'] or ['itzanonymousag@gmail.com']

    # Filter CC recipients
    cc_res = validate_recipients(cc_recipients or [])
    valid_cc = cc_res['valid']

    # Generate timestamp and message id
    msg_id = f"<sleepsia-report-{date_val}-{int(datetime.datetime.now().timestamp())}@sleepsia.com>"
    timestamp = datetime.datetime.now().isoformat()

    html_body = compose_html_report(report, is_test)

    send_success = False
    warning_list = []
    send_method = 'None'

    # Try Gmail API first if token is provided
    if gmail_token and is_stored_google_token_valid():
        print(f"[EmailService] Attempting Gmail API send with token for {get_stored_google_user_email()}")
        gmail_result = send_via_gmail_api(
            gmail_token,
            get_stored_google_user_email(),
            valid_recipients,
            valid_cc,
            subject,
            html_body,
            svg_content
        )
        if gmail_result.get('success'):
            send_success = True
            send_method = 'Gmail API'
            msg_id = gmail_result.get('messageId', msg_id)
            print(f"[EmailService] Gmail API send successful: {msg_id}")
        else:
            warning_list.append(f"Gmail API failed: {gmail_result.get('error', 'Unknown error')}")
            print(f"[EmailService] Gmail API send failed, falling back to SMTP")

    # Fallback to SMTP if Gmail API failed or no token
    if not send_success:
        smtp_host = os.getenv('SMTP_HOST')
        smtp_user = os.getenv('SMTP_USER')
        smtp_pass = os.getenv('SMTP_PASSWORD')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))

        if smtp_host and smtp_user and smtp_pass:
            try:
                msg = MIMEMultipart('related')
                msg['From'] = smtp_user
                msg['To'] = ', '.join(valid_recipients)
                if valid_cc:
                    msg['Cc'] = ', '.join(valid_cc)
                msg['Subject'] = subject
                msg['Message-ID'] = msg_id

                msg.attach(MIMEText(html_body, 'html'))

                # Attach SVG
                svg_attach = MIMEBase('image', 'svg+xml')
                svg_attach.set_payload(svg_content.encode('utf-8'))
                encoders.encode_base64(svg_attach)
                svg_attach.add_header('Content-Disposition', f'attachment; filename="sleepsia_daily_dashboard_{date_val}.svg"')
                msg.attach(svg_attach)

                with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_pass)
                    all_targets = valid_recipients + valid_cc
                    server.sendmail(smtp_user, all_targets, msg.as_string())
                    send_success = True
                    send_method = 'SMTP'
                    print(f"[EmailService] Successfully dispatched report email via SMTP to {all_targets}")
            except Exception as e:
                print(f"[EmailService] SMTP send error: {e}")
                warning_list.append(f"SMTP dispatch warning: {str(e)}")
        else:
            warning_list.append("No Gmail token and SMTP not configured")

    preview_url = f"/api/report/dashboard-image?date={date_val}"

    return {
        'success': send_success,
        'message': f"Executive report {'successfully sent' if send_success else 'rendered'} to {len(valid_recipients)} recipients via {send_method}.",
        'messageId': msg_id,
        'previewUrl': preview_url,
        'timestamp': timestamp,
        'recipients': valid_recipients,
        'ccRecipients': valid_cc,
        'subject': subject,
        'attachedFiles': [f"sleepsia_daily_dashboard_{date_val}.svg"],
        'imageAttachmentGenerated': True,
        'sendMethod': send_method,
        'warnings': warning_list if warning_list else None,
    }
