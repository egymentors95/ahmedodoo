from odoo import models, fields, api


class ResUser(models.Model):
    _inherit = 'res.users'

    department_id = fields.Many2one(comodel_name='user.department')