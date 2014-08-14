# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (c) 2010-2012 Elico Corp. All Rights Reserved.
#    Author:            Andy Lu <andy.lu@elico-corp.com>
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from osv import fields, osv

class account_account(osv.osv):
    _inherit = "account.account"

    def _get_amount_currency(self, cr, uid, ids, field_names, arg=None, context=None,
                  query='', query_params=()):
        """ compute the amount_currency for the provided account ids
        Arguments:
        `ids`: account ids
        `field_names`: the fields to compute (a list of any of...)
        `arg`: unused fields.function stuff
        `query`: additional query filter (as a string)
        `query_params`: parameters for the provided query string
                        (__compute will handle their escaping) as a
                        tuple
        """
        #get all the necessary accounts
        #children_and_consolidated = self._get_children_and_consol(cr, uid, ids, context=context)
        #compute for each account the balance/debit/credit from the move lines
        accounts = {}
        res = {}
        
        if True:
            aml_query = self.pool.get('account.move.line')._query_get(cr, uid, context=context)

            wheres = [""]
            if query.strip():
                wheres.append(query.strip())
            if aml_query.strip():
                wheres.append(aml_query.strip())
            filters = " AND ".join(wheres)
            for id in ids:
                request = "select array_to_string(array(" \
                           " select cast(cast(sum(l.amount_currency) as varchar(32)) || c.symbol as varchar(64))" \
                           " from v_account_move_line l left join res_currency c on l.currency_id = c.id" \
                           " where l.account_id = %d " % (id ) + filters + \
                           " group by l.account_id,c.symbol " \
                           " ), ', ') as amount_currency" \
                           " from v_account_account a where a.id = %d limit 1" % (id ) 
                params = query_params
                cr.execute(request, params)
                res[id] = cr.fetchone()[0] or ''
        return res 

#    _columns = {        
#        'amount_currency': fields.function(_get_amount_currency, type='char', method=True, string='Amount Currency'),
#    }
account_account()    

class account_pl_report(osv.osv_memory):
    _inherit = "account.pl.report"
    _columns = {
        'level': fields.integer("Account Level Detail"),
    }

    _defaults = {
        'level': 5,
    }
    def _print_report(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}
        data = self.pre_print_report(cr, uid, ids, data, context=context)
        data['form'].update(self.read(cr, uid, ids, ['display_type'])[0])        
        level = self.read(cr, uid, ids, ['level'])[0]
        data['form'].update(level)
        context['level'] = level
        if data['form']['display_type']:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'pl.account.horizontal.level',
                'datas': data,
            }
        else:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'pl.account.level',
                'datas': data,
            }

account_pl_report()


class account_bs_report(osv.osv_memory):

    _inherit = 'account.bs.report'
    _columns = {
        'level': fields.integer("Account Level Detail"),
    }

    _defaults = {
        'level': 5,
    }

    def _print_report(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}
        data['form'].update(self.read(cr, uid, ids, ['display_type','reserve_account_id'])[0])
        if not data['form']['reserve_account_id']:
            raise osv.except_osv(_('Warning'),_('Please define the Reserve and Profit/Loss account for current user company !'))
        level = self.read(cr, uid, ids, ['level'])[0]
        data['form'].update(level)
        context['level'] = level
        data = self.pre_print_report(cr, uid, ids, data, context=context)
        if data['form']['display_type']:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'account.balancesheet.horizontal.level',
                'datas': data,
            }
        else:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'account.balancesheet.level',
                'datas': data,
            }

account_bs_report()


class account_balance_report(osv.osv_memory):
    _inherit = 'account.balance.report'

    _columns = {
        'level': fields.integer("Account Level Detail"),
    }

    _defaults = {
        'level': 5,
    }

    def _print_report(self, cr, uid, ids, data, context=None):
        data = self.pre_print_report(cr, uid, ids, data, context=context)      
        level = self.read(cr, uid, ids, ['level'])[0]
        data['form'].update(level)
        context['level'] = level
        return {'type': 'ir.actions.report.xml', 'report_name': 'account.account.balance.level', 'datas': data}

account_balance_report()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
