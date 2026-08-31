import React, { useState, useEffect, useMemo } from 'react';
import {
  LayoutDashboard,
  Layers,
  Zap,
  Package,
  ShieldAlert,
  Truck,
  Sparkles,
  FileText,
  MessageSquare,
  Settings,
  AlertCircle,
  Loader2,
  CheckCircle2,
  Cpu,
  Shield,
  Filter,
  Code2,
  Boxes,
} from 'lucide-react';
import { Header } from './components/Header';
import { ExecutiveOverview } from './components/ExecutiveOverview';
import { CategoryIntelligence } from './components/CategoryIntelligence';
import { MarketplaceAnalysis } from './components/MarketplaceAnalysis';
import { AdvertisingAnalysis } from './components/AdvertisingAnalysis';
import { ProductIntelligence } from './components/ProductIntelligence';
import { CompetitorIntelligence } from './components/CompetitorIntelligence';
import { ShippingIntelligence } from './components/ShippingIntelligence';
import { StockManagement } from './components/StockManagement';
import { AiInsights } from './components/AiInsights';
import { DailyReportView } from './components/DailyReportView';
import { ChatAssistant } from './components/ChatAssistant';
import { SettingsView } from './components/SettingsView';
import { MultiAgentOrchestrator } from './components/MultiAgentOrchestrator';
import { AgentLogicAnalysisView } from './components/AgentLogicAnalysisView';
import { RoleSwitcherModal } from './components/RoleSwitcherModal';
import { UploadModal } from './components/UploadModal';
import { EmailModal } from './components/EmailModal';
import { AgentExecutionModal } from './components/AgentExecutionModal';
import {
  SleepsiaWorkbookData,
  CalculatedKPIs,
  AgentStructuredFinding,
  ExecutiveReportData,
  EmailSettings,
  MarketplaceChannel,
} from './types/commerce';
import { UserRole, UserProfile, MOCK_USERS } from './types/rbac';
import { getActiveDataset, resetToDefaultDataset } from './services/datasetService';
import { calculateKPIs } from './services/kpiEngine';
import {
  runDeterministicMultiAgentAnalysis,
  buildDailyExecutiveReport,
  recordAgentFeedback,
} from './services/multiAgentSupervisor';

export function App() {
  // RBAC State
  const [currentUser, setCurrentUser] = useState<UserProfile>(MOCK_USERS['Executive']);
  const [isRoleSwitcherOpen, setIsRoleSwitcherOpen] = useState<boolean>(false);

  // Time Comparison Preset State
  const [timeRangePreset, setTimeRangePreset] = useState<'today' | 'yesterday' | '7d' | '30d' | 'custom'>('today');

  const [activeTab, setActiveTab] = useState<string>('overview');
  const [dataset, setDataset] = useState<SleepsiaWorkbookData>(getActiveDataset());
  const [selectedDate, setSelectedDate] = useState<string>(dataset.metadata.dateRange.end);
  const [selectedChannel, setSelectedChannel] = useState<MarketplaceChannel | 'All'>('All');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  const [kpis, setKpis] = useState<CalculatedKPIs>(() =>
    calculateKPIs(dataset, { date: selectedDate })
  );
  const [findings, setFindings] = useState<AgentStructuredFinding[]>(() =>
    runDeterministicMultiAgentAnalysis(dataset, selectedDate)
  );
  const [report, setReport] = useState<ExecutiveReportData>(() =>
    buildDailyExecutiveReport(dataset, selectedDate)
  );
  const [emailSettings, setEmailSettings] = useState<EmailSettings>({
    recipients: ['acedavkhills@gmail.com', 'pranay.agileventures@gmail.com'],
    ccRecipients: [],
    reportTime: '09:00',
    timezone: 'Asia/Kolkata',
    frequency: 'Daily',
    autoSendEnabled: true,
  });

  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [isEmailModalOpen, setIsEmailModalOpen] = useState(false);
  const [isAgentExecutionOpen, setIsAgentExecutionOpen] = useState(false);
  const [executionTriggerSource, setExecutionTriggerSource] = useState<'upload' | 'manual' | 'view'>('manual');
  const [notification, setNotification] = useState<{ message: string; type: 'success' | 'info' } | null>(null);

  // Available dates
  const availableDates = Array.from(new Set(dataset.sales.map((s) => s.date))).sort();
  const availableChannels = dataset.marketplaceMasters.map((m) => m.platform);
  const availableCategories = Array.from(new Set(dataset.products.map((p) => p.category)));

  // Role verification guard: ensure activeTab is permitted for current role
  useEffect(() => {
    if (!currentUser.allowedTabs.includes(activeTab)) {
      setActiveTab(currentUser.allowedTabs[0] || 'overview');
    }
  }, [currentUser, activeTab]);

  // Load email and scheduler settings from backend on initial mount
  useEffect(() => {
    fetch('/api/settings')
      .then((res) => res.json())
      .then((json) => {
        if (json.success && json.settings) {
          setEmailSettings(json.settings);
        }
      })
      .catch((err) => console.error('Failed to load settings:', err));
  }, []);

  // Recalculate KPIs and deterministic findings when filters change
  useEffect(() => {
    const updatedKpis = calculateKPIs(dataset, {
      date: selectedDate,
      channel: selectedChannel,
      category: selectedCategory,
    });
    setKpis(updatedKpis);

    const updatedReport = buildDailyExecutiveReport(dataset, selectedDate);
    setReport(updatedReport);

    const updatedFindings = runDeterministicMultiAgentAnalysis(dataset, selectedDate);
    setFindings(updatedFindings);
  }, [dataset, selectedDate, selectedChannel, selectedCategory]);

  const showNotification = (message: string, type: 'success' | 'info' = 'success') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 4000);
  };

  const handleTimeRangeChange = (preset: 'today' | 'yesterday' | '7d' | '30d' | 'custom') => {
    setTimeRangePreset(preset);
    if (availableDates.length > 0) {
      if (preset === 'today') {
        setSelectedDate(availableDates[availableDates.length - 1]);
        showNotification(`Switched view to Today (${availableDates[availableDates.length - 1]}).`);
      } else if (preset === 'yesterday' && availableDates.length > 1) {
        setSelectedDate(availableDates[availableDates.length - 2]);
        showNotification(`Switched view to Yesterday (${availableDates[availableDates.length - 2]}).`);
      } else if (preset === '7d' || preset === '30d') {
        setSelectedDate(availableDates[availableDates.length - 1]);
        showNotification(`Loaded aggregate rolling multi-day comparison period.`);
      }
    }
  };

  const handleRoleSelect = (role: UserRole) => {
    const profile = MOCK_USERS[role];
    setCurrentUser(profile);
    showNotification(`Switched active persona to ${profile.name} (${profile.role}).`);
  };

  const handleRunAiAnalysis = async () => {
    setIsAnalyzing(true);
    setExecutionTriggerSource('manual');
    setIsAgentExecutionOpen(true);
    showNotification('Supervisor AI Agent coordinating 9 specialist agents across omnichannel datasets...', 'info');

    try {
      const res = await fetch('/api/agents/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ date: selectedDate, useGemini: true }),
      });
      const json = await res.json();
      if (json.success && json.findings) {
        setFindings(json.findings);
        showNotification('Multi-Agent Analysis complete! Root causes and actions refreshed.');
      } else {
        const detFindings = runDeterministicMultiAgentAnalysis(dataset, selectedDate);
        setFindings(detFindings);
      }
    } catch (err) {
      const detFindings = runDeterministicMultiAgentAnalysis(dataset, selectedDate);
      setFindings(detFindings);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleFeedback = async (findingId: string, feedback: 'thumbs_up' | 'thumbs_down', note?: string) => {
    recordAgentFeedback(findingId, feedback, note);
    setFindings((prev) =>
      prev.map((f) => (f.id === findingId ? { ...f, feedback, feedbackNote: note } : f))
    );

    try {
      await fetch('/api/agents/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ findingId, feedback, note }),
      });
    } catch (e) {
      // local feedback recorded
    }
    showNotification(`Feedback recorded (${feedback === 'thumbs_up' ? 'Approved' : 'Disputed'}).`);
  };

  const handleResetData = async () => {
    const defaultData = resetToDefaultDataset();
    setDataset(defaultData);
    setSelectedDate(defaultData.metadata.dateRange.end);
    setSelectedChannel('All');
    setSelectedCategory('All');
    showNotification('Reset successfully to Sleepsia unified dataset.');
  };

  const handleChatSendMessage = async (query: string) => {
    const res = await fetch('/api/agents/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: query, date: selectedDate }),
    });
    const json = await res.json();
    return {
      answer: json.answer || 'No response available.',
      sources: json.sources || ['Internal_Sales', 'Marketplace_Data', 'Shipping_Data'],
    };
  };

  const handleNavigateToTab = (tabId: string) => {
    const tabAliases: Record<string, string> = {
      sales: 'marketplaces',
      marketplace: 'marketplaces',
      inventory: 'stocks',
      inventories: 'stocks',
      stock: 'stocks',
      stocks: 'stocks',
      darkstore: 'stocks',
      darkstores: 'stocks',
      product: 'products',
      ads: 'advertising',
      ad: 'advertising',
      logistics: 'shipping',
      actions: 'insights',
      action: 'insights',
      agent: 'orchestration',
      agents: 'orchestration',
      orchestrator: 'orchestration',
      pipeline: 'orchestration',
      'full-pipeline': 'orchestration',
      flow: 'orchestration',
      graph: 'orchestration',
      logic: 'logic',
      spec: 'logic',
      specs: 'logic',
      formulas: 'logic',
    };
    const targetTab = tabAliases[tabId] || tabId;
    setActiveTab(targetTab);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Critical stock alert count for darkstores tab badge
  const criticalStockAlerts = useMemo(() => {
    return dataset.inventory.filter((i) => (i.availableStock || i.closingStock || 0) < 30).length;
  }, [dataset.inventory]);

  // Full Tab Master List
  const allTabs = [
    { id: 'overview', label: 'Executive Overview', icon: LayoutDashboard },
    { id: 'orchestration', label: 'AI Multi-Agent Pipeline', icon: Cpu, badge: '9 Agents' },
    { id: 'logic', label: 'Analysis Logic & Formulas', icon: Code2, badge: 'Specs' },
    {
      id: 'stocks',
      label: 'Stocks & Darkstores',
      icon: Boxes,
      badge: criticalStockAlerts > 0 ? `${criticalStockAlerts} Alerts` : undefined,
    },
    { id: 'categories', label: 'Category Intelligence', icon: Layers },
    { id: 'marketplaces', label: 'Marketplaces (14)', icon: Layers },
    { id: 'advertising', label: 'Advertising & TACoS', icon: Zap },
    { id: 'products', label: 'Product Intelligence', icon: Package },
    { id: 'competitors', label: 'Competitor Matrix', icon: ShieldAlert },
    { id: 'shipping', label: 'Shipping & Logistics', icon: Truck },
    { id: 'insights', label: 'Root Cause Insights', icon: Sparkles, badge: findings.length },
    { id: 'report', label: 'Daily Briefing Report', icon: FileText },
    { id: 'chat', label: 'Chat BI Assistant', icon: MessageSquare },
    { id: 'settings', label: 'Settings & Schedules', icon: Settings },
  ];

  // Filtered by RBAC permissions
  const visibleTabs = allTabs.filter((t) => currentUser.allowedTabs.includes(t.id));

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans selection:bg-blue-600 selection:text-white">
      {/* Header */}
      <Header
        selectedDate={selectedDate}
        onDateChange={setSelectedDate}
        availableDates={availableDates}
        selectedChannel={selectedChannel}
        onChannelChange={setSelectedChannel}
        availableChannels={availableChannels}
        selectedCategory={selectedCategory}
        onCategoryChange={setSelectedCategory}
        availableCategories={availableCategories}
        onOpenUpload={() => setIsUploadOpen(true)}
        onRunAnalysis={handleRunAiAnalysis}
        onOpenEmailModal={() => setIsEmailModalOpen(true)}
        onResetData={handleResetData}
        isAnalyzing={isAnalyzing}
        activeTab={activeTab}
        currentUser={currentUser}
        onOpenRoleSwitcher={() => setIsRoleSwitcherOpen(true)}
        timeRangePreset={timeRangePreset}
        onTimeRangeChange={handleTimeRangeChange}
        onNavigateToTab={handleNavigateToTab}
        onOpenAgentExecution={() => {
          handleNavigateToTab('orchestration');
        }}
        activeAgentsCount={9}
        activeFindingsCount={findings.length || 24}
      />

      {/* Toast Notification Banner */}
      {notification && (
        <div className="bg-blue-600 text-white text-xs font-semibold px-4 py-2.5 shadow-md flex items-center justify-center gap-2 sticky top-[102px] z-20 transition-all">
          <CheckCircle2 className="w-4 h-4" />
          <span>{notification.message}</span>
        </div>
      )}

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full space-y-6">
        {/* Role Access Banner if permissions are scoped */}
        {currentUser.role !== 'Admin' && currentUser.role !== 'Executive' && (
          <div className="bg-blue-50/70 border border-blue-200 rounded-xl px-4 py-2.5 flex items-center justify-between text-xs text-blue-900">
            <div className="flex items-center gap-2">
              <Shield className="w-4 h-4 text-blue-600" />
              <span>
                Logged in as <strong>{currentUser.name}</strong> ({currentUser.role}). Navigation tabs and capabilities are tailored to your department.
              </span>
            </div>
            <button
              onClick={() => setIsRoleSwitcherOpen(true)}
              className="text-blue-700 font-bold hover:underline"
            >
              Switch Role
            </button>
          </div>
        )}

        {/* Navigation Tabs Bar */}
        <div className="bg-white p-1.5 sm:p-2 rounded-2xl border border-slate-200/90 shadow-xs overflow-x-auto">
          <nav className="flex space-x-1.5 min-w-max">
            {visibleTabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  id={`tab-${tab.id}`}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2.5 px-4 py-2.5 sm:px-5 sm:py-3 rounded-xl text-sm sm:text-[15px] font-bold tracking-tight transition-all select-none ${
                    isActive
                      ? 'bg-blue-600 text-white shadow-sm ring-1 ring-blue-700/30'
                      : 'text-slate-700 hover:text-slate-950 hover:bg-slate-100/90'
                  }`}
                >
                  <Icon className={`w-4 h-4 sm:w-5 sm:h-5 ${isActive ? 'text-white' : 'text-slate-500'}`} />
                  <span className="font-display">{tab.label}</span>
                  {tab.badge !== undefined && (
                    <span
                      className={`text-xs font-black px-2 py-0.5 rounded-full leading-none tracking-normal ${
                        isActive
                          ? 'bg-white text-blue-700 shadow-2xs'
                          : typeof tab.badge === 'string'
                          ? 'bg-blue-100 text-blue-800'
                          : 'bg-rose-100 text-rose-700 border border-rose-200'
                      }`}
                    >
                      {tab.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Tab Views Content */}
        <div>
          {activeTab === 'overview' && (
            <ExecutiveOverview
              kpis={kpis}
              data={dataset}
              findings={findings}
              selectedDate={selectedDate}
              onNavigateToTab={handleNavigateToTab}
              onOpenAgentExecution={() => handleNavigateToTab('orchestration')}
            />
          )}

          {activeTab === 'orchestration' && (
            <MultiAgentOrchestrator
              data={dataset}
              kpis={kpis}
              selectedDate={selectedDate}
              onNavigateToTab={handleNavigateToTab}
              onOpenEmailModal={() => setIsEmailModalOpen(true)}
            />
          )}

          {activeTab === 'logic' && (
            <AgentLogicAnalysisView
              dataset={dataset}
              kpis={kpis}
              selectedDate={selectedDate}
            />
          )}

          {activeTab === 'stocks' && (
            <StockManagement
              data={dataset}
              selectedDate={selectedDate}
              onNavigateToTab={handleNavigateToTab}
              onUpdateInventory={(updatedInventory) => {
                setDataset((prev) => ({
                  ...prev,
                  inventory: updatedInventory,
                }));
              }}
            />
          )}

          {activeTab === 'categories' && (
            <CategoryIntelligence
              kpis={kpis}
              data={dataset}
              selectedDate={selectedDate}
              selectedChannel={selectedChannel}
              selectedCategory={selectedCategory}
              onSelectCategory={setSelectedCategory}
            />
          )}

          {activeTab === 'marketplaces' && (
            <MarketplaceAnalysis data={dataset} selectedDate={selectedDate} />
          )}

          {activeTab === 'advertising' && (
            <AdvertisingAnalysis data={dataset} kpis={kpis} selectedDate={selectedDate} />
          )}

          {activeTab === 'products' && (
            <ProductIntelligence data={dataset} kpis={kpis} selectedDate={selectedDate} />
          )}

          {activeTab === 'competitors' && (
            <CompetitorIntelligence data={dataset} kpis={kpis} selectedDate={selectedDate} />
          )}

          {activeTab === 'shipping' && (
            <ShippingIntelligence
              data={dataset}
              kpis={kpis}
              selectedDate={selectedDate}
              onOpenUpload={() => setIsUploadOpen(true)}
              onDataUpdated={(updatedDataset) => {
                setDataset(updatedDataset);
                const targetDate = updatedDataset.metadata?.dateRange?.end || selectedDate;
                setSelectedDate(targetDate);
                setKpis(calculateKPIs(updatedDataset, { date: targetDate }));
                setFindings(runDeterministicMultiAgentAnalysis(updatedDataset, targetDate));
                setReport(buildDailyExecutiveReport(updatedDataset, targetDate));
                showNotification('Logistics spreadsheet imported and recalculations triggered!', 'success');
              }}
            />
          )}

          {activeTab === 'insights' && (
            <AiInsights
              findings={findings}
              onFeedback={handleFeedback}
              isAnalyzing={isAnalyzing}
              onRerun={handleRunAiAnalysis}
              selectedDate={selectedDate}
            />
          )}

          {activeTab === 'report' && (
            <DailyReportView
              report={report}
              onSendEmail={() => setIsEmailModalOpen(true)}
              selectedDate={selectedDate}
            />
          )}

          {activeTab === 'chat' && (
            <ChatAssistant
              onSendMessage={handleChatSendMessage}
              selectedDate={selectedDate}
            />
          )}

          {activeTab === 'settings' && (
            <SettingsView
              settings={emailSettings}
              onSaveSettings={async (newSettings) => {
                setEmailSettings((prev) => ({ ...prev, ...newSettings }));
                try {
                  const res = await fetch('/api/settings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(newSettings),
                  });
                  const json = await res.json();
                  if (json.success && json.settings) {
                    setEmailSettings(json.settings);
                  }
                } catch (err) {
                  console.error('Failed to sync settings:', err);
                }
                showNotification('Settings saved successfully.');
              }}
              data={dataset}
              onResetData={handleResetData}
            />
          )}
        </div>
      </main>

      {/* Role Switcher RBAC Modal */}
      <RoleSwitcherModal
        isOpen={isRoleSwitcherOpen}
        onClose={() => setIsRoleSwitcherOpen(false)}
        currentUser={currentUser}
        onSelectRole={handleRoleSelect}
      />

      {/* Upload Dataset Modal */}
      <UploadModal
        isOpen={isUploadOpen}
        onClose={() => setIsUploadOpen(false)}
        onUploadSuccess={(metadata, parsedData) => {
          const freshData = parsedData || getActiveDataset();
          setDataset(freshData);
          const targetDate = freshData.metadata?.dateRange?.end || selectedDate;
          setSelectedDate(targetDate);
          const freshKpis = calculateKPIs(freshData, { date: targetDate });
          setKpis(freshKpis);
          const freshFindings = runDeterministicMultiAgentAnalysis(freshData, targetDate);
          setFindings(freshFindings);
          const freshReport = buildDailyExecutiveReport(freshData, targetDate);
          setReport(freshReport);

          showNotification(`Workbook "${metadata?.fileName || 'Spreadsheet'}" ingested! Running 9 AI Supervisor Agents on live data...`);
          setExecutionTriggerSource('upload');
          setIsAgentExecutionOpen(true);
        }}
      />

      {/* Live Agent Execution & Real-Time Telemetry Modal */}
      <AgentExecutionModal
        isOpen={isAgentExecutionOpen}
        onClose={() => setIsAgentExecutionOpen(false)}
        data={dataset}
        kpis={kpis}
        findings={findings}
        selectedDate={selectedDate}
        onNavigateToTab={handleNavigateToTab}
        onOpenEmailModal={() => setIsEmailModalOpen(true)}
        onFeedback={handleFeedback}
        initialTrigger={executionTriggerSource}
      />

      {/* Email Report Dispatch Modal */}
      <EmailModal
        isOpen={isEmailModalOpen}
        onClose={() => {
          setIsEmailModalOpen(false);
          // Refresh settings to update lastSentStatus / timestamp
          fetch('/api/settings')
            .then((res) => res.json())
            .then((json) => {
              if (json.success && json.settings) {
                setEmailSettings(json.settings);
              }
            })
            .catch(() => {});
        }}
        report={report}
        settings={emailSettings}
        selectedDate={selectedDate}
      />
    </div>
  );
}

export default App;
