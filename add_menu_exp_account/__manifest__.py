# -*- coding: utf-8 -*-
{
    'name': "add_menu_exp_account",
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "El-Araby",
    'website': "http://www.yourcompany.com",
    'license': 'LGPL-3',

    # for the full list
    'category': 'Uncategorized',
    'version': '19.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'product', 'account'],
    # 'depends': ['base', 'account', 'mail', 'purchase','web', 'product', 'stock', 'hr'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/seq.xml',
        'views/product_product_views.xml',
        'views/expense_line_views.xml',
        'views/res_users_views.xml',
    ],

}
