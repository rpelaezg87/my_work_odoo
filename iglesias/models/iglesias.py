# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo import models, fields, api

SACRAMENTOS = [('bautismo', 'Bautismo'),
               ('confirmacion', 'Confirmacion'),
               ('bendicion', 'Bendicion de matrimonio'),
               ('orden_sagrada', 'Orden sagrada'),
               ('obituario', 'Obituario')]


class Congregacion(models.Model):
    _name = 'iglesias.congregacion'
    _rec_name = 'nombre'
    _order = 'no_registro'

    nombre = fields.Char('Nombre', required=True)
    no_registro = fields.Integer('No de registro', required=True)
    ministro_id = fields.Many2one('hr.employee', 'Ministro o Rector', domain=[('es_empleado', '=', True),
                                                                              ('categoria', 'in',
                                                                               ['diacono', 'presvitero'])])

    status = fields.Selection([('parroquia', 'Parroquias'), ('misiones', 'Misiones de parroquias'),
                               ('extensiones', 'Extensiones de parroquias')], 'Status')
    miembros_ids = fields.One2many('hr.employee', 'congregacion_id', 'Miembros', domain=[('es_miembro', '=', True)])
    liderazgo_ids = fields.One2many('congregacion.employee', 'congregacion_id', 'Liderazgo')
    sacramentos_ids = fields.One2many('iglesias.sacramento', 'congregacion_id', 'Sacramentos')
    mediosb_ids = fields.One2many('product.template', 'congregacion_id', 'Medios básicos')
    enfermos_ids = fields.One2many('hr.employee', 'congregacion_id', 'Enfermos',
                                   domain=[('padecimientos', '!=', False)])
    cantidad_mediosb = fields.Integer(compute='_calc_cantidad_mediosb')

    @api.one
    @api.depends('mediosb_ids')
    def _calc_cantidad_mediosb(self):
        self.cantidad_mediosb = self.mediosb_ids and len(self.mediosb_ids.ids) or 0

    @api.model
    def get_congregaciones_con_altas(self, fecha1, fecha2):
        dom = [('miembros_ids.fecha_alta', '>=', fecha1)]
        if fecha2:
            dom += [('miembros_ids.fecha_alta', '<=', fecha2)]
        return self.search(dom)

    @api.model
    def get_congregaciones_con_bajas(self, fecha1, fecha2):
        dom = [('miembros_ids.fecha_baja', '>=', fecha1)]
        if fecha2:
            dom += [('miembros_ids.fecha_baja', '<=', fecha2)]
        return self.search(dom)


class CongregacionEmployee(models.Model):
    _table = 'congregacion_employee_rel'
    _name = 'congregacion.employee'

    congregacion_id = fields.Many2one('iglesias.congregacion', 'Congregación')
    employee_id = fields.Many2one('hr.employee', 'Líder')
    funcion = fields.Selection([('rector', 'Rector'), ('ministro', 'Ministro'),
                                ('capiller_mayor', 'Capiller mayor'),
                                ('capiller_menor', 'Capiller menor'),
                                ('sercretario', 'Secretario'),
                                ('tesorero', 'Tesorero'),
                                ('vocal', 'Vocal'),
                                ('maestra', 'Maestra EBN')], "Función")
    fecha_instalado = fields.Date("Fecha de instalado")
    fecha_removido = fields.Date("Fecha de removido")


class Sacramento(models.Model):
    _name = 'iglesias.sacramento'
    _order = 'fecha'

    tipo_sacramento = fields.Selection(SACRAMENTOS, required=True)
    estacion_liturgica_id = fields.Many2one('iglesias.estacion_liturgica', 'Estación litúrgica', required=True)
    congregacion_id = fields.Many2one('iglesias.congregacion', 'Congregación', required=True)
    oficio_id = fields.Many2one('iglesias.oficio', 'Oficio')
    fecha = fields.Date('Fecha', required=True)
    lugar = fields.Text('Lugar')
    padre = fields.Many2one('hr.employee', 'Padre',
                            domain="[('id', 'not in', [miembro_id,madre,madrina, padrino]),('gender','in', [False,'male'])]")
    madre = fields.Many2one('hr.employee', 'Madre',
                            domain="[('id', 'not in', [miembro_id,padre,madrina, padrino]),('gender','in', [False,'female'])]")
    padrino = fields.Many2one('hr.employee', 'Padrino',
                              domain="[('id', 'not in', [miembro_id,padre, madre, madrina]),('gender','in', [False,'male'])]")
    madrina = fields.Many2one('hr.employee', 'Madrina',
                              domain="[('id', 'not in', [miembro_id,padre, madre, padrino]),('gender','in', [False,'female'])]")
    ministro = fields.Many2one('hr.employee', 'Ministro',
                               domain=[('es_empleado', '=', True), ('gender', 'in', [False, 'male'])])
    obispo = fields.Many2one('hr.employee', 'Obispo',
                             domain=[('es_empleado', '=', True), ('gender', 'in', [False, 'male'])])
    miembro_id = fields.Many2one('hr.employee', 'Hermano', required=True,
                                 domain="[('es_miembro', '=', True),('congregacion_id', '=', congregacion_id)]",
                                 help="Hermano al que se le realiza el sacramento")

    conyuge = fields.Many2one('hr.employee', 'Nombre', domain="[('es_miembro', '=', True),('id', '!=', miembro_id)]")
    no_registro = fields.Integer('Número de registro')
    testigo1 = fields.Many2one('hr.employee', 'Primer testigo',
                               domain="[('es_miembro', '=', True),('id', 'not in', [conyuge,testigo2, miembro_id])]")
    testigo2 = fields.Many2one('hr.employee', 'Segundo testigo',
                               domain="[('es_miembro', '=', True), ('id', 'not in', [conyuge,testigo1, miembro_id])]")
    miembro_categoria = fields.Selection(related='miembro_id.categoria')
    confirmacion_id = fields.Many2one('iglesias.sacramento', compute='calc_confirmacion_id')

    @api.one
    def calc_confirmacion_id(self):
        confirmacion = False
        if self.tipo_sacramento == 'bautismo' and self.miembro_id:
            confirmacion = self.search([('id', '!=', self.id), ('tipo_sacramento', '=', 'confirmacion'),
                                        ('miembro_id', '=', self.miembro_id.id)], limit=1)
        self.confirmacion_id = confirmacion

    @api.multi
    def print_fe_bautismo(self):
        return self.env['report'].get_action(self, 'iglesias.report_fe_bautismo')

    @api.onchange('tipo_sacramento')
    def onchange_tipo_sacramento(self):
        self.lugar = False
        self.padre = False
        self.madre = False
        self.padrino = False
        self.madrina = False
        self.obispo = False
        self.conyuge = False
        self.no_registro = False
        self.testigo1 = False
        self.testigo2 = False

    @api.onchange('congregacion_id')
    def onchange_congregacion_id(self):
        if self.congregacion_id:
            self.ministro = self.congregacion_id.ministro_id

    @api.model
    def create(self, vals={}):
        res = super(Sacramento, self).create(vals)
        if vals.get('tipo_sacramento', False):
            res.actualizar_hr()
        return res

    @api.multi
    def write(self, vals={}):
        res = super(Sacramento, self).write(vals)
        if vals.get('tipo_sacramento', False):
            for s in self:
                s.actualizar_hr()
        return res

    @api.one
    def actualizar_hr(self):
        if self.miembro_id:
            if self.tipo_sacramento == 'obituario':
                self.miembro_id.fecha_baja = self.fecha
                self.miembro_id.causa = 'fallecido'
            elif self.tipo_sacramento == 'bendicion':
                self.miembro_id.marital = 'married'
                if self.conyuge:
                    self.conyuge.marital = 'married'
            else:
                self.miembro_id.fecha_baja = False
                self.miembro_id.causa = False

    @api.model
    def get_sacramentos_entre_fechas(self, tipo, fecha1, fecha2, congregaciones_ids=[]):
        dom = [('fecha', '>=', fecha1), ('tipo_sacramento', '=', tipo)]
        if fecha2:
            dom += [('fecha', '<=', fecha2)]
        if congregaciones_ids:
            dom += [('miembro_id.congregacion_id', 'in', congregaciones_ids)]
        return self.search(dom)

    @api.constrains('tipo_sacramento', 'miembro_id')
    def _check_unique_sacramento(self):
        for sacramento in self:
            if sacramento.tipo_sacramento != 'orden_sagrada' and self.search(
                    [('tipo_sacramento', '=', sacramento.tipo_sacramento),
                     ('miembro_id', '=', sacramento.miembro_id.id),
					 ('id', '!=', sacramento.id)]):
                raise ValidationError(
                    "El miembro %s solo puede tener un sacramento de tipo %s" % (
                        sacramento.miembro_id.name, sacramento.tipo_sacramento))


class EstacionLiturgica(models.Model):
    _name = 'iglesias.estacion_liturgica'
    _rec_name = 'nombre'

    nombre = fields.Char('Nombre')
