# -*- coding: utf-8 -*-
# from odoo import http


# class WeddingOrganizer(http.Controller):
#     @http.route('/wedding_organizer/wedding_organizer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wedding_organizer/wedding_organizer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wedding_organizer.listing', {
#             'root': '/wedding_organizer/wedding_organizer',
#             'objects': http.request.env['wedding_organizer.wedding_organizer'].search([]),
#         })

#     @http.route('/wedding_organizer/wedding_organizer/objects/<model("wedding_organizer.wedding_organizer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wedding_organizer.object', {
#             'object': obj
#         })
