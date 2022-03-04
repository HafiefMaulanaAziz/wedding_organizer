from odoo import api, fields, models


class Stage(models.Model):
    _name = 'wedding.stage'
    _description = 'Model Stage'

    name = fields.Char(string='Name', required=True)
    aisle_id = fields.Many2one(comodel_name='wedding.aisle', string='Aisle Type', required=True)
    chair_id = fields.Many2one(comodel_name='wedding.chair', string='Chair Type',required=True)
    # aisle = fields.Char(string='Tipe Aisle')
    flower = fields.Selection(string='Flower type', selection = [('fakeflower', 'Fake Flower'),('realflower', 'Real Flower')])
    accessories = fields.Char(string='Accessories')
    stock = fields.Integer(string='Stage Stock')

    price = fields.Integer(compute = '_compute_price' ,string='Total Price')
    @api.depends('aisle_id', 'chair_id')
    def _compute_price(self):
       for record in self:
           record.price = record.aisle_id.price + record.chair_id.price

    desc_aisle = fields.Char(compute='_compute_desc_aisle', string='Aisle Descriptions')
    @api.depends('aisle_id')
    def _compute_desc_aisle(self):
        for record in self:
            record.desc_aisle = record.aisle_id.description

    desc_chair = fields.Char(compute='_compute_desc_chair', string='Chair Descriptions')
    @api.depends('chair_id')
    def _compute_desc_chair(self):
        for record in self:
            record.desc_chair = record.chair_id.description

    
    