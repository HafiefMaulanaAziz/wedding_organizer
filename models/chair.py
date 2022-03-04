from odoo import api, fields, models


class Chair(models.Model):
    _name = 'wedding.chair'
    _description = 'New Description'

    name = fields.Char(string='Name')
    price = fields.Integer(string='Price')
    description = fields.Char(string='Description')
