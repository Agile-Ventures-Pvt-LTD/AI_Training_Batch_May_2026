import React, { useState, useEffect } from 'react';
import {
  Mail,
  Send,
  X,
  CheckCircle2,
  AlertTriangle,
  Loader2,
  Paperclip,
  ExternalLink,
  FlaskConical,
  RefreshCw,
  Clock,
  Calendar,
  Plus,
  Edit2,
  Trash2,
  Play,
  Check,
  Globe,
  Bell,
  Sliders,
  History,
  ShieldCheck,
} from 'lucide-react';
import { EmailSettings, EmailScheduleJob, ExecutiveReportData } from '../types/commerce';

interface EmailModalProps {
  isOpen: boolean;
  onClose: () => void;
  report: ExecutiveReportData;
  settings: EmailSettings;
  selectedDate: string;
}

export const EmailModal: React.FC<EmailModalProps> = ({
  isOpen,
  onClose,
  report,
  settings,
  selectedDate,
}) => {
  const [activeTab, setActiveTab] = useState<'instant' | 'scheduler'>('instant');

  // Instant Send States
  const [recipientInput, setRecipientInput] = useState(
    settings.recipients.join(', ') || 'acedavkhills@gmail.com, pranay.agileventures@gmail.com'
  );
  const [ccInput, setCcInput] = useState(
    settings.ccRecipients.join(', ') || 'analytics@sleepsia.com'
  );
  const [subject, setSubject] = useState(
    `Sleepsia Daily Commerce Intelligence Report - ${selectedDate}`
  );
  const [isSending, setIsSending] = useState(false);
  const [isSendingTest, setIsSendingTest] = useState(false);
  const [deliveryResult, setDeliveryResult] = useState<{
    message: string;
    messageId?: string;
    previewUrl?: string;
    attachedFiles?: string[];
    to?: string[];
  } | null>(null);
  const [sendError, setSendError] = useState<string | null>(null);

  // Schedules State
  const [schedules, setSchedules] = useState<EmailScheduleJob[]>(
    settings.schedules && settings.schedules.length > 0
      ? settings.schedules
      : [
          {
            id: 'sched-daily-exec',
            name: 'Daily 09:00 AM Executive Briefing',
            recipients: settings.recipients || ['pranay.agileventures@gmail.com', 'acedavkhills@gmail.com'],
            ccRecipients: settings.ccRecipients || ['analytics@sleepsia.com'],
            reportTime: '09:00',
            timezone: 'Asia/Kolkata',
            frequency: 'Daily',
            enabled: true,
            subjectTemplate: 'Sleepsia Daily Executive Commerce Intelligence Report - {date}',
            includeVisualAttachment: true,
            includeAnomalyAlerts: true,
            includeKpiSummary: true,
            includeStockoutRisks: true,
            createdDate: new Date().toISOString(),
            lastRunTimestamp: undefined,
            lastRunStatus: undefined,
            nextRunEstimated: 'Tomorrow at 09:00 AM IST',
          },
          {
            id: 'sched-weekly-digest',
            name: 'Weekly Leadership Roundup (Monday 08:30 AM)',
            recipients: settings.recipients || ['pranay.agileventures@gmail.com'],
            ccRecipients: ['analytics@sleepsia.com'],
            reportTime: '08:30',
            timezone: 'Asia/Kolkata',
            frequency: 'Weekly',
            weeklyDay: 'Monday',
            enabled: true,
            subjectTemplate: 'Sleepsia Weekly Executive Digest & Channel Breakdown - {date}',
            includeVisualAttachment: true,
            includeAnomalyAlerts: true,
            includeKpiSummary: true,
            includeStockoutRisks: true,
            createdDate: new Date().toISOString(),
            lastRunTimestamp: undefined,
            lastRunStatus: undefined,
            nextRunEstimated: 'Next Monday at 08:30 AM IST',
          },
        ]
  );

  const [editingJob, setEditingJob] = useState<EmailScheduleJob | null>(null);
  const [isCreatingNew, setIsCreatingNew] = useState(false);
  const [runningJobId, setRunningJobId] = useState<string | null>(null);
  const [scheduleFeedback, setScheduleFeedback] = useState<{
    type: 'success' | 'error';
    message: string;
    previewUrl?: string;
  } | null>(null);

  // Form states for creating/editing a schedule
  const [formName, setFormName] = useState('');
  const [formRecipients, setFormRecipients] = useState('');
  const [formCc, setFormCc] = useState('');
  const [formTime, setFormTime] = useState('09:00');
  const [formTimezone, setFormTimezone] = useState('Asia/Kolkata');
  const [formFrequency, setFormFrequency] = useState<'Daily' | 'Weekdays' | 'Weekly' | 'Hourly'>('Daily');
  const [formWeeklyDay, setFormWeeklyDay] = useState<'Monday' | 'Tuesday' | 'Wednesday' | 'Thursday' | 'Friday' | 'Saturday' | 'Sunday'>('Monday');
  const [formSubject, setFormSubject] = useState('Sleepsia Daily Executive Commerce Intelligence Report - {date}');
  const [formAttachVisual, setFormAttachVisual] = useState(true);
  const [formIncludeAlerts, setFormIncludeAlerts] = useState(true);
  const [formIncludeStockout, setFormIncludeStockout] = useState(true);
  const [formIncludeKpi, setFormIncludeKpi] = useState(true);
  const [formEnabled, setFormEnabled] = useState(true);

  useEffect(() => {
    // Fetch live schedules from backend if available
    fetch('/api/schedules')
      .then((res) => res.json())
      .then((data) => {
        if (data.success && data.schedules && data.schedules.length > 0) {
          setSchedules(data.schedules);
        }
      })
      .catch(() => {
        // Fallback to local default state
      });
  }, []);

  if (!isOpen) return null;

  const parseRecipients = () => {
    const to = recipientInput
      .split(/[,;\n]+/)
      .map((s) => s.replace(/[<>\s"']/g, '').trim())
      .filter((s) => s.length > 0 && s.includes('@'));
    const cc = ccInput
      .split(/[,;\n]+/)
      .map((s) => s.replace(/[<>\s"']/g, '').trim())
      .filter((s) => s.length > 0 && s.includes('@'));
    return { to, cc };
  };

  const handleSend = async (isTest: boolean = false) => {
    setDeliveryResult(null);
    setSendError(null);

    const { to, cc } = parseRecipients();

    if (to.length === 0) {
      setSendError('Please provide at least one recipient email address.');
      return;
    }

    if (isTest) setIsSendingTest(true);
    else setIsSending(true);

    const endpoint = isTest ? '/api/email/send-test' : '/api/email/send-report';

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          date: selectedDate,
          recipients: to,
          ccRecipients: cc,
          customSubject: subject,
        }),
      });

      const json = await res.json();
      if (json.success) {
        setDeliveryResult({
          message: json.message,
          messageId: json.messageId,
          previewUrl: json.previewUrl,
          attachedFiles: json.details?.attachedFiles,
          to: json.details?.to,
        });
      } else {
        setSendError(json.error || 'Failed to dispatch report email.');
      }
    } catch (err: any) {
      setSendError(err?.message || 'Network error communicating with email server.');
    } finally {
      setIsSending(false);
      setIsSendingTest(false);
    }
  };

  // Schedule management handlers
  const handleOpenEditSchedule = (job: EmailScheduleJob) => {
    setEditingJob(job);
    setIsCreatingNew(false);
    setFormName(job.name);
    setFormRecipients(job.recipients.join(', '));
    setFormCc(job.ccRecipients.join(', '));
    setFormTime(job.reportTime);
    setFormTimezone(job.timezone);
    setFormFrequency(job.frequency);
    setFormWeeklyDay(job.weeklyDay || 'Monday');
    setFormSubject(job.subjectTemplate || 'Sleepsia Daily Executive Commerce Intelligence Report - {date}');
    setFormAttachVisual(job.includeVisualAttachment ?? true);
    setFormIncludeAlerts(job.includeAnomalyAlerts ?? true);
    setFormIncludeStockout(job.includeStockoutRisks ?? true);
    setFormIncludeKpi(job.includeKpiSummary ?? true);
    setFormEnabled(job.enabled);
    setScheduleFeedback(null);
  };

  const handleOpenCreateSchedule = () => {
    setEditingJob(null);
    setIsCreatingNew(true);
    setFormName('Daily 09:00 AM Executive Briefing');
    setFormRecipients(recipientInput || 'pranay.agileventures@gmail.com, acedavkhills@gmail.com');
    setFormCc(ccInput || 'analytics@sleepsia.com');
    setFormTime('09:00');
    setFormTimezone('Asia/Kolkata');
    setFormFrequency('Daily');
    setFormWeeklyDay('Monday');
    setFormSubject('Sleepsia Daily Executive Commerce Intelligence Report - {date}');
    setFormAttachVisual(true);
    setFormIncludeAlerts(true);
    setFormIncludeStockout(true);
    setFormIncludeKpi(true);
    setFormEnabled(true);
    setScheduleFeedback(null);
  };

  const handleSaveScheduleForm = async () => {
    const to = formRecipients
      .split(/[,;\n]+/)
      .map((s) => s.replace(/[<>\s"']/g, '').trim())
      .filter((s) => s.length > 0 && s.includes('@'));

    const cc = formCc
      .split(/[,;\n]+/)
      .map((s) => s.replace(/[<>\s"']/g, '').trim())
      .filter((s) => s.length > 0 && s.includes('@'));

    if (to.length === 0) {
      setScheduleFeedback({
        type: 'error',
        message: 'Please provide at least one valid recipient email address.',
      });
      return;
    }

    const payload = {
      name: formName.trim() || 'Executive Commerce Report Schedule',
      recipients: to,
      ccRecipients: cc,
      reportTime: formTime,
      timezone: formTimezone,
      frequency: formFrequency,
      weeklyDay: formFrequency === 'Weekly' ? formWeeklyDay : undefined,
      subjectTemplate: formSubject,
      includeVisualAttachment: formAttachVisual,
      includeAnomalyAlerts: formIncludeAlerts,
      includeKpiSummary: formIncludeKpi,
      includeStockoutRisks: formIncludeStockout,
      enabled: formEnabled,
      nextRunEstimated: `${formFrequency === 'Weekly' ? formWeeklyDay + 's' : formFrequency} at ${formTime} (${formTimezone.split('/')[1] || formTimezone})`,
    };

    try {
      if (editingJob) {
        // Update existing
        const res = await fetch(`/api/schedules/${editingJob.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (data.success && data.schedules) {
          setSchedules(data.schedules);
        } else {
          setSchedules((prev) =>
            prev.map((j) => (j.id === editingJob.id ? { ...j, ...payload } : j))
          );
        }
      } else {
        // Create new
        const res = await fetch('/api/schedules', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (data.success && data.schedules) {
          setSchedules(data.schedules);
        } else {
          const newJob: EmailScheduleJob = {
            id: `sched-${Date.now()}`,
            createdDate: new Date().toISOString(),
            ...payload,
          };
          setSchedules((prev) => [...prev, newJob]);
        }
      }

      setEditingJob(null);
      setIsCreatingNew(false);
      setScheduleFeedback({
        type: 'success',
        message: `Schedule "${payload.name}" saved successfully! Automated delivery is configured for ${payload.reportTime} ${payload.timezone}.`,
      });
    } catch (err: any) {
      setScheduleFeedback({
        type: 'error',
        message: err?.message || 'Failed to persist schedule to server.',
      });
    }
  };

  const handleToggleSchedule = async (jobId: string) => {
    try {
      const res = await fetch(`/api/schedules/${jobId}/toggle`, { method: 'POST' });
      const data = await res.json();
      if (data.success && data.schedules) {
        setSchedules(data.schedules);
      } else {
        setSchedules((prev) =>
          prev.map((j) => (j.id === jobId ? { ...j, enabled: !j.enabled } : j))
        );
      }
    } catch {
      setSchedules((prev) =>
        prev.map((j) => (j.id === jobId ? { ...j, enabled: !j.enabled } : j))
      );
    }
  };

  const handleDeleteSchedule = async (jobId: string) => {
    if (!confirm('Are you sure you want to remove this scheduled distribution job?')) return;
    try {
      const res = await fetch(`/api/schedules/${jobId}`, { method: 'DELETE' });
      const data = await res.json();
      if (data.success && data.schedules) {
        setSchedules(data.schedules);
      } else {
        setSchedules((prev) => prev.filter((j) => j.id !== jobId));
      }
    } catch {
      setSchedules((prev) => prev.filter((j) => j.id !== jobId));
    }
  };

  const handleRunScheduleNow = async (job: EmailScheduleJob) => {
    setRunningJobId(job.id);
    setScheduleFeedback(null);

    try {
      const res = await fetch(`/api/schedules/${job.id}/run-now`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      const data = await res.json();
      if (data.success) {
        setScheduleFeedback({
          type: 'success',
          message: `Successfully executed "${job.name}"! Dispatched email via verified Gmail account to ${job.recipients.join(', ')}.`,
          previewUrl: data.previewUrl,
        });
        // refresh list
        fetch('/api/schedules')
          .then((r) => r.json())
          .then((d) => d.schedules && setSchedules(d.schedules));
      } else {
        setScheduleFeedback({
          type: 'error',
          message: data.error || 'Failed to trigger schedule execution.',
        });
      }
    } catch (err: any) {
      setScheduleFeedback({
        type: 'error',
        message: err?.message || 'Network error triggering schedule execution.',
      });
    } finally {
      setRunningJobId(null);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-3 sm:p-4 overflow-y-auto">
      <div className="bg-white border border-slate-200 rounded-2xl p-5 sm:p-6 max-w-2xl w-full shadow-2xl space-y-5 my-auto max-h-[92vh] flex flex-col">
        {/* Modal Header */}
        <div className="flex items-center justify-between pb-3 border-b border-slate-100 shrink-0">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-blue-50 text-blue-600 border border-blue-100 shadow-xs">
              <Mail className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-900">Executive Report Delivery Center</h3>
              <p className="text-xs text-slate-500">Live Gmail Dispatch &amp; Automated Email Schedulers</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 p-1.5 rounded-lg hover:bg-slate-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Navigation */}
        <div className="flex items-center gap-2 border-b border-slate-100 pb-3 shrink-0">
          <button
            onClick={() => {
              setActiveTab('instant');
              setEditingJob(null);
              setIsCreatingNew(false);
            }}
            className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
              activeTab === 'instant'
                ? 'bg-blue-600 text-white shadow-xs'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
            }`}
          >
            <Send className="w-3.5 h-3.5" />
            <span>Send Now (Live Dispatch)</span>
          </button>

          <button
            onClick={() => {
              setActiveTab('scheduler');
              setEditingJob(null);
              setIsCreatingNew(false);
            }}
            className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
              activeTab === 'scheduler'
                ? 'bg-purple-600 text-white shadow-xs'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
            }`}
          >
            <Clock className="w-3.5 h-3.5" />
            <span>Automated Schedulers ({schedules.filter((s) => s.enabled).length} Active)</span>
          </button>
        </div>

        {/* Modal Body */}
        <div className="flex-1 overflow-y-auto pr-1 space-y-4">
          {/* TAB 1: INSTANT SEND */}
          {activeTab === 'instant' && (
            <div className="space-y-4">
              {/* Delivery confirmation */}
              {deliveryResult ? (
                <div className="space-y-4">
                  <div className="bg-emerald-50 border border-emerald-200 text-emerald-800 p-5 rounded-xl text-center space-y-2.5">
                    <CheckCircle2 className="w-9 h-9 mx-auto text-emerald-600" />
                    <div>
                      <h4 className="font-bold text-sm text-slate-900">Email Dispatched Successfully</h4>
                      <p className="text-xs text-slate-600 mt-1">{deliveryResult.message}</p>
                    </div>

                    {deliveryResult.messageId && (
                      <div className="bg-white/80 border border-emerald-200/80 rounded-lg p-2 text-[11px] font-mono text-slate-600 text-left space-y-0.5 mt-2">
                        <div className="text-slate-500 font-sans font-semibold text-[10px] uppercase">
                          Delivery Verification:
                        </div>
                        <div>• Message ID: <span className="text-slate-900 font-semibold">{deliveryResult.messageId}</span></div>
                        {deliveryResult.to && (
                          <div>• Verified To: <span className="text-slate-900 font-semibold">{deliveryResult.to.join(', ')}</span></div>
                        )}
                        {deliveryResult.attachedFiles && deliveryResult.attachedFiles.length > 0 && (
                          <div>• Attachment: <span className="text-emerald-700 font-semibold">{deliveryResult.attachedFiles.join(', ')}</span></div>
                        )}
                      </div>
                    )}

                    {deliveryResult.previewUrl && (
                      <a
                        href={deliveryResult.previewUrl}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1.5 text-xs font-bold text-blue-600 hover:text-blue-800 bg-blue-50 px-3 py-1.5 rounded-lg border border-blue-200 transition-colors mt-2"
                      >
                        <ExternalLink className="w-3.5 h-3.5" />
                        <span>View Verified Sandbox Inbox Dispatch</span>
                      </a>
                    )}
                  </div>

                  <div className="flex justify-end gap-2 pt-1">
                    <button
                      onClick={() => setDeliveryResult(null)}
                      className="px-4 py-2 text-xs font-semibold text-slate-600 hover:text-slate-900 border border-slate-200 rounded-lg"
                    >
                      Send Another
                    </button>
                    <button
                      onClick={onClose}
                      className="bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-4 py-2 rounded-lg transition-colors shadow-xs"
                    >
                      Done
                    </button>
                  </div>
                </div>
              ) : (
                <div className="space-y-4 text-xs">
                  {/* Recipients */}
                  <div>
                    <label className="font-semibold text-slate-700 block mb-1">To (Recipients):</label>
                    <input
                      type="text"
                      value={recipientInput}
                      onChange={(e) => setRecipientInput(e.target.value)}
                      placeholder="pranay.agileventures@gmail.com, acedavkhills@gmail.com"
                      className="w-full bg-white border border-slate-200 text-slate-900 rounded-lg p-2.5 outline-none focus:ring-1 focus:ring-blue-500 font-mono text-[11px] shadow-xs"
                    />
                  </div>

                  {/* CC */}
                  <div>
                    <label className="font-semibold text-slate-700 block mb-1">CC:</label>
                    <input
                      type="text"
                      value={ccInput}
                      onChange={(e) => setCcInput(e.target.value)}
                      placeholder="analytics@sleepsia.com"
                      className="w-full bg-white border border-slate-200 text-slate-900 rounded-lg p-2.5 outline-none focus:ring-1 focus:ring-blue-500 font-mono text-[11px] shadow-xs"
                    />
                  </div>

                  {/* Subject */}
                  <div>
                    <label className="font-semibold text-slate-700 block mb-1">Subject:</label>
                    <input
                      type="text"
                      value={subject}
                      onChange={(e) => setSubject(e.target.value)}
                      className="w-full bg-white border border-slate-200 text-slate-900 rounded-lg p-2.5 outline-none focus:ring-1 focus:ring-blue-500 font-semibold shadow-xs"
                    />
                  </div>

                  {/* Attachments & Content Summary */}
                  <div className="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-1.5">
                    <div className="flex items-center gap-1.5 font-bold text-slate-800 text-[11px]">
                      <Paperclip className="w-3.5 h-3.5 text-blue-600" />
                      <span>Automated Email Content &amp; Visual Attachment:</span>
                    </div>
                    <div className="text-[11px] text-slate-600 space-y-1 pl-5 font-mono">
                      <div className="text-emerald-700 flex items-center gap-1">
                        • <code>sleepsia_daily_dashboard_{selectedDate}.png</code> (Rendered 1200x900 Visual)
                      </div>
                      <div className="text-slate-700 flex items-center gap-1">
                        • Responsive HTML Briefing with Real KPIs, Wins, Risks &amp; Actions
                      </div>
                    </div>
                  </div>

                  {sendError && (
                    <div className="bg-rose-50 border border-rose-200 text-rose-700 p-3.5 rounded-xl text-xs space-y-2">
                      <div className="flex items-start gap-2">
                        <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
                        <span className="flex-1">{sendError}</span>
                      </div>
                    </div>
                  )}

                  <div className="flex items-center justify-between pt-2 border-t border-slate-100">
                    <button
                      onClick={() => handleSend(true)}
                      disabled={isSending || isSendingTest}
                      className="px-3.5 py-2 rounded-lg text-slate-700 hover:text-slate-900 border border-slate-200 hover:bg-slate-50 transition-colors flex items-center gap-1.5 text-xs font-semibold disabled:opacity-50"
                    >
                      {isSendingTest ? (
                        <>
                          <Loader2 className="w-3.5 h-3.5 animate-spin text-blue-600" />
                          <span>Testing...</span>
                        </>
                      ) : (
                        <>
                          <FlaskConical className="w-3.5 h-3.5 text-slate-500" />
                          <span>Send Sandbox Test</span>
                        </>
                      )}
                    </button>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={onClose}
                        className="px-3.5 py-2 rounded-lg text-slate-600 hover:text-slate-900 border border-slate-200 text-xs font-semibold"
                      >
                        Cancel
                      </button>
                      <button
                        onClick={() => handleSend(false)}
                        disabled={isSending || isSendingTest}
                        className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-4 py-2 rounded-lg transition-colors flex items-center gap-2 disabled:opacity-50 shadow-xs text-xs"
                      >
                        {isSending ? (
                          <>
                            <Loader2 className="w-3.5 h-3.5 animate-spin" />
                            <span>Dispatching Email...</span>
                          </>
                        ) : (
                          <>
                            <Send className="w-3.5 h-3.5" />
                            <span>Send Report Live</span>
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* TAB 2: AUTOMATED EMAIL SCHEDULER */}
          {activeTab === 'scheduler' && (
            <div className="space-y-4">
              {/* Sender Account Info */}
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 flex items-center gap-2.5 text-xs">
                <div className="w-7 h-7 rounded-lg bg-emerald-50 text-emerald-600 border border-emerald-200 flex items-center justify-center shrink-0">
                  <ShieldCheck className="w-4 h-4" />
                </div>
                <div>
                  <div className="font-bold text-slate-900 flex items-center gap-1.5">
                    <span>Sender Account:</span>
                    <span className="font-mono text-[11px] text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                      Configured SMTP Account
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-500">
                    All scheduled automation jobs dispatch via the server's configured SMTP account.
                  </p>
                </div>
              </div>

              {/* Top Banner & Quick Add */}
              <div className="flex items-center justify-between bg-purple-50 border border-purple-200 rounded-xl p-3.5">
                <div>
                  <h4 className="text-xs font-bold text-purple-900 flex items-center gap-1.5">
                    <Clock className="w-4 h-4 text-purple-600" />
                    <span>Automated Email Distribution Schedulers</span>
                  </h4>
                  <p className="text-[11px] text-purple-700 mt-0.5">
                    Configured schedules run automatically in the background on your chosen timezone and send reports to your stakeholders.
                  </p>
                </div>
                {!editingJob && !isCreatingNew && (
                  <button
                    onClick={handleOpenCreateSchedule}
                    className="bg-purple-600 hover:bg-purple-700 text-white px-3 py-1.5 rounded-lg text-xs font-bold transition-all shadow-xs flex items-center gap-1.5 shrink-0"
                  >
                    <Plus className="w-3.5 h-3.5" />
                    <span>New Schedule</span>
                  </button>
                )}
              </div>

              {scheduleFeedback && (
                <div
                  className={`p-3 rounded-xl text-xs flex items-start gap-2 border ${
                    scheduleFeedback.type === 'success'
                      ? 'bg-emerald-50 border-emerald-200 text-emerald-800'
                      : 'bg-rose-50 border-rose-200 text-rose-800'
                  }`}
                >
                  {scheduleFeedback.type === 'success' ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  ) : (
                    <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
                  )}
                  <div className="flex-1">
                    <p>{scheduleFeedback.message}</p>
                    {scheduleFeedback.previewUrl && (
                      <a
                        href={scheduleFeedback.previewUrl}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1 text-[11px] font-bold text-blue-600 hover:text-blue-800 mt-1"
                      >
                        <ExternalLink className="w-3 h-3" />
                        <span>View Verified Email Dispatch</span>
                      </a>
                    )}
                  </div>
                </div>
              )}

              {/* SCHEDULE CREATION / EDITING FORM */}
              {(editingJob || isCreatingNew) ? (
                <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-4 text-xs">
                  <div className="flex items-center justify-between pb-2 border-b border-slate-200">
                    <h4 className="font-bold text-slate-900 flex items-center gap-1.5">
                      <Sliders className="w-4 h-4 text-purple-600" />
                      <span>{editingJob ? `Edit Schedule: ${editingJob.name}` : 'Create New Automated Schedule'}</span>
                    </h4>
                    <button
                      onClick={() => {
                        setEditingJob(null);
                        setIsCreatingNew(false);
                      }}
                      className="text-slate-400 hover:text-slate-600"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>

                  {/* Schedule Name */}
                  <div>
                    <label className="font-semibold text-slate-700 block mb-1">Schedule Name / Job Title:</label>
                    <input
                      type="text"
                      value={formName}
                      onChange={(e) => setFormName(e.target.value)}
                      placeholder="e.g. Daily 09:00 AM Executive Briefing"
                      className="w-full bg-white border border-slate-200 text-slate-900 rounded-lg p-2 text-xs focus:ring-1 focus:ring-purple-500 outline-none font-semibold shadow-xs"
                    />
                  </div>

                  {/* Frequency & Time Grid */}
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <div>
                      <label className="font-semibold text-slate-700 block mb-1">Frequency:</label>
                      <select
                        value={formFrequency}
                        onChange={(e) => setFormFrequency(e.target.value as any)}
                        className="w-full bg-white border border-slate-200 text-slate-900 rounded-lg p-2 text-xs focus:ring-1 focus:ring-purple-500 outline-none"
                      >
                        <option value="Daily">Daily (7 Days/Week)</option>
                        <option value="Weekdays">Weekdays (Mon - Fri)</option>
                        <option value="Weekly">Weekly (Specific Day)</option>
                        <option value="Hourly">Hourly</option>
                      </select>
                    </div>

                    {formFrequency === 'Weekly' && (
                      <div>
                        <label className="font-semibold text-slate-700 block mb-1">Day of Week:</label>
                        <select
                          value={formWeeklyDay}
                          onChange={(e) => setFormWeeklyDay(e.target.value as any)}
                          className="w-full bg-white border border-slate-200 text-slate-900 rounded-lg p-2 text-xs focus:ring-1 focus:ring-purple-500 outline-none"
                        >
                          <option value="Monday">Monday</option>
                          <option value="Tuesday">Tuesday</option>
                          <option value="Wednesday">Wednesday</option>
                          <option value="Thursday">Thursday</option>
                          <option value="Friday">Friday</option>
                          <option value="Saturday">Saturday</option>
                          <option value="Sunday">Sunday</option>
                        </select>
                      </div>
                    )}

                    <div>
                      <label className="font-semibold text-slate-700 block mb-1">Execution Time:</label>
                      <input
                        type="time"
                        value={formTime}
                        onChange={(e) => setFormTime(e.target.value)}
                        className="w-full bg-white border border-slate-200 text-slate-900 rounded-lg p-2 text-xs focus:ring-1 focus:ring-purple-500 outline-none font-mono"
                      />
                    </div>

                    <div>
                      <label className="font-semibold text-slate-700 block mb-1">Timezone:</label>
                      <select
                        value={formTimezone}
                        onChange={(e) => setFormTimezone(e.target.value)}
                        className="w-full bg-white border border-slate-200 text-slate-900 rounded-lg p-2 text-xs focus:ring-1 focus:ring-purple-500 outline-none"
                      >
                        <option value="Asia/Kolkata">Asia/Kolkata (IST)</option>
                        <option value="UTC">UTC (Universal Time)</option>
                        <option value="America/New_York">America/New_York (EST)</option>
                        <option value="America/Los_Angeles">America/Los_Angeles (PST)</option>
                        <option value="Europe/London">Europe/London (GMT)</option>
                        <option value="Asia/Dubai">Asia/Dubai (GST)</option>
                      </select>
                    </div>
                  </div>

                  {/* Preset Time Buttons */}
                  <div className="flex items-center gap-1.5 flex-wrap">
                    <span className="text-[11px] text-slate-500 font-medium mr-1">Presets:</span>
                    {['08:00', '08:30', '09:00', '12:00', '18:00', '21:00'].map((timePreset) => (
                      <button
                        key={timePreset}
                        type="button"
                        onClick={() => setFormTime(timePreset)}
                        className={`text-[11px] px-2 py-0.5 rounded-md border font-mono transition-all ${
                          formTime === timePreset
                            ? 'bg-purple-600 text-white border-purple-600 font-bold'
                            : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-100'
                        }`}
                      >
                        {timePreset}
                      </button>
                    ))}
                  </div>

                  {/* Recipients */}
                  <div>
                    <label className="font-semibold text-slate-700 block mb-1">To (Recipients - Comma Separated):</label>
                    <input
                      type="text"
                      value={formRecipients}
                      onChange={(e) => setFormRecipients(e.target.value)}
                      placeholder="pranay.agileventures@gmail.com, acedavkhills@gmail.com"
                      className="w-full bg-white border border-slate-200 text-slate-900 rounded-lg p-2 text-xs focus:ring-1 focus:ring-purple-500 outline-none font-mono"
                    />
                  </div>

                  <div>
                    <label className="font-semibold text-slate-700 block mb-1">CC Recipients:</label>
                    <input
                      type="text"
                      value={formCc}
                      onChange={(e) => setFormCc(e.target.value)}
                      placeholder="analytics@sleepsia.com"
                      className="w-full bg-white border border-slate-200 text-slate-900 rounded-lg p-2 text-xs focus:ring-1 focus:ring-purple-500 outline-none font-mono"
                    />
                  </div>

                  {/* Subject Template */}
                  <div>
                    <label className="font-semibold text-slate-700 block mb-1">Subject Line Template:</label>
                    <input
                      type="text"
                      value={formSubject}
                      onChange={(e) => setFormSubject(e.target.value)}
                      className="w-full bg-white border border-slate-200 text-slate-900 rounded-lg p-2 text-xs focus:ring-1 focus:ring-purple-500 outline-none font-mono"
                    />
                    <p className="text-[10px] text-slate-500 mt-0.5">Tip: <code>{'{date}'}</code> automatically dynamically resolves to the execution date.</p>
                  </div>

                  {/* Report Options Checklist */}
                  <div className="bg-white border border-slate-200 rounded-lg p-3 space-y-2">
                    <span className="font-semibold text-slate-700 block text-[11px]">Included Email Sections:</span>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px]">
                      <label className="flex items-center gap-2 cursor-pointer text-slate-700">
                        <input
                          type="checkbox"
                          checked={formAttachVisual}
                          onChange={(e) => setFormAttachVisual(e.target.checked)}
                          className="rounded text-purple-600 focus:ring-purple-500"
                        />
                        <span>Rendered Visual Dashboard (.png attachment)</span>
                      </label>
                      <label className="flex items-center gap-2 cursor-pointer text-slate-700">
                        <input
                          type="checkbox"
                          checked={formIncludeAlerts}
                          onChange={(e) => setFormIncludeAlerts(e.target.checked)}
                          className="rounded text-purple-600 focus:ring-purple-500"
                        />
                        <span>AI Diagnostic Anomaly Alerts &amp; Root Cause</span>
                      </label>
                      <label className="flex items-center gap-2 cursor-pointer text-slate-700">
                        <input
                          type="checkbox"
                          checked={formIncludeStockout}
                          onChange={(e) => setFormIncludeStockout(e.target.checked)}
                          className="rounded text-purple-600 focus:ring-purple-500"
                        />
                        <span>Darkstore Inventory &amp; Stockout Cover</span>
                      </label>
                      <label className="flex items-center gap-2 cursor-pointer text-slate-700">
                        <input
                          type="checkbox"
                          checked={formIncludeKpi}
                          onChange={(e) => setFormIncludeKpi(e.target.checked)}
                          className="rounded text-purple-600 focus:ring-purple-500"
                        />
                        <span>Executive Summary &amp; KPI Table</span>
                      </label>
                    </div>
                  </div>

                  {/* Enabled Toggle */}
                  <div className="flex items-center justify-between pt-1">
                    <label className="flex items-center gap-2 cursor-pointer font-semibold text-slate-800">
                      <input
                        type="checkbox"
                        checked={formEnabled}
                        onChange={(e) => setFormEnabled(e.target.checked)}
                        className="rounded text-purple-600 focus:ring-purple-500"
                      />
                      <span>Active (Enable automated cron execution)</span>
                    </label>

                    <div className="flex items-center gap-2">
                      <button
                        type="button"
                        onClick={() => {
                          setEditingJob(null);
                          setIsCreatingNew(false);
                        }}
                        className="px-3 py-1.5 border border-slate-200 text-slate-600 rounded-lg hover:bg-slate-100 font-medium"
                      >
                        Cancel
                      </button>
                      <button
                        type="button"
                        onClick={handleSaveScheduleForm}
                        className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-1.5 rounded-lg font-bold shadow-xs flex items-center gap-1.5"
                      >
                        <Check className="w-3.5 h-3.5" />
                        <span>Save Schedule</span>
                      </button>
                    </div>
                  </div>
                </div>
              ) : (
                /* LIST OF CONFIGURED SCHEDULES */
                <div className="space-y-3">
                  {schedules.length === 0 ? (
                    <div className="text-center py-8 text-slate-400 bg-slate-50 border border-slate-200 rounded-xl">
                      <Clock className="w-8 h-8 mx-auto mb-2 text-slate-300" />
                      <p className="font-semibold text-slate-600 text-xs">No email schedules configured yet.</p>
                      <p className="text-[11px] text-slate-400 mt-1">Create your first automated reporting rule above.</p>
                    </div>
                  ) : (
                    schedules.map((job) => (
                      <div
                        key={job.id}
                        className={`bg-white border rounded-xl p-4 transition-all shadow-xs space-y-3 ${
                          job.enabled ? 'border-purple-200 hover:border-purple-300' : 'border-slate-200 opacity-75'
                        }`}
                      >
                        <div className="flex items-start justify-between gap-3">
                          <div>
                            <div className="flex items-center gap-2 flex-wrap">
                              <h4 className="font-bold text-slate-900 text-sm">{job.name}</h4>
                              <span
                                className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                                  job.enabled
                                    ? 'bg-purple-100 text-purple-800 border-purple-200'
                                    : 'bg-slate-100 text-slate-600 border-slate-200'
                                }`}
                              >
                                {job.enabled ? '● Active' : '○ Paused'}
                              </span>
                              <span className="text-[10px] font-semibold bg-slate-100 text-slate-700 px-2 py-0.5 rounded-md border border-slate-200">
                                {job.frequency === 'Weekly' ? `Weekly (${job.weeklyDay || 'Mon'})` : job.frequency} @ {job.reportTime} {job.timezone.split('/')[1] || job.timezone}
                              </span>
                            </div>
                            <p className="text-[11px] text-slate-500 mt-1 font-mono">
                              To: <strong className="text-slate-700">{job.recipients.join(', ')}</strong>
                              {job.ccRecipients && job.ccRecipients.length > 0 && (
                                <span className="text-slate-400"> (CC: {job.ccRecipients.join(', ')})</span>
                              )}
                            </p>
                          </div>

                          <div className="flex items-center gap-1.5 shrink-0">
                            {/* Run now button */}
                            <button
                              onClick={() => handleRunScheduleNow(job)}
                              disabled={runningJobId === job.id}
                              title="Test trigger / Execute now"
                              className="text-xs bg-slate-50 hover:bg-purple-50 text-purple-700 border border-purple-200 hover:border-purple-300 px-2.5 py-1 rounded-lg font-semibold transition-all flex items-center gap-1 disabled:opacity-50"
                            >
                              {runningJobId === job.id ? (
                                <Loader2 className="w-3.5 h-3.5 animate-spin text-purple-600" />
                              ) : (
                                <Play className="w-3.5 h-3.5" />
                              )}
                              <span>Run Now</span>
                            </button>

                            {/* Edit */}
                            <button
                              onClick={() => handleOpenEditSchedule(job)}
                              title="Edit schedule configuration"
                              className="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors border border-transparent hover:border-slate-200"
                            >
                              <Edit2 className="w-3.5 h-3.5" />
                            </button>

                            {/* Delete */}
                            <button
                              onClick={() => handleDeleteSchedule(job.id)}
                              title="Delete schedule"
                              className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors border border-transparent hover:border-rose-200"
                            >
                              <Trash2 className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        </div>

                        {/* Status bar */}
                        <div className="flex items-center justify-between text-[11px] pt-2 border-t border-slate-100 text-slate-500">
                          <div className="flex items-center gap-3">
                            <span>
                              Next run: <strong className="text-slate-700">{job.nextRunEstimated || 'Configured schedule'}</strong>
                            </span>
                            {job.lastRunTimestamp && (
                              <span className="flex items-center gap-1">
                                • Last run: <strong className="text-slate-700">{job.lastRunTimestamp}</strong> ({job.lastRunStatus})
                              </span>
                            )}
                          </div>

                          <button
                            onClick={() => handleToggleSchedule(job.id)}
                            className="text-xs font-semibold text-slate-600 hover:text-slate-900 underline"
                          >
                            {job.enabled ? 'Pause Schedule' : 'Resume Schedule'}
                          </button>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="pt-3 border-t border-slate-100 flex items-center justify-between shrink-0 text-xs">
          <div className="text-[11px] text-slate-500 flex items-center gap-1">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
            <span>Multi-channel reporting engine • Powered by Sleepsia Intelligence</span>
          </div>

          <button
            onClick={onClose}
            className="px-4 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold rounded-lg transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
