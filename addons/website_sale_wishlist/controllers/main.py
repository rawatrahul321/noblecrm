# -*- coding: utf-8 -*-
from noblecrm import http
from noblecrm.http import request
from noblecrm.addons.website_sale.controllers.main import WebsiteSale
import json


class WebsiteSaleWishlist(WebsiteSale):

    @http.route(['/shop/wishlist/add'], type='json', auth="public", website=True)
    def add_to_wishlist(self, product_id, price=False, **kw):
        if not price:
            compute_currency, pricelist_context, pl = self._get_compute_currency_and_context()
            p = request.env['product.product'].with_context(pricelist_context, display_default_code=False).browse(product_id)
            price = p.website_price

        partner_id = session = False
        if not request.website.is_public_user():
            partner_id = request.env.user.partner_id.id
        else:
            session = request.session.sid
        return request.env['product.wishlist']._add_to_wishlist(
            pl.id,
            pl.currency_id.id,
            request.website.id,
            price,
            product_id,
            partner_id,
            session
        )

    @http.route(['/shop/wishlist'], type='http', auth="public", website=True)
    def get_wishlist(self, count=False, **kw):
        values = request.env['product.wishlist'].with_context(display_default_code=False).current()
        if count:
            return request.make_response(json.dumps(values.mapped('product_id').ids))

        if not len(values):
            return request.redirect("/shop")

        return request.render("website_sale_wishlist.product_wishlist", dict(wishes=values))

    @http.route(['/shop/wishlist/remove/<model("product.wishlist"):wish>'], type='json', auth="public", website=True)
    def rm_from_wishlist(self, wish, **kw):
        wish.active = False
        return True
