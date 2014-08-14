# -*- encoding: utf-8 -*-
# __author__ = jeff@openerp.cn
##############################################################################
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

{
    "name" : "Print all chinese account documents for legal requirements",
    "version" : "2.0",
    "description" : '''
    In china, all account documents need to be printed and keep for internal
    or external audit. So this module will print following account documnets
    with china standard format:
    Account moves

    General ledger (accouts move history)
    Cash journal (for cash and bank accounts)
    Detail ledger  (accounts move histoy group by partner or product)
        
        Three columns ledger
        Stock ledger
        Cash journal
        Foreign currency cash journal
         
    ==== todo ====
    Balance Sheet
    Profit and Loss Sheet
    Cash Flow Statement

    Further more, we hide the concept "Journal" for chinese accountant never
    use this concept. They care more about move number and move number must
    be organized in a period
    ''',
    "author" : "Shine IT",
    "website" : "http://www.openerp.cn",
    "depends" : ["account"],
    "update_xml" : [
#"oecn_account_print_view.xml",
                    "wizard/oecn_account_print_wizard_view.xml",
                    "report/oecn_account_print_report.xml"
    ],
    "installable" : True,
    "certificate" : ""
   
}
