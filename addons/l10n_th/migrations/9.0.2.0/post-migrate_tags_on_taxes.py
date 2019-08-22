from noblecrmerp.modules.registry import RegistryManager

def migrate(cr, version):
    registry = RegistryManager.get(cr.dbname)
    from noblecrmerp.addons.account.models.chart_template import migrate_tags_on_taxes
    migrate_tags_on_taxes(cr, registry)
