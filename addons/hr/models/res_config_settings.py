# -*- coding: utf-8 -*-

from noblecrm import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    resource_calendar_id = fields.Many2one(
        'resource.calendar', 'Company Working Hours',
        related='company_id.resource_calendar_id')
    module_hr_org_chart = fields.Boolean(string="Show Organizational Chart")
