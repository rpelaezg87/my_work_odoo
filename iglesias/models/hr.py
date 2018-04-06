# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import datetime

CATEGORIA = [('lector_laico', 'Lector Laico'),
             ('diacono', 'Diacono'),
             ('presvitero', 'Presbitero'),
             ('arcediano', 'Arcediano'),
             ('obispo', 'Obispo')]


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    @api.depends('name', 'categoria')
    def name_get(self):
        result = []
        for persona in self:
            if persona.name:
                if persona.categoria == 'lector_laico' :
                    name = 'L.Lco ' + persona.name
                elif persona.categoria in ['diacono', 'presvitero']:
                    name = 'Rev ' + persona.name
                elif persona.categoria == 'arcediano':
                    name = 'Ven ' + persona.name
                elif persona.categoria == 'obispo':
                    name = 'Exmo ' + persona.name
                else:
                    name = persona.name
            result.append((persona.id, name))
        return result

    es_miembro = fields.Boolean('Es miembro?')
    es_empleado = fields.Boolean('Es empleado?')
    no_registro = fields.Integer('No de registro')
    congregacion_id = fields.Many2one('iglesias.congregacion', 'Congregación')
    padecimientos = fields.Text('Padecimientos')
    medicamentos = fields.Text('Medicamentos')
    membresia = fields.Selection([('visitante', 'Visitante'), ('catecumeno', 'Catecumeno'),
                                  ('comulgante', 'Comulgante'), ('pasivo', 'Pasivo')], 'Tipo de membresía')
    fecha_alta = fields.Date('Fecha de alta', default=fields.Date.today())
    es_diezmador = fields.Boolean('Es Diezmador?')
    no_familia = fields.Integer('# de familia episcopal')
    fecha_baja = fields.Date('Fecha de baja')
    causa = fields.Selection([('traslado', 'Traslado'), ('fallecido', 'Fallecido')], 'Causa de baja')
    edad = fields.Integer('Edad', compute='calc_edad')
    categoria = fields.Selection(CATEGORIA, 'Categoría')
    cantidad_sacramentos = fields.Integer(compute='_calc_cantidad_sacramentos')
    sacramento_ids = fields.One2many('iglesias.sacramento', 'miembro_id')
    cantidad_mediosb = fields.Integer(compute='_calc_cantidad_mediosb')
    medios_basicos_ids = fields.One2many('product.template', 'responsable_id')


    _sql_constraints = [('iglesias_employee_ci_unique', 'unique(identification_id)', 'El CI debe ser único en la bd!')]

    @api.one
    @api.depends('birthday')
    def calc_edad(self):
        edad = self.birthday and (
        (datetime.datetime.now().date() - datetime.datetime.strptime(self.birthday, '%Y-%m-%d').date()).days / 365) or 0
        if edad < 0:
            self.edad = 0
        else:
            self.edad = edad

    @api.one
    @api.depends('sacramento_ids')
    def _calc_cantidad_sacramentos(self):
        self.cantidad_sacramentos = self.sacramento_ids and len(self.sacramento_ids.ids) or 0

    @api.one
    @api.depends('medios_basicos_ids')
    def _calc_cantidad_mediosb(self):
        self.cantidad_mediosb = self.medios_basicos_ids and len(self.medios_basicos_ids.ids) or 0

    @api.onchange('identification_id')
    def onchange_identification_id(self):
        if self.identification_id:
            self.gender = int(self.identification_id[-2]) % 2 == 0 and 'male' or 'female'
            self._set_date_from_ci()

    @api.one
    def _set_date_from_ci(self):
        if self.identification_id and len(self.identification_id) == 11:
            strdate = str(self.identification_id[:6])
            try:
                aux_str = "19" + strdate if int(strdate[:2]) > 25 else "20" + strdate
                self.birthday = datetime.datetime.strptime(aux_str, "%Y%m%d").date()
            except Exception, e:
                raise ValidationError(_('There are errors on employee CI'))
        else:
            self.birthday = False

    @api.multi
    def print_fe_bautismo(self):
        bautismos_ids = []
        for employe in self:
            for s in employe.sacramento_ids:
                if s.tipo_sacramento == 'bautismo':
                    bautismos_ids.append(s.id)
                    break
        return self.env['iglesias.sacramento'].browse(bautismos_ids).print_fe_bautismo()



