import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'replace-this-with-your-secret-key'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',          # Admin UI (safe to include even if not used yet)
    'django.contrib.auth',           # Auth system (required for Permission model, context processors, etc.)
    'django.contrib.contenttypes',
    'django.contrib.sessions',       # Required for admin + PDF templates
    'django.contrib.messages',       # Required for admin + PDF templates
    'django.contrib.staticfiles',    # Required for serving static files (WeasyPrint may reference fonts etc.)
    'rest_framework',                # DRF → required for your APIs
    'calculators',                   # Your public calculators app
    'payroll',                       # Your payroll engine app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',    # Required
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',                # Safe to include even for API-only → protects admin if used
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Required
    'django.contrib.messages.middleware.MessageMiddleware',     # Required
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hapi_pay_calc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],               # You can add custom template folders here later if needed
        'APP_DIRS': True,         # Required → loads calculators/templates and payroll/templates
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Required by Django admin and WeasyPrint often relies on it
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hapi_pay_calc.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JS, Images) → important for WeasyPrint / PDF styling
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
