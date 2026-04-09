from odoo import fields, models


class UserDepartment(models.Model):
    _name = 'user.department'
    _description = 'User Department'

    name = fields.Char(string='Name')