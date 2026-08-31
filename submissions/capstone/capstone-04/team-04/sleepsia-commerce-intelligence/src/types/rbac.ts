/**
 * Role-Based Access Control (RBAC) System
 * Defines enterprise roles, permissions, user profiles, and access control matrices.
 */

export type UserRole =
  | 'Admin'
  | 'Executive'
  | 'Marketplace Manager'
  | 'Advertising Manager'
  | 'Inventory/Stock Manager'
  | 'Product Manager';

export interface UserProfile {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  avatar: string;
  department: string;
  allowedTabs: string[];
  permissions: {
    canViewExecutiveDashboard: boolean;
    canViewMarketplaceData: boolean;
    canViewAdvertising: boolean;
    canViewInventoryAndShipping: boolean;
    canViewProductAnalytics: boolean;
    canViewCompetitorMatrix: boolean;
    canRunMultiAgentAnalysis: boolean;
    canSendExecutiveEmails: boolean;
    canModifySettingsAndSchedules: boolean;
    canUploadDatasets: boolean;
    canExecuteActionRecommendations: boolean;
  };
}

export const MOCK_USERS: Record<UserRole, UserProfile> = {
  Admin: {
    id: 'usr-admin-01',
    name: 'Aarav Sharma',
    email: 'aarav.sharma@sleepsia.com',
    role: 'Admin',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80',
    department: 'Commerce Operations & Platform Engineering',
    allowedTabs: [
      'overview',
      'orchestration',
      'orchestrator',
      'logic',
      'stocks',
      'categories',
      'marketplaces',
      'advertising',
      'products',
      'competitors',
      'shipping',
      'insights',
      'report',
      'chat',
      'settings',
    ],
    permissions: {
      canViewExecutiveDashboard: true,
      canViewMarketplaceData: true,
      canViewAdvertising: true,
      canViewInventoryAndShipping: true,
      canViewProductAnalytics: true,
      canViewCompetitorMatrix: true,
      canRunMultiAgentAnalysis: true,
      canSendExecutiveEmails: true,
      canModifySettingsAndSchedules: true,
      canUploadDatasets: true,
      canExecuteActionRecommendations: true,
    },
  },
  Executive: {
    id: 'usr-exec-02',
    name: 'Dheeraj Kapoor',
    email: 'dheeraj.kapoor@sleepsia.com',
    role: 'Executive',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80',
    department: 'Office of the CEO / Strategic Finance',
    allowedTabs: [
      'overview',
      'orchestration',
      'orchestrator',
      'stocks',
      'categories',
      'marketplaces',
      'shipping',
      'insights',
      'report',
      'chat',
    ],
    permissions: {
      canViewExecutiveDashboard: true,
      canViewMarketplaceData: true,
      canViewAdvertising: true,
      canViewInventoryAndShipping: true,
      canViewProductAnalytics: true,
      canViewCompetitorMatrix: true,
      canRunMultiAgentAnalysis: true,
      canSendExecutiveEmails: true,
      canModifySettingsAndSchedules: false,
      canUploadDatasets: false,
      canExecuteActionRecommendations: true,
    },
  },
  'Marketplace Manager': {
    id: 'usr-mkt-03',
    name: 'Priya Nair',
    email: 'priya.nair@sleepsia.com',
    role: 'Marketplace Manager',
    avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=100&auto=format&fit=crop&q=80',
    department: 'Omnichannel & Quick Commerce Growth',
    allowedTabs: [
      'overview',
      'orchestration',
      'orchestrator',
      'stocks',
      'categories',
      'marketplaces',
      'products',
      'competitors',
      'shipping',
      'insights',
      'chat',
    ],
    permissions: {
      canViewExecutiveDashboard: true,
      canViewMarketplaceData: true,
      canViewAdvertising: false,
      canViewInventoryAndShipping: true,
      canViewProductAnalytics: true,
      canViewCompetitorMatrix: true,
      canRunMultiAgentAnalysis: true,
      canSendExecutiveEmails: false,
      canModifySettingsAndSchedules: false,
      canUploadDatasets: true,
      canExecuteActionRecommendations: true,
    },
  },
  'Advertising Manager': {
    id: 'usr-ads-04',
    name: 'Rohan Verma',
    email: 'rohan.verma@sleepsia.com',
    role: 'Advertising Manager',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&auto=format&fit=crop&q=80',
    department: 'Performance Marketing & PPC Optimization',
    allowedTabs: [
      'overview',
      'orchestration',
      'orchestrator',
      'advertising',
      'products',
      'competitors',
      'insights',
      'chat',
    ],
    permissions: {
      canViewExecutiveDashboard: true,
      canViewMarketplaceData: false,
      canViewAdvertising: true,
      canViewInventoryAndShipping: false,
      canViewProductAnalytics: true,
      canViewCompetitorMatrix: true,
      canRunMultiAgentAnalysis: true,
      canSendExecutiveEmails: false,
      canModifySettingsAndSchedules: false,
      canUploadDatasets: true,
      canExecuteActionRecommendations: true,
    },
  },
  'Inventory/Stock Manager': {
    id: 'usr-inv-05',
    name: 'Vikram Malhotra',
    email: 'vikram.malhotra@sleepsia.com',
    role: 'Inventory/Stock Manager',
    avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&auto=format&fit=crop&q=80',
    department: 'Supply Chain, Warehousing & Fulfillment',
    allowedTabs: [
      'overview',
      'orchestration',
      'orchestrator',
      'stocks',
      'shipping',
      'products',
      'insights',
      'chat',
    ],
    permissions: {
      canViewExecutiveDashboard: true,
      canViewMarketplaceData: false,
      canViewAdvertising: false,
      canViewInventoryAndShipping: true,
      canViewProductAnalytics: true,
      canViewCompetitorMatrix: false,
      canRunMultiAgentAnalysis: true,
      canSendExecutiveEmails: false,
      canModifySettingsAndSchedules: false,
      canUploadDatasets: true,
      canExecuteActionRecommendations: true,
    },
  },
  'Product Manager': {
    id: 'usr-prod-06',
    name: 'Ananya Sen',
    email: 'ananya.sen@sleepsia.com',
    role: 'Product Manager',
    avatar: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=100&auto=format&fit=crop&q=80',
    department: 'Category Innovation & Product Lifecycle',
    allowedTabs: [
      'overview',
      'orchestration',
      'orchestrator',
      'categories',
      'products',
      'competitors',
      'insights',
      'chat',
    ],
    permissions: {
      canViewExecutiveDashboard: true,
      canViewMarketplaceData: false,
      canViewAdvertising: false,
      canViewInventoryAndShipping: false,
      canViewProductAnalytics: true,
      canViewCompetitorMatrix: true,
      canRunMultiAgentAnalysis: true,
      canSendExecutiveEmails: false,
      canModifySettingsAndSchedules: false,
      canUploadDatasets: true,
      canExecuteActionRecommendations: true,
    },
  },
};
