"""
Django settings for mediaplayer project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0*4*^(gho+ik&8al^o&9mh-%7mp%irv+p0d@!=1yormlo1z9d%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.192.29']
INTERNAL_IPS = ('127.0.0.1','192.168.192.29','192.168.192.48')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'library.apps.LibraryConfig',
    'alarmclock.apps.AlarmclockConfig',
    'multiselectfield',
    'redis_cache',
    'django_redis',
    'django_celery_results',
    'django_celery_beat',
    'sphinxdoc',
    'haystack',
    'django_nose',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR,'logs/debug.log'),
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'library': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'alarmclock': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'validator': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'scheduler': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'utils': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'processor': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'player': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'tasks': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },

    },
}


ROOT_URLCONF = 'mediacenter.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./templates',],
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

WSGI_APPLICATION = 'mediacenter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'mediacenter.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
# success login redirct
LOGIN_REDIRECT_URL = '/media/'

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
DATETIME_FORMAT = 'Y-m-d H:i:s'     # '2006-10-25 14:30:59'


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True


#cache backend
CACHES2 = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'mediacenter_cache.sqlite3'),
            },
    'redis': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://192.168.192.26:6379/0',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

#cache backend
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://192.168.192.26:6379/0',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'CONFIG': {
            'hosts':'redis://192.168.192.26:6379/0',
            'capacity':100,
        },
        'ROUTING':'coinpricemonitor.routing.channel_routing',
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR,'mediafiles')
MEDIA_URL = '/mediafiles/'

#CELERY settings

#CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = 'redis://192.168.192.26:6379/0' # CACHES['redis']['LOCATION'] #'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://192.168.192.26:6379/0' # CACHES['redis']['LOCATION'] #'django-cache' #CACHES['default']['LOCATION'] #'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Amsterdam'
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'visibility_timeout': 180
}




# documentation

SPHINXDOC_CACHE_MINUTES = 1
SPHINXDOC_BUILD_DIR = os.path.join(BASE_DIR,'docs')

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}


# unit test setting
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=tests',
    '--cover-html',
]
