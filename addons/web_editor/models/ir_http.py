# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import models
from noblecrm.http import request
from noblecrm.osv import expression


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _dispatch(cls):
        context = dict(request.context)
        if 'editable' in request.httprequest.args and 'editable' not in context:
            context['editable'] = True
        if 'edit_translations' in request.httprequest.args and 'edit_translations' not in context:
            context['edit_translations'] = True
        if context.get('edit_translations') and 'translatable' not in context:
            context['translatable'] = True
        request.context = context
        return super(IrHttp, cls)._dispatch()

    @classmethod
    def _get_translation_frontend_modules_domain(cls):
        domain = super(IrHttp, cls)._get_translation_frontend_modules_domain()
        return expression.OR([domain, [('name', '=', 'web_editor')]])
