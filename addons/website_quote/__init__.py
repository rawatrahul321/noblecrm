# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from . import controllers
from . import models

from noblecrm.api import Environment, SUPERUSER_ID

def _install_sale_payment(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    env['ir.module.module'].search([
        ('name', '=', 'sale_payment'),
        ('state', '=', 'uninstalled'),
    ]).button_install()
