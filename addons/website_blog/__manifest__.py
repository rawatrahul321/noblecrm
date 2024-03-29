# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

{
    'name': 'Blogs',
    'category': 'Website',
    'sequence': 140,
    'website': 'https://www.infonoble.com/page/blog-engine',
    'summary': 'News, Blogs, Announces, Discussions',
    'version': '1.0',
    'description': "",
    'depends': ['website_mail', 'website_partner'],
    'data': [
        'data/website_blog_data.xml',
        'views/website_blog_views.xml',
        'views/website_blog_templates.xml',
        'views/snippets.xml',
        'security/ir.model.access.csv',
        'security/website_blog_security.xml',
    ],
    'demo': [
        'data/website_blog_demo.xml'
    ],
    'test': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
}
