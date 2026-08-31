import React from 'react';
import {
  Shield,
  UserCheck,
  Check,
  Lock,
  Layers,
  Sparkles,
  ArrowRight,
  X,
  Briefcase,
  Key,
} from 'lucide-react';
import { UserRole, UserProfile, MOCK_USERS } from '../types/rbac';

interface RoleSwitcherModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentUser: UserProfile;
  onSelectRole: (role: UserRole) => void;
}

export const RoleSwitcherModal: React.FC<RoleSwitcherModalProps> = ({
  isOpen,
  onClose,
  currentUser,
  onSelectRole,
}) => {
  if (!isOpen) return null;

  const rolesList: UserRole[] = [
    'Admin',
    'Executive',
    'Marketplace Manager',
    'Advertising Manager',
    'Inventory/Stock Manager',
    'Product Manager',
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in duration-200">
      <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-3xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="px-6 py-5 border-b border-slate-100 flex items-center justify-between bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-600/30 border border-blue-400/40 flex items-center justify-center text-blue-400">
              <Shield className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold">Role-Based Access Control (RBAC)</h3>
              <p className="text-xs text-slate-300">
                Switch user persona to test role-aware navigation, permission guards, and tailored dashboards.
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-700/60 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Current Active Persona Banner */}
        <div className="px-6 py-3 bg-blue-50/70 border-b border-blue-100 flex items-center justify-between text-xs">
          <div className="flex items-center gap-2.5">
            <span className="text-slate-500 font-medium">Currently Logged In:</span>
            <span className="font-bold text-blue-900">{currentUser.name}</span>
            <span className="px-2 py-0.5 rounded-full bg-blue-600 text-white font-bold text-[10px]">
              {currentUser.role}
            </span>
          </div>
          <span className="text-slate-500">{currentUser.department}</span>
        </div>

        {/* Roles List */}
        <div className="p-6 overflow-y-auto space-y-3.5 flex-1">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
            {rolesList.map((r) => {
              const profile = MOCK_USERS[r];
              const isSelected = currentUser.role === r;

              return (
                <div
                  key={r}
                  onClick={() => {
                    onSelectRole(r);
                    onClose();
                  }}
                  className={`p-4 rounded-xl border transition-all cursor-pointer flex flex-col justify-between ${
                    isSelected
                      ? 'bg-blue-50/60 border-blue-500 ring-2 ring-blue-500/20 shadow-xs'
                      : 'bg-white border-slate-200 hover:border-slate-300 hover:bg-slate-50/70'
                  }`}
                >
                  <div>
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center gap-2.5">
                        <img
                          src={profile.avatar}
                          alt={profile.name}
                          className="w-9 h-9 rounded-full object-cover border border-slate-200"
                        />
                        <div>
                          <h4 className="text-xs font-bold text-slate-900">{profile.name}</h4>
                          <span className="text-[11px] font-semibold text-blue-700">{profile.role}</span>
                        </div>
                      </div>
                      {isSelected ? (
                        <span className="w-5 h-5 rounded-full bg-blue-600 text-white flex items-center justify-center text-[10px] font-bold">
                          <Check className="w-3.5 h-3.5" />
                        </span>
                      ) : (
                        <span className="text-[10px] font-bold text-slate-400 hover:text-blue-600 flex items-center gap-1">
                          Switch <ArrowRight className="w-3 h-3" />
                        </span>
                      )}
                    </div>

                    <p className="text-[11px] text-slate-600 mb-3 leading-relaxed">
                      {profile.department}
                    </p>

                    {/* Permissions tags */}
                    <div className="flex flex-wrap gap-1 mb-2">
                      {profile.allowedTabs.slice(0, 4).map((tab) => (
                        <span
                          key={tab}
                          className="px-1.5 py-0.5 rounded text-[9px] font-semibold bg-slate-100 text-slate-700 uppercase"
                        >
                          {tab}
                        </span>
                      ))}
                      {profile.allowedTabs.length > 4 && (
                        <span className="px-1.5 py-0.5 rounded text-[9px] font-semibold bg-slate-100 text-slate-500">
                          +{profile.allowedTabs.length - 4} more
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[10px] text-slate-400 font-mono">
                    <span>{profile.email}</span>
                    <span className="text-slate-500 font-sans">Pass: ••••••••</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-xs text-slate-500">
          <div className="flex items-center gap-1.5">
            <Key className="w-3.5 h-3.5 text-slate-400" />
            <span>Mock enterprise credentials pre-loaded for instant role verification.</span>
          </div>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg font-bold text-xs transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
