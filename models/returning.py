from odoo import api, fields, models


class Returning(models.Model):
    _name = 'wedding.returning'
    _description = 'Pengembalian Sewa'

    name = fields.Char(string='Name', required=True)
    order_id = fields.Many2one(comodel_name='wedding.order', string='Order ID', required=True)
    date = fields.Date(string='Returning Date', default=fields.Date.today())
    customer_name = fields.Char(compute='_compute_customer_name', string='Customer Name')
    bill = fields.Integer(compute='_compute_bill', string='Bill')

   
    @api.depends('order_id')
    def _compute_customer_name(self):
        for record in self:
            # record.customer_name = self.env['wedding.order'].search([('id', '=', record.order_id.id)]).mapped('customer_id').name
            record.customer_name = record.order_id.customer_id.name

    @api.depends('order_id')
    def _compute_bill(self):
        for record in self :
            record.bill = record.order_id.total
    
    @api.model
    def create(self, vals):
        record = super(Returning, self).create(vals)
        if record.date:
            self.env['wedding.order'].search(
                [('id', '=', record.order_id.id)]).write({'is_return': True})
            self.env['wedding.accounting'].create({'credit': record.bill, 'name': record.name})
            return record

    def unlink(self):
        for un in self:
            self.env['wedding.order'].search(
                [('id', '=', un.order_id.id)]).write({'is_return': False})
        record = super(Returning, self).unlink()


    
