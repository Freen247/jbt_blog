"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.0.10.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import datetime
import os
from apps.utils.handler import get_local_host_ip
from datetime import timedelta
try:
    from apps.passwords import EMAIL_PD, POSTGRESQL_PD
except:
    print('↓'*20)
    print('网站所需要的密码请重新定义')
    print('↑'*20)
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)
VUE_WEB_DIR = os.path.join(
    os.path.dirname(BASE_DIR), 'Vue_web')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1ek)3z+-*)(&1c&3fv=2*=lr_cyGst85w&a4y#5!2m*ik@=&!p0'

# SECURITY WARNING: don't run with debug turned on in production!

# 自由选择需要开启的功能
# 是否开始[在线工具]应用
# TOOL_FLAG = True
# # 是否开启[API]应用
# API_FLAG = False
# DEBUG模式是否开始的选择
# 值为0：所有平台关闭DEBUG,值为1:所有平台开启DEBUG,值为其他：根据平台类型判断开启（默认设置的Windows下才开启）
# DEBUG = True
# # 默认状态 COMPRESS_ENABLED=False，因为生产环境 DEBUG=False
# # 只有在生产环境才有压缩静态资源的需求
# # 如果是开发环境就主动开启压缩功能、开启手动压缩功能
# if DEBUG:
#     COMPRESS_ENABLED = True  # 开启压缩功能
#     COMPRESS_OFFLINE = True  # 开启手动压缩
# else:
#     DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = ['*']

SYSTEM_HOST = get_local_host_ip()
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'crispy_forms',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # lib
    'imagekit',  # 注册 imagekit处理压缩图片
    'mdeditor',  # django mdeditor富文本编辑器
    'django.contrib.sitemaps',  # 网站地图
    'uuslug',  # 将中文转化成拼音 slug 的插件
    'markdown',  # python自带的md翻译工具
    # allauth需要注册的应用
    'django.contrib.auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # github 登陆
    'allauth.socialaccount.providers.github',
    # 搜索
    'haystack',
    # 压缩
    'compressor',
    # rest框架
    'rest_framework',
    # 分页
    'pure_pagination',
    # django3 异步
    'djcelery'
]

# 自动添加app
APPS_FLODER = os.path.join(BASE_DIR, 'apps')
APPS = [_ for _ in os.listdir(APPS_FLODER) if os.path.isdir(
    os.path.join(APPS_FLODER, _)) and 'pycache' not in _]
INSTALLED_APPS += ['apps.'+_ for _ in APPS]

# restframework settings
REST_FRAMEWORK = {
    # 配置报错路由
    'EXCEPTION_HANDLER': 'apps.api_exception.exception_process',
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.AllowAny',
    # ),
    # 设置 DEFAULT_PAGINATION_CLASS 后，将全局启用分页，所有 List 接口的返回结果都会被分页。如果想单独控制每个接口的分页情况，可不设置这个选项，而是在视图函数中进行配置
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 这个选项控制分页后每页的资源个数
    'PAGE_SIZE': 20,
    # 接口限流
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/min',
        # 版本管理
        'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
        'DEFAULT_VERSION': 'v1'
        # 以上两项设置分别全局指定使用的 API 版本管理方式和客户端缺省版本号的情况下默认请求的 API 版本。尽管这些配置项也可以在单个视图或者视图集的范围内指定，但是，统一的版本管理模式更为可取，因此我们在全局配置中指定。
    },
    # jwt登陆机制
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # JWT认证
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # Session认证
        # 'rest_framework.authentication.SessionAuthentication',
        # # Basic认证
        # 'rest_framework.authentication.BasicAuthentication',
    ),

}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    # https://django-rest-framework-simplejwt.readthedocs.io/en/latest/token_types.html
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.SlidingToken','rest_framework_simplejwt.tokens.SlidingToken'),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
# 日志
# [process:%(process)d %(threadName)s-thread:%(thread)d]
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    # 'filters': {
    #     'require_debug_false': {
    #         '()': 'django.utils.logging.RequireDebugFalse',
    #     },
    #     'require_debug_true': {
    #         '()': 'django.utils.logging.RequireDebugTrue',
    #     },
    # },
    'formatters': {
        'django.server': {
            'format': '%(pathname)s:%(lineno)s %(asctime)s %(levelname)s\n%(message)s',
            # 'style': '{',
        },
        'console_format': {
            'format': '%(color)s\n%(pathname)s:%(lineno)s %(asctime)s %(levelname)s\n%(message)s',
            # 'style': '{',
        },
        'file_format': {
            'format': '%(pathname)s:%(lineno)s %(asctime)s %(levelname)s\n%(message)s',
            # 'style': '{',
        }
    },
    'handlers': {
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/info_{}.log'.format(datetime.datetime.now().date())),
            'formatter': 'file_format',
        },
        'console': {
            # 'filters': ['require_debug_false'],
            'level': 'INFO',
            'class': 'apps.utils.logging.handler.ColorHandler',
            # 'class': 'logging.StreamHandler',
            'formatter': 'console_format',
        },
    },

    'loggers': {
        'apps': {
            # 'handlers': ['file','console'],
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['django.server', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# 如果需要在本地压缩，需要在settings.py中添加 COMPRESS_OFFLINE=True才能执行下边命令手动压缩
COMPRESS_OFFLINE = True
# mdeditor
MDEDITOR_CONFIGS = {
    'default': {
        'width': '90% ',  # Custom edit box width
        'heigth': 500,  # Custom edit box height
        'toolbar': ["undo", "redo", "|",
                    "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                    "h1", "h2", "h3", "h5", "h6", "|",
                    "list-ul", "list-ol", "hr", "|",
                    "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime"
                    "emoji", "html-entities", "pagebreak", "goto-line", "|",
                    "help", "info",
                    "||", "preview", "watch", "fullscreen"],  # custom edit box toolbar
        # image upload format type
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
        'image_floder': 'mdeditor/article',  # image save the folder name
        'theme': 'default',  # edit box theme, dark / default
        'preview_theme': 'default',  # Preview area theme, dark / default
        'editor_theme': 'default',  # edit area theme, pastel-on-dark / default
        'toolbar_autofixed': True,  # Whether the toolbar capitals
        'search_replace': True,  # Whether to open the search for replacement
        'emoji': True,  # whether to open the expression function
        'tex': True,  # whether to open the tex chart function
        'flow_chart': True,  # whether to open the flow chart function
        'syncScrolling': 'single',
        'sequence': True,  # Whether to open the sequence diagram function
    }
}
# 搜索配置
HAYSTACK_CONNECTIONS = {
    'default': {
        # 选择语言解析器为自己更换的结巴分词
        'ENGINE': 'apps.search.haystack_search_engin.WhooshEngine',
        # 保存索引文件的地址，选择主目录下，这个会自动生成
        'PATH': os.path.join(APPS_FLODER, 'search', 'whoosh_index'),
    },
}
# 指定什么时候更新索引，这里定义为每当有文章更新时就更新索引。由于博客文章更新不会太频繁，因此实时更新没有问题。
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# 防止标题被截断
HAYSTACK_CUSTOM_HIGHLIGHTER = 'apps.search.Highlighter'

CACHES = {
    "default": {
        # redis缓存配置
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{redis_ip}:{port}/1".format(redis_ip=SYSTEM_HOST, port='6379'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    # }
}

# 登陆成功后的回调路由
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
AUTHENTICATION_BACKENDS = (
    # django默认的身份验证
    'django.contrib.auth.backends.ModelBackend',
    # allauth身份验证
    'allauth.account.auth_backends.AuthenticationBackend',
)


# 网站信息设置 用于SEO
SITE_DESCRIPTION = "Stray_Camel的个人技术博客，config，django2.0+python3技术搭建。"
SITE_KEYWORDS = "Stray_Camel,django2.0博客，人工智能,网络,IT,技术,博客,Python"

AUTHOR_NAME = "Stray_Camel"
AUTHOR_DESC = 'early to bed, early to rise.'
AUTHOR_EMAIL = 'aboyinsky@outlook.com'
AUTHOR_TITLE = 'rookie'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'config',
#         'USER': 'postgres',
#         'PASSWORD': POSTGRESQL_PD,
#         'HOST': '127.0.0.1',
#         'PORT': '5432'
#     }
# }

# 使用django设置将错误报告发送到指定邮箱
# 发送邮件尽量使用send_mass_mail:https://docs.djangoproject.com/en/2.1/topics/email/
ADMINS = (('stray_camel', '1351975058@qq.com'))
# Email setting
# SMTP服务器，我使用的是sendclound的服务
# 邮件是否启用安全协议，与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false
#EMAIL_USE_SSL = True
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.outlook.com'
# EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'aboyinsky@outlook.com'
EMAIL_HOST_PASSWORD = EMAIL_PD
DEFAULT_FROM_EMAIL = 'aboyinsky@outlook.com'
# 邮件发送后端
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# 这里是随便写的一个 也可以是 /accounts/logsout/ 测试比较随便
LOGIN_REDIRECT_URL = '/'
# 要求用户注册时必须填写email
ACCOUNT_EMAIL_REQUIRED = True
# 注册中邮件验证方法:“强制（mandatory）”,“可选（optional）【默认】”或“否（none）”之一。
# 开启邮箱验证的话，如果邮箱配置不可用会报错，所以默认关闭，根据需要自行开启
ACCOUNT_EMAIL_VERIFICATION = "optional"
# 作用于第三方账号的注册
# SOCIALACCOUNT_EMAIL_VERIFICATION = 'optional' | 'mandatory' | 'none'
# 邮件发送后的冷却时间(以秒为单位)
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 10
# # 邮箱确认邮件的截止日期(天数)
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1

# # 指定要使用的登录方法(用户名、电子邮件地址或两者之一)"username" | "email" | "username_email"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
# # 登录尝试失败的次数
# ACCOUNT_LOGIN_ATTEMPTS_LIMIT(=5)
# # 从上次失败的登录尝试，用户被禁止尝试登录的持续时间
# ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT(=300)
# # 更改为True，用户一旦确认他们的电子邮件地址，就会自动登录
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# # 更改或设置密码后是否自动退出
# ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE(=False)
# 更改为True，用户将在重置密码后自动登录
# ROOT_URLCONF = 'blog.urls'

AUTH_USER_MODEL = 'accounts.Ouser'

MIDDLEWARE = [
<<<<<<< HEAD
    'apps.utils.corsheaders.middleware.CorsMiddleware',
=======
    # 允许跨域请求
    'apps.utils.core.corsheaders.middleware.CorsMiddleware',
    # Django 中间件
>>>>>>> 4b14ef293b084790e6fd92b7886246dcd59eb6f1
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    '*'
)
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)
db_table = 'user'
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [VUE_WEB_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 全局变量
                'apps.index.views.global_setting',
                # allauth 需要 django 提供这个处理器
                'django.template.context_processors.request',
            ],
        },
    },
]
# 位于django.contrib.sites的site。
# SITE_ID指定与特定配置文件相关联的site对象之数据库的ID。
# 当出现"SocialApp matching query does not exist"，这种报错的时候就需要更换这个ID
SITE_ID = 1
WSGI_APPLICATION = 'config.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# 使用上海的UTC时间。
LANGUAGE_CODE = 'zh-hans'  # 有改动

TIME_ZONE = 'Asia/Shanghai'  # 有改动

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',)
# 静态文件收集
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# 媒体文件
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# 统一分页设置
# 指定如何对搜索结果分页，这里设置为每 2 项结果为一页。
BASE_PAGE_BY = 7
BASE_ORPHANS = 4

# django-pure-pagination 分页设置
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 4,  # 分页条当前页前后应该显示的总页数（两边均匀分布，因此要设置为偶数），
    'MARGIN_PAGES_DISPLAYED': 1,  # 分页条开头和结尾显示的页数
    'SHOW_FIRST_PAGE_WHEN_INVALID': False,  # 当请求了不存在页，显示第一页
}

# 网站上线时长
ONLINE_TIME_DAYS = (datetime.datetime.now() -
                    datetime.datetime(2018, 1, 1)).days

# django网站国际化
USE_I18N = True
