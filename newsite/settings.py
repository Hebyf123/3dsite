"""
Django settings for newsite project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv,find_dotenv
import os
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8xdvjr$a!3hth+yr8q1u%z0z61x-@f3b&b7$gen3lq3bj(u!1s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = [
    'https://glowing-boa-definite.ngrok-free.app',
    'https://example.com',
    'http://localhost:5173',
    'http://localhost:8080',

]

CORS_ALLOW_HEADERS = [
    'authorization',
    'content-type',
    'x-requested-with',
    'ngrok-skip-browser-warning', 
    'x-csrftoken', 
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

CORS_ALLOW_ALL_ORIGINS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'django_extensions',
    'django.contrib.sites',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'djoser',
    'corsheaders',
    'channels',  
    'dj_rest_auth',
    'django_filters',
    'rosetta',
    'allauth',
    'easy_thumbnails',
    'model_utils',
    'cart',
    'items',
    'usersmodel',

]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',  # 1000 запросов в день на пользователя
    },
}
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',  # "/1" - номер базы данных Redis (их может быть несколько)
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
AUTH_USER_MODEL = 'usersmodel.CustomUser'
SITE_ID = 1
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('JWT',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
STRIPE_WEBHOOK_SECRET = "whsec_ce83c486a32e1edb828bb95adf45d5e99d7e638e03325c0c3c646b81f0f6180c"

STRIPE_SECRET_KEY = 'sk_test_51Q6UI8Ca7V035Tb0Cn8M0ctf2lzUCTKWu6x09uy2npyT1J8OvhI9P6ZOAtJPsfjgI60YVSYfdTNFpXlbgh0eqbJq00NbdadbCd'
STRIPE_PUBLISHABLE_KEY = 'pk_test_51Q6UI8Ca7V035Tb0ptYEFPbdJiLQ57jEKnbT3a5QQPdXwgO36XzSil3S5HyghTae3QxFjGwAnI9zRubuGzA5Z65U00Nvpyyog5'
SESSION_ENGINE = 'django.contrib.sessions.backends.db' 
MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'allauth.account.middleware.AccountMiddleware',  
    'corsheaders.middleware.CorsMiddleware', 
    #'socialauth.middleware.ForceJSONMiddleware',
    #'items.rate_limit_middleware.RateLimitMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
DJOSER = {
    'USER_ID_FIELD': 'email',  
    'LOGIN_FIELD': 'email',  
    'SERIALIZERS': {
        'activation': 'djoser.serializers.ActivationSerializer',
        'password_reset': 'djoser.serializers.SendEmailResetSerializer',
        'password_reset_confirm': 'djoser.serializers.PasswordResetConfirmSerializer',
        'password_reset_confirm_retype': 'djoser.serializers.PasswordResetConfirmRetypeSerializer',
        'set_password': 'djoser.serializers.SetPasswordSerializer',
        'set_password_retype': 'djoser.serializers.SetPasswordRetypeSerializer',
        'set_username': 'djoser.serializers.SetUsernameSerializer',
        'set_username_retype': 'djoser.serializers.SetUsernameRetypeSerializer',
        'username_reset': 'djoser.serializers.SendEmailResetSerializer',
        'username_reset_confirm': 'djoser.serializers.UsernameResetConfirmSerializer',
        'username_reset_confirm_retype': 'djoser.serializers.UsernameResetConfirmRetypeSerializer',
        'user_create': 'usersmodel.serializers.UserCreateSerializer',  
        'user': 'usersmodel.serializers.UserSerializer', 
        'current_user': 'usersmodel.serializers.UserSerializer',
        'user_create_password_retype': 'djoser.serializers.UserCreatePasswordRetypeSerializer',
        'user_delete': 'djoser.serializers.UserDeleteSerializer',
        'token': 'djoser.serializers.TokenSerializer',
        'token_create': 'djoser.serializers.TokenCreateSerializer',
    },
    'PERMISSIONS': {
        'user_list': [
            'rest_framework.permissions.AllowAny'
        ],
    },
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': [
        'http://127.0.0.1:8000',
    ],
    'BLACKLIST_AFTER_ROTATION': True,  # Блокировка токена после ротации
    'UPDATE_LAST_LOGIN': True,  # Обновление последнего входа
    'SEND_ACTIVATION_EMAIL': True,  
    'SEND_CONFIRMATION_EMAIL': True,  
    'PASSWORD_RESET_CONFIRM_RETYPE': True,  
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': False,  
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,  
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset-confirm/{uid}/{token}',  # URL для сброса пароля
    'ACTIVATION_URL': 'activate/{uid}/{token}',  # URL для активации пользователя
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',  


    'PASSWORD_VALIDATORS': [
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            'OPTIONS': {
                'min_length': 8,
            }
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MaximumLengthValidator',
            'OPTIONS': {
                'max_length': 64,
            }
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumUpperCaseValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLowerCaseValidator',
        },
    ],
    }
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ROOT_URLCONF = 'newsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'newsite.wsgi.application'

from django.utils.log import DEFAULT_LOGGING

LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {name} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django_info.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django_errors.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['error_file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['django.server', 'error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
AUTHLIB_OAUTH_CLIENTS = {
    'google': {
        'client_id': 'ВАШ_GOOGLE_CLIENT_ID',
        'client_secret': 'ВАШ_GOOGLE_CLIENT_SECRET',
        'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
        'token_url': 'https://accounts.google.com/o/oauth2/token',
        'userinfo_endpoint': 'https://www.googleapis.com/oauth2/v3/userinfo',
        'client_kwargs': {
            'scope': 'openid profile email',
        },
    },

}



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
ASGI_APPLICATION = 'newsite.asgi.application'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGES = [
    ('en', _('English')),
    ('ua', _('Ukraine')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',  
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

BASE_DIR = Path(__file__).resolve().parent.parent


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
