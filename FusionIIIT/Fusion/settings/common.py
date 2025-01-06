'''
Django settings for Fusion project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
'''
import os

from celery.schedules import crontab

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
CLIENT_ID = '187004491411-frc3j36n04o9k0imgnbl02qg42vkq36f.apps.googleusercontent.com'
CLIENT_SECRET = 'enHu3RD0yBvCM_9C0HQmEp0z'
# SECURITY WARNING: don't run with debug turned on in production!

# Google authentication
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'hd': 'iiitdmj.ac.in',
        }
    }
}

# allauth settings

LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/dashboard'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'

# email of sender

EMAIL_HOST_USER = 'fusionmailservice@iiitdmj.ac.in'

EMAIL_PORT = 587
ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

ACCOUNT_CONFIRM_EMAIL_ON_GET = False

ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/accounts/login/'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True

ACCOUNT_EMAIL_VERIFICATION = 'optional'

ACCOUNT_EMAIL_SUBJECT_PREFIX = 'Fusion: '

DEFAULT_FROM_EMAIL = 'Fusion IIIT <fusionmailservice@iiitdmj.ac.in>'

SERVER_EMAIL = 'fusionmailservice@iiitdmj.ac.in'

ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_USERNAME_MIN_LENGTH = 3

SOCIALACCOUNT_ADAPTER = 'applications.globals.adapters.MySocialAccountAdapter'


# CELERY STUFF
# CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Calcutta'
CELERY_BEAT_SCHEDULE = {
    'leave-migration-task': {
        'task': 'applications.leave.tasks.execute_leave_migrations',
        'schedule': crontab(minute='1', hour='0')
    }
}

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django_crontab',
    'corsheaders',

    'applications.eis',
    'notification',
    'notifications',
    'applications.academic_procedures',
    'applications.examination',
    'applications.academic_information',
    'applications.leave',
    'applications.library',
    'applications.notifications_extension',
    'applications.gymkhana',
    'applications.office_module',
    'applications.globals',
    'applications.central_mess',
    'applications.complaint_system',
    'applications.filetracking',
    'applications.finance_accounts',
    'applications.health_center',
    'applications.online_cms',
    'applications.ps1',
    'applications.programme_curriculum',
    'applications.placement_cell',
    'applications.otheracademic',
    'applications.recruitment',
    'applications.scholarships',
    'applications.visitor_hostel',
    'applications.establishment',
    'applications.estate_module',
    'applications.counselling_cell',
    'applications.hostel_management',
    'applications.research_procedures',
    'applications.income_expenditure',
    'applications.hr2',
    'applications.department',
    'applications.iwdModuleV2',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    'semanticuiforms',
    'applications.feeds.apps.FeedsConfig',
    'pagedown',
    'markdown_deux',
    'django_cleanup.apps.CleanupConfig',
    'django_unused_media',
    'rest_framework',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Fusion.middleware.custom_middleware.user_logged_in_middleware',
]

ROOT_URLCONF = 'Fusion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '..', 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Fusion.context_processors.global_vars',
            ],
        },
    },
]

WSGI_APPLICATION = 'Fusion.wsgi.application'

# Database template for mysql

# DATABASES = {
#     'default':
#         {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'test',
#             'USER': 'root',
#             'PASSWORD': 'sksingh55',
#             'HOST': 'localhost',
#             'PORT': '3306',
#         },
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(PROJECT_DIR, 'fusion.db'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


AUTHENTICATION_BACKENDS = (
    # Default backend -- used to login by username in Django admin
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = False

USE_TZ = False

SITE_ID = 1
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/


# os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
MEDIA_URL = '/media/'

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
LOGIN_REDIRECT_URL = "/"

DJANGO_NOTIFICATIONS_CONFIG = {
    'USE_JSONFIELD': True,
}

DJANGO_NOTIFICATIONS_CONFIG = {
    'USE_JSONFIELD': True,
}

CRISPY_TEMPLATE_PACK = 'semantic-ui'
CRISPY_ALLOWED_TEMPLATE_PACKS = ('semantic-ui')
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240
YOUTUBE_DATA_API_KEY = 'api_key'



CORS_ORIGIN_ALLOW_ALL = True
ALLOW_PASS_RESET = True

# session settings
SESSION_COOKIE_AGE = 15 * 60
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True