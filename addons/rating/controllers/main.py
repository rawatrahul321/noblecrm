# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

import werkzeug

from noblecrm import http
from noblecrm.http import request
from noblecrm.tools.translate import _


class Rating(http.Controller):

    @http.route('/rating/<string:token>/<int:rate>', type='http', auth="public")
    def open_rating(self, token, rate, **kwargs):
        assert rate in (1, 5, 10), "Incorrect rating"
        rating = request.env['rating.rating'].sudo().search([('access_token', '=', token)])
        if not rating:
            return request.not_found()
        rate_names={
            5: _("not satisfied"),
            1: _("highly dissatisfied"),
            10: _("satisfied")
        }
        rating.write({'rating': rate, 'consumed': True})
        lang = rating.partner_id.lang or 'en_US'
        return request.env['ir.ui.view'].with_context(lang=lang).render_template('rating.rating_external_page_submit', {
            'rating': rating, 'token': token,
            'rate_name': rate_names[rate], 'rate': rate
        })

    @http.route(['/rating/<string:token>/<int:rate>/submit_feedback'], type="http", auth="public", methods=['post'])
    def submit_rating(self, token, rate, **kwargs):
        rating = request.env['rating.rating'].sudo().search([('access_token', '=', token)])
        if not rating:
            return request.not_found()
        record_sudo = request.env[rating.res_model].sudo().browse(rating.res_id)
        record_sudo.rating_apply(rate, token=token, feedback=kwargs.get('feedback'))
        lang = rating.partner_id.lang or 'en_US'
        return request.env['ir.ui.view'].with_context(lang=lang).render_template('rating.rating_external_page_view', {
            'web_base_url': request.env['ir.config_parameter'].sudo().get_param('web.base.url'),
            'rating': rating,
        })
