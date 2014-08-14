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
import logging
_logger = logging.getLogger(__name__)


class account_voucher(orm.Model):
    _inherit = "account.voucher"

    def account_move_get(self, cr, uid, voucher_id, context=None):
        '''
        This method is inherited to add the voucher reference to account move..

        :param voucher_id: Id of voucher for which we are creating account_move
        :return: mapping between fieldname and value of account move to create
        :rtype: dict
        '''
        context = context or {}
        voucher = self.browse(cr, uid, voucher_id, context=context)
        move = super(account_voucher, self).account_move_get(
            cr, uid, voucher_id, context=context)
        # if not context.get('origin', False):
        #     context['origin'] = voucher.reference
        reference = voucher.reference
        if reference.endswith(':'):
            reference = reference[:-1]
        move['name'] = (move['name'] and move['name'] + ':' or '') + \
            reference
        return move


class account_move(orm.Model):
    _inherit = "account.move"

    def create(self, cr, uid, vals, context=None):
        context = context or {}
        # from account_journal_name/_create_product_valuation_moves()
        if context.get('origin', None):
            vals_name = vals.get('name', '')
            vals['name'] = (vals_name and vals_name + ':' or '') +\
                context.get('origin')
        # invoice in context is passed from
        # account_invoice.py/action_move_create()
        elif context.get('invoice', False):
            invoice = context['invoice']
            if type(invoice) == orm.browse_record and \
                    invoice.origin:
                vals_name = vals.get('name', '')
                vals['name'] = (vals_name and vals_name + ':' or '') + \
                    invoice.origin
        return super(account_move, self).create(cr, uid, vals, context=context)
