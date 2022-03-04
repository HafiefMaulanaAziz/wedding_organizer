# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class wedding_organizer(models.Model):
#     _name = 'wedding_organizer.wedding_organizer'
#     _description = 'wedding_organizer.wedding_organizer'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
