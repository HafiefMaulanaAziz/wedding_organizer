from odoo import api, fields, models


class Accounting(models.Model):
    _name = 'wedding.accounting'
    _description = 'New Description'
    _order = 'id asc'

    name = fields.Char(string='Name')
    id_acc = fields.Char('Accounting Code')
    date = fields.Datetime(string='Date', default=fields.Datetime.now())
    debit = fields.Integer(string='Debit')
    credit = fields.Integer(string='Credit')
    saldo = fields.Integer(compute='_compute_saldo', string='Saldo')
    
    @api.depends('debit', 'credit')
    def _compute_saldo(self):
        for record in self:
            prev = self.search_read([('id', '<', record.id)], limit=1, order='date desc')
            prev_saldo = prev[0]['saldo'] if prev else 0
            record.saldo = prev_saldo + record.debit + record.credit