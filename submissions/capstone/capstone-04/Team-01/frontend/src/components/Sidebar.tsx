import React from 'react';
import {
  LayoutDashboard,
  TrendingUp,
  Store,
  DollarSign,
  Search,
  Users,
  Sparkles,
  MessageSquareText,
  BadgePercent,
  RotateCcw,
  Building2,
  CalendarClock,
  Box,
  AlertTriangle,
  Zap,
  Bot,
  FileText,
  Settings,
  ShieldCheck,
  BotMessageSquare,
  Lock
} from 'lucide-react';
import { UserRole, ViewMode } from '../types';
import { useData } from '../context/DataContext';

export type ViewId = ViewMode;

interface SidebarProps {
  activeView: ViewMode;
  onSelectView: (view: ViewMode) => void;
  onOpenAIAssistant?: () => void;
  currentUserRole: UserRole;
  activeAnomaliesCount: number;
  pendingActionsCount?: number;
}

interface NavItem {
  id: ViewMode;
  label: string;
  icon: any;
  badge?: string;
  alertCount?: number;
  isUrgent?: boolean;
  isAction?: boolean;
  highlight?: string;
}

interface NavSection {
  title: string;
  items: NavItem[];
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeView,
  onSelectView,
  onOpenAIAssistant,
  currentUserRole,
  activeAnomaliesCount,
  pendingActionsCount = 4
}) => {
  const { currentUser, skus } = useData();

  const navSections: NavSection[] = [
    {
      title: 'CORE WORKSPACES',
      items: [
        {
          id: 'command-center' as ViewMode,
          label: 'Command Center',
          icon: LayoutDashboard,
          badge: 'Executive & Sales'
        },
        {
          id: 'digital-shelf' as ViewMode,
          label: 'Digital Shelf & MAP',
          icon: DollarSign,
          badge: 'Price & VOC'
        },
        {
          id: 'supply-chain' as ViewMode,
          label: 'Supply Chain & Dark Stores',
          icon: Building2,
          badge: 'Quick Commerce'
        },
        {
          id: 'autonomous-ai' as ViewMode,
          label: 'Autonomous AI & Playbooks',
          icon: Zap,
          alertCount: activeAnomaliesCount,
          isUrgent: activeAnomaliesCount > 0
        },
        {
          id: 'dataset-sync' as ViewMode,
          label: 'Dataset & Live Sync',
          icon: Settings,
          badge: `${skus.length} SKUs`
        }
      ]
    }
  ];

  // Role-Based Filtering
  const isViewAllowed = (viewId: ViewMode): boolean => {
    if (!currentUser) return true;
    return currentUser.allowedViews.includes(viewId);
  };

  // Filter sections that have at least one allowed item
  const filteredNavSections = navSections
    .map((section) => ({
      ...section,
      items: section.items.filter((item) => isViewAllowed(item.id))
    }))
    .filter((section) => section.items.length > 0);

  return (
    <aside id="main-sidebar" className="w-64 bg-white text-slate-800 flex flex-col shrink-0 border-r border-slate-200 select-none h-screen sticky top-0">
      {/* Brand Header */}
      <div className="p-4 border-b border-slate-200 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-blue-600 to-indigo-700 flex items-center justify-center text-white font-black text-sm shadow-xs tracking-tight">
            AS
          </div>
          <div>
            <div className="flex items-center space-x-1.5">
              <span className="text-sm font-bold tracking-tight text-slate-900">Agile Solutions</span>
              <span className="text-[10px] bg-blue-100 text-blue-700 font-bold px-1.5 py-0.5 rounded border border-blue-200">
                TOWER
              </span>
            </div>
            <p className="text-[10px] text-slate-500 font-medium">Autonomous Control Tower</p>
          </div>
        </div>
      </div>

      {/* Navigation Sections */}
      <div className="flex-1 overflow-y-auto px-3 py-3 space-y-4 custom-scrollbar">
        {filteredNavSections.map((section) => (
          <div key={section.title} className="space-y-0.5">
            <div className="px-3 text-[10px] uppercase tracking-widest text-slate-400 font-bold mb-1">
              {section.title}
            </div>
            {section.items.map((item) => {
              const Icon = item.icon;
              const isActive = activeView === item.id;

              return (
                <button
                  key={item.id}
                  id={`nav-btn-${item.id}`}
                  onClick={() => onSelectView(item.id)}
                  className={`w-full flex items-center justify-between px-3 py-2 text-xs font-medium rounded-lg transition-all text-left ${
                    isActive
                      ? 'bg-blue-50 text-blue-700 border border-blue-200/80 font-bold shadow-2xs'
                      : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                  }`}
                >
                  <div className="flex items-center space-x-2.5 truncate">
                    <Icon
                      className={`w-4 h-4 shrink-0 ${
                        isActive
                          ? 'text-blue-700'
                          : item.isUrgent
                          ? 'text-red-600'
                          : item.isAction
                          ? 'text-amber-600'
                          : 'text-slate-400'
                      }`}
                    />
                    <span className="truncate">{item.label}</span>
                  </div>

                  <div className="flex items-center space-x-1 shrink-0 ml-2">
                    {item.badge && (
                      <span className={`text-[10px] px-1.5 py-0.5 rounded font-semibold ${
                        isActive ? 'bg-blue-100 text-blue-800' : 'bg-slate-100 text-slate-600'
                      }`}>
                        {item.badge}
                      </span>
                    )}
                    {item.alertCount && item.alertCount > 0 ? (
                      <span className={`text-[10px] px-1.5 py-0.2 rounded-full font-bold ${
                        item.isUrgent
                          ? 'bg-red-600 text-white animate-pulse'
                          : 'bg-amber-100 text-amber-800 border border-amber-200'
                      }`}>
                        {item.alertCount}
                      </span>
                    ) : null}
                  </div>
                </button>
              );
            })}
          </div>
        ))}

        {currentUser?.role !== 'Owner' && (
          <div className="p-2.5 bg-amber-50/80 border border-amber-200/80 rounded-lg text-[11px] text-amber-800 flex items-start space-x-2">
            <Lock className="w-3.5 h-3.5 text-amber-600 shrink-0 mt-0.5" />
            <span>
              <strong>RBAC Active:</strong> Options restricted for <em>{currentUser.role}</em>. Non-authorized views removed.
            </span>
          </div>
        )}
      </div>

      {/* User Role & Status Footer */}
      <div className="p-3 bg-slate-50 border-t border-slate-200 space-y-2">
        <div className="flex items-center justify-between px-2">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 rounded-full bg-emerald-500 ring-2 ring-emerald-500/20"></div>
            <span className="text-[11px] text-slate-600 font-semibold">{skus.length} SKUs Synced</span>
          </div>
          <span className="text-[10px] text-slate-400 font-mono">Dynamic DB</span>
        </div>

        <div className="p-2.5 bg-white rounded-lg border border-slate-200 flex items-center justify-between shadow-2xs">
          <div className="flex items-center gap-2.5 truncate">
            <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-600 shrink-0 text-white text-[10px] font-bold flex items-center justify-center">
              {currentUser?.avatar || 'AO'}
            </div>
            <div className="truncate">
              <div className="flex items-center space-x-1.5">
                <span className="text-xs font-bold text-slate-900 truncate">
                  {currentUser?.name.split(' (')[0] || 'Agile Owner'}
                </span>
                <span className="text-[9px] bg-emerald-100 text-emerald-800 font-semibold px-1 py-0.2 rounded border border-emerald-200 shrink-0">
                  {currentUser?.role || currentUserRole}
                </span>
              </div>
              <p className="text-[10px] text-slate-500 truncate font-mono">
                {currentUser?.email || 'owner@agileventures.net'}
              </p>
            </div>
          </div>
          <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
        </div>
      </div>
    </aside>
  );
};
