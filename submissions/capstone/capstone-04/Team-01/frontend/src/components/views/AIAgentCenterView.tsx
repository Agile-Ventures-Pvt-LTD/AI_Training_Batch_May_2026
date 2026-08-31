import React from 'react';
import {
  Bot,
  Play,
  CheckCircle2,
  Clock,
  Sparkles,
  RefreshCw,
  Layers,
  ShieldCheck
} from 'lucide-react';
import { AIAgentStatus } from '../../types';
import { AI_AGENTS_LIST } from '../../data/mockData';
import confetti from 'canvas-confetti';

export const AIAgentCenterView: React.FC = () => {
  const [agents, setAgents] = React.useState<AIAgentStatus[]>(AI_AGENTS_LIST);
  const [runningAgentId, setRunningAgentId] = React.useState<string | null>(null);

  const handleRunAgent = (agentId: string) => {
    setRunningAgentId(agentId);
    setTimeout(() => {
      setAgents((prev) =>
        prev.map((a) =>
          a.id === agentId
            ? { ...a, lastRunTimestamp: 'Just now', actionsTakenCount: a.actionsTakenCount + 1 }
            : a
        )
      );
      setRunningAgentId(null);
      confetti({
        particleCount: 40,
        spread: 40,
        origin: { y: 0.6 }
      });
    }, 1200);
  };

  return (
    <div id="ai-agents-center-view" className="space-y-6">
      {/* Header */}
      <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Autonomous AI Agent Director & 16 Specialized Agents</h2>
            <span className="px-2 py-0.5 bg-emerald-50 text-emerald-700 border border-emerald-200 text-[10px] font-bold rounded">
              All 16 Healthy
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Continuous background reasoning agents for digital shelf, perishables FEFO, MAP compliance, and quick commerce supply chain
          </p>
        </div>
      </div>

      {/* Agents Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agents.map((agent) => {
          const isRunning = runningAgentId === agent.id;

          return (
            <div key={agent.id} className="p-5 bg-white rounded-xl border border-slate-200 shadow-xs space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 rounded-lg bg-blue-50 border border-blue-200 text-blue-700 flex items-center justify-center">
                    <Bot className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="font-bold text-xs text-slate-900 leading-tight">{agent.name}</h3>
                    <span className="font-mono text-[10px] text-slate-500">{agent.id}</span>
                  </div>
                </div>

                <span className="px-2 py-0.5 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded text-[10px] font-bold">
                  {agent.status}
                </span>
              </div>

              <p className="text-xs text-slate-600 leading-relaxed min-h-[36px]">
                {agent.description}
              </p>

              <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-xs space-y-1">
                <div className="flex justify-between text-[11px]">
                  <span className="text-slate-500">Execution Frequency:</span>
                  <span className="font-semibold text-slate-800">{agent.frequency}</span>
                </div>
                <div className="flex justify-between text-[11px]">
                  <span className="text-slate-500">Actions Logged:</span>
                  <span className="font-bold text-blue-700">{agent.actionsTakenCount} actions</span>
                </div>
              </div>

              <div className="flex items-center justify-between pt-2 border-t border-slate-100">
                <span className="text-[10px] text-slate-500">Last run: {agent.lastRunTimestamp}</span>
                <button
                  id={`run-agent-${agent.id}`}
                  onClick={() => handleRunAgent(agent.id)}
                  disabled={isRunning}
                  className="px-3 py-1.5 bg-blue-50 hover:bg-blue-100 border border-blue-200 disabled:opacity-50 text-blue-700 text-xs font-bold rounded-md flex items-center space-x-1.5 shadow-2xs transition-colors"
                >
                  <Play className={`w-3 h-3 ${isRunning ? 'animate-spin' : ''}`} />
                  <span>{isRunning ? 'Executing...' : 'Run Agent Now'}</span>
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
