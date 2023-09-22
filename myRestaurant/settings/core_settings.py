from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


AUTH_USER_MODEL='account.UserBase'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


SESSION_COOKIE_AGE = 86400
CART_SESSION_ID = 'chats'

SUBCRIPTION_TIMEOUT = 3


INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'apps.core',
    'apps.account',
    'apps.account_api',
    'apps.product_api',
    'apps.checkout_api',
    'apps.vendor_api',
    'apps.product',
    'apps.order',
    'apps.cart',
    'apps.checkout',
    'apps.vendor',
]
PAYSTACK_PUBLIC_KEY =  os.getenv("PAYSTACK_PUBLIC_KEY")
PAYSTACK_SECRET_KEY =  os.getenv("PAYSTACK_SECRET_KEY")
FLUTTERWAVE_PUBLIC_KEY = os.getenv("FLUTTERWAVE_PUBLIC_KEY")
FLUTTERWAVE_SECRET_KEY = os.getenv("FLUTTERWAVE_SECRET_KEY")


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]


# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:80',
#     'http://localhost:8000',
#     'http://127.0.0.1:8000',
# ]
# CORS_ALLOWED_METHODS = [
#     'DELETE', 'GET', 
#     'OPTIONS', "PATCH", 
#     "POST", "PUT"
# ]
# CORS_ALLOW_HEADERS = [
#     'accept', 'accept-encoding', 'authorization',
#     'content-type', 'dnt', 'origin', 'user-agent', 
#     'x-csrftoken', 'x-requested-with', 'x-frame-options',
#      'content-encoding',  'transfer-encoding', 'connection', "x-runtime"
# ]

# REST_FRAMEWORK = {'DEFAULT_PERMISSION_CLASSES': [
#     'rest_framework.permissions.AllowAny',
#     # 'rest_framework.authentication.TokenAuthentication'
# ]}
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.authentication.TokenAuthentication'
    ],
}
CORS_ORIGIN_ALLOW_ALL = True

from datetime import timedelta
api_settings = {
# SIMPLE_JWT = {
     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
     'ROTATE_REFRESH_TOKENS': True,
     'BLACKLIST_AFTER_ROTATION': True,

     'ALGORITHM': 'HS256',
     'SIGNING_KEY': SECRET_KEY,
     'VERIFYING_KEY': None,
     'AUDIENCE': None,
     'ISSUER': None,

     'AUTH_HEADER_TYPES':('Bearer', 'JWT'),
     'USER_ID_FIELD': 'id',
     'USER_ID_CLAIM': 'user_id',
 
     'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken'),
     'TOKEN_TYPE_CLAIM': 'token_type',

     'JTI_CLAIM': 'jti',

     'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
     'SLIDING_TOKEN_LIFETIME': timedelta(days=5),
     'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ORIGINS_WHITELIST = [
#     'http://localhost:80',
#     'http://localhost:8000',
#     'http://127.0.0.1:8000',
# ]
# CORS_EXPOSE_HEADERS = [
#     'http://localhost:80',
#     'http://localhost:8000',
#     'http://127.0.0.1:8000',
# ]

ROOT_URLCONF = 'myRestaurant.urls'

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
                'apps.cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'myRestaurant.wsgi.application'

DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.getenv("PGDATABASE"),
#         'USER': os.getenv("PGUSER"),
#         "PASSWORD": os.getenv("PGPASSWORD"),
#         "HOST": os.getenv("PGHOST"),
#         "PORT": os.getenv("PGPORT"),
#     }
# }
DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
}


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS=[
    BASE_DIR / 'static'
]
STATIC_ROOT = os.path.join(BASE_DIR, "static", "staticfiles_build", "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MPTT_ADMIN_LEVEL_INDENT = 20

