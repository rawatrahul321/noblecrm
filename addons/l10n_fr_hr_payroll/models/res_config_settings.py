# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    plafond_secu = fields.Float(related='company_id.plafond_secu', string="Plafond de la Securite Sociale")
    nombre_employes = fields.Integer(related='company_id.nombre_employes', string="Nombre d'employes")
    cotisation_prevoyance = fields.Float(related='company_id.cotisation_prevoyance', string='Cotisation Patronale Prevoyance')
    org_ss = fields.Char(related='company_id.org_ss', string="Organisme de securite sociale")
    conv_coll = fields.Char(related='company_id.conv_coll', string="Convention collective")
