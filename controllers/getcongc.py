from odoo import http, fields, models
from odoo.http import request
import json

class GetConGC(http.Controller):
    @http.route(['/guestchair', '/guestchair/<int:idnya>'], auth='public', type='json', methods=['GET'], csrf=True)
    def getGuestChair(self, idnya=None, **kwargs):
        value=[]
        if not idnya:
            chair = request.env['wedding.guest_chair'].search([])
            for k in chair:
                value.append({
                    "id" : k.id,
                    "name" : k.name,
                    "type" : k.type,
                    "price" : k.price,
                    "stock" : k.stock,
                })
            return json.dumps(value)
        else :
            chair_id = request.env['wedding.guest_chair'].search(['id', '=', idnya])
            for k in chair_id:
                value.append({
                    "id" : k.id,
                    "name" : k.name,
                    "type" : k.type,
                    "price" : k.price,
                    "stock" : k.stock,
                })
            return json.dumps(value)