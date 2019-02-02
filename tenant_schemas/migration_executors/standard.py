from tenant_schemas.migration_executors.base import MigrationExecutor, run_migrations
from tenant_schemas.utils import get_database

class StandardExecutor(MigrationExecutor):
    codename = 'standard'

    def run_tenant_migrations(self, tenants):
        for schema_name in tenants:
            self.options['database'] = get_database(schema_name)
            run_migrations(self.args, self.options, self.codename, schema_name)