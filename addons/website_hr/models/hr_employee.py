# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import api, fields, models

class HrEmployee(models.Model):
    _name = 'hr.employee'
    _inherit = ['hr.employee', 'website.published.mixin']

    public_info = fields.Char(string='Public Info')

    @api.multi
    def _compute_website_url(self):
        super(HrEmployee, self)._compute_website_url()
        for employee in self:
            employee.website_url = '/aboutus#team'
