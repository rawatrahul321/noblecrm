# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import fields, models


class Website(models.Model):

    _inherit = "website"

    channel_id = fields.Many2one('im_livechat.channel', string='Website Live Chat Channel')
