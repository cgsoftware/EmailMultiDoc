# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2008 Zikzakmedia S.L. (http://zikzakmedia.com) All Rights Reserved.
#                       Jordi Esteve <jesteve@zikzakmedia.com>
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

{
    "name" : "Invia Massivo di Documenti via E_mail",
    "version" : "1.0",
    "depends" : ["smtpclient","account"],
    "author" : "C. & G. Software",
    "website" : "www.cgsoftware.it",
    "license" : "GPL-3",
    "description": """ Invia in allegato documenti FiscalDoc al o ai documenti selezionati
    per quelli dove non c'è indirizzo e_mail salva il pdf in in /home/openerp/documenti/
""",
    "category" : "Generic Modules",
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : ["account_invoice_wizard.xml"],
    "active": False,
    "installable": True
}
