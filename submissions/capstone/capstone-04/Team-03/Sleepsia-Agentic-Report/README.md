# Sleepsia Agentic Business Reporting System

A comprehensive business intelligence and analytics platform that consolidates sales, advertising, financial, inventory, and operational data from multiple e-commerce platforms with AI-powered insights and recommendations.

## 📋 Overview

The Sleepsia Agentic Reporting System provides:

- **Unified Business Reporting** - Consolidated view across all platforms
- **Platform Analysis** - Performance metrics for Amazon, Flipkart, Myntra, Blinkit, JioMart
- **Product-wise Analysis** - SKU-level profitability and performance
- **Advertising Analytics** - ROAS, ACOS, and ad spend analysis
- **Inventory Management** - Warehouse-level stock tracking and optimization
- **AI Business Assistant** - Natural language queries with structured data responses
- **Management Reports** - Automated PDF/Excel report generation
- **Business Alerts** - Real-time notifications for critical metrics

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** - Backend runtime
- **Node.js 18+** - Frontend build tool
- **MySQL 8.0+** - Database
- **Git** - Version control

### Installation Steps

#### 1. Clone the Repository

```bash
git clone https://github.com/Ashish-Sinha07/Sleepsia-Agentic-Report.git
cd Sleepsia-Agentic-Report
```

#### 2. Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://sleepsia:sleepsia@localhost:3306/sleepsia_reporting

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Frontend Configuration
VITE_API_BASE_URL=http://localhost:8000

# Source Data
SOURCE_WORKBOOK=data/final_sleepsia_report_data.xlsx

# Groq API (for AI Assistant) - Get key from https://console.groq.com/
GROQ_API_KEY=your-api-key-here
```

#### 3. Set Up MySQL Database

**Option A: Using the automated setup script**

```bash
cd backend
python setup_mysql.py
```

**Option B: Manual setup**

```bash
# Login to MySQL as root
mysql -u root -p

# Run these commands:
CREATE DATABASE IF NOT EXISTS sleepsia_reporting;
CREATE USER IF NOT EXISTS 'sleepsia'@'localhost' IDENTIFIED BY 'sleepsia';
GRANT ALL PRIVILEGES ON sleepsia_reporting.* TO 'sleepsia'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 4. Set Up Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database schema and load data
python app/db_init.py

# Or use the ETL loader
python etl/run_etl.py
```

#### 5. Set Up Frontend

```bash
# Open new terminal window
cd dashboard

# Install dependencies
npm install

# Start development server (runs on http://localhost:5173)
npm run dev
```

#### 6. Start Backend API

```bash
# In backend terminal (with venv activated)
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

## 📁 Project Structure

```
Sleepsia-Agentic-Report/
├── backend/                          # FastAPI backend
│   ├── app/
│   │   ├── db_init.py               # Database initialization
│   │   ├── models/                  # Database models
│   │   ├── schemas/                 # Pydantic schemas
│   │   ├── services/                # Business logic
│   │   └── api/routes/              # API endpoints
│   ├── etl/
│   │   ├── run_etl.py              # ETL pipeline
│   │   ├── loader.py               # Data loader
│   │   └── validate.py             # Data validation
│   ├── routes/                      # Legacy API routes
│   │   ├── kpis.py
│   │   ├── platform_performance.py
│   │   ├── product_performance.py
│   │   ├── advertising.py
│   │   ├── profitability.py
│   │   ├── inventory.py
│   │   ├── warehouses.py
│   │   ├── alerts.py
│   │   ├── ai_assistant.py
│   │   └── reports.py
│   ├── services/                    # Agent services
│   │   ├── agent_orchestrator.py
│   │   └── agent_service.py
│   ├── scripts/                     # Utility scripts
│   │   ├── generate_report_now.py
│   │   ├── run_autonomous_scheduler.py
│   │   └── start_report_scheduler.py
│   ├── config.py                    # Configuration
│   ├── app.py                       # FastAPI app entry point
│   ├── setup_mysql.py              # Database setup
│   ├── requirements.txt            # Python dependencies
│   └── venv/                       # Virtual environment
│
├── dashboard/                        # React frontend
│   ├── src/
│   │   ├── components/             # Reusable components
│   │   ├── pages/                  # Page components
│   │   ├── hooks/                  # Custom React hooks
│   │   ├── utils/                  # Utility functions
│   │   └── App.jsx                 # Main app component
│   ├── package.json               # NPM dependencies
│   ├── vite.config.js             # Vite configuration
│   └── tailwind.config.js         # Tailwind CSS config
│
├── data/                            # Source data
│   └── final_sleepsia_report_data.xlsx
│
├── .env.example                    # Environment variables template
├── .claude/
│   └── CLAUDE.md                  # Project guidelines
└── README.md                       # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | MySQL connection string | `mysql+pymysql://sleepsia:sleepsia@localhost:3306/sleepsia_reporting` |
| `API_HOST` | API server host | `0.0.0.0` |
| `API_PORT` | API server port | `8000` |
| `VITE_API_BASE_URL` | Frontend API endpoint | `http://localhost:8000` |
| `GROQ_API_KEY` | Groq API key for AI | Get from https://console.groq.com/ |
| `SOURCE_WORKBOOK` | Path to source Excel file | `data/final_sleepsia_report_data.xlsx` |

### API Base URLs (for development)

- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:5173
- **API Documentation (Swagger)**: http://localhost:8000/docs

## 📊 API Endpoints

### KPIs
```
GET /api/kpis - Get key performance indicators
```

### Platform Performance
```
GET /api/platform-performance - Platform-wise metrics
GET /api/platform-performance/{platform} - Specific platform details
```

### Product Performance
```
GET /api/product-performance - Product-wise metrics
GET /api/product-performance/{product_id} - Specific product details
GET /api/products - List all products
```

### Advertising
```
GET /api/advertising - Advertising metrics
GET /api/advertising/platform/{platform} - Platform-specific ad metrics
GET /api/advertising/roas-summary - ROAS analysis
```

### Profitability
```
GET /api/profitability - Profitability analysis
GET /api/profitability/product - Product profitability
GET /api/profitability/platform - Platform profitability
```

### Inventory & Warehouses
```
GET /api/inventory - Inventory status
GET /api/inventory/low-stock - Low stock items
GET /api/warehouses - Warehouse information
GET /api/warehouses/{warehouse_id} - Specific warehouse
GET /api/warehouses/map-data - Warehouse location data
```

### Alerts
```
GET /api/alerts - Business alerts
GET /api/alerts/active - Active alerts
```

### AI Assistant
```
POST /api/ai/ask - Ask business questions
GET /api/ai/health - Check AI service status
```

### Reports
```
GET /api/reports - List generated reports
POST /api/reports/generate - Generate new report
GET /api/reports/{report_id}/download - Download report
```

## 🏃 Running the Application

### Complete Startup (3 terminals)

**Terminal 1 - Backend API:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn backend.app:app --reload
```

**Terminal 2 - Frontend Dev Server:**
```bash
cd dashboard
npm run dev
```

**Terminal 3 - Report Scheduler (Optional):**
```bash
cd backend
source venv/bin/activate
python scripts/start_report_scheduler.py
```

### Access the Application

- Dashboard: http://localhost:5173
- API Docs: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

## 📊 Loading Source Data

### Initial Data Load

```bash
cd backend
# Load data from Excel into database
python etl/run_etl.py
```

### Verify Data Load

```bash
python etl/verify_load.py
```

### Audit Post-ETL

```bash
python etl/post_etl_audit.py
```

## 🧪 Running Tests

```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_products.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=backend tests/
```

## 🏗️ Architecture

### Technology Stack

**Frontend:**
- React 18
- Vite (build tool)
- Tailwind CSS (styling)
- Recharts (data visualization)
- React Leaflet (maps)
- Axios (HTTP client)

**Backend:**
- Python 3.11
- FastAPI (web framework)
- SQLAlchemy (ORM)
- Pydantic (data validation)
- Groq (AI/LLM)

**Database:**
- MySQL 8.0+
- SQLAlchemy for ORM

### Data Flow

```
Source Excel
    ↓
ETL Pipeline
    ↓
MySQL Database
    ↓
FastAPI Analytics Engine
    ↓
React Dashboard + AI Assistant
```

### AI Architecture

The AI assistant uses a **controlled analytical approach**:

```
User Question
    ↓
Intent Understanding (Groq LLM)
    ↓
Controlled Analytical Tools
    ↓
SQL Queries (database queries)
    ↓
Structured Results
    ↓
LLM Explanation & Recommendations
    ↓
User Response
```

**Key Principle:** The AI never calculates or fabricates numerical values. All numbers come from the database.

## 🔐 Security Considerations

1. **Environment Variables**: Never commit `.env` file with real credentials
2. **Database**: Use strong MySQL root password
3. **API Keys**: Groq API key should be stored in `.env` only
4. **CORS**: Frontend URLs are whitelisted in backend
5. **SQL Injection**: Use SQLAlchemy parameterized queries

## 🐛 Troubleshooting

### Issue: "Connection refused" for MySQL

**Solution:**
```bash
# Verify MySQL is running
# On Windows: Check Services
# On macOS: brew services list
# On Linux: sudo systemctl status mysql

# Try reconnecting
mysql -u root -p
```

### Issue: Frontend can't connect to API

**Solution:**
1. Check backend is running: `http://localhost:8000`
2. Verify `VITE_API_BASE_URL` in `.env`
3. Check CORS settings in `backend/app.py`

### Issue: Data not loading

**Solution:**
```bash
cd backend
# Verify database connection
python -c "from backend.config import settings; print(settings.database_url)"

# Reload data
python etl/run_etl.py
```

### Issue: Port already in use

```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process and restart
```

## 📚 Documentation

- **Architecture**: See `.claude/CLAUDE.md`
- **Database Schema**: Check `backend/app/models/`
- **API Schema**: Run backend and visit http://localhost:8000/docs
- **Frontend Components**: See `dashboard/src/components/`

## 🚢 Deployment

### Docker (Optional)

```bash
# Build backend image
docker build -t sleepsia-backend ./backend

# Build frontend image
docker build -t sleepsia-frontend ./dashboard

# Run with docker-compose
docker-compose up
```

### Production Checklist

- [ ] Set `APP_ENV=production` in `.env`
- [ ] Use strong database password
- [ ] Configure SMTP for email reports
- [ ] Set up Groq API key
- [ ] Update CORS allowed origins
- [ ] Configure report scheduling timezone
- [ ] Set up log rotation
- [ ] Database backups configured
- [ ] SSL/TLS enabled

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes following the code quality rules
3. Run tests: `pytest`
4. Commit with clear messages
5. Push to branch and create a Pull Request

## 📝 Development Workflow

```
1. Create feature branch from main
   ↓
2. Implement changes
   ↓
3. Run tests and linting
   ↓
4. Create pull request
   ↓
5. Code review
   ↓
6. Merge to main
```

## 📞 Support

For issues, questions, or contributions:

1. Check the [troubleshooting section](#troubleshooting)
2. Review `.claude/CLAUDE.md` for project guidelines
3. Create an issue on GitHub
4. Contact: ashish.sinha@agileventures.net

## 📄 License

This project is part of the Sleepsia platform.

## 🎯 Project Status

**MVP Status**: Active Development

**Key Features Implemented:**
- ✅ Database and data loading
- ✅ KPI calculations
- ✅ Platform analysis
- ✅ Product analysis
- ✅ Advertising metrics
- ✅ Profitability analysis
- ✅ Warehouse management
- ✅ React dashboard
- ✅ AI assistant (Groq integration)
- ✅ Report generation

**Roadmap:**
- Warehouse map visualization
- Automated report distribution
- Power Automate integration
- Advanced recommendations
- Mobile app

