from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Order(models.Model):
    _name = 'wedding.order'
    _description = 'New Description'

    orderstagedetail_ids = fields.One2many('wedding.orderstage_detail', inverse_name='order_id', string='Order Stage Detail')
    orderguestchairdetail_ids = fields.One2many('wedding.orderguestchair_detail', inverse_name='ordergc_id', string='Order Guest Chair Detail')
    name = fields.Char(string='Order Name Code',  required=True)
    date = fields.Datetime('Date Order', default=fields.Datetime.now())
    total = fields.Integer(compute='_compute_total',
                           string='Total Price', store=True)
    customer_id = fields.Many2one(comodel_name='res.partner', string='Buyer', domain=[('is_customer', '=', True)])
    # domain berguna untuk memfilter data sama seperti WHERE dalam SQL

    is_return = fields.Boolean(string='Returned', default=False)


    @api.depends('orderstagedetail_ids', 'orderguestchairdetail_ids')
    def _compute_total(self):
        for record in self:
            a = sum(self.env['wedding.orderstage_detail'].search([('order_id', '=', record.id)]).mapped('price'))
            b = sum(self.env['wedding.orderguestchair_detail'].search([('ordergc_id', '=', record.id)]).mapped('price'))
            record.total = a + b

    def invoice(self):
        invoices = self.env['account.move'].create({
            'move_type' : 'out_invoice',
            'partner_id': self.customer_id,
            'date' : fields.Datetime.now(),
            'invoice_date' : self.date,
            'invoice_line_ids' : [(0, 0, {
                'product_id' : 0,
                'quantity' : 1,
                'price_unit' : self.total,
                'price_subtotal' : self.total,
            })]
        })
        self.is_return = True
        return invoices

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
    guestchair_id = fields.Many2one(comodel_name='wedding.guest_chair', string='Guest Chair', domain=[('stock', '>', '5')])
    
    name = fields.Char(string='Name')
    price = fields.Integer(compute='_compute_price', string='Price')
    qty = fields.Integer(string='Quantity', default=1)
    price_unit = fields.Integer(
        compute='_compute_price_unit', string='Price/Unit')

    @api.constrains('qty')
    def _constrains_check_qty(self):
        for record in self:
            check = self.env['wedding.guest_chair'].search([('id', '=',record.guestchair_id.id),('stock', '<', record.qty)])
            if check:
                raise ValidationError("Stok %s tidak cukup" % record.guestchair_id.name)

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