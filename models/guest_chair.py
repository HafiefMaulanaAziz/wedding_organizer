from odoo import api, fields, models


class GuestChair(models.Model):
    _name = 'wedding.guest_chair'
    _description = 'New Description'

    name = fields.Char(string='Name')
    type = fields.Selection(string='Type', selection=[('plastic', 'Plastic'),('stainless', 'Stainless')])
    stock = fields.Integer(string='Stock')
    price = fields.Integer(string='Price')
    