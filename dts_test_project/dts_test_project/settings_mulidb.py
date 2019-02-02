from .settings import *


DATABASES = {
    'default': {
        'ENGINE': 'tenant_schemas.postgresql_backend',
        'NAME': os.environ.get('PG_NAME', 'dts_test_project'),
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': int(os.environ.get('PG_PORT')) if os.environ.get('PG_PORT') else None,
    },
    'db1': {
        'ENGINE': 'tenant_schemas.postgresql_backend',
        'NAME': os.environ.get('PG_NAME', 'dts_test_project1'),
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': int(os.environ.get('PG_PORT')) if os.environ.get('PG_PORT') else None,
    },
    'db2': {
        'ENGINE': 'tenant_schemas.postgresql_backend',
        'NAME': os.environ.get('PG_NAME', 'dts_test_project2'),
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': int(os.environ.get('PG_PORT')) if os.environ.get('PG_PORT') else None,
    },

}
