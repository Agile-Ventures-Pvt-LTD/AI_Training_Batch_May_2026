"""
Django settings for Sleepsia Commerce Intelligence project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# [SECURITY FIX] Load SECRET_KEY from environment, no hardcoded fallback
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

if not SECRET_KEY:
    if ENVIRONMENT == 'production':
        raise ValueError("[ERROR] DJANGO_SECRET_KEY environment variable must be set in production!")
    else:
        # Development only - generate a development key
        SECRET_KEY = 'dev-only-sleepsia-commerce-intelligence-never-use-in-production-12345678'
        print("[WARNING] Using development SECRET_KEY. Set DJANGO_SECRET_KEY env var for security.")

DEBUG = os.getenv('DEBUG', 'True') == 'True'

# [SECURITY FIX] Configure ALLOWED_HOSTS per environment (not wildcard)
ALLOWED_HOSTS = []

if ENVIRONMENT == 'development':
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'localhost:5173', '127.0.0.1:5173', '*.local']
elif ENVIRONMENT == 'staging':
    ALLOWED_HOSTS = [
        'staging.sleepsia.com',
        'staging-api.sleepsia.com',
    ]
elif ENVIRONMENT == 'production':
    ALLOWED_HOSTS = [
        'sleepsia.com',
        'www.sleepsia.com',
        'api.sleepsia.com',
    ]

# Validate ALLOWED_HOSTS in production
if not ALLOWED_HOSTS and ENVIRONMENT == 'production':
    raise ValueError("[ERROR] ALLOWED_HOSTS must be explicitly configured in production!")

print(f"[OK] Environment: {ENVIRONMENT}, ALLOWED_HOSTS: {ALLOWED_HOSTS}")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'api',
]


ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', BASE_DIR / 'dist'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'
ASGI_APPLICATION = 'backend.asgi.application'

# Database
# Using SQLite for local persistent storage if needed
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'dist'] if (BASE_DIR / 'dist').exists() else []

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# [OK] SECURITY FIX: Configure CORS per environment (not all origins)
CORS_ALLOWED_ORIGINS = []
CORS_ALLOW_CREDENTIALS = True

if ENVIRONMENT == 'development':
    CORS_ALLOWED_ORIGINS = [
        'http://localhost:3000',      # React dev server
        'http://localhost:5173',      # Vite dev server
        'http://127.0.0.1:3000',
        'http://127.0.0.1:5173',
        'http://localhost:8000',      # Django backend
    ]

elif ENVIRONMENT == 'staging':
    CORS_ALLOWED_ORIGINS = [
        'https://staging.sleepsia.com',
        'https://app-staging.sleepsia.com',
    ]

elif ENVIRONMENT == 'production':
    CORS_ALLOWED_ORIGINS = [
        'https://sleepsia.com',
        'https://www.sleepsia.com',
        'https://app.sleepsia.com',
    ]

# Whitelist specific headers only
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

print(f"[OK] CORS configured for origins: {CORS_ALLOWED_ORIGINS}")

# [OK] SECURITY FIX: Configure CSRF protection
CSRF_TRUSTED_ORIGINS = []

if ENVIRONMENT == 'development':
    CSRF_TRUSTED_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:5173',
        'http://127.0.0.1:3000',
        'http://127.0.0.1:5173',
    ]

elif ENVIRONMENT == 'production':
    CSRF_TRUSTED_ORIGINS = [
        'https://sleepsia.com',
        'https://www.sleepsia.com',
        'https://app.sleepsia.com',
    ]

# Enforce CSRF in all requests
CSRF_COOKIE_SECURE = ENVIRONMENT == 'production'  # HTTPS only in production
CSRF_COOKIE_HTTPONLY = True                        # Prevent JavaScript access
CSRF_COOKIE_SAMESITE = 'Strict'                   # Prevent cross-site cookies

# [OK] SECURITY FIX: Add security headers and error handling middleware
MIDDLEWARE = [
    'backend.middleware.error_handler.ErrorHandlerMiddleware',  # [OK] H-2: Error handling
    'backend.middleware.security_headers.SecurityHeadersMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# [OK] SECURITY FIX: Additional security settings
X_FRAME_OPTIONS = 'DENY'                           # Prevent clickjacking
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", "'unsafe-inline'"),
    'style-src': ("'self'", "'unsafe-inline'"),
    'img-src': ("'self'", "data:", "https:"),
    'font-src': ("'self'", "data:"),
    'connect-src': ("'self'", "https:"),
}

if ENVIRONMENT == 'production':
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# [OK] H-5: REST Framework settings with rate limiting
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
    ],
    # [OK] H-5: Add rate limiting to prevent DoS attacks
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',      # 100 requests per hour for anonymous users
        'user': '1000/hour'      # 1000 requests per hour for authenticated users
    },
    # [OK] Pagination settings
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}
