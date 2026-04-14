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
    'website': "",
    'license': 'LGPL-3',

    # for the full list
    'category': 'Uncategorized',
    'version': '19.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'product', 'account', 'utm', 'hr', 'contacts'],
    # 'depends': ['base', 'account', 'mail', 'purchase','web', 'product', 'stock', 'hr'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/financial_exp_security.xml',
        'security/hide_menu_items_views.xml',
        'security/ir.model.access.csv',
        'data/seq.xml',
        'data/email_template_views.xml',
        'views/views.xml',
        'views/financial_expense_views.xml',
        'views/product_product_views.xml',
        'views/expense_line_views.xml',
        'views/res_users_views.xml',
        'reports/print_expenses.xml',
    ],

}
