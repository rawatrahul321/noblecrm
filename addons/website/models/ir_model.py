# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details

from noblecrm import api, models


# This is a nasty hack, targeted for V11 only
class IrModel(models.Model):
    _inherit = 'ir.model'

    @api.multi
    def unlink(self):
        self.env.cr.execute("DELETE FROM ir_model_fields WHERE name='website_id'")
        self.env.cr.execute("DELETE FROM res_config_settings WHERE website_id IS NOT NULL")
        return super(IrModel, self).unlink()
