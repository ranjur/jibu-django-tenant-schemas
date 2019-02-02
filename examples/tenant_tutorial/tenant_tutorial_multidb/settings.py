from tenant_tutorial.settings import *

DATABASES = {
    'default':{
        'ENGINE': 'tenant_schemas.postgresql_backend',
        'NAME': 'dts_test_project',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    },
    'db1': {
        'ENGINE': 'tenant_schemas.postgresql_backend',
        'NAME': 'dts_test_project1',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    },
    'db2': {
        'ENGINE': 'tenant_schemas.postgresql_backend',
        'NAME': 'dts_test_project2',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

WSGI_APPLICATION = 'tenant_tutorial_multidb.wsgi.application'

DATABASE_ROUTERS += ('tenant_schemas.multidb.MultiDBRouter',)


MIDDLEWARE_CLASSES = (
    'tenant_schemas.multidb.MultiDBTenantMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


