"""
Django settings for ecom project.
For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY', 'unsafe-secret-key')

# Set DEBUG from environment variable for production
DEBUG = os.getenv("DEBUG", "False") == "True"

# Dynamically set ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS
if DEBUG:
    ALLOWED_HOSTS = ['*']
    CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://localhost:8000']
else:
    # Add your Railway production domain here
    ALLOWED_HOSTS = [os.getenv('RAILWAY_STATIC_URL')]
    CSRF_TRUSTED_ORIGINS = [f"https://{os.getenv('RAILWAY_STATIC_URL')}"]

# For debugging purposes, print the DEBUG value to your terminal
print(f"Django DEBUG is set to: {DEBUG}")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cart',
    'store',
    'payment',
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
                'store.context_processor.categories_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecom.wsgi.application'

# --- CHANGE MADE HERE ---
# Use SQLite for development and PostgreSQL for production
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
        )
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files for development and production
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files for development and production
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Conditional storage for development vs. production
if DEBUG:
    # Use local storage in development
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
else:
    # Use Cloudinary storage in production
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
        'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
    }
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
