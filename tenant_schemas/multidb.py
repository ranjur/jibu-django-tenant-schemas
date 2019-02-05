import threading

from django.conf import settings 
from django.http import Http404
from django.db import connections

from tenant_schemas.utils import app_labels, get_tenant_model, get_public_schema_name, get_db_from_connections

from .middleware import TenantMiddleware



request_cfg = threading.local()

"""
Database selection based on URL variable
Ref: https://djangosnippets.org/snippets/2037/
"""

class MultiDBTenantMiddleware(TenantMiddleware):


    def process_request(self, request, *args, **kwargs):

        for db in settings.DATABASES.keys():
            connections[db].set_schema_to_public()
        
        hostname = self.hostname_from_request(request)
        TenantModel = get_tenant_model()
        try:
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





class MultiDBRouter:
    """
    A router to control which applications will be synced,
    depending if we are syncing the shared apps or the tenant apps.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label in app_labels(settings.SHARED_APPS) and \
            model._meta.app_label not in app_labels(settings.TENANT_APPS):
            return 'default'
        return get_db_from_connections()


    def db_for_write(self, model, **hints):
        if model._meta.app_label in app_labels(settings.SHARED_APPS) and \
            model._meta.app_label not in app_labels(settings.TENANT_APPS):
            return 'default'
        return get_db_from_connections()