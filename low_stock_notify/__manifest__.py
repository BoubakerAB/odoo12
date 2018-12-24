# -*- coding: utf-8 -*-
{
    'name' : 'Product Low Stock Notification',
    'version' : '1.1',
    'author' : 'Boubaker Tunisoft',
    'summary' : '',
    'license' : 'OPL-1',
    'description' : 'Module that automatically E-mails a list of products with low stock. ',
    'category' : 'Sales Management',
    'depends' : ['base', 'mail', 'product'],
    'images': ['static/description/banner.png'],
    'price': 7.00,
    'currency': 'EUR',
    'data':[
    			'data/email_template.xml',
                'views/product_template.xml',
                'views/ir_cron.xml'
    		],
    'installable': True
}