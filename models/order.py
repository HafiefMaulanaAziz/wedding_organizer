from odoo import api, fields, models


class Order(models.Model):
    _name = 'wedding.order'
    _description = 'New Description'

    orderdetail_ids = fields.One2many('wedding.order_detail', inverse_name='order_id', string='Order Detail')
    name = fields.Char(string='Order ID',  required=True)
    total = fields.Integer(compute='_compute_total',
                           string='Price Total', store=True)

    @api.depends('orderdetail_ids')
    def _compute_total(self):
        for record in self:
            a = sum(self.env['wedding.order_detail'].search(
                [('order_id', '=', record.id)]).mapped('price'))

            record.total = a


class OrderDetail(models.Model):
    _name = 'wedding.order_detail'
    _description = 'New Description'

    order_id = fields.Many2one(comodel_name='wedding.order', string='Order')
    stage_id = fields.Many2one(comodel_name='wedding.stage', string='Stage')
    
    name = fields.Selection(string='Name',  selection=[('stage', 'Stage'),('guest chair', 'Guest Chair')])
    price = fields.Integer(compute='_compute_price', string='Price')
    qty = fields.Integer(string='Quantity')
    price_unit = fields.Char(
        compute='_compute_price_unit', string='Price/Unit')

    @api.depends('stage_id')
    def _compute_price_unit(self):
        for record in self:
            record.price_unit = record.stage_id.price

    @api.depends('qty', 'price_unit')
    def _compute_price(self):
        for record in self:
            record.price = record.stage_id.price * record.qty