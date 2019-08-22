# -*- coding: utf-8 -*-

from noblecrm import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    stock_move_id = fields.Many2one('stock.move', string='Stock Move')

