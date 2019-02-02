import threading

from django.conf import settings 
from django.http import Http404
from django.db import connection, connections
from django.db import router

from tenant_schemas.utils import get_tenant_model, get_public_schema_name

from .middleware import TenantMiddleware



request_cfg = threading.local()

"""
Database selection based on URL variable
Ref: https://djangosnippets.org/snippets/2037/
"""

class MultiDBTenantMiddleware(TenantMiddleware):


    def process_request(self, request, *args, **kwargs):

        connection.set_schema_to_public()
        
        # request_cfg.db = db
        hostname = self.hostname_from_request(request)
        TenantModel = get_tenant_model()
        try:
            # get_tenant must be implemented by extending this class.
            tenant = self.get_tenant(TenantModel, hostname, request)            
            assert isinstance(tenant, TenantModel)
            database = tenant.database
        except TenantModel.DoesNotExist:
            raise self.TENANT_NOT_FOUND_EXCEPTION(
                'No tenant for {!r}'.format(request.get_host()))
        except AssertionError:
            raise self.TENANT_NOT_FOUND_EXCEPTION(
                'Invalid tenant {!r}'.format(request.tenant))

        request.tenant = tenant
        request_cfg.database = database
        connections[database].set_tenant(request.tenant)

        # Do we have a public-specific urlconf?
        if hasattr(settings, 'PUBLIC_SCHEMA_URLCONF') and request.tenant.schema_name == get_public_schema_name():
            request.urlconf = settings.PUBLIC_SCHEMA_URLCONF


    def process_response( self, request, response ):
        if hasattr(request_cfg, 'database' ):
            del request_cfg.database
        return response



from django.conf import settings

class MultiDBRouter:
    """
    A router to control which applications will be synced,
    depending if we are syncing the shared apps or the tenant apps.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label in settings.SHARED_APPS and model._meta.app_label not in settings.TENANT_APPS:
            return 'default'
        if hasattr(request_cfg, 'database'):            
            return request_cfg.database
        return None


    def db_for_write(self, model, **hints):
        if model._meta.app_label in settings.SHARED_APPS and model._meta.app_label not in settings.TENANT_APPS:
            return 'default'
        if hasattr(request_cfg, 'database'):
            return request_cfg.database
        return None