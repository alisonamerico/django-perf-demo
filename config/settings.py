import logging
import socket
from pathlib import Path

import dj_database_url
from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Segurança ─────────────────────────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv()
)

# ── Apps ──────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'silk',
    'store',
]

MIDDLEWARE = [
    'store.middleware.QueryCountMiddleware',  # PRIMEIRO - captura queries iniciais
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'silk.middleware.SilkyMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.query_count',
            ],
        },
    },
]

# ── Banco de dados ────────────────────────────────────────────────────────────
DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_HOST = config('DB_HOST', default='localhost')
DB_PORT = config('DB_PORT', default=5432, cast=int)

DATABASES = {
    'default': dj_database_url.parse(
        f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
        conn_max_age=config('DB_CONN_MAX_AGE', default=600, cast=int),
    )
}

# ── Internationalization ───────────────────────────────────────────────────────
LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True
LANGUAGES = [
    ('en', 'English'),
    ('pt-BR', 'Português (Brasil)'),
]
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# ── Static files ─────────────────────────────────────────────────────────────────
STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Django Debug Toolbar ──────────────────────────────────────────────────────
# Debug Toolbar requires client IP to be in this list.
# In Docker, we try to detect the container IP automatically.
BASE_IPS = [
    '127.0.0.1',
    'localhost',
]

# Add common Docker bridge networks
for i in range(1, 30):
    BASE_IPS.append(f'172.{i}.0.1')

BASE_IPS.append('host.docker.internal')

# Start with base IPs
INTERNAL_IPS = list(BASE_IPS)

# Add any extra IPs from environment
extra = config('INTERNAL_IPS', default='')
if extra:
    for ip in extra.split(','):
        ip = ip.strip()
        if ip and ip not in INTERNAL_IPS:
            INTERNAL_IPS.append(ip)

# Try to add container IPs automatically
try:
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    for ip in ips:
        if ip not in INTERNAL_IPS:
            INTERNAL_IPS.append(ip)
except Exception:
    pass

# ── Silk ──────────────────────────────────────────────────────────────────────
SILKY_PYTHON_PROFILER = config(
    'SILKY_PYTHON_PROFILER', default=True, cast=bool
)

# ── Logging ─────────────────────────────────────────────────────────────────
if DEBUG:
    logging.basicConfig()
    logging.getLogger('django.db.backends').setLevel(logging.DEBUG)
