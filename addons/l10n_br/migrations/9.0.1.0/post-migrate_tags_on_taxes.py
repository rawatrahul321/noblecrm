# -*- coding: utf-8 -*-

import noblecrm

def migrate(cr, version):
    registry = noblecrm.registry(cr.dbname)
    from noblecrm.addons.account.models.chart_template import migrate_tags_on_taxes
    migrate_tags_on_taxes(cr, registry)
