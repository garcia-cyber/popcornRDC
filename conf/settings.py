"""
Django settings for conf project, adapted for production deployment on Render.
"""

from pathlib import Path
import os
import dj_database_url # Nécessite 'pip install dj-database-url psycopg2-binary'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- 1. SECURITY AND DEBUGGING (PRODUCTION CONFIG) ---

# CRITIQUE : Toujours charger la SECRET_KEY depuis les variables d'environnement.
# Si SECRET_KEY n'est pas définie dans l'ENV, l'application ne démarrera PAS (sécurité).
SECRET_KEY = os.environ.get('SECRET_KEY')

# DEBUG: Charger la valeur depuis l'ENV, avec une valeur par défaut 'False'.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# CRITIQUE : ALLOWED_HOSTS doit également être chargé depuis l'ENV pour la flexibilité.
# J'ai ajouté un fallback pour le développement local si DEBUG est True.
if DEBUG:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'popcornrdc.onrender.com']
else:
    # Récupère tous les hôtes autorisés depuis la variable d'environnement (séparés par des virgules)
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')


# CRITIQUE : CSRF_TRUSTED_ORIGINS doit aussi être chargé depuis l'ENV.
# Render fournit la variable (ou vous devez la définir)
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app' , 
]

MIDDLEWARE = [
    # WhiteNoise doit être placé juste après SecurityMiddleware.
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Pour servir les statiques en prod
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'


# --- 2. DATABASE CONFIG (POSTGRESQL FOR RENDER) ---

# Par défaut (pour le développement local si DEBUG=True)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Si DEBUG est False (production), on configure la connexion PostgreSQL
# en utilisant la variable d'environnement DATABASE_URL fournie par Render.
if not DEBUG:
    # Utilisez dj_database_url pour analyser la chaîne de connexion
    # On vérifie si DATABASE_URL existe avant d'essayer de la configurer
    if os.environ.get('DATABASE_URL'):
        DATABASES['default'] = dj_database_url.config(
            conn_max_age=600, 
            ssl_require=True # Exigé par Render pour les connexions sécurisées
        )


# Password validation
# (Reste inchangé)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# --- 3. STATIC FILES (WHITENOISE CONFIG) ---
# WhiteNoise gérera ces fichiers en production.
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
 BASE_DIR / 'static' 
] 


# Configuration de WhiteNoise pour la gestion des statiques en production.
if not DEBUG:
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }


# Auth URLs (Reste inchangé)
LOGIN_REDIRECT_URL = '/dashboard/' 
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/home/' 


# Media files (Fichiers utilisateurs)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'