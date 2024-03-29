# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        rule = self.env.ref('delivery.delivery_carrier_comp_rule', False)
        if rule:
            rule.write({'active': not bool(self.company_share_product)})
