# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-Today Serpent Consulting Services Pvt. Ltd.
#    (<http://www.serpentcs.com>)
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
    "name": "My Custom Work",
    "version": "1.1",
    "category": "Tools",
    "description": """
Gestor de Ordenes de Servicios.
=================================

Gestionar el Trabajo de Mantenimiento a Equipos
""",
    "author": "Reinaldo",
    # "images": ['images/1_servers_synchro.jpeg', 'images/2_synchronize.jpeg', 'images/3_objects_synchro.jpeg',],
    "depends": ['resource', 'report', 'hr'],
    'website': "",
    "data": [
        "security/my_work_security.xml",
        "security/ir.model.access.csv",
        "data/my_work_data.xml",
        # "wizard/base_synchro_view.xml",
        "views/my_work_view.xml",
        "views/resource_view.xml",
        "report/my_work_template_reports.xml",
        'reports.xml',
        # "views/res_request_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
