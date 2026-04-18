from odoo import models, fields, api


class ResUser(models.Model):
    _inherit = 'res.users'

    department_id = fields.Many2one(comodel_name='user.department')
                # Managers Expenses
    direct_manager = fields.Many2one(comodel_name='res.users', string='Direct Manager')
    administration_management = fields.Many2one(comodel_name='res.users', string='Administration Management')
    chief_acc = fields.Many2one(comodel_name='res.users', string='Chief Acc')
    cfo = fields.Many2one(comodel_name='res.users', string='CFO')
    upload_bank = fields.Many2one(comodel_name='res.users', string='Upload Bank')
    approve = fields.Many2one(comodel_name='res.users', string='Approve')
    account2 = fields.Many2one(comodel_name='res.users', string='Accounts')

    # Managers Financial Expenses
    financial_chief_acc = fields.Many2one(comodel_name='res.users', string='Chief Acc')
    financial_cfo = fields.Many2one(comodel_name='res.users', string='CFO')
    financial_upload_bank = fields.Many2one(comodel_name='res.users', string='Upload Bank')
    financial_approve = fields.Many2one(comodel_name='res.users', string='Approve')
    financial_account2 = fields.Many2one(comodel_name='res.users', string='Accounts')

