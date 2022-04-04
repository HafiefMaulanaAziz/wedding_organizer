from odoo import api, fields, models


class Returning(models.Model):
    _name = 'wedding.returning'
    _description = 'Pengembalian Sewa'

    name = fields.Char(string='Name', required=True)
    order_id = fields.Many2one(comodel_name='wedding.order', string='Order ID', required=True)
    orderstagedetail_ids = fields.One2many(related='order_id.orderstagedetail_ids', string='Order Stage Detail')
    orderguestchairdetail_ids = fields.One2many(related='order_id.orderguestchairdetail_ids', string='Order Guest Chair Detail')
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
            for s in record.orderstagedetail_ids:
                self.env['wedding.stage'].search([('id', '=', s.stage_id.id)]).write({'stock' : s.stage_id.stock + s.qty})
            for gc in record.orderguestchairdetail_ids:
                self.env['wedding.guest_chair'].search([('id', '=', gc.guestchair_id.id)]).write({'stock' : gc.guestchair_id.stock + gc.qty})

            return record

    def unlink(self):
        for un in self:
            self.env['wedding.order'].search(
                [('id', '=', un.order_id.id)]).write({'is_return': False})
        record = super(Returning, self).unlink()


    
