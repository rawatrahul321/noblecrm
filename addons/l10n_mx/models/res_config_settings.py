# -*- coding: utf-8 -*-

from noblecrm import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_l10n_mx_edi = fields.Boolean('Mexican Electronic Invoicing')
