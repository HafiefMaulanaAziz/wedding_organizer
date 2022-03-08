from odoo import api, fields, models


class Order(models.Model):
    _name = 'wedding.order'
    _description = 'New Description'

    orderstagedetail_ids = fields.One2many('wedding.orderstage_detail', inverse_name='order_id', string='Order Stage Detail')
    orderguestchairdetail_ids = fields.One2many('wedding.orderguestchair_detail', inverse_name='ordergc_id', string='Order Guest Chair Detail')
    name = fields.Char(string='Order Name Code',  required=True)
    date = fields.Datetime('Date Order', default=fields.Datetime.now())
    total = fields.Integer(compute='_compute_total',
                           string='Total Price', store=True)

    @api.depends('orderstagedetail_ids', 'orderguestchairdetail_ids')
    def _compute_total(self):
        for record in self:
            a = sum(self.env['wedding.orderstage_detail'].search([('order_id', '=', record.id)]).mapped('price'))
            b = sum(self.env['wedding.orderguestchair_detail'].search([('ordergc_id', '=', record.id)]).mapped('price'))
            record.total = a + b


class OrderStageDetail(models.Model):
    _name = 'wedding.orderstage_detail'
    _description = 'New Description'

    order_id = fields.Many2one(comodel_name='wedding.order', string='Order')
    stage_id = fields.Many2one(comodel_name='wedding.stage', string='Stage')
    
    name = fields.Char(string='Name')
    price = fields.Integer(compute='_compute_price', string='Price')
    qty = fields.Integer(string='Quantity', default=1)
    price_unit = fields.Integer(
        compute='_compute_price_unit', string='Price/Unit')

    @api.depends('stage_id')
    def _compute_price_unit(self):
        for record in self:
            record.price_unit = record.stage_id.price

    @api.depends('qty', 'price_unit')
    def _compute_price(self):
        for record in self:
            record.price = record.price_unit * record.qty

    @api.model
    def create(self, vals):
        record = super(OrderStageDetail, self).create(vals)
        if record.qty:
            self.env['wedding.stage'].search([('id', '=', record.stage_id.id)]).write({'stock':record.stage_id.stock-record.qty})
            return record

class OrderGuestChairDetail(models.Model):
    _name = 'wedding.orderguestchair_detail'
    _description = 'New Description'

    ordergc_id = fields.Many2one(comodel_name='wedding.order', string='Order')
    guestchair_id = fields.Many2one(comodel_name='wedding.guest_chair', string='Guest Chair')
    
    name = fields.Char(string='Name')
    price = fields.Integer(compute='_compute_price', string='Price')
    qty = fields.Integer(string='Quantity', default=1)
    price_unit = fields.Integer(
        compute='_compute_price_unit', string='Price/Unit')

    @api.depends('guestchair_id')
    def _compute_price_unit(self):
        for record in self:
            record.price_unit = record.guestchair_id.price

    @api.depends('qty', 'price_unit')
    def _compute_price(self):
        for record in self:
            record.price = record.price_unit * record.qty

    @api.model
    def create(self, vals):
        record = super(OrderGuestChairDetail, self).create(vals)
        if record.qty:
            self.env['wedding.guest_chair'].search([('id', '=', record.guestchair_id.id)]).write({'stock':record.guestchair_id.stock-record.qty})
            return record