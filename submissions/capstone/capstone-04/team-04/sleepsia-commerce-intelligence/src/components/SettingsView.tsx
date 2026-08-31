import React, { useState } from 'react';
import {
  Settings,
  Mail,
  Clock,
  Globe,
  Database,
  RefreshCw,
  CheckCircle2,
  AlertTriangle,
  Server,
  Save,
  Plus,
  Trash2,
  Send,
  FlaskConical,
  Loader2,
  ExternalLink,
  Calendar,
} from 'lucide-react';
import { EmailSettings, SleepsiaWorkbookData } from '../types/commerce';

interface SettingsViewProps {
  settings: EmailSettings;
  onSaveSettings: (newSettings: Partial<EmailSettings>) => void;
  data: SleepsiaWorkbookData;
  onResetData: () => void;
}

export const SettingsView: React.FC<SettingsViewProps> = ({
  settings,
  onSaveSettings,
  data,
  onResetData,
}) => {
  const [recipients, setRecipients] = useState<string[]>(
    settings.recipients || ['pranay.agileventures@gmail.com']
  );
  const [newRecipient, setNewRecipient] = useState('');
  const [ccRecipients, setCcRecipients] = useState<string[]>(
    settings.ccRecipients || ['analytics@sleepsia.com']
  );
  const [newCc, setNewCc] = useState('');
  const [reportTime, setReportTime] = useState(settings.reportTime || '09:00');
  const [timezone, setTimezone] = useState(settings.timezone || 'Asia/Kolkata');
  const [frequency, setFrequency] = useState<'Daily' | 'Weekdays' | 'Weekly'>(
    settings.frequency || 'Daily'
  );
  const [autoSendEnabled, setAutoSendEnabled] = useState(settings.autoSendEnabled ?? true);
  const [savedSuccess, setSavedSuccess] = useState(false);

  // Quick Action States
  const [isSendingReport, setIsSendingReport] = useState(false);
  const [isSendingTest, setIsSendingTest] = useState(false);
  const [actionFeedback, setActionFeedback] = useState<{
    type: 'success' | 'error';
    message: string;
    messageId?: string;
    previewUrl?: string;
  } | null>(null);

  const handleAddRecipient = () => {
    if (newRecipient.trim() && !recipients.includes(newRecipient.trim())) {
      setRecipients([...recipients, newRecipient.trim()]);
      setNewRecipient('');
    }
  };

  const handleRemoveRecipient = (email: string) => {
    setRecipients(recipients.filter((r) => r !== email));
  };

  const handleAddCc = () => {
    if (newCc.trim() && !ccRecipients.includes(newCc.trim())) {
      setCcRecipients([...ccRecipients, newCc.trim()]);
      setNewCc('');
    }
  };

  const handleRemoveCc = (email: string) => {
    setCcRecipients(ccRecipients.filter((r) => r !== email));
  };

  const handleSave = () => {
    onSaveSettings({
      recipients,
      ccRecipients,
      reportTime,
      timezone,
      frequency,
      autoSendEnabled,
    });
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 3000);
  };

  const handleSendTestEmail = async () => {
    setIsSendingTest(true);
    setActionFeedback(null);

    try {
      const res = await fetch('/api/email/send-test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          recipients,
          ccRecipients,
        }),
      });

      const json = await res.json();
      if (json.success) {
        setActionFeedback({
          type: 'success',
          message: json.message || 'Diagnostic test email sent successfully.',
          messageId: json.messageId,
          previewUrl: json.previewUrl,
        });
        onSaveSettings({
          lastSentTimestamp: json.timestamp,
          lastSentStatus: 'Success',
          lastSentMessage: json.message,
          lastMessageId: json.messageId,
          lastPreviewUrl: json.previewUrl,
        });
      } else {
        setActionFeedback({
          type: 'error',
          message: json.error || 'Failed to dispatch test email.',
        });
      }
    } catch (err: any) {
      setActionFeedback({
        type: 'error',
        message: err?.message || 'Network error sending test email.',
      });
    } finally {
      setIsSendingTest(false);
    }
  };

  const handleSendReportNow = async () => {
    setIsSendingReport(true);
    setActionFeedback(null);

    try {
      const res = await fetch('/api/email/send-report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          recipients,
          ccRecipients,
        }),
      });

      const json = await res.json();
      if (json.success) {
        setActionFeedback({
          type: 'success',
          message: json.message || 'Live Executive Report sent successfully.',
          messageId: json.messageId,
          previewUrl: json.previewUrl,
        });
        onSaveSettings({
          lastSentTimestamp: json.timestamp,
          lastSentStatus: 'Success',
          lastSentMessage: json.message,
          lastMessageId: json.messageId,
          lastPreviewUrl: json.previewUrl,
        });
      } else {
        setActionFeedback({
          type: 'error',
          message: json.error || 'Failed to send executive report.',
        });
      }
    } catch (err: any) {
      setActionFeedback({
        type: 'error',
        message: err?.message || 'Network error sending report.',
      });
    } finally {
      setIsSendingReport(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 border border-blue-100 flex items-center justify-center">
              <Settings className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900">
                Platform Configuration &amp; Automation Settings
              </h2>
              <p className="text-xs text-slate-500">
                Manage automated executive distribution, live email delivery, and daily scheduler workflows.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleSendTestEmail}
              disabled={isSendingTest || isSendingReport}
              className="bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold px-3.5 py-2 rounded-lg border border-slate-200 shadow-xs transition-colors flex items-center gap-1.5 disabled:opacity-50"
            >
              {isSendingTest ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin text-blue-600" />
                  <span>Testing...</span>
                </>
              ) : (
                <>
                  <FlaskConical className="w-3.5 h-3.5 text-slate-500" />
                  <span>Send Test Email</span>
                </>
              )}
            </button>

            <button
              onClick={handleSendReportNow}
              disabled={isSendingTest || isSendingReport}
              className="bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold px-3.5 py-2 rounded-lg shadow-xs transition-colors flex items-center gap-1.5 disabled:opacity-50"
            >
              {isSendingReport ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  <span>Sending Report...</span>
                </>
              ) : (
                <>
                  <Send className="w-3.5 h-3.5" />
                  <span>Send Report Now</span>
                </>
              )}
            </button>

            <button
              onClick={handleSave}
              className="bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-4 py-2 rounded-lg transition-colors flex items-center gap-1.5 shadow-xs"
            >
              <Save className="w-3.5 h-3.5" />
              <span>Save Settings</span>
            </button>
          </div>
        </div>
      </div>

      {savedSuccess && (
        <div className="bg-emerald-50 border border-emerald-200 text-emerald-700 p-3.5 rounded-xl text-xs flex items-center gap-2 font-medium">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>Automation settings successfully saved to server environment.</span>
        </div>
      )}

      {actionFeedback && (
        <div
          className={`p-4 rounded-xl border text-xs space-y-1.5 ${
            actionFeedback.type === 'success'
              ? 'bg-emerald-50 border-emerald-200 text-emerald-800'
              : 'bg-rose-50 border-rose-200 text-rose-800'
          }`}
        >
          <div className="flex items-center gap-2 font-bold">
            {actionFeedback.type === 'success' ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            ) : (
              <AlertTriangle className="w-4 h-4 text-rose-600" />
            )}
            <span>{actionFeedback.type === 'success' ? 'Delivery Confirmed' : 'Action Failed'}</span>
          </div>
          <p className="text-slate-700 pl-6">{actionFeedback.message}</p>
          {actionFeedback.messageId && (
            <div className="pl-6 font-mono text-[11px] text-slate-500">
              Message ID: <span className="font-semibold text-slate-800">{actionFeedback.messageId}</span>
            </div>
          )}
          {actionFeedback.previewUrl && (
            <div className="pl-6 pt-1">
              <a
                href={actionFeedback.previewUrl}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1 text-blue-600 hover:text-blue-800 font-semibold underline"
              >
                <ExternalLink className="w-3 h-3" />
                <span>Open Verified Inbox Message</span>
              </a>
            </div>
          )}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Section 1: Email Distribution & Scheduling */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 space-y-5 shadow-xs">
          <div className="flex items-center gap-2 pb-3 border-b border-slate-100 text-slate-900 font-bold text-sm">
            <Mail className="w-4 h-4 text-blue-600" />
            <span>Executive Email Distribution List</span>
          </div>

          {/* Primary Recipients */}
          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-700">
              Primary Recipients (To):
            </label>
            <div className="flex gap-2">
              <input
                type="email"
                placeholder="e.g. executive@sleepsia.com"
                value={newRecipient}
                onChange={(e) => setNewRecipient(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAddRecipient()}
                className="flex-1 bg-white border border-slate-200 text-slate-900 text-xs rounded-lg px-3 py-2 outline-none focus:ring-1 focus:ring-blue-500 shadow-xs"
              />
              <button
                onClick={handleAddRecipient}
                className="bg-white hover:bg-slate-50 text-slate-700 px-3 py-2 rounded-lg text-xs font-semibold flex items-center gap-1 border border-slate-200 shadow-xs"
              >
                <Plus className="w-3.5 h-3.5" /> Add
              </button>
            </div>
            <div className="flex flex-wrap gap-2 pt-1">
              {recipients.map((email) => (
                <span
                  key={email}
                  className="bg-slate-50 text-slate-700 border border-slate-200 text-xs px-2.5 py-1 rounded-md flex items-center gap-2 font-mono font-medium"
                >
                  {email}
                  <button
                    onClick={() => handleRemoveRecipient(email)}
                    className="text-slate-400 hover:text-rose-600"
                  >
                    <Trash2 className="w-3 h-3" />
                  </button>
                </span>
              ))}
            </div>
          </div>

          {/* CC Recipients */}
          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-700">
              CC Analytics &amp; Operations:
            </label>
            <div className="flex gap-2">
              <input
                type="email"
                placeholder="e.g. analytics@sleepsia.com"
                value={newCc}
                onChange={(e) => setNewCc(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAddCc()}
                className="flex-1 bg-white border border-slate-200 text-slate-900 text-xs rounded-lg px-3 py-2 outline-none focus:ring-1 focus:ring-blue-500 shadow-xs"
              />
              <button
                onClick={handleAddCc}
                className="bg-white hover:bg-slate-50 text-slate-700 px-3 py-2 rounded-lg text-xs font-semibold flex items-center gap-1 border border-slate-200 shadow-xs"
              >
                <Plus className="w-3.5 h-3.5" /> Add
              </button>
            </div>
            <div className="flex flex-wrap gap-2 pt-1">
              {ccRecipients.map((email) => (
                <span
                  key={email}
                  className="bg-slate-50 text-slate-700 border border-slate-200 text-xs px-2.5 py-1 rounded-md flex items-center gap-2 font-mono font-medium"
                >
                  {email}
                  <button
                    onClick={() => handleRemoveCc(email)}
                    className="text-slate-400 hover:text-rose-600"
                  >
                    <Trash2 className="w-3 h-3" />
                  </button>
                </span>
              ))}
            </div>
          </div>

          {/* Timing & Timezone */}
          <div className="grid grid-cols-2 gap-4 pt-2 border-t border-slate-100">
            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">
                Scheduled Dispatch Time:
              </label>
              <input
                type="time"
                value={reportTime}
                onChange={(e) => setReportTime(e.target.value)}
                className="w-full bg-white border border-slate-200 text-slate-900 text-xs rounded-lg p-2 outline-none shadow-xs font-semibold"
              />
            </div>
            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">
                Timezone:
              </label>
              <select
                value={timezone}
                onChange={(e) => setTimezone(e.target.value)}
                className="w-full bg-white border border-slate-200 text-slate-900 text-xs rounded-lg p-2 outline-none shadow-xs font-medium"
              >
                <option value="Asia/Kolkata">Asia/Kolkata (IST)</option>
                <option value="UTC">UTC</option>
                <option value="America/New_York">America/New_York (EST)</option>
                <option value="Europe/London">Europe/London (GMT)</option>
              </select>
            </div>
          </div>

          {/* Frequency & Auto-Send Switch */}
          <div className="grid grid-cols-2 gap-4 pt-2 border-t border-slate-100 items-center">
            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">
                Frequency:
              </label>
              <select
                value={frequency}
                onChange={(e) => setFrequency(e.target.value as any)}
                className="w-full bg-white border border-slate-200 text-slate-900 text-xs rounded-lg p-2 outline-none shadow-xs"
              >
                <option value="Daily">Daily</option>
                <option value="Weekdays">Weekdays (Mon-Fri)</option>
                <option value="Weekly">Weekly (Every Monday)</option>
              </select>
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">
                Auto-Send Automation:
              </label>
              <button
                type="button"
                onClick={() => setAutoSendEnabled(!autoSendEnabled)}
                className={`w-full py-2 px-3 rounded-lg text-xs font-bold border transition-colors flex items-center justify-center gap-2 ${
                  autoSendEnabled
                    ? 'bg-emerald-50 border-emerald-300 text-emerald-700'
                    : 'bg-slate-100 border-slate-300 text-slate-600'
                }`}
              >
                <div
                  className={`w-2 h-2 rounded-full ${
                    autoSendEnabled ? 'bg-emerald-500 animate-pulse' : 'bg-slate-400'
                  }`}
                />
                <span>{autoSendEnabled ? 'Active (Auto-Send ON)' : 'Paused (Manual Only)'}</span>
              </button>
            </div>
          </div>
        </div>

        {/* Section 2: Automated Pipeline & Delivery Status */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 space-y-5 shadow-xs">
          <div className="flex items-center gap-2 pb-3 border-b border-slate-100 text-slate-900 font-bold text-sm">
            <Server className="w-4 h-4 text-blue-600" />
            <span>Automated Execution Pipeline &amp; Delivery Status</span>
          </div>

          {/* Last Delivery Status Card */}
          <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="font-bold text-slate-900">Latest Delivery Status:</span>
              <span
                className={`text-[10px] font-black px-2 py-0.5 rounded-full ${
                  settings.lastSentStatus === 'Success'
                    ? 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                    : settings.lastSentStatus === 'Failed'
                    ? 'bg-rose-100 text-rose-800 border border-rose-200'
                    : 'bg-slate-200 text-slate-700'
                }`}
              >
                {settings.lastSentStatus || 'Never Sent'}
              </span>
            </div>

            <div className="text-[11px] text-slate-600 space-y-1">
              <div>
                • Timestamp:{' '}
                <span className="text-slate-900 font-medium">
                  {settings.lastSentTimestamp || 'No dispatches recorded yet'}
                </span>
              </div>
              {settings.lastSentMessage && (
                <div>
                  • Message:{' '}
                  <span className="text-slate-800">{settings.lastSentMessage}</span>
                </div>
              )}
              {settings.lastMessageId && (
                <div>
                  • Message ID:{' '}
                  <span className="text-slate-900 font-mono font-semibold">
                    {settings.lastMessageId}
                  </span>
                </div>
              )}
              {settings.lastPreviewUrl && (
                <div className="pt-1">
                  <a
                    href={settings.lastPreviewUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="text-blue-600 hover:text-blue-800 font-semibold underline inline-flex items-center gap-1"
                  >
                    <ExternalLink className="w-3 h-3" />
                    <span>View Last Dispatched Message</span>
                  </a>
                </div>
              )}
            </div>
          </div>

          {/* Pipeline Diagram */}
          <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 space-y-2 text-xs">
            <div className="font-bold text-blue-800 text-[11px] uppercase tracking-wide">
              Automated Pipeline Workflow:
            </div>
            <div className="font-mono text-[11px] bg-white p-2.5 rounded-lg border border-slate-200 text-slate-700 leading-relaxed overflow-x-auto">
              Load latest data → Analyze data → Generate executive summary → Generate dashboard visual → Compose email → Send email
            </div>
            <p className="text-[11px] text-slate-500">
              Cloud Scheduler or local timer invokes the pipeline daily at{' '}
              <strong className="text-slate-800">{reportTime} {timezone}</strong>.
            </p>
          </div>

          {/* Dataset Status */}
          <div className="pt-3 border-t border-slate-100">
            <div className="flex items-center justify-between text-xs mb-2">
              <span className="font-bold text-slate-900">Active Sleepsia Dataset:</span>
              <button
                onClick={onResetData}
                className="text-xs text-blue-600 hover:text-blue-700 font-semibold flex items-center gap-1"
              >
                <RefreshCw className="w-3 h-3" /> Reset Synthetic Data
              </button>
            </div>
            <div className="bg-slate-50 p-3 rounded-lg border border-slate-200 text-[11px] text-slate-600 space-y-1">
              <div>
                • File:{' '}
                <span className="text-slate-900 font-mono font-medium">
                  {data.metadata.fileName}
                </span>
              </div>
              <div>
                • Sheets Connected:{' '}
                <span className="text-emerald-700 font-bold">11 Sheets (Unified Model)</span>
              </div>
              <div>
                • Date Range:{' '}
                <span className="text-slate-800 font-medium">
                  {data.metadata.dateRange.start} to {data.metadata.dateRange.end}
                </span>
              </div>
              <div>
                • SKUs:{' '}
                <span className="text-slate-800 font-bold">{data.products.length} Products</span>{' '}
                across{' '}
                <span className="text-slate-800 font-bold">
                  {data.metadata.activeChannels} Marketplaces
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
