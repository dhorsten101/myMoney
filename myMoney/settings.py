import json
import os
from pathlib import Path

from decouple import config
from django.contrib import staticfiles
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

LUNO_API_KEY = "kc8yscuuw72cm"
LUNO_API_SECRET = "rLB2aJAt-DRysys6Hvh2Kg__Qw1M2SWKf9m8qnnAQrQ"

BINANCE_API_KEY = "8DYDIi3BXx8SANk7pCUX1VBA8VEvxTtxMg78dk04418ctILHetrjD7QVkwKfZNDt"
BINANCE_SECRET_KEY = "PiVTqEjitltvVXb1Zw6KSRQmBKe1LtZsz0MfqmPwv3gohoOLbGTBFfC3PFvhPN0N"

SECRET_KEY = "django-insecure-$)^1s5m&dj6vf0b29a+^6wjli1i)o=wi$99yo0&j4vo!loz&dh"

OPENAI_API_KEY = config("OPENAI_API_KEY")
STORMGLASS_API_KEY = config("STORMGLASS_API_KEY")

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"django.contrib.staticfiles",
	"django.contrib.humanize",
	"widget_tweaks",
	"django_crontab",
	"django_extensions",
	"channels",
	'django_ckeditor_5',
	"api",
	"cryptos",
	"incomes",
	"credits",
	"expenses",
	"history_records",
	"main",
	"sellables",
	"to_do",
	"weight",
	"ideas",
	"worth",
	"documents",
	"folders",
	"metrics",
	"logs",
	"llm",
	"weather",
	"system",
	"monitoring",
	"cameras",
	"pen_tester",
	"reminders",
]

# CKEditor 5 config
CKEDITOR_5_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

CKEDITOR_5_CONFIGS = {
	"default": {
		"toolbar": ["heading", "|", "bold", "italic", "link", "bulletedList", "numberedList", "blockQuote", "imageUpload"],
		"language": "en",
	}
}

MIDDLEWARE = [
	"django.middleware.security.SecurityMiddleware",
	"django.contrib.sessions.middleware.SessionMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
	"django.middleware.clickjacking.XFrameOptionsMiddleware",
	"crum.CurrentRequestUserMiddleware",
	"logs.query_profiler.QueryProfilerMiddleware",
]

SLOW_QUERY_THRESHOLD = 1.0

CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
	'https://192.168.0.100',
	'http://192.168.0.100',
	'https://192.168.0.100',
]

ROOT_URLCONF = "myMoney.urls"

TEMPLATES = [
	{
		"BACKEND": "django.template.backends.django.DjangoTemplates",
		"DIRS": [BASE_DIR / "templates"],
		"APP_DIRS": True,
		"OPTIONS": {
			"context_processors": [
				"django.template.context_processors.debug",
				"django.template.context_processors.request",
				"django.contrib.auth.context_processors.auth",
				"django.contrib.messages.context_processors.messages",
				'system.context_processors.version_info',
			],
		},
	},
]

WSGI_APPLICATION = "myMoney.wsgi.application"
ASGI_APPLICATION = "myMoney.asgi.application"

CHANNEL_LAYERS = {
	"default": {
		"BACKEND": "channels_redis.core.RedisChannelLayer",
		"CONFIG": {
			"hosts": [{
				"address": "redis://127.0.0.1:6379",
				# "password": "Wu!",
			}],
		},
	},
}

DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.sqlite3",
		"NAME": BASE_DIR / "db.sqlite3",
	}
}

AUTH_PASSWORD_VALIDATORS = [
	{
		"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
	},
	{
		"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
	},
	{
		"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
	},
	{
		"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
	},
]

SESSION_ENGINE = "django.contrib.sessions.backends.db"

# Redirect user after login
LOGIN_REDIRECT_URL = "home"

# Redirect user to login page if not authenticated
LOGIN_URL = "login"

# Logout URL
LOGOUT_REDIRECT_URL = "/"

LANGUAGE_CODE = "en-us"

TIME_ZONE = 'Africa/Johannesburg'
USE_TZ = True
USE_I18N = True

# STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
STATICFILES_DIRS = [
	BASE_DIR / "static",
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_FROM_EMAIL = "dhorsten101@gmail.com"
CONTACT_EMAIL = "dhorsten101@gmail.com"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # Use SMTP in prod

try:
	with open(BASE_DIR / "version.json") as f:
		VERSION = json.load(f)
except Exception:
	VERSION = {
		"version": "unknown",
		"commit": "-",
		"branch": "-",
		"message": "",
		"build_date": "-"
	}

# Email configuration
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'yourgmail@gmail.com'  # your Gmail address
# EMAIL_HOST_PASSWORD = 'your-app-password'  # the 16-char app password
#
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# CONTACT_EMAIL = 'support@yourdomain.com'  # wherever you want to receive emails

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	
	'formatters': {
		'verbose': {
			'format': '[{levelname}] {asctime} {name}: {message}',
			'style': '{',
		},
	},
	
	'handlers': {
		'db': {
			'level': 'ERROR',
			'class': 'main.handlers.DBLogHandler',
		},
	},
	
	'loggers': {
		'django': {
			'handlers': ['db'],
			'level': 'ERROR',
			'propagate': True,
		},
		'myMoney': {
			'handlers': ['db'],
			'level': 'DEBUG',
			'propagate': False,
		},
	},
	
	'root': {
		'handlers': ['db'],
		'level': 'WARNING',
	},
}
