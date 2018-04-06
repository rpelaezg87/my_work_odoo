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
    "name": "Iglesias",
    "version": "1.1",
    "category": "Iglesias",
    "description": """
Registro de Oficios.
=================================

Gestionar Medios Básicos, Miembros, Sacramentos y Gastos en las Iglesias
""",
    "author": "Reinaldo",
    # "images": ['images/1_servers_synchro.jpeg', 'images/2_synchronize.jpeg', 'images/3_objects_synchro.jpeg',],
    "depends": ['report', 'hr', 'contacts', 'product'],
    'website': "",
    "data": [
        # "security/my_work_security.xml",
        # "security/ir.model.access.csv",
        # "data/my_work_data.xml",
        # "wizard/base_synchro_view.xml",
        "views/iglesias_view.xml",
        "views/product_views.xml",
        "views/congregacion_view.xml",
        "views/sacramento_view.xml",
        "views/oficio_view.xml",
        "views/hr_view.xml",
        "views/estacion_liturgica_view.xml",
        "wizard/wizard_reporte_comun_view.xml",
        "wizard/wizard_reporte_estado_congregaciones_view.xml",
        "wizard/wizard_reporte_estado_financiero_view.xml",
        "wizard/wizard_reporte_listado_altas_view.xml",
        "wizard/wizard_reporte_listado_bajas_view.xml",
        "wizard/wizard_reporte_listado_bautizos_view.xml",
        "wizard/wizard_reporte_fe_bautismo_view.xml",
        "views/report_congregacion.xml",
        "views/report_fe_bautismo.xml",
        "views/report_congregacion_junta.xml",
        "views/report_congregacion_membresia.xml",
        "views/report_congregacion_mediosb.xml",
        "views/report_congregacion_enfermos.xml",
        "views/report_congregacion_estado.xml",
        "views/report_estado_financiero.xml",
        "views/report_congregacion_altas.xml",
        "views/report_congregacion_bajas.xml",
        "views/report_congregacion_bautizos.xml",
        "views/iglesias_report.xml",
        # "report/my_work_template_reports.xml",
        # 'reports.xml',
        # "views/res_request_view.xml",
    ],
    "installable": True,
    'application': True,
    "auto_install": False,
}
