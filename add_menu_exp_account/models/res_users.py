from odoo import models, fields, api


class ResUser(models.Model):
    _inherit = 'res.users'

    department_id = fields.Many2one(comodel_name='user.department')
    manager_id = fields.Many2one(comodel_name='res.users', string='Manager')