# -*- coding: utf-8 -*-
import contextlib
import logging
import json
import uuid

import werkzeug.urls
import requests

from noblecrm import api, fields, models, exceptions
from noblecrm.tools import pycompat

_logger = logging.getLogger(__name__)

DEFAULT_ENDPOINT = 'https://iap.infonoble.com'


#----------------------------------------------------------
# Helpers for both clients and proxy
#----------------------------------------------------------
def get_endpoint(env):
    url = env['ir.config_parameter'].sudo().get_param('iap.endpoint', DEFAULT_ENDPOINT)
    return url


#----------------------------------------------------------
# Helpers for clients
#----------------------------------------------------------
class InsufficientCreditError(Exception):
    pass


class AuthenticationError(Exception):
    pass


def jsonrpc(url, method='call', params=None):
    """
    Calls the provided JSON-RPC endpoint, unwraps the result and
    returns JSON-RPC errors as exceptions.
    """
    payload = {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': uuid.uuid4().hex,
    }


    _logger.info('iap jsonrpc %s', url)
    try:
        req = requests.post(url, json=payload)
        response = req.json()
        if 'error' in response:
            name = response['error']['data'].get('name').rpartition('.')[-1]
            message = response['error']['data'].get('message')
            if name == 'InsufficientCreditError':
                e_class = InsufficientCreditError
            elif name == 'AccessError':
                e_class = exceptions.AccessError
            elif name == 'UserError':
                e_class = exceptions.UserError
            else:
                raise requests.exceptions.ConnectionError()
            e = e_class(message)
            e.data = response['error']['data']
            raise e
        return response.get('result')
    except (ValueError, requests.exceptions.ConnectionError, requests.exceptions.MissingSchema) as e:
        raise exceptions.AccessError('The url that this service requested returned an error. Please contact the author the app. The url it tried to contact was ' + url)

#----------------------------------------------------------
# Helpers for proxy
#----------------------------------------------------------
class IapTransaction(object):

    def __init__(self):
        self.credit = None

@contextlib.contextmanager
def charge(env, key, account_token, credit, description=None, credit_template=None):
    """
    Account charge context manager: takes a hold for ``credit``
    amount before executing the body, then captures it if there
    is no error, or cancels it if the body generates an exception.

    :param str key: service identifier
    :param str account_token: user identifier
    :param int credit: cost of the body's operation
    :param description: a description of the purpose of the charge,
                        the user will be able to see it in their
                        dashboard
    :type description: str
    :param credit_template: a QWeb template to render and show to the
                            user if their account does not have enough
                            credits for the requested operation
    :type credit_template: str
    """
    endpoint = get_endpoint(env)
    params = {
        'account_token': account_token,
        'credit': credit,
        'key': key,
        'description': description,
    }
    try:
        transaction_token = jsonrpc(endpoint + '/iap/1/authorize', params=params)
    except InsufficientCreditError as e:
        if credit_template:
            arguments = json.loads(e.args[0])
            arguments['body'] = pycompat.to_text(env['ir.qweb'].render(credit_template))
            e.args = (json.dumps(arguments),)
        raise e
    try:
        transaction = IapTransaction()
        transaction.credit = credit
        yield transaction
    except Exception as e:
        params = {
            'token': transaction_token,
            'key': key,
        }
        r = jsonrpc(endpoint + '/iap/1/cancel', params=params)
        raise e
    else:
        params = {
            'token': transaction_token,
            'key': key,
            'credit_to_capture': transaction.credit,
        }
        r = jsonrpc(endpoint + '/iap/1/capture', params=params) # noqa


#----------------------------------------------------------
# Models for client
#----------------------------------------------------------
class IapAccount(models.Model):
    _name = 'iap.account'
    _rec_name = 'service_name'

    service_name = fields.Char()
    account_token = fields.Char(default=lambda s: uuid.uuid4().hex)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id)

    @api.model
    def get(self, service_name):
        account = self.search([('service_name', '=', service_name), ('company_id', 'in', [self.env.user.company_id.id, False])])
        if not account:
            # TODO: remove this sudo in v12 as we change the user rights.
            account = self.sudo().create({'service_name': service_name}).with_env(self.env)
            # Since the account did not exist yet, we will encounter a NoCreditError,
            # which is going to rollback the database and undo the account creation,
            # preventing the process to continue any further.
            self.env.cr.commit()
        return account

    @api.model
    def get_credits_url(self, base_url, service_name, credit):
        dbuuid = self.env['ir.config_parameter'].sudo().get_param('database.uuid')
        account_token = self.get(service_name).account_token
        d = {
            'dbuuid': dbuuid,
            'service_name': service_name,
            'account_token': account_token,
            'credit': credit,
        }
        return '%s?%s' % (base_url, werkzeug.urls.url_encode(d))

    @api.model
    def get_account_url(self):
        route = '/iap/services'
        endpoint = get_endpoint(self.env)
        d = {'dbuuid': self.env['ir.config_parameter'].sudo().get_param('database.uuid')}

        return '%s?%s' % (endpoint + route, werkzeug.urls.url_encode(d))
