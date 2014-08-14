# -*- encoding: utf-8 -*-
# __author__ = jeff@openerp.cn
from osv import osv, fields
from tools.translate import _

class account_move(osv.osv):
    _inherit = 'account.move'
    """
    添加制单、审核、附件数三个字段
    """
    _columns = {
        'write_uid':fields.many2one('res.users', '审核', readonly=True),
        'create_uid':fields.many2one('res.users', '制单', readonly=True, select=True),      
        'proof':fields.integer('附件数', required=False, help='该记账凭证对应的原始凭证数量'),
    }
    """
    附件数默认为1张
    凭证业务类型默认为总帐     
    """
    _defaults = {
        'proof': lambda *args: 1,
        'journal_id': lambda self, cr, uid, context:self.pool.get('account.journal').search(cr, uid, [('type', '=', 'general')], limit=1)[0]
    }

account_move()

class account_account(osv.osv):
    _inherit = 'account.account'
    """
    Replace metheod accoun.account.name_get(), show full name of account on many2one field
    Sample “100902 其他货币资金/银行本票”

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        reads = self.read(cr, uid, ids, ['name', 'code','parent_id'], context)
        res = []
        for record in reads:
            name = record['name']
            if record['code']:
                
                if record['parent_id']:
                    account_parent_id = record['parent_id'][0]
                    while account_parent_id:
                            parent_obj = self.read(cr, uid, account_parent_id, ['name', 'parent_id'], context)
                            name = parent_obj['name'] + '/'+name
                            if  parent_obj['parent_id']:
                                account_parent_id = parent_obj['parent_id'][0]
                            else:
                                account_parent_id = False

            name = record['code'] + ' '+name
            res.append((record['id'], name))
        return res
"""        
    def get_balance(self, cr, uid, ids, date_start=False, date_stop=False, product=False, partner=False ):
        '''
        Get the balance from date_start to date_stop,fielter by product or partner 
        '''
        result = {
            'debit':0.0,
            'debit_quantity':0.0,
            'debit_amount_currency':0.0,
            'credit':0.0,
            'credit_quantity':0.0,
            'credit_amount_currency':0.0,
            'balance':0.0,
            'amount_currency':0.0,
            'quantity':0.0,
        }
        account_move_line_obj = self.pool.get('account.move.line')
        account_obj = self.pool.get('account.account')
        account_ids = account_obj.search(cr, uid, [('parent_id', 'child_of', ids)])
        search_condition = [('account_id','in',account_ids),('state','=','valid')]
        if date_start:
            search_condition.append(('date', '>=', date_start))
        if date_stop:
            search_condition.append(('date', '<=', date_stop))
        if product: 
            search_condition.append(('product_id', '=', product))
        if partner:
            search_condition.append(('partner_id', '=', partner))

        line_ids = account_move_line_obj.search(cr, uid, search_condition)
        lines = account_move_line_obj.browse(cr, uid, line_ids)
        for line in lines:
            if line.debit > 0:
                result['debit_quantity'] += line.quantity or 0
                result['debit_amount_currency'] += line.amount_currency or 0
            else:
                result['credit_quantity'] += line.quantity or 0
                result['credit_amount_currency'] += abs(line.amount_currency) or 0
            result['balance'] += line.debit-line.credit
            result['quantity'] =  result['debit_quantity'] - result['credit_quantity']
            result['amount_currency'] =  result['debit_amount_currency'] - result['credit_amount_currency']
            result['debit'] += line.debit or 0
            result['credit'] += line.credit or 0

        return result

account_account()

