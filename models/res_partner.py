from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    is_staff = fields.Boolean(string='Staff', default=False)
    is_customer = fields.Boolean(string='Customer', default=False)
