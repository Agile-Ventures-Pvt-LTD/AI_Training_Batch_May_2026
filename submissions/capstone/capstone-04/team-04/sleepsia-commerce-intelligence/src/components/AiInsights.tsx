import React, { useState } from 'react';
import {
  Sparkles,
  ShieldAlert,
  TrendingDown,
  TrendingUp,
  ThumbsUp,
  ThumbsDown,
  MessageSquare,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  Database,
  ArrowRight,
  Filter,
} from 'lucide-react';
import { AgentStructuredFinding } from '../types/commerce';

interface AiInsightsProps {
  findings: AgentStructuredFinding[];
  onFeedback: (findingId: string, feedback: 'thumbs_up' | 'thumbs_down', note?: string) => void;
  isAnalyzing: boolean;
  onRerun: () => void;
  selectedDate: string;
}

export const AiInsights: React.FC<AiInsightsProps> = ({
  findings,
  onFeedback,
  isAnalyzing,
  onRerun,
  selectedDate,
}) => {
  const [agentFilter, setAgentFilter] = useState<string>('All');
  const [feedbackNoteModal, setFeedbackNoteModal] = useState<{ id: string; feedback: 'thumbs_up' | 'thumbs_down' } | null>(null);
  const [noteText, setNoteText] = useState('');

  const agents = ['All', 'Sales', 'Advertising', 'Competitor', 'Inventory & Shipping'];

  const filteredFindings = agentFilter === 'All'
    ? findings
    : findings.filter((f) => f.agent === agentFilter || (agentFilter === 'Inventory & Shipping' && (f.area === 'Inventory' || f.area === 'Shipping')));

  const handleFeedbackSubmit = () => {
    if (feedbackNoteModal) {
      onFeedback(feedbackNoteModal.id, feedbackNoteModal.feedback, noteText);
      setFeedbackNoteModal(null);
      setNoteText('');
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner Card */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="p-1.5 rounded-lg bg-blue-50 text-blue-600 border border-blue-100">
                <Sparkles className="w-4 h-4" />
              </span>
              <h2 className="text-base font-bold text-slate-900">
                Autonomous Multi-Agent Root Cause Intelligence
              </h2>
            </div>
            <p className="text-xs text-slate-500 mt-1">
              Cross-functional causal synthesis answering "What happened?", "Why did it happen?", and "What should Sleepsia do?" for {selectedDate}.
            </p>
          </div>

          <div className="flex items-center gap-3">
            {/* Filter by Agent */}
            <div className="flex items-center gap-1.5 bg-slate-50 border border-slate-200 p-1 rounded-lg text-xs">
              <Filter className="w-3.5 h-3.5 text-slate-400 ml-1" />
              <span className="text-slate-500 text-[11px] font-medium mr-1">Agent:</span>
              {agents.map((ag) => (
                <button
                  key={ag}
                  onClick={() => setAgentFilter(ag)}
                  className={`px-2.5 py-1 rounded font-semibold text-xs transition-colors ${
                    agentFilter === ag ? 'bg-blue-600 text-white shadow-xs' : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  {ag}
                </button>
              ))}
            </div>

            <button
              onClick={onRerun}
              disabled={isAnalyzing}
              className="bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-3 py-2 rounded-lg transition-colors flex items-center gap-1.5 disabled:opacity-50 shadow-xs"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>{isAnalyzing ? 'Analyzing...' : 'Re-Run Multi-Agent Engine'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Findings Cards List */}
      <div className="space-y-4">
        {filteredFindings.length === 0 ? (
          <div className="bg-white border border-slate-200 rounded-xl p-8 text-center text-slate-500 shadow-xs">
            <CheckCircle2 className="w-8 h-8 text-emerald-600 mx-auto mb-2" />
            <p className="font-semibold text-slate-900">No anomalies detected for the selected filter.</p>
            <p className="text-xs mt-1 text-slate-500">All commercial metrics are operating within expected baseline thresholds.</p>
          </div>
        ) : (
          filteredFindings.map((f) => {
            const isCritical = f.severity === 'critical' || f.severity === 'high';
            const hasFeedback = !!f.feedback;

            return (
              <div
                key={f.id}
                className={`bg-white border rounded-xl p-5 transition-all shadow-xs ${
                  isCritical ? 'border-rose-300 hover:border-rose-400 ring-1 ring-rose-50' : 'border-slate-200 hover:border-slate-300'
                }`}
              >
                {/* Finding Header */}
                <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-slate-100">
                  <div className="flex items-center gap-2">
                    <span className={`px-2 py-0.5 rounded text-[11px] font-bold uppercase border ${
                      f.priority?.startsWith('P0')
                        ? 'bg-rose-50 text-rose-700 border-rose-200'
                        : f.priority?.startsWith('P1')
                        ? 'bg-amber-50 text-amber-700 border-amber-200'
                        : 'bg-blue-50 text-blue-700 border-blue-200'
                    }`}>
                      {f.priority || 'P1 - Urgent'}
                    </span>
                    <span className="text-xs font-semibold text-slate-700 px-2 py-0.5 bg-slate-100 rounded border border-slate-200">
                      Agent: {f.agent}
                    </span>
                    <span className="text-xs font-semibold text-slate-700 px-2 py-0.5 bg-slate-100 rounded border border-slate-200">
                      Area: {f.area}
                    </span>
                  </div>

                  <div className="flex items-center gap-3 text-xs">
                    <div className="flex items-center gap-1.5 text-slate-700 font-mono font-bold bg-slate-50 px-2.5 py-1 rounded border border-slate-200">
                      <span>{f.metric}:</span>
                      <strong className="text-slate-900">{f.current_value}</strong>
                      <span className={`text-[11px] ${f.change_percent < 0 ? 'text-rose-700' : 'text-emerald-700'}`}>
                        ({f.change_percent > 0 ? `+${f.change_percent}%` : `${f.change_percent}%`})
                      </span>
                    </div>

                    <span className="text-slate-500 font-medium">
                      Confidence: <strong className="text-emerald-700 font-mono">{(f.confidence * 100).toFixed(0)}%</strong>
                    </span>
                  </div>
                </div>

                {/* Finding Body: 3-Pillar Causal Architecture */}
                <div className="mt-4 grid grid-cols-1 lg:grid-cols-3 gap-4">
                  {/* Column 1: What Happened? */}
                  <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2">
                    <div className="flex items-center gap-1.5 text-xs font-bold text-slate-900">
                      <span className="w-2 h-2 rounded-full bg-blue-600"></span>
                      <span>1. What Happened?</span>
                    </div>
                    <p className="text-xs text-slate-700 leading-relaxed font-medium">
                      {f.finding}
                    </p>
                  </div>

                  {/* Column 2: Why Did It Happen? (Root Cause Hypotheses) */}
                  <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2">
                    <div className="flex items-center gap-1.5 text-xs font-bold text-amber-700">
                      <span className="w-2 h-2 rounded-full bg-amber-500"></span>
                      <span>2. Why Did It Happen? (Drivers &amp; Correlation)</span>
                    </div>
                    <ul className="text-xs text-slate-700 space-y-1.5 list-none">
                      {f.possible_causes.map((cause, cIdx) => (
                        <li key={cIdx} className="flex items-start gap-1.5 leading-relaxed">
                          <span className="text-slate-400 mt-0.5">•</span>
                          <span>{cause}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Column 3: What Should Sleepsia Do? (Prescription) */}
                  <div className="bg-blue-50/50 p-4 rounded-xl border border-blue-200 space-y-2">
                    <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-700">
                      <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                      <span>3. What Should Sleepsia Do?</span>
                    </div>
                    <p className="text-xs text-slate-900 font-semibold leading-relaxed">
                      {f.recommended_action}
                    </p>
                    {f.expected_business_impact && (
                      <div className="text-[11px] text-blue-900 pt-1.5 border-t border-blue-200 font-medium">
                        <strong>Expected Impact:</strong> {f.expected_business_impact}
                      </div>
                    )}
                  </div>
                </div>

                {/* Footer: Data Sources Cited & Interactive Feedback */}
                <div className="mt-4 pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3 text-xs">
                  {/* Cited Datasets */}
                  <div className="flex items-center gap-2 text-slate-500">
                    <Database className="w-3.5 h-3.5 text-slate-400" />
                    <span className="text-[11px] font-medium">Evidence Sources:</span>
                    <div className="flex flex-wrap gap-1.5">
                      {f.source.map((src) => (
                        <span
                          key={src}
                          className="bg-slate-100 text-slate-700 text-[10px] font-mono px-2 py-0.5 rounded border border-slate-200 font-medium"
                        >
                          [{src}]
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Feedback Controls */}
                  <div className="flex items-center gap-2">
                    <span className="text-[11px] text-slate-500 font-medium">Was this finding helpful?</span>
                    <button
                      onClick={() => setFeedbackNoteModal({ id: f.id, feedback: 'thumbs_up' })}
                      className={`p-1.5 rounded-md transition-colors ${
                        f.feedback === 'thumbs_up'
                          ? 'bg-emerald-600 text-white'
                          : 'bg-white text-slate-500 hover:text-slate-800 border border-slate-200 hover:bg-slate-50'
                      }`}
                      title="Helpful recommendation"
                    >
                      <ThumbsUp className="w-3.5 h-3.5" />
                    </button>
                    <button
                      onClick={() => setFeedbackNoteModal({ id: f.id, feedback: 'thumbs_down' })}
                      className={`p-1.5 rounded-md transition-colors ${
                        f.feedback === 'thumbs_down'
                          ? 'bg-rose-600 text-white'
                          : 'bg-white text-slate-500 hover:text-slate-800 border border-slate-200 hover:bg-slate-50'
                      }`}
                      title="Not applicable or incorrect"
                    >
                      <ThumbsDown className="w-3.5 h-3.5" />
                    </button>

                    {f.feedback && (
                      <span className="text-[11px] text-emerald-700 font-semibold flex items-center gap-1">
                        <CheckCircle2 className="w-3 h-3" /> Recorded ({f.feedback === 'thumbs_up' ? 'Approved' : 'Disputed'})
                      </span>
                    )}
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Optional Feedback Note Dialog */}
      {feedbackNoteModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white border border-slate-200 rounded-xl p-5 max-w-md w-full shadow-xl space-y-4">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <MessageSquare className="w-4 h-4 text-blue-600" />
              Provide Recommendation Feedback
            </h3>
            <p className="text-xs text-slate-600">
              Help the AI Supervisor learn from human executive oversight:
            </p>
            <textarea
              rows={3}
              value={noteText}
              onChange={(e) => setNoteText(e.target.value)}
              placeholder="Add optional notes (e.g. 'Supplier confirmed stock delay is resolved', 'Approved price cut on Blinkit')..."
              className="w-full bg-white border border-slate-200 rounded-lg p-2.5 text-xs text-slate-900 outline-none focus:ring-1 focus:ring-blue-500 shadow-xs"
            />
            <div className="flex justify-end gap-2 text-xs">
              <button
                onClick={() => setFeedbackNoteModal(null)}
                className="px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 border border-slate-200"
              >
                Cancel
              </button>
              <button
                onClick={handleFeedbackSubmit}
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-4 py-1.5 rounded-lg shadow-xs"
              >
                Save Feedback
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
