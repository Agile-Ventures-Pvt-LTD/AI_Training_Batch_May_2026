# Platform Skills & Features

## Overview
This document outlines all available skills, features, and functional modules in the Django Agile Tower platform. Each skill represents a distinct operational capability or analytical module within the e-commerce intelligence and automation system.

---

## Core Dashboard Skills

### 1. **Command Center**
**Module**: `CommandCenterView`  
**Type**: Executive Command Dashboard  
**Access**: Owner, Super Admin, Operations Manager

#### Description
Central hub for real-time operational monitoring and autonomous action management. Displays live marketplace metrics, active anomalies, and queued autonomous actions.

#### Key Features
- Real-time marketplace status overview
- Active anomaly count display
- Queued actions visualization
- Quick-action execution interface
- Executive KPI dashboard
- Marketplace channel selector
- 30-day date range filtering

#### Capabilities
- Monitor 100+ SKUs across 6+ marketplaces
- View active critical anomalies
- Execute autonomous actions (pricing, inventory, promotions)
- Track action queue status
- Access quick links to revenue impact metrics

#### Data Metrics
- Total Gross Revenue (30-day)
- Channel Revenue Distribution
- Active Anomalies Count
- In-Transit Stock Transfers
- Action Queue Depth

---

### 2. **Digital Shelf Management**
**Module**: `DigitalShelfView`  
**Type**: Marketplace Listing Optimization  
**Access**: Owner, Super Admin, Marketing Manager

#### Description
Optimize product listings across multiple marketplaces with AI-driven content recommendations and competitive pricing intelligence.

#### Key Features
- Multi-marketplace SKU display (Amazon, Flipkart, Myntra, Blinkit, Zepto)
- Dynamic title and bullet point optimization
- Search keyword recommendations
- Buy Box win rate tracking
- Competitor price comparison
- A+ content recommendations
- MAP compliance checking

#### Capabilities
- Search ranking optimization
- Listing conversion rate improvement
- A10 algorithm compliance for Amazon
- Flipkart PLA & sponsored rank optimization
- Blinkit quick commerce pod readiness
- Real-time competitor monitoring

#### Supported Marketplaces
- Amazon India
- Flipkart
- Myntra
- Blinkit
- Zepto
- Swiggy Instamart

---

### 3. **Supply Chain Management**
**Module**: `SupplyChainView`  
**Type**: Logistics & Inventory Operations  
**Access**: Owner, Super Admin, Operations Manager, Logistics Coordinator

#### Description
End-to-end supply chain visibility from Mother Hub reserves to Dark Store pods with real-time transfer tracking.

#### Key Features
- Mother Hub inventory overview
- Dark Store stock status monitoring
- Batch and expiry date tracking
- Transfer request initiation
- Courier partner integration (Shadowfax, etc.)
- Transit time estimation
- Lead time calculation (intra-city 3.5 hours)

#### Capabilities
- Initiate stock transfers between hubs
- Track in-transit shipments
- Monitor FEFO (First Expired, First Out) compliance
- Prevent dark store stockouts (OOS)
- Optimize transfer batching
- Manage multiple warehouse locations

#### Mother Hub Regions
- Bengaluru Central (Nelamangala): 14,820+ units capacity
- Mumbai West (Bhiwandi): 18,450+ units capacity
- NCR North (Manesar): 12,900+ units capacity

#### Dark Store Pod Categories
- Blinkit pods
- Zepto pods
- Swiggy Instamart pods
- Local convenience stores

---

### 4. **Autonomous AI Control Panel**
**Module**: `AutonomousAIView`  
**Type**: AI-Powered Intelligence Hub  
**Access**: Owner, Super Admin

#### Description
Central command for autonomous AI decision-making, action approval, and safety guardrail configuration.

#### Key Features
- Autonomous action queue with AI recommendations
- Action approval/rejection interface
- Safety guardrail configuration
- Revenue impact pre-calculation
- Confidence scoring for recommendations
- Action history and telemetry
- Marketplace connector status

#### Capabilities
- Review AI-generated action recommendations
- Approve/reject autonomous actions before execution
- Monitor action execution success rates
- Adjust safety thresholds
- View revenue recovery tracking
- Configure AI behavior parameters

#### Safety Features
- Pre-execution revenue impact simulation
- Guardrail engine verification
- Maximum action size limits
- Hourly action frequency caps
- Marketplace-specific validation rules

---

### 5. **Autonomous Actions**
**Module**: `AutonomousActionsView`  
**Type**: Marketplace Automation  
**Access**: Owner, Super Admin, Operations Manager

#### Description
Execute and manage autonomous marketplace operations including dynamic pricing, promotions, and inventory adjustments.

#### Key Features
- Autonomous action execution interface
- Channel-specific routing (Amazon, Flipkart, Blinkit)
- Action type templates
- Execution logging and tracking
- Revenue impact measurement
- Real-time execution status
- Rollback capability

#### Supported Actions
- Dynamic pricing updates
- Coupon/promotion deployment
- Buy Box optimization
- Inventory rebalancing
- Stock visibility adjustments
- Advertising bid management
- Search term expansion

#### Execution Channels
- Amazon SP-API
- Flipkart Seller API
- Blinkit Marketplace API
- Zepto Partner Integration
- Direct API connectors

---

## Intelligence & Analytics Skills

### 6. **Alerts & Anomalies Detection**
**Module**: `AlertsAnomaliesView`  
**Type**: Real-Time Alerting  
**Access**: All Roles

#### Description
Real-time detection and alerting for operational anomalies including stockouts, pricing issues, sales velocity drops, and competitive threats.

#### Key Features
- Real-time anomaly detection across all SKUs
- Critical alerts dashboard
- Anomaly root cause analysis
- Supply chain impact assessment
- Financial impact quantification
- Recommended resolution playbooks
- Alert acknowledgment and resolution tracking

#### Anomaly Types Monitored
- **Stock-Outs**: Dark store OOS events with duration tracking
- **Sales Velocity Drops**: Unexpected sales decline detection
- **Pricing Anomalies**: MAP breach detection and competitor pricing squeezes
- **Inventory Imbalance**: Uneven distribution across dark stores
- **Quality Issues**: Product rating/review sentiment drops
- **Competitive Threats**: Competitor promotions and pricing moves
- **Logistics Delays**: Transfer delays and failed shipments

#### Response Integration
- Email notifications to stakeholders
- In-app alert display
- AI root cause analysis triggering
- Automated action recommendations
- Escalation based on severity

---

### 7. **Executive Reports**
**Module**: `ExecutiveReportsView`  
**Type**: Business Intelligence Reporting  
**Access**: Owner, Super Admin, Analyst

#### Description
Comprehensive executive reporting with multi-dimensional analysis and send capabilities.

#### Key Features
- Weekly Business Review (WBR) generation
- Channel performance breakdown
- Anomaly summary reporting
- Email distribution and scheduling
- Report template management
- Historical report archival
- Export to PDF/Excel

#### Report Types
- **Weekly Business Review (WBR)**
  - Revenue performance vs targets
  - Channel-wise breakdown
  - Anomaly summary with root causes
  - Action completion status
  
- **Live Anomaly & Supply Chain Briefing**
  - Current operational status
  - Mother Hub reserve levels
  - Dark store stockout summary
  - Recommended actions

- **Sales Intelligence Report**
  - SKU performance metrics
  - Sales trend analysis
  - Competitive positioning
  - Customer segment analysis

#### Distribution Options
- Email dispatch (immediate or scheduled)
- In-platform dashboard view
- PDF download
- Excel export
- Slack/Teams integration (future)

---

### 8. **Advertising ROAS Analysis**
**Module**: `AdvertisingRoasView`  
**Type**: Ad Performance Analytics  
**Access**: Owner, Super Admin, Marketing Manager

#### Description
Comprehensive advertising ROI and ROAS analysis across sponsored and organic channels.

#### Key Features
- Blended ROAS calculation (Target: 3.80x)
- Channel-wise ROAS breakdown
- TACoS (Total Advertising Cost of Sales) tracking
- Ad spend efficiency metrics
- Bid optimization recommendations
- Campaign performance comparison
- Budget allocation optimization

#### Metrics Tracked
- **Return on Ad Spend (ROAS)**: 4.22x (blended current)
- **Total Advertising Cost of Sales (TACoS)**: 23.7% (target <25%)
- **Ad Spend**: ₹18.58L (weekly average)
- **Advertising Efficiency**: Cost per acquisition
- **Channel Attribution**: Multi-touch attribution model

#### Channels Analyzed
- Amazon Sponsored Products (ASP)
- Flipkart Smart Ads
- Blinkit Promoted Listings
- Zepto Brand Discovery
- External ad networks (Google Ads, Facebook)

---

### 9. **Competitor Watch Intelligence**
**Module**: `CompetitorWatchView`  
**Type**: Competitive Intelligence  
**Access**: Owner, Super Admin, Analyst

#### Description
Real-time competitor monitoring and pricing intelligence across all marketplaces.

#### Key Features
- Competitor price tracking
- Promotional monitoring
- Buy Box possession tracking
- Search ranking monitoring
- Competitor inventory estimation
- Pricing elasticity analysis
- Market share estimation

#### Monitored Competitors
- SleepSupport (Sleepsia pillow competitor)
- Regional and category-specific competitors
- Direct e-commerce sellers
- Private label alternatives

#### Intelligence Outputs
- Price differential alerts
- Promotional threat detection
- Market positioning reports
- Recommended counter-actions
- Competitive advantage scoring

---

### 10. **Content Studio**
**Module**: `ContentStudioView`  
**Type**: Content Creation & Optimization  
**Access**: Owner, Super Admin, Content Manager

#### Description
AI-powered content creation studio for generating optimized product listings, A+ content, and marketing copy.

#### Key Features
- AI title generation (marketplace-optimized)
- Bullet point creation (5-point format)
- Search keyword recommendations
- A+ content design recommendations
- Before/After narrative generation
- Ingredient highlight copywriting
- Endorsement template creation

#### Content Types Supported
- **Listings**
  - Amazon A10-optimized titles
  - Flipkart algorithm-friendly content
  - Blinkit pod-optimized descriptions
  - Myntra aesthetic-aligned copy

- **A+ Content**
  - Tri-fold impact modules
  - Ingredient breakdown sections
  - Step-by-step regimen guides
  - Dermatologist endorsement layouts

- **Marketing Copy**
  - Product benefit statements
  - Unique selling proposition (USP) articulation
  - Social proof generation
  - Call-to-action copy

#### AI Optimization Engine
- Marketplace algorithm compliance
- Conversion rate optimization
- SEO keyword density optimization
- Semantic relevance scoring
- Readability analysis

---

## Data & Integration Skills

### 11. **Dataset Sync**
**Module**: `DatasetSyncView`  
**Type**: Data Integration & Synchronization  
**Access**: Owner, Super Admin, Operations Manager

#### Description
Bidirectional synchronization between the platform and Google Sheets for SKU master data, inventory, and operational updates.

#### Key Features
- Google Sheets URL integration
- XLSX/CSV import/export
- Real-time data sync
- Webhook-based push updates
- Google Apps Script integration
- Sheet tab routing (SKU_Master, Inventory, etc.)
- Data validation and transformation
- Batch update processing

#### Data Sources
- Google Sheets (primary)
- CSV files (fallback)
- XLSX workbooks
- Direct API feeds

#### Supported Sheets Tabs
- **1_SKU_Master**: Core SKU definitions
- **2_Inventory**: Mother Hub and dark store inventory
- **3_Pricing**: Marketplace pricing and MAP rules
- **4_Competitors**: Competitor pricing data
- **5_Promotions**: Active promotions and discounts

#### Synchronization Options
- **Pull**: Fetch latest data from Google Sheets
- **Push**: Send updates via webhook
- **Sync**: Bidirectional real-time synchronization

---

### 12. **Email Dispatch & Scheduling**
**Module**: `EmailDispatchModal`, Email Services  
**Type**: Communication Automation  
**Access**: All Roles (with approval gates)

#### Description
Automated email dispatch for reports, alerts, and operational notifications with scheduling capabilities.

#### Key Features
- Live email sending with rich HTML formatting
- Email scheduling (daily, weekly, bi-weekly)
- Template-based formatting
- Multi-recipient support
- Delivery status tracking
- SMTP configuration management
- Email history archive

#### Email Types
- **Executive Reports**
  - Weekly Business Review (WBR)
  - Live anomaly briefings
  - Sales intelligence reports

- **Operational Alerts**
  - Stock transfer notifications
  - Anomaly alerts
  - Action execution confirmations

- **Scheduled Reports**
  - Monday morning WBR
  - Weekly performance summary
  - End-of-month financial recap

#### Email Features
- HTML/plain text rendering
- Embedded links and CTAs
- Markdown formatting support
- Recipient email personalization
- Carbon copy (CC/BCC) support
- Delivery confirmation tracking

#### Status Tracking
- Delivered: Email sent successfully
- Pending: Awaiting delivery
- Failed: Delivery failed (with retry)

---

### 13. **Stock Transfer Management**
**Module**: `StockTransferModal`, Transfer Services  
**Type**: Logistics Operations  
**Access**: Owner, Super Admin, Operations Manager, Logistics Coordinator

#### Description
Orchestrate inventory transfers between Mother Hubs and Dark Store pods with real-time tracking.

#### Key Features
- Transfer request creation interface
- Mother Hub selection and stock verification
- Dark Store pod targeting
- Priority-based routing (Normal/High/Critical)
- Courier partner selection
- Tracking number generation
- Real-time transit status updates
- Estimated delivery time calculation

#### Transfer Parameters
- **Source**: Mother Hub selection
- **Destination**: Dark Store pod selection
- **SKU**: Product selection with batch details
- **Units**: Quantity to transfer
- **Priority**: Normal, High, Critical
- **Courier**: Shadowfax, other logistics partners

#### Courier Integration
- Shadowfax Quick-Commerce Express (primary)
- Intra-city estimated lead time: 3.5 hours
- Real-time tracking integration
- Delivery confirmation

#### Transfer Status Lifecycle
1. Pending (Initial state)
2. In Transit (Picked and dispatched)
3. Delivered (Successfully received)
4. Failed (Delivery failed, requires retry)

---

### 14. **Dark Store Shortage Management**
**Module**: `DarkStoreShortageModal`  
**Type**: Emergency Inventory Response  
**Access**: Owner, Super Admin, Operations Manager

#### Description
Emergency response module for rapid dark store stockout resolution with pre-configured transfer recommendations.

#### Key Features
- Dark store shortage detection
- Affected pod inventory status
- Multi-pod batch transfers
- One-click dispatch recommendations
- Priority escalation
- Estimated resolution timeline
- Revenue impact calculator

#### Shortage Resolution Workflow
1. Detect dark store OOS condition
2. Calculate deficit quantity
3. Identify optimal Mother Hub
4. Recommend transfer quantity (130-150% of deficit)
5. Execute transfer dispatch
6. Track resolution status

#### Monitoring Thresholds
- Critical: 0 units
- Low: <10 units
- Warning: <20 units

---

## SKU & Product Skills

### 15. **SKU 360 View**
**Module**: `Sku360View`  
**Type**: Product Intelligence Dashboard  
**Access**: All Roles

#### Description
Comprehensive 360-degree product view with multi-dimensional analysis and recommendations.

#### Key Features
- Single SKU performance dashboard
- Channel-wise sales breakdown
- Pricing analysis across marketplaces
- Review and rating tracking
- Inventory distribution heatmap
- Competitor comparison
- Trend analysis (7-day, 30-day)
- Content optimization opportunities
- Quick action access

#### Data Dimensions
- **Sales Performance**: Revenue, units sold, conversion rate
- **Pricing**: Current price, competitor pricing, MAP compliance
- **Inventory**: Dark store distribution, Mother Hub reserves, turnover rate
- **Reviews**: Rating, review count, sentiment analysis
- **Advertising**: ROAS, ad spend, keyword performance

#### Quick Actions Available
- Edit listing (launch Content Studio)
- Transfer stock (launch Stock Transfer)
- Adjust pricing
- Send promotional email
- View competitor data

---

## Supply Chain & Logistics Skills

### 16. **Dark Stores & Supply Chain**
**Module**: `DarkStoresSupplyChainView`  
**Type**: Quick Commerce Operations  
**Access**: Owner, Super Admin, Operations Manager, Logistics Coordinator

#### Description
Specialized view for quick commerce dark store network management and supply chain optimization.

#### Key Features
- Dark store pod inventory visualization
- Multi-region dark store dashboard
- OOS incident tracking and resolution
- Pod-level replenishment recommendations
- Supply chain health metrics
- Logistics partner performance
- Demand surge detection and response
- Micro-buffer optimization

#### Dark Store Metrics
- Total pods active: 24 (example)
- Optimal stock pods: 20
- Low stock pods: 4
- OOS pods (critical): 1
- Rebalancing efficiency: 95.2%

#### Regional Pod Coverage
- **Bengaluru**: 8 pods (Blinkit, Zepto mix)
- **Mumbai**: 6 pods
- **Delhi NCR**: 5 pods
- **Hyderabad**: 3 pods
- **Pune**: 2 pods

#### Supply Chain Operations
- Real-time pod telemetry
- Demand surge detection
- Automated replenishment triggers
- Multi-pod coordinated transfers
- Logistics capacity planning

---

### 17. **Perishables & Expiry Management**
**Module**: `PerishablesExpiryView`  
**Type**: Inventory Quality Assurance  
**Access**: Owner, Super Admin, Operations Manager

#### Description
Specialized management for perishable inventory with FEFO (First Expired, First Out) compliance and expiry tracking.

#### Key Features
- Batch-level expiry date tracking
- FEFO compliance monitoring
- Low shelf-life alert system
- Write-off prevention strategies
- Rotation recommendations
- Markdown opportunity identification
- Inventory aging analysis

#### Key Metrics
- **Shelf Life Remaining**: Days until expiry
- **Inventory Age**: Days in warehouse
- **Velocity**: Units sold per day
- **Risk Level**: Green/Yellow/Red status

#### Compliance Standards
- Minimum 20-month shelf life (typical)
- FEFO rotation enforcement
- Batch traceability
- Regulatory compliance tracking
- Temperature/humidity monitoring alerts

---

## Financial & Business Skills

### 18. **Sales Intelligence**
**Module**: `SalesIntelligenceView`  
**Type**: Revenue & Performance Analytics  
**Access**: All Roles

#### Description
Comprehensive sales performance analysis with forecasting and trend analysis capabilities.

#### Key Features
- Revenue performance vs targets
- Channel-wise sales breakdown
- Period-over-period comparison
- Trend analysis (7-day, 30-day, quarterly)
- Seasonal pattern detection
- Forecast accuracy tracking
- Sales velocity by SKU
- AOV (Average Order Value) analysis

#### Key Metrics
- **Total Gross Revenue**: ₹78.42 Lakhs (weekly example)
- **Channel Distribution**: Amazon (44.4%), Quick Commerce (36.5%), Flipkart/Myntra (19.1%)
- **Period Growth**: +8.4% YoY, +3.2% vs previous week
- **High Velocity Products**: Sleepsia (₹2.84L weekly leakage potential)

---

### 19. **Price Map Intelligence**
**Module**: `PriceMapIntelView`  
**Type**: Pricing Compliance & Optimization  
**Access**: Owner, Super Admin, Pricing Manager

#### Description
Manufacturer's Authorized Price (MAP) compliance monitoring and dynamic pricing intelligence.

#### Key Features
- MAP policy enforcement across channels
- Price differential monitoring
- Competitor price analysis
- Dynamic pricing recommendations
- MAP breach alerts
- Pricing elasticity analysis
- Revenue optimization
- Discount strategy optimization

#### Key Features
- Rogue seller detection
- Price undercut alerts
- MAP violation automation (delisting or correction)
- Channel price consistency
- Promotional pricing approval workflows

---

### 20. **Returns & Quality Management**
**Module**: `ReturnsQualityView`  
**Type**: Quality & Customer Satisfaction  
**Access**: Owner, Super Admin, Operations Manager

#### Description
Returns analysis, RMA (Return Merchandise Authorization) tracking, and quality issue management.

#### Key Features
- Return rate by SKU and channel
- Return reason categorization
- Quality defect tracking
- Supplier quality reporting
- Refund processing status
- Net Promoter Score (NPS) integration
- Quality trend analysis
- Process improvement recommendations

#### Return Categories
- Defective product
- Quality issues
- Damaged in transit
- Incorrect item shipped
- Customer changed mind
- Product not as described

#### Quality Metrics
- **Return Rate**: % of units returned
- **Defect Rate**: % of returns due to quality
- **Processing Time**: Days to resolve
- **Refund Cycle**: Days to complete refund

---

### 21. **Reviews & Voice of Customer**
**Module**: `ReviewsVocView`  
**Type**: Customer Sentiment Analysis  
**Access**: All Roles

#### Description
Customer review aggregation, sentiment analysis, and Voice of Customer (VOC) insights.

#### Key Features
- Multi-channel review aggregation
- Sentiment analysis (positive, neutral, negative)
- Topic extraction and keyword analysis
- Customer segment analysis
- Review response automation
- Trend detection over time
- Competitor review comparison
- Action item generation

#### Review Sources
- Amazon reviews and Q&A
- Flipkart reviews
- Blinkit ratings
- Zepto feedback
- Myntra customer reviews
- Direct website reviews

#### Sentiment Categories
- **Positive**: 4-5 star reviews, satisfied customers
- **Neutral**: 3-star reviews, mixed feedback
- **Negative**: 1-2 star reviews, dissatisfied customers

#### VOC Analysis
- Feature requests
- Common complaints
- Quality issues
- Shipping/delivery concerns
- Pricing sensitivity
- Competitive comparisons

---

### 22. **Search Share of Search**
**Module**: `SearchShareOfSearchView`  
**Type**: SEO & Search Performance  
**Access**: Owner, Super Admin, Marketing Manager

#### Description
Organic search performance analysis with keyword-level visibility and competitive benchmarking.

#### Key Features
- Organic keyword tracking
- Search visibility by keyword
- Rank position monitoring
- Share of search (vs competitors)
- Search volume analysis
- Click-through rate (CTR) optimization
- Keyword bid recommendations
- Long-tail keyword opportunities

#### Key Metrics
- **Organic Rank**: Current SERP position
- **Search Visibility**: Aggregated visibility score
- **Search Volume**: Monthly search volume
- **CTR**: Click-through rate from search results
- **Volume Lost**: Due to stockouts or bad reviews

---

## Admin & Settings Skills

### 23. **Settings & RBAC (Role-Based Access Control)**
**Module**: `SettingsRbacView`  
**Type**: Administration & Configuration  
**Access**: Owner, Super Admin only

#### Description
System configuration, user management, role-based access control, and feature toggles.

#### Key Features
- User role management
- Permission configuration
- Email settings (SMTP configuration)
- API key management
- Feature flags and toggles
- Data retention policies
- Audit log access
- System health monitoring

#### Available Roles
1. **Owner**: Full system access, strategic decisions
2. **Super Admin**: All operations, configuration access
3. **Operations Manager**: Supply chain and order operations
4. **Marketing Manager**: Pricing, content, advertising
5. **Analyst**: View-only reports and analytics
6. **Logistics Coordinator**: Transfer and logistics operations
7. **Content Manager**: Product listings and content

#### Permissions Configurable
- View reports
- Send emails
- Execute actions
- Modify listings
- Manage users
- Configure integrations
- Access admin panel

---

## Sidebar Navigation Skills

### 24. **AI Assistant Drawer**
**Module**: `AIAssistantDrawer`  
**Type**: Conversational AI Interface  
**Access**: All Roles

#### Description
Floating AI assistant panel for real-time conversational intelligence with context awareness.

#### Key Features
- Natural language queries
- Context-aware responses
- Multi-turn conversations
- Query suggestions
- Response confidence scoring
- Source attribution
- Quick action integration
- Conversation history

#### Supported Query Types
- **Operational**: "What's the status of Blinkit?"
- **Analytical**: "Why did sales drop on Monday?"
- **Transactional**: "Transfer 250 units to HSR layout"
- **Reporting**: "Send WBR to vikash@example.com"
- **Forecast**: "Predict demand for next week"

#### AI Capabilities
- Weekly Business Review insights
- Anomaly analysis and root causes
- Mother Hub status queries
- Competitive intelligence
- Action recommendations

---

### 25. **Topbar Navigation & Filters**
**Module**: `Topbar`  
**Type**: Navigation & Filtering  
**Access**: All Roles

#### Description
Top navigation bar with view switching, channel selection, date range filtering, and search.

#### Key Features
- View mode switcher (Command Center → Digital Shelf → Supply Chain, etc.)
- Channel filter (All, Amazon, Flipkart, Myntra, Blinkit, Zepto, Swiggy)
- Date range selector (Last 7 Days, Last 30 Days, Custom Range)
- Search functionality
- User role indicator
- Notification badge (active anomalies count)
- Quick action buttons

#### Navigation Options
- Dashboard
- Intelligence Views
- Operations
- Administration
- Help & Support

---

### 26. **Sidebar Navigation**
**Module**: `Sidebar`  
**Type**: Main Navigation Menu  
**Access**: Role-based visibility

#### Description
Collapsible sidebar with hierarchical navigation to all platform modules.

#### Navigation Structure
```
Dashboard
├── Command Center
├── Executive Reports
└── Alerts & Anomalies

Intelligence
├── Sales Intelligence
├── Advertising ROAS
├── Competitor Watch
├── Price Map Intelligence
├── Reviews & VOC
└── Search Intelligence

Operations
├── Digital Shelf
├── Supply Chain
├── Dark Stores
├── Perishables & Expiry
└── Returns & Quality

Automation
├── Autonomous AI
├── Autonomous Actions
├── Content Studio
└── Dataset Sync

Settings
├── Email & Dispatch
└── RBAC & Configuration
```

---

## Context & Data Management

### 27. **Data Context Provider**
**Module**: `DataContext.tsx`  
**Type**: Application State Management  
**Access**: Internal component state

#### Description
React Context API-based state management for application-wide data and user context.

#### Features
- User persona management
- SKU catalog state
- Alert/anomaly state
- Marketplace selection state
- Date range filtering
- User role tracking
- Data caching and synchronization

#### User Personas
- **Owner**: vikashr984@gmail.com (Full access)
- **Operations Manager**: ops@agileventures.net
- **Marketing Manager**: marketing@agileventures.net
- **Analyst**: analyst@agileventures.net

---

## Support & Help

### 28. **Acronym Reference**
**Module**: `AcronymBadge.tsx`, `acronyms.ts`  
**Type**: Help & Reference  
**Access**: All Roles

#### Description
Interactive acronym definitions and glossary for all platform terminology.

#### Common Acronyms
- **WBR**: Weekly Business Review
- **SKU**: Stock Keeping Unit
- **OOS**: Out of Stock
- **FEFO**: First Expired, First Out
- **ROAS**: Return on Ad Spend
- **TACoS**: Total Advertising Cost of Sales
- **MAP**: Manufacturer's Authorized Price
- **RMA**: Return Merchandise Authorization
- **VOC**: Voice of Customer
- **CTR**: Click-Through Rate
- **AOV**: Average Order Value
- **NPS**: Net Promoter Score
- **ASP**: Amazon Sponsored Products
- **MOM**: Month-over-Month
- **YoY**: Year-over-Year
- **PSI**: Perfect Stock Inventory

---

## Network & Architecture

### 29. **Network Architecture Flow**
**Module**: `NetworkArchitectureFlow.tsx`  
**Type**: System Visualization  
**Access**: Super Admin, Owner

#### Description
Visual representation of the system architecture including platform, marketplaces, and data flows.

#### Architecture Components
```
Frontend (React/TypeScript)
    ↓
Django REST Backend
    ├→ AI Services (Gemini API)
    ├→ Email Services (SMTP)
    ├→ Database (Models)
    └→ Marketplace APIs
         ├→ Amazon SP-API
         ├→ Flipkart Seller API
         ├→ Blinkit API
         ├→ Zepto API
         └→ Logistics APIs (Shadowfax)

External Integrations
    ├→ Google Sheets (Data Sync)
    ├→ Google Gemini (AI)
    └→ Marketplace Connectors
```

---

## Summary Table

| Skill # | Module Name | Type | Access Level | Primary Use |
|---------|------------|------|--------------|------------|
| 1 | Command Center | Dashboard | Owner/Super Admin | Real-time monitoring |
| 2 | Digital Shelf | Optimization | Marketing/Super Admin | Listing optimization |
| 3 | Supply Chain | Logistics | Operations/Logistics | Inventory movement |
| 4 | Autonomous AI | Intelligence | Owner/Super Admin | AI decisions |
| 5 | Autonomous Actions | Automation | Operations/Super Admin | Marketplace automation |
| 6 | Alerts & Anomalies | Monitoring | All | Issue detection |
| 7 | Executive Reports | Reporting | Owner/Analyst | Business reporting |
| 8 | Advertising ROAS | Analytics | Marketing/Super Admin | Ad performance |
| 9 | Competitor Watch | Intelligence | Analyst/Super Admin | Competitive analysis |
| 10 | Content Studio | Creation | Content/Super Admin | Content generation |
| 11 | Dataset Sync | Integration | Operations/Super Admin | Data synchronization |
| 12 | Email Dispatch | Automation | All | Email communication |
| 13 | Stock Transfer | Operations | Logistics/Operations | Transfer management |
| 14 | Dark Store Shortage | Emergency | Operations/Super Admin | Rapid resolution |
| 15 | SKU 360 | Analytics | All | Product analysis |
| 16 | Dark Stores | Operations | Operations/Logistics | Quick commerce management |
| 17 | Perishables | Management | Operations/Super Admin | Expiry management |
| 18 | Sales Intelligence | Analytics | All | Revenue analysis |
| 19 | Price Map | Compliance | Pricing/Super Admin | Pricing management |
| 20 | Returns & Quality | Management | Operations/Super Admin | Quality tracking |
| 21 | Reviews & VOC | Analytics | All | Customer feedback |
| 22 | Search Intelligence | Analytics | Marketing/Super Admin | SEO/Search tracking |
| 23 | Settings & RBAC | Admin | Owner/Super Admin | System configuration |
| 24 | AI Assistant | Interface | All | Conversational AI |
| 25 | Topbar | Navigation | All | Navigation & filtering |
| 26 | Sidebar | Navigation | Role-based | Main menu |
| 27 | Data Context | State | Internal | App state management |
| 28 | Acronym Reference | Help | All | Glossary & definitions |
| 29 | Network Architecture | Visualization | Admin | System architecture |

---

## Feature Roadmap

### Planned Skills for Future Releases
1. **Predictive Analytics**: Demand forecasting and trend prediction
2. **Customer Segmentation**: Behavioral clustering and targeting
3. **Marketing Automation**: Campaign orchestration and automation
4. **Mobile App**: Native iOS/Android applications
5. **Video Analytics**: Product video performance tracking
6. **Influencer Management**: Influencer campaign coordination
7. **Inventory Forecasting**: ML-based stock predictions
8. **Dynamic Bundling**: Recommendation engine for product bundles
9. **Customer Lifetime Value**: CLV prediction and optimization
10. **Supply Chain Optimization**: Advanced route and logistics optimization

---

## Skill Access Control Matrix

| Skill | Owner | Super Admin | Operations Manager | Marketing Manager | Analyst | Logistics Coordinator | Content Manager |
|-------|-------|------------|-------------------|------------------|---------|----------------------|-----------------|
| Command Center | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| Digital Shelf | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ |
| Supply Chain | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ |
| Autonomous AI | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Autonomous Actions | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Alerts & Anomalies | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Executive Reports | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Advertising ROAS | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ |
| Competitor Watch | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ |
| Content Studio | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ | ✓ |
| Dataset Sync | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Email Dispatch | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Stock Transfer | ✓ | ✓ | ✓ | ✗ | ✗ | ✓ | ✗ |
| Dark Store Shortage | ✓ | ✓ | ✓ | ✗ | ✗ | ✓ | ✗ |
| SKU 360 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Dark Stores | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ |
| Perishables | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ |
| Sales Intelligence | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Price Map | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ |
| Returns & Quality | ✓ | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ |
| Reviews & VOC | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ |
| Search Intelligence | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ |
| Settings & RBAC | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |

---

## Performance & Optimization

### Load Times
- Command Center: <2s
- Digital Shelf: <3s
- Supply Chain: <2.5s
- Executive Reports: <4s
- SKU 360: <2.5s

### Data Refresh Rates
- Real-time alerts: 30-60 seconds
- Daily reports: Once per day
- Weekly reports: Once per week
- Monthly forecasts: Once per month

### Concurrent User Support
- Platform supports 100+ concurrent users
- Real-time updates via WebSocket (future enhancement)
- Automatic pagination for large datasets

---

## End of Skills Documentation
**Last Updated**: 2026-08-26  
**Version**: 1.0
