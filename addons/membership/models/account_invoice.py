# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import api, fields, models


class Invoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_cancel_draft(self):
        self.env['membership.membership_line'].search([
            ('account_invoice_line', 'in', self.mapped('invoice_line_ids').ids)
        ]).write({'date_cancel': False})
        return super(Invoice, self).action_cancel_draft()

    @api.multi
    def action_cancel(self):
        '''Create a 'date_cancel' on the membership_line object'''
        self.env['membership.membership_line'].search([
            ('account_invoice_line', 'in', self.mapped('invoice_line_ids').ids)
        ]).write({'date_cancel': fields.Date.today()})
        return super(Invoice, self).action_cancel()

    @api.multi
    def write(self, vals):
        '''Change the partner on related membership_line'''
        if 'partner_id' in vals:
            self.env['membership.membership_line'].search([
                ('account_invoice_line', 'in', self.mapped('invoice_line_ids').ids)
            ]).write({'partner': vals['partner_id']})
        return super(Invoice, self).write(vals)


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def write(self, vals):
        MemberLine = self.env['membership.membership_line']
        res = super(AccountInvoiceLine, self).write(vals)
        for line in self.filtered(lambda line: line.invoice_id.type == 'out_invoice'):
            member_lines = MemberLine.search([('account_invoice_line', '=', line.id)])
            if line.product_id.membership and not member_lines:
                # Product line has changed to a membership product
                date_from = line.product_id.membership_date_from
                date_to = line.product_id.membership_date_to
                if line.invoice_id.date_invoice > (date_from or '0000-00-00') and line.invoice_id.date_invoice < (date_to or '0000-00-00'):
                    date_from = line.invoice_id.date_invoice
                MemberLine.create({
                    'partner': line.invoice_id.partner_id.id,
                    'membership_id': line.product_id.id,
                    'member_price': line.price_unit,
                    'date': fields.Date.today(),
                    'date_from': date_from,
                    'date_to': date_to,
                    'account_invoice_line': line.id,
                })
            if line.product_id and not line.product_id.membership and member_lines:
                # Product line has changed to a non membership product
                member_lines.unlink()
        return res

    @api.model
    def create(self, vals):
        MemberLine = self.env['membership.membership_line']
        invoice_line = super(AccountInvoiceLine, self).create(vals)
        if invoice_line.invoice_id.type == 'out_invoice' and \
                invoice_line.product_id.membership and \
                not MemberLine.search([('account_invoice_line', '=', invoice_line.id)]):
            # Product line is a membership product
            date_from = invoice_line.product_id.membership_date_from
            date_to = invoice_line.product_id.membership_date_to
            if date_from and date_from < (invoice_line.invoice_id.date_invoice or '0000-00-00') < (date_to or '0000-00-00'):
                date_from = invoice_line.invoice_id.date_invoice
            MemberLine.create({
                'partner': invoice_line.invoice_id.partner_id.id,
                'membership_id': invoice_line.product_id.id,
                'member_price': invoice_line.price_unit,
                'date': fields.Date.today(),
                'date_from': date_from,
                'date_to': date_to,
                'account_invoice_line': invoice_line.id,
            })
        return invoice_line
