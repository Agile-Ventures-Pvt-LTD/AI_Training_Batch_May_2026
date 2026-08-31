import React, { useState } from 'react';
import {
  MessageSquare,
  Send,
  Sparkles,
  Bot,
  User,
  Database,
  ArrowRight,
  Loader2,
} from 'lucide-react';
import { ChatMessage } from '../types/commerce';

interface ChatAssistantProps {
  onSendMessage: (query: string) => Promise<{ answer: string; sources: string[] }>;
  selectedDate: string;
}

export const ChatAssistant: React.FC<ChatAssistantProps> = ({
  onSendMessage,
  selectedDate,
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'msg-welcome',
      sender: 'agent',
      content: `Hello! I am the Sleepsia Multi-Agent Commerce Intelligence Assistant. Ask me anything about yesterday's revenue (${selectedDate}), Amazon performance, ad campaign efficiency, competitor price shifts, or carrier delivery delays.`,
      sources: ['Internal_Sales', 'Marketplace_Data', 'Competitor_Data', 'Shipping_Data'],
      timestamp: 'Just now',
    },
  ]);
  const [inputQuery, setInputQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sampleQueries = [
    'Why did Amazon sales decline yesterday?',
    'Which carrier has the lowest on-time delivery rate?',
    'Which products are at critical risk of stockout?',
    'How did Quick Commerce (Blinkit & Instamart) perform?',
    'What is our TACoS and paid vs organic sales contribution?',
    'What price changes did Wakefit make?',
  ];

  const handleSend = async (queryToSend?: string) => {
    const text = queryToSend || inputQuery;
    if (!text.trim() || isLoading) return;

    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!queryToSend) setInputQuery('');
    setIsLoading(true);

    try {
      const response = await onSendMessage(text);
      const assistantMsg: ChatMessage = {
        id: `assistant-${Date.now()}`,
        sender: 'agent',
        content: response.answer,
        sources: response.sources,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      const errorMsg: ChatMessage = {
        id: `err-${Date.now()}`,
        sender: 'agent',
        content: 'Sorry, I encountered an issue retrieving that analysis. Please try again or rephrase.',
        sources: ['System_Error'],
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 border border-blue-100 flex items-center justify-center">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              Conversational Commerce Intelligence BI Agent
            </h2>
            <p className="text-xs text-slate-500">
              Query unified cross-marketplace data for {selectedDate} with automatic source attribution.
            </p>
          </div>
        </div>
      </div>

      {/* Suggested Starter Prompts */}
      <div className="flex flex-wrap gap-2">
        {sampleQueries.map((sq, i) => (
          <button
            key={i}
            onClick={() => handleSend(sq)}
            className="text-xs bg-white hover:bg-slate-50 text-slate-700 hover:text-slate-900 px-3 py-1.5 rounded-lg border border-slate-200 hover:border-slate-300 transition-colors flex items-center gap-1.5 shadow-xs font-medium"
          >
            <Sparkles className="w-3 h-3 text-blue-600" />
            <span>{sq}</span>
          </button>
        ))}
      </div>

      {/* Chat Messages Log */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 min-h-[420px] flex flex-col justify-between shadow-xs">
        <div className="space-y-4 overflow-y-auto max-h-[500px] pr-2">
          {messages.map((m) => (
            <div
              key={m.id}
              className={`flex gap-3 text-xs ${
                m.sender === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {m.sender !== 'user' && (
                <div className="w-7 h-7 rounded-lg bg-blue-50 text-blue-600 border border-blue-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <Bot className="w-4 h-4" />
                </div>
              )}

              <div
                className={`max-w-2xl rounded-xl p-4 space-y-2 leading-relaxed ${
                  m.sender === 'user'
                    ? 'bg-blue-600 text-white font-medium shadow-xs'
                    : 'bg-slate-50 text-slate-800 border border-slate-200 shadow-xs'
                }`}
              >
                <div className="whitespace-pre-wrap">{m.content}</div>

                {m.sources && m.sources.length > 0 && (
                  <div className="pt-2 border-t border-slate-200/80 flex items-center gap-1.5 text-[10px] text-slate-500 font-medium">
                    <Database className="w-3 h-3 text-slate-400" />
                    <span>Evidence Sources:</span>
                    {m.sources.map((s) => (
                      <span
                        key={s}
                        className="bg-white text-slate-700 font-mono px-1.5 py-0.5 rounded border border-slate-200"
                      >
                        [{s}]
                      </span>
                    ))}
                  </div>
                )}

                <div className={`text-[10px] text-right ${m.sender === 'user' ? 'text-blue-100' : 'text-slate-400'}`}>{m.timestamp}</div>
              </div>

              {m.sender === 'user' && (
                <div className="w-7 h-7 rounded-lg bg-slate-100 text-slate-700 border border-slate-200 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex gap-3 text-xs justify-start">
              <div className="w-7 h-7 rounded-lg bg-blue-50 text-blue-600 border border-blue-100 flex items-center justify-center flex-shrink-0">
                <Bot className="w-4 h-4 animate-spin" />
              </div>
              <div className="bg-slate-50 text-slate-600 border border-slate-200 rounded-xl p-3.5 flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
                <span>Gemini Multi-Agent reasoning over commerce tables...</span>
              </div>
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div className="mt-5 pt-4 border-t border-slate-100 flex gap-2">
          <input
            type="text"
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask about revenue trends, product margins, ad efficiency, logistics..."
            className="flex-1 bg-white border border-slate-200 text-slate-900 text-xs rounded-xl px-4 py-3 outline-none focus:ring-1 focus:ring-blue-500 shadow-xs"
          />
          <button
            onClick={() => handleSend()}
            disabled={!inputQuery.trim() || isLoading}
            className="bg-blue-600 hover:bg-blue-700 text-white px-5 rounded-xl text-xs font-bold transition-colors disabled:opacity-50 flex items-center gap-1.5 shadow-xs"
          >
            <Send className="w-3.5 h-3.5" />
            <span>Send</span>
          </button>
        </div>
      </div>
    </div>
  );
};
