# Agile Solutions Control Tower

A production-grade e-commerce management platform combining Django REST API backend with a React/TypeScript frontend. This AI-powered control tower provides real-time inventory management, pricing intelligence, and autonomous decision-making capabilities for multi-channel e-commerce operations.

## 🏗️ Project Structure

```
django-agile-tower/
│
├── backend/                              # Django REST API Backend
│   ├── config/                           # Django configuration
│   │   ├── settings.py                   # Main Django settings
│   │   ├── urls.py                       # URL routing
│   │   ├── wsgi.py                       # WSGI application
│   │   └── __init__.py
│   │
│   ├── api/                              # Main API application
│   │   ├── models.py                     # Database models (EmailLog, ScheduledEmail, StockTransfer, ExecutedAction)
│   │   ├── views.py                      # API endpoints
│   │   ├── serializers.py                # DRF serializers
│   │   ├── urls.py                       # API routes
│   │   ├── apps.py                       # App config
│   │   ├── ai_utils.py                   # AI/Gemini integration utilities
│   │   ├── email_utils.py                # Email sending utilities
│   │   ├── signals.py                    # Django signals
│   │   ├── migrations/                   # Database migrations
│   │   └── __init__.py
│   │
│   ├── manage.py                         # Django management command
│   ├── requirements.txt                  # Python dependencies
│   ├── db.sqlite3                        # SQLite database (development)
│   ├── venv/                             # Python virtual environment
│   └── .env                              # Environment variables (Git ignored)
│
├── frontend/                             # React + TypeScript Frontend
│   ├── src/
│   │   ├── components/                   # Reusable React components
│   │   │   ├── AcronymBadge.tsx
│   │   │   ├── DarkStoreShortageModal.tsx
│   │   │   ├── NetworkArchitectureFlow.tsx
│   │   │   └── views/                    # Page-specific components (20+ feature views)
│   │   │       ├── ExecutiveTowerView.tsx
│   │   │       ├── AdvertisingRoasView.tsx
│   │   │       ├── SalesIntelligenceView.tsx
│   │   │       ├── DarkStoresSupplyChainView.tsx
│   │   │       ├── PerishablesExpiryView.tsx
│   │   │       ├── AIAgentCenterView.tsx
│   │   │       └── ...more views
│   │   │
│   │   ├── services/                     # API service layer
│   │   │   ├── datasetService.ts         # Dataset API calls
│   │   │   ├── rulesEngine.ts            # Business rules
│   │   │   └── .env.local                # Frontend environment
│   │   │
│   │   ├── data/
│   │   │   └── mockData.ts               # Mock data for development
│   │   │
│   │   ├── utils/
│   │   │   ├── acronyms.ts               # Utility functions
│   │   │   └── emailTemplateGenerator.ts
│   │   │
│   │   ├── types.ts                      # TypeScript type definitions
│   │   ├── App.tsx                       # Main App component
│   │   └── main.tsx                      # React entry point
│   │
│   ├── public/                           # Static assets
│   │   ├── assets/
│   │   │   └── .aistudio/
│   │   ├── firebase-applet-config.json   # Firebase configuration
│   │   └── metadata.json                 # App metadata
│   │
│   ├── index.html                        # HTML entry point
│   ├── package.json                      # npm dependencies
│   ├── tsconfig.json                     # TypeScript configuration
│   ├── vite.config.ts                    # Vite bundler configuration
│   ├── tailwind.config.js                # Tailwind CSS configuration
│   ├── postcss.config.js                 # PostCSS configuration
│   ├── node_modules/                     # npm packages
│   ├── dist/                             # Build output (production)
│   └── bun.lock                          # Lock file (if using bun)
│
├── AGENTS.md                             # Claude AI agents documentation
├── SKILLS.md                             # Development skills documentation
├── code_review.md                        # Code review findings
├── .env                                  # Root environment file
├── .env.example                          # Environment variables template
├── .gitignore                            # Git ignore rules
├── .claude/                              # Claude Code IDE configuration
├── .git/                                 # Git repository
├── db.sqlite3                            # SQLite database (root level)
├── bun.lock                              # Package lock file
├── start.bat                             # Windows startup script (root)
├── start.sh                              # Mac/Linux startup script (root)
└── README.md                             # This file
```

## 🚀 Quick Start

### Prerequisites
- **Python**: 3.8 or higher
- **Node.js**: 16+ or **Bun** (modern JavaScript runtime)
- **npm** or **yarn** (Node.js package manager)
- **Git**: For version control
- **Environment variables**: See `.env.example` for required keys

### System Requirements
- **Disk Space**: ~2GB for dependencies and database
- **RAM**: Minimum 4GB recommended
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)

### Option 1: Automated Full Setup (Recommended)

This is the quickest way to get everything running.

**Windows (PowerShell/Command Prompt):**
```bash
start.bat
```

**macOS/Linux (Bash/Zsh):**
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manual Setup - Step by Step

#### Step 1: Clone & Navigate to Project
```bash
# Navigate to project directory (if not already there)
cd django-agile-tower
```

#### Step 2: Backend Setup (Terminal 1)

```bash
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# Windows (Command Prompt):
venv\Scripts\activate.bat

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create/update database
python manage.py migrate

# Create superuser (optional, for Django admin)
python manage.py createsuperuser

# Start Django development server
python manage.py runserver 0.0.0.0:8000
```

#### Step 3: Frontend Setup (Terminal 2)

```bash
cd frontend

# Install npm dependencies (first time only)
npm install
# OR if using yarn:
# yarn install

# Start Vite development server
npm run dev
# OR if using yarn:
# yarn dev
```

#### Step 4: Access the Application

- **Frontend Dashboard**: http://localhost:5173
- **Backend API**: http://localhost:8000/api
- **Django Admin Panel**: http://localhost:8000/admin (use superuser credentials)

## 🌐 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend Dashboard** | http://localhost:5173 | Main React application UI |
| **Backend API** | http://localhost:8000/api | REST API endpoints |
| **Django Admin** | http://localhost:8000/admin | Django administration panel |
| **API Documentation** | http://localhost:8000/api/docs (if enabled) | API endpoint documentation |

## 📋 Backend Stack

- Django 4.2
- Django REST Framework
- SQLite (development)
- Gemini AI Integration
- CORS enabled

## 🎨 Frontend Stack

- React 19
- TypeScript
- Vite
- Tailwind CSS
- Lucide Icons

## 🔧 Configuration

### Environment Variables Setup

#### 1. Create `.env` file in root directory
Copy from `.env.example` if available, or create new:

```bash
# Backend Configuration
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# API Keys
GEMINI_API_KEY=your-google-genai-api-key

# CORS Configuration (for frontend access)
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Email Configuration (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@agileventures.net

# Database (optional - defaults to SQLite)
# DATABASE_URL=postgresql://user:password@localhost/dbname
```

#### 2. Frontend Environment (Optional)
Create `frontend/.env.local`:
```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_DEBUG=true
```

### Backend Configuration

**File**: `backend/config/settings.py`
- Database configuration (currently SQLite, can switch to PostgreSQL)
- Installed Django apps
- Middleware stack
- Static files settings
- CORS allowed origins
- Email backend configuration

### Frontend Configuration

**File**: `frontend/vite.config.ts`
- Development server settings
- Build output path
- Plugin configuration (React, Tailwind)
- Proxy settings for API calls

**File**: `frontend/tailwind.config.js`
- Tailwind CSS customization
- Theme colors and spacing
- Component styles

## 📦 API Endpoints

All endpoints prefixed with `/api/`

### AI Endpoints
- `POST /api/ai/chat` - AI chat analysis
- `POST /api/ai/root-cause` - Root cause diagnosis
- `POST /api/ai/generate-content` - Content optimization

### Email Endpoints
- `POST /api/email/send-live` - Send emails
- `POST /api/email/schedule` - Schedule emails
- `GET /api/email/history` - Email history

### Action Endpoints
- `POST /api/actions/transfer-stock` - Stock transfers
- `POST /api/actions/execute` - Execute actions

## 🗄️ Database

### Models
- `EmailLog` - Email history
- `ScheduledEmail` - Scheduled tasks
- `StockTransfer` - Inventory transfers
- `ExecutedAction` - Action logs

### Migrations
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

## 🧪 Testing

### Backend Testing

#### Run All Tests
```bash
cd backend
python manage.py test
```

#### Run Specific App Tests
```bash
python manage.py test api
```

#### Run Specific Test Class
```bash
python manage.py test api.tests.YourTestClass
```

#### Run with Verbose Output
```bash
python manage.py test -v 2
```

#### Run with Coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # generates htmlcov/index.html
```

### Frontend Testing

#### Run Tests
```bash
cd frontend
npm test
```

#### Run Tests in Watch Mode
```bash
npm test -- --watch
```

#### Generate Coverage Report
```bash
npm test -- --coverage
```

### Integration Testing
Before deployment, test the full workflow:
1. Backend API responds to requests
2. Frontend connects to backend
3. Database migrations work correctly
4. Email notifications send properly
5. AI endpoints function with API keys

## 🐛 Troubleshooting

### Common Issues & Solutions

#### Port Already in Use
**Problem**: "Address already in use" error

**Solution**:
```bash
# Windows - Find process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux - Find and kill process
lsof -i :8000
kill -9 <PID>

# Or use a different port
python manage.py runserver 0.0.0.0:8001
```

#### Virtual Environment Issues
**Problem**: Python packages not found after activation

**Solution**:
```bash
# Deactivate and reactivate
deactivate

# Remove venv and create fresh
rm -rf backend/venv  # Linux/macOS
rmdir /s backend\venv  # Windows

# Recreate venv
python -m venv backend/venv

# Activate and reinstall
# (see Backend Setup section)
```

#### CORS Errors
**Problem**: Frontend can't connect to backend API

**Symptoms**: Browser console shows "Cross-Origin Request Blocked"

**Solution**:
1. Ensure backend is running on correct port (8000)
2. Check `.env` file has correct `CORS_ALLOWED_ORIGINS`
3. Frontend URL should match exactly (http://localhost:5173)
4. Restart Django after `.env` changes

```env
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

#### Database Lock Error
**Problem**: "database is locked" error

**Solution**:
```bash
cd backend

# Delete the database and recreate
rm db.sqlite3  # or del db.sqlite3 on Windows

# Recreate tables
python manage.py migrate
```

#### Node Modules Issues
**Problem**: Dependencies not installing or strange npm errors

**Solution**:
```bash
cd frontend

# Clear npm cache
npm cache clean --force

# Delete node_modules and lock file
rm -rf node_modules package-lock.json  # Linux/macOS
rmdir /s node_modules  # Windows
del package-lock.json  # Windows

# Reinstall
npm install
```

#### API Key Not Working
**Problem**: Gemini API returns authentication error

**Solution**:
1. Verify `GEMINI_API_KEY` in `.env` is correct
2. Check API key is not expired or disabled
3. Ensure API is enabled in Google Cloud Console
4. Restart Django: `python manage.py runserver`

#### Frontend Shows Blank Page
**Problem**: React app doesn't load, blank white screen

**Solution**:
1. Check browser console for JavaScript errors
2. Verify frontend is running: `npm run dev` output shows "Local: http://localhost:5173"
3. Hard refresh browser: Ctrl+Shift+R (Cmd+Shift+R on Mac)
4. Check backend is running and accessible

#### Can't Create Superuser
**Problem**: `createsuperuser` hangs or fails

**Solution**:
```bash
# Use interactive mode
python manage.py createsuperuser --noinput \
  --username admin \
  --email admin@example.com

# Then set password
python manage.py changepassword admin
```

### Getting Help

1. Check Django logs in terminal for detailed error messages
2. Review browser console (F12 → Console tab) for frontend errors
3. Check `.env` file configuration
4. Ensure all prerequisites are installed correctly
5. See AGENTS.md for AI assistance capabilities

## 📦 Deployment Guide

### Prerequisites for Production
- PostgreSQL database (recommended over SQLite)
- Environment with Python 3.8+ and Node.js 16+
- SSL/TLS certificate for HTTPS
- Separate environment variables for production

### Step 1: Build Frontend

```bash
cd frontend

# Install dependencies (if not done)
npm install

# Build for production
npm run build

# This creates optimized files in frontend/dist/
```

### Step 2: Prepare Backend

```bash
cd backend

# Ensure venv is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate.bat  # Windows

# Install production WSGI server
pip install gunicorn

# Collect static files (if using)
python manage.py collectstatic --noinput
```

### Step 3: Configure Production Environment

Create or update `.env` with production values:
```env
DEBUG=False
DJANGO_SECRET_KEY=your-very-long-random-secret-key-min-50-chars
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com

# Database - PostgreSQL example
DATABASE_URL=postgresql://user:password@db-host:5432/db-name

# CORS - Only allow production frontend
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-production-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# API Keys
GEMINI_API_KEY=your-production-api-key

# Optional: CDN settings for frontend
STATIC_URL=https://cdn.yourdomain.com/static/
```

### Step 4: Run Backend with Gunicorn

```bash
cd backend

# Run Gunicorn
gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 120 \
  --log-level info

# Or use environment variables
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Step 5: Serve Frontend Files

Use a web server (Nginx, Apache) to serve the built frontend:

**Nginx Example:**
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS (recommended)
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    # Serve frontend
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests to Django
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 6: Database Migration

```bash
cd backend

# Run migrations on production database
python manage.py migrate --settings=config.settings

# Create superuser for admin access
python manage.py createsuperuser
```

### Production Checklist

- [ ] `DEBUG=False` in `.env`
- [ ] `SECRET_KEY` is strong and unique
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] Database is PostgreSQL (not SQLite)
- [ ] HTTPS/SSL certificate installed
- [ ] CORS origins limited to your domain
- [ ] Email configuration working
- [ ] API keys are production keys
- [ ] Frontend built with `npm run build`
- [ ] Static files collected
- [ ] Gunicorn/ASGI server running
- [ ] Web server (Nginx/Apache) configured
- [ ] Database backups scheduled
- [ ] Error logging/monitoring enabled
- [ ] Security headers configured

### Optional: Use Process Manager

Consider using PM2 or similar to keep services running:

```bash
npm install -g pm2

# Start backend
pm2 start "gunicorn config.wsgi:application --bind 0.0.0.0:8000" --name "agile-backend"

# Monitor
pm2 monit
```

## 🛠️ Development Guide

### Backend Development Workflow

#### Activate Virtual Environment
```bash
cd backend

# Windows (Command Prompt)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Create Database Migrations
When you modify `models.py`:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Run Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```

#### Access Django Shell
```bash
python manage.py shell
```

#### Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
# Follow prompts for username, email, password
```

### Frontend Development Workflow

#### Install Dependencies
```bash
cd frontend
npm install
```

#### Start Development Server
```bash
npm run dev
# Server runs on http://localhost:5173
```

#### Build for Production
```bash
npm run build
# Output: frontend/dist/
```

#### Preview Production Build
```bash
npm run preview
```

#### Type Checking
```bash
npm run lint
# Checks TypeScript types without emitting
```

### Adding New Features

#### Backend: Adding a New API Endpoint
1. Create model in `backend/api/models.py`
2. Create serializer in `backend/api/serializers.py`
3. Create view in `backend/api/views.py`
4. Update `backend/api/urls.py`
5. Run migrations: `python manage.py makemigrations && python manage.py migrate`

#### Frontend: Adding a New Page View
1. Create component in `frontend/src/components/views/YourFeatureView.tsx`
2. Import in main app router
3. Add navigation entry
4. Create corresponding API service method

### Code Quality & Linting

#### Backend
```bash
# Install development dependencies
pip install pylint flake8

# Lint code
flake8 backend/api/

# Format code (optional)
pip install black
black backend/
```

#### Frontend
```bash
# Type checking
npm run lint

# Format code (optional)
npx prettier --write src/
```

## 📚 Project Features

### Core Features
- ✅ **Real-time Inventory Management** - Live tracking of stock levels across multiple channels
- ✅ **Multi-Channel Integration** - Support for Amazon, Flipkart, Myntra, Blinkit, Zepto, and more
- ✅ **Dark Store & Hub Management** - Track dark store shortage and mother hub reserves
- ✅ **Perishables Tracking** - Monitor expiry dates and inventory freshness
- ✅ **AI-Powered Analysis** - Gemini AI integration for intelligent insights and recommendations
- ✅ **Pricing Intelligence** - Dynamic pricing, MAP compliance, and competitor analysis
- ✅ **Stock Transfer Automation** - Automated stock movement between locations
- ✅ **Email Campaign Management** - Schedule and send bulk email campaigns
- ✅ **Returns & Quality Management** - Track return rates and quality metrics
- ✅ **Search Share Analysis** - Monitor search performance metrics
- ✅ **Executive Dashboard** - High-level business insights and KPIs
- ✅ **Autonomous Actions** - AI-driven automated decision-making
- ✅ **Role-Based Access Control (RBAC)** - Manage user permissions and access levels
- ✅ **Rules Engine** - Custom business rules for automation
- ✅ **Advertising ROI Tracking** - Monitor advertising spend and returns
- ✅ **Google Sheets Integration** - Sync data with spreadsheets
- ✅ **Supplier Management** - Track and manage suppliers
- ✅ **Content Studio** - Create and manage marketing content
- ✅ **Competitor Watch** - Monitor competitor activities and pricing

## 🔐 Security Best Practices

### Development Environment
- ✅ Store sensitive credentials in `.env` file (Git ignored)
- ✅ Never commit `.env` to version control
- ✅ Use strong `DJANGO_SECRET_KEY` (min 50 characters)
- ✅ Keep dependencies updated: `pip install --upgrade -r requirements.txt`

### Production Environment
- ✅ Set `DEBUG=False`
- ✅ Use environment-specific `.env` files
- ✅ Enable HTTPS/SSL certificates
- ✅ Configure CORS for specific domains only
- ✅ Use PostgreSQL instead of SQLite
- ✅ Implement rate limiting on API endpoints
- ✅ Regular security audits of dependencies
- ✅ Enable Django security headers middleware
- ✅ Rotate secrets regularly
- ✅ Monitor logs for suspicious activity

### Dependency Security
```bash
# Check for vulnerable dependencies
pip install safety
safety check

# Frontend
npm audit
npm audit fix
```

## 📚 Additional Documentation

- **AGENTS.md** - AI agents and automation capabilities
- **SKILLS.md** - Development skills and utilities
- **code_review.md** - Code review guidelines and findings
- **Django Documentation** - https://docs.djangoproject.com/
- **React Documentation** - https://react.dev/
- **Django REST Framework** - https://www.django-rest-framework.org/

## 🤝 Contributing

### Setting Up for Contribution

1. **Fork or Clone Repository**
   ```bash
   git clone <repository-url>
   cd django-agile-tower
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Follow existing code style
   - Write descriptive commit messages
   - Add tests for new features

4. **Test Thoroughly**
   ```bash
   # Backend
   cd backend
   python manage.py test

   # Frontend
   cd frontend
   npm test
   ```

5. **Submit Pull Request**
   - Provide detailed description of changes
   - Reference any related issues
   - Ensure all tests pass

### Code Style Guidelines

**Backend (Python)**:
- Follow PEP 8 standards
- Use type hints where possible
- Write docstrings for classes and methods

**Frontend (TypeScript/React)**:
- Use functional components with hooks
- Follow TypeScript strict mode
- Name components with PascalCase
- Use kebab-case for file names

## 📄 License

© 2024 Agile Ventures. All rights reserved.

## 📞 Support & Contact

### Getting Help
1. Check this README for common issues
2. Review the Troubleshooting section
3. Check existing issues on GitHub
4. Review AGENTS.md for AI assistance

### Reporting Bugs
- Describe the issue clearly
- Include steps to reproduce
- Attach error messages/logs
- Note your environment (OS, Python version, Node version)

### Feature Requests
- Explain the use case
- Describe expected behavior
- Reference any related features

### Contact Information
- **Email**: Vaibhav.Kesarwani@agileventures.net
- **Team**: Agile Ventures Development Team
- **Documentation**: See AGENTS.md and SKILLS.md for more info

## 🚀 Next Steps After Setup

1. **Explore the Dashboard**
   - Visit http://localhost:5173
   - Familiarize yourself with the UI

2. **Check Backend API**
   - Visit http://localhost:8000/api
   - Review available endpoints

3. **Access Django Admin**
   - Visit http://localhost:8000/admin
   - Use superuser credentials

4. **Read Documentation**
   - Review AGENTS.md for AI features
   - Check SKILLS.md for available tools

5. **Run Tests**
   - Verify everything works: `cd backend && python manage.py test`
   - Check frontend: `cd frontend && npm test`

6. **Start Contributing**
   - Pick an issue or feature
   - Follow the contributing guidelines
   - Submit a pull request

---

**Version**: 1.0.0  
**Last Updated**: 2026-08-31  
**Status**: Active Development
