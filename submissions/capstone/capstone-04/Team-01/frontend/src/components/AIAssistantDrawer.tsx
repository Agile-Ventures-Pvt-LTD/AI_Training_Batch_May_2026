import React, { useState, useEffect, useRef } from 'react';
import {
  X,
  Send,
  Sparkles,
  Bot,
  User,
  Zap,
  ArrowRight,
  ShieldCheck,
  TrendingDown,
  Building2,
  Mail,
  Loader2,
  Volume2,
  VolumeX,
  Mic,
  MicOff,
  Radio,
  Play,
  Square,
  CheckCircle2,
  ExternalLink,
  AlertTriangle
} from 'lucide-react';
import { AlertAnomaly } from '../types';
import { OWNER_EMAIL, SENDER_GMAIL } from '../data/mockData';
import { useData } from '../context/DataContext';

interface AIAssistantDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  onOpenEmailModal: (anomaly?: AlertAnomaly) => void;
  onOpenStockTransfer: (sku: string, hub: string) => void;
}

interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  timestamp: string;
  confidence?: number;
  sources?: string[];
  suggestedAction?: {
    label: string;
    actionType: 'transfer' | 'email' | 'coupon';
    payload?: any;
  };
}

// Clean markdown characters for smooth natural voice synthesis
function cleanMarkdownForSpeech(md: string): string {
  return md
    .replace(/#{1,6}\s?/g, '')
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/\*(.*?)\*/g, '$1')
    .replace(/`(.*?)`/g, '$1')
    .replace(/\[(.*?)\]\(.*?\)/g, '$1')
    .replace(/[•\-\*]\s+/g, '. ')
    .replace(/\n+/g, '. ')
    .replace(/\s{2,}/g, ' ')
    .trim();
}

export const AIAssistantDrawer: React.FC<AIAssistantDrawerProps> = ({
  isOpen,
  onClose,
  onOpenEmailModal,
  onOpenStockTransfer
}) => {
  const { skus, alerts } = useData();
  const getDynamicWelcomeMessage = (skus: any[], alerts: any[]): string => {
    const activeAlerts = alerts.filter(a => a.status !== 'Resolved').length;
    return `### 👋 Welcome Vikash! I am your Autonomous Control Tower AI Director

I am actively orchestrating multi-channel telemetry across all connected marketplaces.

#### ⚡ Real-Time Operational Briefing:
1. **Live Synchronized Catalog**: **${skus.length} active SKUs** currently monitored.
2. **Stock & Hub Availability**: Mother Hub reserves are being tracked in real-time.
3. **Active Anomalies**: **${activeAlerts} active issues** flagged across dark stores and pricing guardrails.
4. **Executive Direct Email Connected**: Reports are configured for 1-click delivery to **${OWNER_EMAIL}**.

*Feel free to speak via the microphone button or ask any inquiry below for a deep natural language breakdown.*`;
  };

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'msg-1',
      sender: 'assistant',
      text: getDynamicWelcomeMessage(skus, alerts),
      timestamp: 'Just now',
      confidence: 98,
      sources: ['Connected Dataset Stream', 'Mother Hub WMS', 'Real-Time Price Engine'],
      suggestedAction: {
        label: 'Initiate Stock Transfer from Nelamangala Hub (250 units)',
        actionType: 'transfer',
        payload: { sku: skus[0]?.sku || 'SLP-1001', hub: 'Bengaluru Central Mother Hub (Nelamangala)' }
      }
    }
  ]);

  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Voice Text-to-Speech (TTS) state
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [activeSpeechMsgId, setActiveSpeechMsgId] = useState<string | null>(null);
  const [speechRate, setSpeechRate] = useState<number>(1.0);

  // Speech-to-Text (STT) Microphone state
  const [isListening, setIsListening] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);
  const [micError, setMicError] = useState<string | null>(null);
  const recognitionRef = useRef<any>(null);

  // Initialize Speech Recognition (STT)
  useEffect(() => {
    const SpeechRec = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRec) {
      setSpeechSupported(true);
      const recognition = new SpeechRec();
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.lang = 'en-US';

      recognition.onresult = (event: any) => {
        const transcript = Array.from(event.results)
          .map((res: any) => res[0].transcript)
          .join('');
        setInputMessage(transcript);
        setMicError(null);
      };

      recognition.onerror = (event: any) => {
        console.warn('Speech recognition error:', event.error);
        setIsListening(false);
        if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
          setMicError('Microphone access was not allowed by your browser. Please allow microphone permissions in your browser URL bar or open the app in a new tab.');
        } else if (event.error === 'no-speech') {
          // No speech detected, silent timeout
        } else if (event.error === 'audio-capture') {
          setMicError('No microphone detected on your device.');
        } else {
          setMicError(`Voice input error (${event.error}). You can type your query in the input box below.`);
        }
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    }
  }, []);

  // Clean up speech synthesis when unmounting or closing
  useEffect(() => {
    return () => {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);


  // Text-To-Speech Play / Pause / Stop
  const handleToggleSpeak = (msgId: string, text: string) => {
    if (!('speechSynthesis' in window)) {
      alert('Speech synthesis is not supported in this browser environment.');
      return;
    }

    if (isSpeaking && activeSpeechMsgId === msgId) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      setActiveSpeechMsgId(null);
      return;
    }

    window.speechSynthesis.cancel();
    const cleanText = cleanMarkdownForSpeech(text);
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = speechRate;
    utterance.pitch = 1.0;
    utterance.lang = 'en-US';

    utterance.onstart = () => {
      setIsSpeaking(true);
      setActiveSpeechMsgId(msgId);
    };

    utterance.onend = () => {
      setIsSpeaking(false);
      setActiveSpeechMsgId(null);
    };

    utterance.onerror = (e) => {
      console.warn('TTS error:', e);
      setIsSpeaking(false);
      setActiveSpeechMsgId(null);
    };

    window.speechSynthesis.speak(utterance);
  };

  // Toggle Microphone Listening
  const handleToggleListening = async () => {
    if (!speechSupported || !recognitionRef.current) {
      setMicError('Voice microphone input is not supported in this browser. You can type your question directly.');
      return;
    }

    if (isListening) {
      try {
        recognitionRef.current.stop();
      } catch (e) {
        console.warn('Error stopping recognition:', e);
      }
      setIsListening(false);
    } else {
      setMicError(null);
      // Attempt to prompt/verify microphone permissions
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          // Stop media stream tracks right away since SpeechRecognition handles audio capture
          stream.getTracks().forEach((track) => track.stop());
        } catch (mediaErr: any) {
          console.warn('getUserMedia audio error:', mediaErr);
          if (mediaErr.name === 'NotAllowedError' || mediaErr.name === 'PermissionDeniedError') {
            setMicError('Microphone permission was blocked. Please enable microphone permissions in your browser URL bar or open the app in a new tab.');
            return;
          }
        }
      }

      try {
        recognitionRef.current.start();
        setIsListening(true);
      } catch (err: any) {
        console.warn('Recognition start error:', err);
        setIsListening(false);
        if (err.name === 'InvalidStateError') {
          // Already running
          setIsListening(true);
        } else {
          setMicError('Could not start speech recognition. Please check your microphone permissions.');
        }
      }
    }
  };

  if (!isOpen) return null;

  const quickPrompts = [
    'Why is Wedge Support Pillow Sales decreasing?',
    'Give me overview of SLP-1002',
    'What is the revenue of Car Neck Rest Pillow',
    'Check MAP violations and rogue sellers'
  ];

  const handleSendMessage = async (msgText?: string) => {
    const textToSend = msgText || inputMessage;
    if (!textToSend.trim() || isLoading) return;

    // Stop active speech if any
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      setActiveSpeechMsgId(null);
    }

    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: textToSend,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!msgText) setInputMessage('');
    setIsLoading(true);

    const getDynamicFallbackMessage = (promptText: string): string => {
      const activeAlerts = alerts.filter(a => a.status !== 'Resolved');
      const alertSummary = activeAlerts.length > 0
        ? `<li><strong>Latest Priority Alert</strong>: ${activeAlerts[0].summary}</li>`
        : '<li><strong>System Status</strong>: All systems operating within target guardrails.</li>';

      return `<div class="space-y-2">
        <h3 class="font-bold text-sm">📊 Cross-Channel Telemetry Response: "${promptText}"</h3>
        <ul class="list-disc pl-5 text-xs">
          ${alertSummary}
          <li><strong>Catalog Status</strong>: Monitoring ${skus.length} active Sleepsia SKUs.</li>
          <li><strong>Executive Email</strong>: Briefing is queued for 1-click delivery to <strong>${OWNER_EMAIL}</strong>.</li>
        </ul>
      </div>`;
    };

    try {
      const response = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: textToSend,
          context: {
            ownerEmail: OWNER_EMAIL,
            activeAnomalies: alerts.filter(a => a.status !== 'Resolved').length,
            catalogCount: skus.length,
            sampleSkus: skus.slice(0, 5).map(s => ({
              sku: s.sku,
              name: s.name,
              mrp: s.mrp,
              targetMap: s.targetMap,
              sellingPrice: s.sellingPrice,
              darkStoreStock: s.darkStoreStock,
              motherHubStock: s.motherHubStock
            }))
          }
        })
      });

      const data = await response.json();

      const aiMsg: ChatMessage = {
        id: `ai-${Date.now()}`,
        sender: 'assistant',
        text: data.reply || `<div class="space-y-2">
          <h3 class="font-bold text-sm">Operational Analysis for: "${textToSend}"</h3>
          <p>Cross-marketplace telemetry synchronized across ${skus.length} active Sleepsia SKUs. Mother Hub reserves are ready for dispatch. All systems operating within target guardrails.</p>
        </div>`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        confidence: data.confidence || 96,
        sources: data.sources || ['Real-Time Channel Telemetry', 'Mother Hub Logistics Feed', 'Shadowfax ERP'],
        suggestedAction: {
          label: 'Initiate Stock Transfer from Nelamangala Hub (250 units)',
          actionType: 'transfer',
          payload: { sku: skus[0]?.sku || 'SLP-1001', hub: 'Bengaluru Central Mother Hub (Nelamangala)' }
        }
      };

      setMessages((prev) => [...prev, aiMsg]);
    } catch (e) {
      console.error(e);
      const fallbackMsg: ChatMessage = {
        id: `ai-err-${Date.now()}`,
        sender: 'assistant',
        text: getDynamicFallbackMessage(textToSend),
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        confidence: 94
      };
      setMessages((prev) => [...prev, fallbackMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      id="ai-assistant-drawer"
      className="fixed inset-y-0 right-0 z-50 w-full sm:w-[540px] bg-white border-l border-slate-200 shadow-2xl flex flex-col animate-in slide-in-from-right duration-200 text-slate-900"
    >
      {/* Drawer Header */}
      <div className="px-5 py-3.5 bg-slate-900 border-b border-slate-800 text-white flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-blue-600 border border-blue-400/40 text-white flex items-center justify-center shadow-xs">
            <Sparkles className="w-4 h-4 text-amber-300 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-sm font-bold text-white tracking-tight">Agile Solutions AI Copilot</h3>
              <span className="text-[10px] bg-emerald-500/20 text-emerald-300 font-semibold px-2 py-0.5 rounded border border-emerald-400/30">
                Gemini 2.5 Active
              </span>
            </div>
            <p className="text-[11px] text-slate-300">Natural language telemetry reasoning & voice assistant</p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          {/* TTS Speed selector */}
          <button
            onClick={() => setSpeechRate((prev) => (prev === 1.0 ? 1.25 : prev === 1.25 ? 1.5 : 1.0))}
            title="Adjust Voice Speed Rate"
            className="text-[10px] font-mono px-2 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded transition-colors"
          >
            {speechRate}x Voice
          </button>
          
          <button
            id="close-ai-assistant-btn"
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 rounded-md hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Email Sender Information */}
      <div className="px-4 py-2 bg-blue-50 border-b border-blue-100 flex items-center text-xs">
        <div className="flex items-center space-x-2 text-blue-900">
          <Mail className="w-3.5 h-3.5 text-blue-600 shrink-0" />
          <span className="font-medium truncate">Sender Account: <strong className="font-mono">{OWNER_EMAIL}</strong></span>
        </div>
      </div>

      {/* Quick Prompts Bar */}
      <div className="p-3 bg-slate-50 border-b border-slate-200 space-y-1.5">
        <div className="flex items-center justify-between">
          <span className="text-[10px] uppercase font-bold tracking-wider text-slate-500 block">
            Executive Inquiries (Natural Language & Voice):
          </span>
          {isSpeaking && (
            <span className="inline-flex items-center space-x-1 text-[10px] font-semibold text-blue-700 animate-pulse">
              <Volume2 className="w-3 h-3" />
              <span>Voice Narration Active</span>
            </span>
          )}
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
          {quickPrompts.map((prompt, idx) => (
            <button
              key={idx}
              onClick={() => handleSendMessage(prompt)}
              className="px-2.5 py-1.5 text-[11px] font-medium bg-white hover:bg-blue-50/70 hover:border-blue-300 border border-slate-200 text-slate-700 rounded-md transition-all text-left shadow-2xs line-clamp-1"
            >
              {prompt}
            </button>
          ))}
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar bg-slate-100/50">
        {messages.map((msg) => {
          const isCurrentlySpeaking = isSpeaking && activeSpeechMsgId === msg.id;

          return (
            <div
              key={msg.id}
              className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
            >
              <div className="flex items-start space-x-2 max-w-[94%]">
                {msg.sender === 'assistant' && (
                  <div className="w-7 h-7 rounded-full bg-blue-600 text-white flex items-center justify-center shrink-0 mt-0.5 shadow-xs">
                    <Bot className="w-4 h-4" />
                  </div>
                )}
                
                <div
                  className={`p-4 rounded-xl text-xs leading-relaxed ${
                    msg.sender === 'user'
                      ? 'bg-blue-600 text-white rounded-br-none shadow-sm'
                      : 'bg-white border border-slate-200 text-slate-800 rounded-bl-none shadow-sm'
                  }`}
                >
                  {/* Top action bar for AI message: Voice Readout button */}
                  {msg.sender === 'assistant' && (
                    <div className="mb-2.5 pb-2 border-b border-slate-100 flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className="text-[10px] font-bold text-blue-700 uppercase tracking-wider">
                          Autonomous AI Telemetry
                        </span>
                        {isCurrentlySpeaking && (
                          <span className="flex items-center space-x-1 text-[10px] text-blue-600 bg-blue-50 px-1.5 py-0.5 rounded font-medium">
                            <span className="w-1.5 h-1.5 rounded-full bg-blue-600 animate-ping"></span>
                            <span>Speaking...</span>
                          </span>
                        )}
                      </div>

                      {/* TTS Voice Narration Button */}
                      <button
                        onClick={() => handleToggleSpeak(msg.id, msg.text)}
                        title={isCurrentlySpeaking ? 'Stop Voice Narration' : 'Listen to Voice Readout'}
                        className={`px-2 py-1 rounded text-[10px] font-semibold flex items-center space-x-1 transition-all ${
                          isCurrentlySpeaking
                            ? 'bg-red-100 text-red-700 border border-red-200 hover:bg-red-200'
                            : 'bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200'
                        }`}
                      >
                        {isCurrentlySpeaking ? (
                          <>
                            <Square className="w-3 h-3 fill-red-600 text-red-600" />
                            <span>Stop Voice</span>
                          </>
                        ) : (
                          <>
                            <Volume2 className="w-3 h-3 text-blue-600" />
                            <span>Read Out Voice</span>
                          </>
                        )}
                      </button>
                    </div>
                  )}

                  {/* Render HTML Content */}
                  <div 
                    className="prose prose-sm prose-slate max-w-none text-xs leading-relaxed font-sans select-text [&_h3]:font-bold [&_h3]:text-slate-900 [&_h3]:text-sm [&_h3]:mt-1 [&_h3]:mb-1 [&_h3]:pb-1 [&_h3]:border-b [&_h3]:border-slate-200 [&_h4]:font-bold [&_h4]:text-slate-900 [&_h4]:text-xs [&_h4]:text-blue-800 [&_h4]:mt-2 [&_h4]:mb-0.5 [&_ul]:pl-5 [&_ul]:list-disc [&_li]:mb-1"
                    dangerouslySetInnerHTML={{ __html: msg.text }}
                  />

                  {/* Evidence & Confidence meta */}
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="mt-3 pt-2.5 border-t border-slate-100 text-[10px] space-y-1">
                      <div className="flex items-center justify-between text-slate-500">
                        <span className="font-semibold text-slate-700">AI Confidence: {msg.confidence}%</span>
                        <span className="font-mono">{msg.timestamp}</span>
                      </div>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {msg.sources.map((src, i) => (
                          <span
                            key={i}
                            className="px-1.5 py-0.5 bg-slate-100 text-slate-700 border border-slate-200 rounded text-[9px] font-medium"
                          >
                            {src}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Direct Action Shortcut inside AI response */}
                  {msg.suggestedAction && (
                    <div className="mt-3 pt-2.5 border-t border-slate-100 flex flex-col gap-2">
                      <button
                        onClick={() =>
                          onOpenStockTransfer('SKU-SC-001', 'Bengaluru Central Mother Hub (Nelamangala)')
                        }
                        className="w-full px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg text-xs flex items-center justify-center space-x-1.5 shadow-sm transition-colors"
                      >
                        <Building2 className="w-3.5 h-3.5" />
                        <span>{msg.suggestedAction.label}</span>
                      </button>
                      <button
                        onClick={() => onOpenEmailModal()}
                        className="w-full px-3 py-2 bg-emerald-50 hover:bg-emerald-100 text-emerald-900 border border-emerald-300 font-bold rounded-lg text-xs flex items-center justify-center space-x-1.5 transition-colors"
                      >
                        <Mail className="w-3.5 h-3.5 text-emerald-600" />
                        <span>1-Click Auto-Send Email to {OWNER_EMAIL}</span>
                      </button>
                    </div>
                  )}
                </div>

                {msg.sender === 'user' && (
                  <div className="w-7 h-7 rounded-full bg-slate-200 text-slate-700 flex items-center justify-center shrink-0 mt-0.5">
                    <User className="w-4 h-4" />
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {isLoading && (
          <div className="flex items-center space-x-2 text-slate-700 text-xs py-2.5 px-3.5 bg-white border border-slate-200 rounded-xl max-w-[280px] shadow-sm">
            <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
            <span>Reasoning across channel telemetry...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Microphone Permission Warning / Error Banner */}
      {micError && (
        <div className="px-3.5 py-2 bg-amber-50 border-t border-amber-200 flex items-start justify-between text-xs text-amber-900 gap-2">
          <div className="flex items-start space-x-2">
            <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
            <div className="text-[11px] leading-tight">
              <span className="font-bold">Microphone Notice: </span>
              {micError}
            </div>
          </div>
          <button
            type="button"
            onClick={() => setMicError(null)}
            className="text-amber-700 hover:text-amber-900 font-bold text-xs shrink-0 p-0.5"
            title="Dismiss"
          >
            ✕
          </button>
        </div>
      )}

      {/* Voice Listening Active Waveform Banner */}
      {isListening && (
        <div className="px-4 py-2 bg-red-50 border-t border-red-200 flex items-center justify-between text-xs text-red-800 animate-pulse">
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-red-600 animate-ping"></span>
            <span className="font-semibold">Microphone Listening... Speak your question</span>
          </div>
          <button
            onClick={handleToggleListening}
            className="text-[11px] underline font-semibold text-red-700 hover:text-red-900"
          >
            Done
          </button>
        </div>
      )}

      {/* Input Form with Microphone (STT) and Send */}
      <div className="p-3 bg-white border-t border-slate-200">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSendMessage();
          }}
          className="relative flex items-center space-x-1.5"
        >
          {/* Voice Microphone Button */}
          <button
            id="voice-mic-btn"
            type="button"
            onClick={handleToggleListening}
            title={isListening ? 'Stop Listening' : 'Voice Input (Speak to AI)'}
            className={`p-2 rounded-lg border transition-all ${
              isListening
                ? 'bg-red-600 text-white border-red-700 shadow-md animate-pulse'
                : 'bg-slate-100 hover:bg-slate-200 text-slate-700 border-slate-300'
            }`}
          >
            {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4 text-blue-600" />}
          </button>

          <input
            id="ai-assistant-input"
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder={isListening ? 'Listening to your voice...' : 'Ask in natural language (or tap microphone to speak)...'}
            className="flex-1 pl-3.5 pr-10 py-2.5 text-xs bg-slate-50 border border-slate-300 text-slate-900 placeholder:text-slate-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all"
          />

          <button
            id="submit-ai-chat-btn"
            type="submit"
            disabled={!inputMessage.trim() || isLoading}
            className="p-2.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-40 text-white rounded-lg transition-colors shadow-xs"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
};
