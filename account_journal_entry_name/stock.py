# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2010-2014 Elico Corp. All Rights Reserved.
#    Alex Duan <alex.duan@elico-corp.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import orm


class stock_move(orm.Model):
    _inherit = "stock.move"

    def _create_product_valuation_moves(
            self, cr, uid, move, context=None):
        context = context or {}
        # if the picking comes from MO or PO, we should extract
        # the information to pass to journal entry's name.
        context['origin'] = ''
        mo_obj = self.pool.get('mrp.production')
        # check if this move comes from a PO
        # check if this move comes from a MO
        if move.purchase_line_id and move.purchase_line_id.order_id:
            context['origin'] += move.purchase_line_id.order_id.name or ''
        elif mo_obj.search(cr, uid, [('name', '=', move.name)]):
            context['origin'] += move.name
        # adding product information.
        origin = move.product_id.name_get(context=context)
        if origin:
            context['origin'] += (
                context['origin'] and ':' or '') + origin[0][1]
        return super(stock_move, self)._create_product_valuation_moves(
            cr, uid, move, context=context)
