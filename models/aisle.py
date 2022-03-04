from odoo import api, fields, models


class Aisle(models.Model):
    _name = 'wedding.aisle'
    _description = 'New Description'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')
    price = fields.Integer(string='Price')
