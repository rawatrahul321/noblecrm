# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.
{
    'name': 'Mailing List Archive',
    'category': 'Website',
    'description': """
NobleCRM Mail Group : Mailing List Archives
==========================================

        """,
    'depends': ['website_mail'],
    'data': [
        'data/mail_template_data.xml',
        'views/website_mail_channel_templates.xml',
        'views/snippets.xml',
    ],
}
