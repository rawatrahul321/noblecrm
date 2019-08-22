# -*- coding: utf-8 -*-

import noblecrm

def migrate(cr, version):
    registry = noblecrm.registry(cr.dbname)
    from noblecrm.addons.account.models.chart_template import migrate_set_tags_and_taxes_updatable
    migrate_set_tags_and_taxes_updatable(cr, registry, 'l10n_nl')
