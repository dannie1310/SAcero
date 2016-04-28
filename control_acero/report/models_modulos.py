# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Addendums(models.Model):
    idaddendum = models.IntegerField(db_column='IDAddendum', primary_key=True)  # Field name made lowercase.
    idsubcontrato = models.ForeignKey('Subcontratos', db_column='IDSubcontrato')  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=10)  # Field name made lowercase.
    monto = models.DecimalField(db_column='Monto', max_digits=19, decimal_places=4)  # Field name made lowercase.
    montoanticipo = models.DecimalField(db_column='MontoAnticipo', max_digits=19, decimal_places=4)  # Field name made lowercase.
    pctretencionfg = models.DecimalField(db_column='PctRetencionFG', max_digits=5, decimal_places=2)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Addendums'


class Agrupacioncuentascontpaq(models.Model):
    idproyecto = models.IntegerField(db_column='IDProyecto')  # Field name made lowercase.
    codigocuenta = models.CharField(db_column='CodigoCuenta', max_length=30)  # Field name made lowercase.
    idagrupador = models.ForeignKey('Agrupadores', db_column='IDAgrupador')  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AgrupacionCuentasContpaq'
        unique_together = (('idproyecto', 'codigocuenta', 'idagrupador'),)


class Agrupacionfactvarios(models.Model):
    idproyecto = models.IntegerField(db_column='IDProyecto')  # Field name made lowercase.
    idtransaccioncdc = models.IntegerField(db_column='IDTransaccionCDC')  # Field name made lowercase.
    iditem = models.IntegerField(db_column='IDItem')  # Field name made lowercase.
    idagrupadornaturaleza = models.ForeignKey('Agrupadores', db_column='IDAgrupadorNaturaleza', blank=True, null=True)  # Field name made lowercase.
    idagrupadorfamilia = models.ForeignKey('Agrupadores', db_column='IDAgrupadorFamilia', blank=True, null=True)  # Field name made lowercase.
    idagrupadorinsumogenerico = models.ForeignKey('Agrupadores', db_column='IDAgrupadorInsumoGenerico', blank=True, null=True)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AgrupacionFactVarios'
        unique_together = (('idproyecto', 'idtransaccioncdc', 'iditem'),)


class Agrupacioninsumos(models.Model):
    idproyecto = models.ForeignKey('Proyectos', db_column='IDProyecto')  # Field name made lowercase.
    idinsumo = models.IntegerField(db_column='IDInsumo')  # Field name made lowercase.
    idagrupadornaturaleza = models.ForeignKey('Agrupadores', db_column='IDAgrupadorNaturaleza', blank=True, null=True)  # Field name made lowercase.
    idagrupadorfamilia = models.ForeignKey('Agrupadores', db_column='IDAgrupadorFamilia', blank=True, null=True)  # Field name made lowercase.
    idagrupadorinsumogenerico = models.ForeignKey('Agrupadores', db_column='IDAgrupadorInsumoGenerico', blank=True, null=True)  # Field name made lowercase.
    esamortizable = models.BooleanField(db_column='EsAmortizable')  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AgrupacionInsumos'
        unique_together = (('idproyecto', 'idinsumo'),)


class Agrupacionsubcontratos(models.Model):
    idproyecto = models.ForeignKey('Proyectos', db_column='IDProyecto')  # Field name made lowercase.
    idempresa = models.IntegerField(db_column='IDEmpresa')  # Field name made lowercase.
    idsubcontrato = models.IntegerField(db_column='IDSubcontrato')  # Field name made lowercase.
    idactividad = models.IntegerField(db_column='IDActividad')  # Field name made lowercase.
    idagrupadornaturaleza = models.ForeignKey('Agrupadores', db_column='IDAgrupadorNaturaleza', blank=True, null=True)  # Field name made lowercase.
    idagrupadorfamilia = models.ForeignKey('Agrupadores', db_column='IDAgrupadorFamilia', blank=True, null=True)  # Field name made lowercase.
    idagrupadorinsumogenerico = models.ForeignKey('Agrupadores', db_column='IDAgrupadorInsumoGenerico', blank=True, null=True)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AgrupacionSubcontratos'
        unique_together = (('idproyecto', 'idempresa', 'idsubcontrato', 'idactividad'),)


class Agrupadores(models.Model):
    idagrupador = models.IntegerField(db_column='IDAgrupador', primary_key=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    agrupador = models.CharField(db_column='Agrupador', max_length=300)  # Field name made lowercase.
    unidad = models.ForeignKey('Unidad', db_column='Unidad', blank=True, null=True)  # Field name made lowercase.
    idtipoagrupador = models.ForeignKey('Tiposagrupador', db_column='idTipoAgrupador')  # Field name made lowercase.
    idtipogasto = models.ForeignKey('Tiposgasto', db_column='idTipoGasto', blank=True, null=True)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Agrupadores'


class Agrupadores2(models.Model):
    idagrupador = models.IntegerField(db_column='IDAgrupador')  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    agrupador = models.CharField(db_column='Agrupador', max_length=300)  # Field name made lowercase.
    idtipoagrupador = models.IntegerField(db_column='idTipoAgrupador')  # Field name made lowercase.
    idtipogasto = models.IntegerField(db_column='idTipoGasto', blank=True, null=True)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Agrupadores2'


class Almacenescosto(models.Model):
    idalmacen = models.IntegerField(db_column='IDAlmacen', unique=True)  # Field name made lowercase.
    idproyecto = models.IntegerField(db_column='IDProyecto')  # Field name made lowercase.
    idtipocosto = models.ForeignKey('Tiposcosto', db_column='IDTipoCosto')  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50)  # Field name made lowercase.
    idalmacensao = models.IntegerField(db_column='IDAlmacenSAO')  # Field name made lowercase.
    nombrealmacensao = models.CharField(db_column='NombreAlmacenSAO', max_length=100)  # Field name made lowercase.
    cuentacontable = models.CharField(db_column='CuentaContable', max_length=30)  # Field name made lowercase.
    estaactivo = models.BooleanField(db_column='EstaActivo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AlmacenesCosto'
        unique_together = (('idproyecto', 'idalmacensao'),)


class Aplicaciones(models.Model):
    idaplicacion = models.IntegerField(db_column='IDAplicacion', primary_key=True)  # Field name made lowercase.
    aplicacion = models.CharField(db_column='Aplicacion', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Aplicaciones'


class Aplicacionesmenu(models.Model):
    idnodo = models.IntegerField(db_column='IDNodo', primary_key=True)  # Field name made lowercase.
    idaplicacion = models.ForeignKey(Aplicaciones, db_column='IDAplicacion')  # Field name made lowercase.
    nodo = models.BinaryField(db_column='Nodo')  # Field name made lowercase.
    nodonivel = models.SmallIntegerField(db_column='NodoNivel', blank=True, null=True)  # Field name made lowercase.
    essubmenu = models.BooleanField(db_column='EsSubmenu')  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nombreicono = models.CharField(db_column='NombreIcono', max_length=50, blank=True, null=True)  # Field name made lowercase.
    estaactivo = models.BooleanField(db_column='EstaActivo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AplicacionesMenu'
        unique_together = (('idaplicacion', 'nodo'),)


class Basedatosobra(models.Model):
    basedatos = models.CharField(db_column='BaseDatos', max_length=140)  # Field name made lowercase.
    creado = models.DateTimeField(db_column='Creado')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BaseDatosObra'


class Basesdatos(models.Model):
    idbasedatos = models.IntegerField(db_column='IDBaseDatos', unique=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50)  # Field name made lowercase.
    mascara = models.CharField(db_column='Mascara', max_length=50)  # Field name made lowercase.
    servidor = models.CharField(db_column='Servidor', max_length=100)  # Field name made lowercase.
    idtiposistemaorigen = models.ForeignKey('Tipossistemaorigen', db_column='IDTipoSistemaOrigen')  # Field name made lowercase.
    idtipobasedatos = models.ForeignKey('Tiposbasedatos', db_column='IDTipoBaseDatos')  # Field name made lowercase.
    estaactiva = models.BooleanField(db_column='EstaActiva')  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BasesDatos'
        unique_together = (('idtiposistemaorigen', 'idtipobasedatos'),)


class Clasificadores(models.Model):
    idclasificador = models.IntegerField(db_column='IDClasificador', primary_key=True)  # Field name made lowercase.
    clasificador = models.CharField(db_column='Clasificador', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Clasificadores'


class Clavestrabajadores(models.Model):
    idproyecto = models.IntegerField(db_column='IDProyecto', primary_key=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ClavesTrabajadores'


class Conceptoscalculo(models.Model):
    idproyecto = models.IntegerField(db_column='IDProyecto')  # Field name made lowercase.
    idconceptonom = models.IntegerField(db_column='IDConceptoNOM')  # Field name made lowercase.
    idnaturaleza = models.ForeignKey('Tiposnaturaleza', db_column='IDNaturaleza')  # Field name made lowercase.
    concepto = models.CharField(db_column='Concepto', max_length=50)  # Field name made lowercase.
    aplicainterfaz = models.BooleanField(db_column='AplicaInterfaz')  # Field name made lowercase.
    aplicafacturacion = models.BooleanField(db_column='AplicaFacturacion')  # Field name made lowercase.
    aplicaimss = models.BooleanField(db_column='AplicaIMSS')  # Field name made lowercase.
    aplicaestatal = models.BooleanField(db_column='AplicaEstatal')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ConceptosCalculo'
        unique_together = (('idproyecto', 'idconceptonom'),)


class Cuentasbancarias(models.Model):
    idcta = models.IntegerField(db_column='IDCta', primary_key=True)  # Field name made lowercase.
    numerocuenta = models.CharField(db_column='NumeroCuenta', unique=True, max_length=50)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True, null=True)  # Field name made lowercase.
    esorigen = models.BooleanField(db_column='EsOrigen')  # Field name made lowercase.
    esdestino = models.BooleanField(db_column='EsDestino')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CuentasBancarias'


class Diasordinarios(models.Model):
    idproyecto = models.IntegerField(db_column='IDProyecto', primary_key=True)  # Field name made lowercase.
    numerodiasordinarios = models.SmallIntegerField(db_column='NumeroDiasOrdinarios')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DiasOrdinarios'


class Documentos(models.Model):
    idremesa = models.ForeignKey('Remesas', db_column='IDRemesa')  # Field name made lowercase.
    iddocumento = models.IntegerField(db_column='IDDocumento')  # Field name made lowercase.
    seleccionado = models.BooleanField(db_column='Seleccionado')  # Field name made lowercase.
    revisado = models.ForeignKey('Documentosestadoproceso', db_column='Revisado', blank=True, null=True)  # Field name made lowercase.
    validado = models.ForeignKey('Documentosestadoproceso', db_column='Validado', blank=True, null=True)  # Field name made lowercase.
    autorizado = models.ForeignKey('Documentosestadoproceso', db_column='Autorizado', blank=True, null=True)  # Field name made lowercase.
    liberadopago = models.BooleanField(db_column='LiberadoPago')  # Field name made lowercase.
    idtransaccioncdc = models.IntegerField(db_column='IDTransaccionCDC', blank=True, null=True)  # Field name made lowercase.
    idtipodocumento = models.ForeignKey('Documentostipo', db_column='IDTipoDocumento')  # Field name made lowercase.
    idorigendocumento = models.ForeignKey('Documentosorigendocumento', db_column='IDOrigenDocumento')  # Field name made lowercase.
    idrubro = models.ForeignKey('Documentosrubro', db_column='IDRubro', blank=True, null=True)  # Field name made lowercase.
    idtipogasto = models.ForeignKey('Documentostipogasto', db_column='IDTipoGasto', blank=True, null=True)  # Field name made lowercase.
    idtipopago = models.ForeignKey('Documentostipopago', db_column='IDTipoPago', blank=True, null=True)  # Field name made lowercase.
    iddestinatario = models.IntegerField(db_column='IDDestinatario')  # Field name made lowercase.
    idempresasolicitante = models.IntegerField(db_column='IDEmpresaSolicitante')  # Field name made lowercase.
    numerofolio = models.TextField(db_column='NumeroFolio', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    referencia = models.TextField(db_column='Referencia', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fecha = models.CharField(db_column='Fecha', max_length=10)  # Field name made lowercase.
    fechavencimiento = models.CharField(db_column='FechaVencimiento', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechaingresosistema = models.CharField(db_column='FechaIngresoSistema', max_length=10, blank=True, null=True)  # Field name made lowercase.
    concepto = models.TextField(db_column='Concepto', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    montototal = models.DecimalField(db_column='MontoTotal', max_digits=19, decimal_places=4)  # Field name made lowercase.
    montoautorizado = models.DecimalField(db_column='MontoAutorizado', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    montoacuenta = models.DecimalField(db_column='MontoACuenta', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    saldo = models.DecimalField(db_column='Saldo', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    idmoneda = models.SmallIntegerField(db_column='IDMoneda')  # Field name made lowercase.
    tipocambio = models.DecimalField(db_column='TipoCambio', max_digits=10, decimal_places=4)  # Field name made lowercase.
    saldomonedanacional = models.DecimalField(db_column='SaldoMonedaNacional', max_digits=19, decimal_places=4)  # Field name made lowercase.
    montototalsolicitado = models.DecimalField(db_column='MontoTotalSolicitado', max_digits=19, decimal_places=4)  # Field name made lowercase.
    observaciones = models.TextField(db_column='Observaciones', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    idusuarioregistro = models.IntegerField(db_column='IDUsuarioRegistro', blank=True, null=True)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.
    aprobado = models.SmallIntegerField(db_column='Aprobado', blank=True, null=True)  # Field name made lowercase.
    aprobadosocios = models.SmallIntegerField(db_column='AprobadoSocios', blank=True, null=True)  # Field name made lowercase.
    idtipodestinatario = models.SmallIntegerField(db_column='IDTipoDestinatario')  # Field name made lowercase.
    destinatario = models.CharField(db_column='Destinatario', max_length=140)  # Field name made lowercase.
    iddestinatario2 = models.IntegerField(db_column='IDDestinatario2', blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', max_length=20)  # Field name made lowercase.
    validadocontrolproyectos = models.SmallIntegerField(db_column='ValidadoControlProyectos', blank=True, null=True)  # Field name made lowercase.
    fechainicioperiodo = models.CharField(db_column='FechaInicioPeriodo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechaterminoperiodo = models.CharField(db_column='FechaTerminoPeriodo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    iddocumento_0 = models.IntegerField(db_column='IDDocumento')  # Field name made lowercase. Field renamed because of name conflict.
    idsubcontrato = models.IntegerField(db_column='IDSubcontrato')  # Field name made lowercase.
    idtipodocumento_0 = models.ForeignKey('Documentostipo', db_column='IDTipoDocumento')  # Field name made lowercase. Field renamed because of name conflict.
    idestatusdocumento = models.ForeignKey('Documentosestatus', db_column='IDEstatusDocumento')  # Field name made lowercase.
    fechahoraregistro_0 = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase. Field renamed because of name conflict.

    class Meta:
        managed = False
        db_table = 'Documentos'
        unique_together = (('iddocumento_0', 'iddocumento_0'),)


class Documentos(models.Model):
    idremesa = models.ForeignKey('Remesas', db_column='IDRemesa')  # Field name made lowercase.
    iddocumento = models.IntegerField(db_column='IDDocumento')  # Field name made lowercase.
    seleccionado = models.BooleanField(db_column='Seleccionado')  # Field name made lowercase.
    revisado = models.ForeignKey('Documentosestadoproceso', db_column='Revisado', blank=True, null=True)  # Field name made lowercase.
    validado = models.ForeignKey('Documentosestadoproceso', db_column='Validado', blank=True, null=True)  # Field name made lowercase.
    autorizado = models.ForeignKey('Documentosestadoproceso', db_column='Autorizado', blank=True, null=True)  # Field name made lowercase.
    liberadopago = models.BooleanField(db_column='LiberadoPago')  # Field name made lowercase.
    idtransaccioncdc = models.IntegerField(db_column='IDTransaccionCDC', blank=True, null=True)  # Field name made lowercase.
    idtipodocumento = models.ForeignKey('Documentostipo', db_column='IDTipoDocumento')  # Field name made lowercase.
    idorigendocumento = models.ForeignKey('Documentosorigendocumento', db_column='IDOrigenDocumento')  # Field name made lowercase.
    idrubro = models.ForeignKey('Documentosrubro', db_column='IDRubro', blank=True, null=True)  # Field name made lowercase.
    idtipogasto = models.ForeignKey('Documentostipogasto', db_column='IDTipoGasto', blank=True, null=True)  # Field name made lowercase.
    idtipopago = models.ForeignKey('Documentostipopago', db_column='IDTipoPago', blank=True, null=True)  # Field name made lowercase.
    iddestinatario = models.IntegerField(db_column='IDDestinatario')  # Field name made lowercase.
    idempresasolicitante = models.IntegerField(db_column='IDEmpresaSolicitante')  # Field name made lowercase.
    numerofolio = models.TextField(db_column='NumeroFolio', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    referencia = models.TextField(db_column='Referencia', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fecha = models.CharField(db_column='Fecha', max_length=10)  # Field name made lowercase.
    fechavencimiento = models.CharField(db_column='FechaVencimiento', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechaingresosistema = models.CharField(db_column='FechaIngresoSistema', max_length=10, blank=True, null=True)  # Field name made lowercase.
    concepto = models.TextField(db_column='Concepto', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    montototal = models.DecimalField(db_column='MontoTotal', max_digits=19, decimal_places=4)  # Field name made lowercase.
    montoautorizado = models.DecimalField(db_column='MontoAutorizado', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    montoacuenta = models.DecimalField(db_column='MontoACuenta', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    saldo = models.DecimalField(db_column='Saldo', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    idmoneda = models.SmallIntegerField(db_column='IDMoneda')  # Field name made lowercase.
    tipocambio = models.DecimalField(db_column='TipoCambio', max_digits=10, decimal_places=4)  # Field name made lowercase.
    saldomonedanacional = models.DecimalField(db_column='SaldoMonedaNacional', max_digits=19, decimal_places=4)  # Field name made lowercase.
    montototalsolicitado = models.DecimalField(db_column='MontoTotalSolicitado', max_digits=19, decimal_places=4)  # Field name made lowercase.
    observaciones = models.TextField(db_column='Observaciones', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    idusuarioregistro = models.IntegerField(db_column='IDUsuarioRegistro', blank=True, null=True)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.
    aprobado = models.SmallIntegerField(db_column='Aprobado', blank=True, null=True)  # Field name made lowercase.
    aprobadosocios = models.SmallIntegerField(db_column='AprobadoSocios', blank=True, null=True)  # Field name made lowercase.
    idtipodestinatario = models.SmallIntegerField(db_column='IDTipoDestinatario')  # Field name made lowercase.
    destinatario = models.CharField(db_column='Destinatario', max_length=140)  # Field name made lowercase.
    iddestinatario2 = models.IntegerField(db_column='IDDestinatario2', blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', max_length=20)  # Field name made lowercase.
    validadocontrolproyectos = models.SmallIntegerField(db_column='ValidadoControlProyectos', blank=True, null=True)  # Field name made lowercase.
    fechainicioperiodo = models.CharField(db_column='FechaInicioPeriodo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechaterminoperiodo = models.CharField(db_column='FechaTerminoPeriodo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    iddocumento_0 = models.IntegerField(db_column='IDDocumento')  # Field name made lowercase. Field renamed because of name conflict.
    idsubcontrato = models.IntegerField(db_column='IDSubcontrato')  # Field name made lowercase.
    idtipodocumento_0 = models.ForeignKey('Documentostipo', db_column='IDTipoDocumento')  # Field name made lowercase. Field renamed because of name conflict.
    idestatusdocumento = models.ForeignKey('Documentosestatus', db_column='IDEstatusDocumento')  # Field name made lowercase.
    fechahoraregistro_0 = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase. Field renamed because of name conflict.

    class Meta:
        managed = False
        db_table = 'Documentos'
        unique_together = (('iddocumento_0', 'iddocumento_0'),)


class Documentosdestinatario(models.Model):
    iddestinatario = models.IntegerField(db_column='IDDestinatario', primary_key=True)  # Field name made lowercase.
    destinatario = models.TextField(db_column='Destinatario')  # Field name made lowercase. This field type is a guess.
    idtipodestinatario = models.ForeignKey('Documentosdestinatariotipo', db_column='IDTipoDestinatario')  # Field name made lowercase.
    idempresacdc = models.IntegerField(db_column='IDEmpresaCDC', blank=True, null=True)  # Field name made lowercase.
    idfondocdc = models.IntegerField(db_column='IDFondoCDC', blank=True, null=True)  # Field name made lowercase.
    idproyecto = models.IntegerField(db_column='IDProyecto', blank=True, null=True)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocumentosDestinatario'


class Documentosdestinatariotipo(models.Model):
    idtipodestinatario = models.SmallIntegerField(db_column='IDTipoDestinatario', primary_key=True)  # Field name made lowercase.
    tipodestinatario = models.CharField(db_column='TipoDestinatario', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocumentosDestinatarioTipo'


class Documentosestadoproceso(models.Model):
    idestadoproceso = models.SmallIntegerField(db_column='IDEstadoProceso', primary_key=True)  # Field name made lowercase.
    estadoproceso = models.CharField(db_column='EstadoProceso', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocumentosEstadoProceso'


class Documentosestatus(models.Model):
    idestatusdocumento = models.IntegerField(db_column='IDEstatusDocumento', primary_key=True)  # Field name made lowercase.
    estatusdocumento = models.CharField(db_column='EstatusDocumento', max_length=50)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocumentosEstatus'


class Documentosliberados(models.Model):
    iddocumento = models.ForeignKey('Documentosprocesados', db_column='IDDocumento')  # Field name made lowercase.
    idproceso = models.ForeignKey('Documentosprocesados', db_column='IDProceso')  # Field name made lowercase.
    idusuarioliberacion = models.IntegerField(db_column='IDUsuarioLiberacion')  # Field name made lowercase.
    fechahoraliberacion = models.DateTimeField(db_column='FechaHoraLiberacion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocumentosLiberados'
        unique_together = (('iddocumento', 'idproceso'),)


class Documentosmovimientos(models.Model):
    iddocumento = models.ForeignKey(Documentos, db_column='IDDocumento')  # Field name made lowercase.
    idtipomovimiento = models.ForeignKey('Documentosmovimientostipo', db_column='IDTipoMovimiento')  # Field name made lowercase.
    idproceso = models.ForeignKey('Procesos', db_column='IDProceso')  # Field name made lowercase.
    idusuariomovimiento = models.IntegerField(db_column='IDUsuarioMovimiento')  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocumentosMovimientos'


class Documentosmovimientostipo(models.Model):
    idtipomovimiento = models.SmallIntegerField(db_column='IDTipoMovimiento', primary_key=True)  # Field name made lowercase.
    tipomovimiento = models.CharField(db_column='TipoMovimiento', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocumentosMovimientosTipo'


class Documentosobservaciones(models.Model):
    idobservacion = models.IntegerField(db_column='IDObservacion', primary_key=True)  # Field name made lowercase.
    iddocumento = models.ForeignKey(Documentos, db_column='IDDocumento')  # Field name made lowercase.
    idmotivoobservacion = models.ForeignKey('Documentosobservacionesmotivo', db_column='IDMotivoObservacion')  # Field name made lowercase.
    idproceso = models.ForeignKey('Procesos', db_column='IDProceso')  # Field name made lowercase.
    observaciones = models.TextField(db_column='Observaciones')  # Field name made lowercase. This field type is a guess.
    idusuarioregistro = models.IntegerField(db_column='IDUsuarioRegistro', blank=True, null=True)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocumentosObservaciones'


class Documentosobservacionesmotivo(models.Model):
    idmotivoobservacion = models.SmallIntegerField(db_column='IDMotivoObservacion', primary_key=True)  # Field name made lowercase.
    motivoobservacion = models.CharField(db_column='MotivoObservacion', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocumentosObservacionesMotivo'


class Documentosorigendocumento(models.Model):
    idorigendocumento = models.SmallIntegerField(db_column='IDOrigenDocumento', primary_key=True)  # Field name made lowercase.
    origendocumento = models.CharField(db_column='OrigenDocumento', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocumentosOrigenDocumento'


class Documentosprocesados(models.Model):
    iddocumento = models.ForeignKey(Documentos, db_column='IDDocumento')  # Field name made lowercase.
    idproceso = models.ForeignKey('Procesos', db_column='IDProceso')  # Field name made lowercase.
    montoautorizadoprimerenvio = models.DecimalField(db_column='MontoAutorizadoPrimerEnvio', max_digits=19, decimal_places=4)  # Field name made lowercase.
    montoautorizadosegundoenvio = models.DecimalField(db_column='MontoAutorizadoSegundoEnvio', max_digits=19, decimal_places=4)  # Field name made lowercase.
    idusuarioautorizacion = models.IntegerField(db_column='IDUsuarioAutorizacion', blank=True, null=True)  # Field name made lowercase.
    fechahoraautorizacion = models.DateTimeField(db_column='FechaHoraAutorizacion', blank=True, null=True)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocumentosProcesados'
        unique_together = (('iddocumento', 'idproceso'),)


class Documentosrubro(models.Model):
    idrubro = models.SmallIntegerField(db_column='IDRubro', primary_key=True)  # Field name made lowercase.
    rubro = models.CharField(db_column='Rubro', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocumentosRubro'


class Documentostipo(models.Model):
    idtipodocumento = models.IntegerField(db_column='IDTipoDocumento', primary_key=True)  # Field name made lowercase.
    tipodocumento = models.CharField(db_column='TipoDocumento', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocumentosTipo'


class Documentostipodocumento(models.Model):
    idtipodocumento = models.SmallIntegerField(db_column='IDTipoDocumento', primary_key=True)  # Field name made lowercase.
    idtipotransaccioncdc = models.IntegerField(db_column='IDTipoTransaccionCDC', blank=True, null=True)  # Field name made lowercase.
    opcionescdc = models.IntegerField(db_column='OpcionesCDC', blank=True, null=True)  # Field name made lowercase.
    tipodocumento = models.CharField(db_column='TipoDocumento', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocumentosTipoDocumento'


class Documentostipogasto(models.Model):
    idtipogasto = models.IntegerField(db_column='IDTipoGasto', primary_key=True)  # Field name made lowercase.
    tipogasto = models.CharField(db_column='TipoGasto', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocumentosTipoGasto'


class Documentostipopago(models.Model):
    idtipopago = models.IntegerField(db_column='IDTipoPago', primary_key=True)  # Field name made lowercase.
    tipopago = models.CharField(db_column='TipoPago', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocumentosTipoPago'


class Empresas(models.Model):
    idempresa = models.IntegerField(db_column='IDEmpresa', primary_key=True)  # Field name made lowercase.
    empresa = models.CharField(db_column='Empresa', max_length=100)  # Field name made lowercase.
    idtipoempresa = models.ForeignKey('Empresastipos', db_column='IDTipoEmpresa')  # Field name made lowercase.
    idempresasao = models.IntegerField(db_column='IDEmpresaSAO')  # Field name made lowercase.
    idlogotipo = models.ForeignKey('Logotipos', db_column='IDLogotipo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Empresas'


class Empresastipos(models.Model):
    idtipoempresa = models.SmallIntegerField(db_column='IDTipoEmpresa', primary_key=True)  # Field name made lowercase.
    tipoempresa = models.CharField(db_column='TipoEmpresa', max_length=50)  # Field name made lowercase.
    tipoempresasimple = models.CharField(db_column='TipoEmpresaSimple', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EmpresasTipos'


class Equivalenciahorasoperacion(models.Model):
    idequivalenciahoras = models.IntegerField(db_column='IDEquivalenciaHoras', unique=True)  # Field name made lowercase.
    idproyecto = models.ForeignKey('Proyectos', db_column='IDProyecto')  # Field name made lowercase.
    horasoperacion = models.SmallIntegerField(db_column='HorasOperacion')  # Field name made lowercase.
    horaslunesaviernes = models.DecimalField(db_column='HorasLunesAViernes', max_digits=4, decimal_places=2)  # Field name made lowercase.
    horassabado = models.DecimalField(db_column='HorasSabado', max_digits=4, decimal_places=2)  # Field name made lowercase.
    horasdomingo = models.DecimalField(db_column='HorasDomingo', max_digits=4, decimal_places=2)  # Field name made lowercase.
    vigencia = models.CharField(db_column='Vigencia', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EquivalenciaHorasOperacion'
        unique_together = (('idproyecto', 'horasoperacion', 'vigencia'),)


class Estados(models.Model):
    idestado = models.IntegerField(db_column='IDEstado', primary_key=True)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Estados'


class Horasmensuales(models.Model):
    idhoramensual = models.IntegerField(db_column='IDHoraMensual', unique=True)  # Field name made lowercase.
    idequivalenciahoras = models.ForeignKey(Equivalenciahorasoperacion, db_column='IDEquivalenciaHoras')  # Field name made lowercase.
    idproyecto = models.IntegerField(db_column='IDProyecto')  # Field name made lowercase.
    idmaquina = models.ForeignKey('Maquinas', db_column='IDMaquina')  # Field name made lowercase.
    vigencia = models.CharField(db_column='Vigencia', max_length=10)  # Field name made lowercase.
    horascontrato = models.SmallIntegerField(db_column='HorasContrato')  # Field name made lowercase.
    horasoperacion = models.SmallIntegerField(db_column='HorasOperacion')  # Field name made lowercase.
    horasprograma = models.SmallIntegerField(db_column='HorasPrograma')  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HorasMensuales'
        unique_together = (('idmaquina', 'idproyecto', 'vigencia'),)


class Horasmensualses(models.Model):
    idhoramensual = models.IntegerField(db_column='IDHoraMensual')  # Field name made lowercase.
    idequivalenciahoras = models.IntegerField(db_column='IDEquivalenciaHoras')  # Field name made lowercase.
    idproyecto = models.IntegerField(db_column='IDProyecto')  # Field name made lowercase.
    idmaquina = models.IntegerField(db_column='IDMaquina')  # Field name made lowercase.
    vigencia = models.CharField(db_column='Vigencia', max_length=10)  # Field name made lowercase.
    horascontrato = models.SmallIntegerField(db_column='HorasContrato')  # Field name made lowercase.
    horasoperacion = models.SmallIntegerField(db_column='HorasOperacion')  # Field name made lowercase.
    horasprograma = models.SmallIntegerField(db_column='HorasPrograma')  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HorasMensualses'


class Listasasistencia(models.Model):
    idlistaasistencia = models.IntegerField(db_column='IDListaAsistencia', unique=True)  # Field name made lowercase.
    idnomina = models.ForeignKey('Nominas', db_column='IDNomina')  # Field name made lowercase.
    idtipolistaasistencia = models.ForeignKey('Tiposlistaasistencia', db_column='IDTipoListaAsistencia')  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=10)  # Field name made lowercase.
    referencia = models.CharField(db_column='Referencia', max_length=100, blank=True, null=True)  # Field name made lowercase.
    observaciones = models.CharField(db_column='Observaciones', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aprobada = models.BooleanField(db_column='Aprobada')  # Field name made lowercase.
    enviadasao = models.BooleanField(db_column='EnviadaSAO')  # Field name made lowercase.
    idtransaccion = models.IntegerField(db_column='IDTransaccion', blank=True, null=True)  # Field name made lowercase.
    numerofolio = models.IntegerField(db_column='NumeroFolio', blank=True, null=True)  # Field name made lowercase.
    fechahoraenvio = models.DateTimeField(db_column='FechaHoraEnvio', blank=True, null=True)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ListasAsistencia'
        unique_together = (('idnomina', 'fecha'),)


class Listasasistenciatrabajadores(models.Model):
    idlistaasistencia = models.ForeignKey(Listasasistencia, db_column='IDListaAsistencia')  # Field name made lowercase.
    idempleadonom = models.IntegerField(db_column='IDEmpleadoNOM')  # Field name made lowercase.
    idcategoria = models.IntegerField(db_column='IDCategoria')  # Field name made lowercase.
    idalmacen = models.ForeignKey(Almacenescosto, db_column='IDAlmacen', blank=True, null=True)  # Field name made lowercase.
    cantidad = models.DecimalField(db_column='Cantidad', max_digits=10, decimal_places=4)  # Field name made lowercase.
    unidad = models.CharField(db_column='Unidad', max_length=20)  # Field name made lowercase.
    esdestajo = models.BooleanField(db_column='EsDestajo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ListasAsistenciaTrabajadores'
        unique_together = (('idlistaasistencia', 'idempleadonom'),)


class Loglanzamientos(models.Model):
    idlanzamiento = models.IntegerField(db_column='IDLanzamiento')  # Field name made lowercase.
    idreporte = models.IntegerField(db_column='IDReporte')  # Field name made lowercase.
    tiempoinicio = models.DateTimeField(db_column='TiempoInicio')  # Field name made lowercase.
    tiempotermino = models.DateTimeField(db_column='TiempoTermino')  # Field name made lowercase.
    duracionsegundos = models.DecimalField(db_column='DuracionSegundos', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LogLanzamientos'
        unique_together = (('idlanzamiento', 'idreporte'),)


class Logotipos(models.Model):
    idlogotipo = models.IntegerField(db_column='IDLogotipo', primary_key=True)  # Field name made lowercase.
    esdelgrupo = models.BooleanField(db_column='EsDelGrupo')  # Field name made lowercase.
    estavigente = models.BooleanField(db_column='EstaVigente')  # Field name made lowercase.
    logotipooriginal = models.BinaryField(db_column='LogotipoOriginal')  # Field name made lowercase.
    logotiporeportes = models.BinaryField(db_column='LogotipoReportes')  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Logotipos'


class Maquinas(models.Model):
    idmaquina = models.IntegerField(db_column='IDMaquina', unique=True)  # Field name made lowercase.
    idproyecto = models.IntegerField(db_column='IDProyecto')  # Field name made lowercase.
    idalmacensao = models.IntegerField(db_column='IDAlmacenSAO')  # Field name made lowercase.
    idactivoscaf = models.IntegerField(db_column='IDActivoSCAF', blank=True, null=True)  # Field name made lowercase.
    idclasemotor = models.SmallIntegerField(db_column='IDClaseMotor', blank=True, null=True)  # Field name made lowercase.
    numeroeconomico = models.CharField(db_column='NumeroEconomico', max_length=50, blank=True, null=True)  # Field name made lowercase.
    numeroseriemotor = models.CharField(db_column='NumeroSerieMotor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    marca = models.CharField(db_column='Marca', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modelo = models.CharField(db_column='Modelo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    capacidad = models.CharField(db_column='Capacidad', max_length=20, blank=True, null=True)  # Field name made lowercase.
    capacidadhp = models.CharField(db_column='CapacidadHP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    idcategoria = models.IntegerField(db_column='IDCategoria', blank=True, null=True)  # Field name made lowercase.
    idpropiedad = models.IntegerField(db_column='IDPropiedad', blank=True, null=True)  # Field name made lowercase.
    horasparamantenimiento = models.SmallIntegerField(db_column='HorasParaMantenimiento', blank=True, null=True)  # Field name made lowercase.
    fechaentrada = models.CharField(db_column='FechaEntrada', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechasalida = models.CharField(db_column='FechaSalida', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.
    idusuarioregistro = models.IntegerField(db_column='idUsuarioRegistro', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Maquinas'
        unique_together = (('idproyecto', 'idalmacensao'),)


class Maquinascategoria(models.Model):
    idcategoria = models.IntegerField(db_column='IDCategoria', primary_key=True)  # Field name made lowercase.
    categoria = models.CharField(db_column='Categoria', max_length=50)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MaquinasCategoria'


class Maquinaspropiedad(models.Model):
    idpropiedad = models.IntegerField(db_column='IDPropiedad', primary_key=True)  # Field name made lowercase.
    propiedad = models.CharField(db_column='Propiedad', max_length=50)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MaquinasPropiedad'


class Nominas(models.Model):
    idnomina = models.IntegerField(db_column='IDNomina', unique=True)  # Field name made lowercase.
    idproyecto = models.IntegerField(db_column='IDProyecto')  # Field name made lowercase.
    idperiodo = models.IntegerField(db_column='IDPeriodo')  # Field name made lowercase.
    numeroperiodo = models.SmallIntegerField(db_column='NumeroPeriodo', blank=True, null=True)  # Field name made lowercase.
    inicioperiodo = models.CharField(db_column='InicioPeriodo', max_length=10)  # Field name made lowercase.
    finperiodo = models.CharField(db_column='FinPeriodo', max_length=10)  # Field name made lowercase.
    diasperiodo = models.SmallIntegerField(db_column='DiasPeriodo')  # Field name made lowercase.
    idporcentaje = models.ForeignKey('Porcentajesfacturacion', db_column='IDPorcentaje')  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Nominas'
        unique_together = (('idproyecto', 'idperiodo'),)


class Nominasconceptos(models.Model):
    idnomina = models.IntegerField(db_column='IDNomina')  # Field name made lowercase.
    idempleadonom = models.IntegerField(db_column='IDEmpleadoNOM')  # Field name made lowercase.
    idconceptonom = models.IntegerField(db_column='IDConceptoNOM')  # Field name made lowercase.
    idnaturaleza = models.ForeignKey('Tiposnaturaleza', db_column='IDNaturaleza')  # Field name made lowercase.
    importetotal = models.DecimalField(db_column='ImporteTotal', max_digits=10, decimal_places=4)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NominasConceptos'


class Nominasempleados(models.Model):
    idnomina = models.ForeignKey(Nominas, db_column='IDNomina')  # Field name made lowercase.
    idempleadonom = models.IntegerField(db_column='IDEmpleadoNOM')  # Field name made lowercase.
    codigoempleado = models.CharField(db_column='CodigoEmpleado', max_length=10, blank=True, null=True)  # Field name made lowercase.
    claveproyectonom = models.CharField(db_column='ClaveProyectoNOM', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nombrenom = models.CharField(db_column='NombreNOM', max_length=100)  # Field name made lowercase.
    nssnom = models.CharField(db_column='NSSNOM', max_length=20)  # Field name made lowercase.
    rfcnom = models.CharField(db_column='RFCNOM', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fechaalta = models.CharField(db_column='FechaAlta', max_length=10, blank=True, null=True)  # Field name made lowercase.
    estadoempleado = models.CharField(db_column='EstadoEmpleado', max_length=1)  # Field name made lowercase.
    fechabaja = models.CharField(db_column='FechaBaja', max_length=10, blank=True, null=True)  # Field name made lowercase.
    departamento = models.CharField(db_column='Departamento', max_length=100, blank=True, null=True)  # Field name made lowercase.
    clavecategorianom = models.CharField(db_column='ClaveCategoriaNOM', max_length=10, blank=True, null=True)  # Field name made lowercase.
    categorianom = models.CharField(db_column='CategoriaNOM', max_length=100, blank=True, null=True)  # Field name made lowercase.
    idcategorianomsao = models.IntegerField(db_column='IDCategoriaNOMSAO', blank=True, null=True)  # Field name made lowercase.
    categorianomsao = models.CharField(db_column='CategoriaNOMSAO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cuentacontablenomsao = models.CharField(db_column='CuentaContableNOMSAO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sueldodiario = models.DecimalField(db_column='SueldoDiario', max_digits=19, decimal_places=4)  # Field name made lowercase.
    diastrabajados = models.SmallIntegerField(db_column='DiasTrabajados')  # Field name made lowercase.
    valorjornalnom = models.DecimalField(db_column='ValorJornalNOM', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    valorprestacionnom = models.DecimalField(db_column='ValorPrestacionNOM', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    porcentajeextranom = models.DecimalField(db_column='PorcentajeExtraNOM', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    nombresao = models.CharField(db_column='NombreSAO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nsssao = models.CharField(db_column='NSSSAO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rfcsao = models.CharField(db_column='RFCSAO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    idcategoriasao = models.IntegerField(db_column='IDCategoriaSAO', blank=True, null=True)  # Field name made lowercase.
    clavecategoriasao = models.CharField(db_column='ClaveCategoriaSAO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    categoriasao = models.CharField(db_column='CategoriaSAO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cuentacontablesao = models.CharField(db_column='CuentaContableSAO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    valorjornalsao = models.DecimalField(db_column='ValorJornalSAO', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    valorprestacionsao = models.DecimalField(db_column='ValorPrestacionSAO', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    porcentajeextrasao = models.DecimalField(db_column='PorcentajeExtraSAO', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    igualdadnss = models.SmallIntegerField(db_column='IgualdadNSS')  # Field name made lowercase.
    tieneclaveproyecto = models.BooleanField(db_column='TieneClaveProyecto')  # Field name made lowercase.
    igualdadcategoria = models.SmallIntegerField(db_column='IgualdadCategoria')  # Field name made lowercase.
    igualdadvalorjornal = models.SmallIntegerField(db_column='IgualdadValorJornal')  # Field name made lowercase.
    estaduplicado = models.BooleanField(db_column='EstaDuplicado')  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NominasEmpleados'


class Nominasincidencias(models.Model):
    idnomina = models.IntegerField(db_column='IDNomina')  # Field name made lowercase.
    idempleadonom = models.IntegerField(db_column='IDEmpleadoNOM')  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NominasIncidencias'


class Notificacioneseventos(models.Model):
    idevento = models.IntegerField(db_column='IDEvento', primary_key=True)  # Field name made lowercase.
    evento = models.CharField(db_column='Evento', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NotificacionesEventos'


class Notificacionessuscripciones(models.Model):
    idsuscripcion = models.IntegerField(db_column='IDSuscripcion', primary_key=True)  # Field name made lowercase.
    idsuscriptor = models.ForeignKey('Notificacionessuscriptores', db_column='IDSuscriptor')  # Field name made lowercase.
    idevento = models.ForeignKey(Notificacioneseventos, db_column='IDEvento')  # Field name made lowercase.
    suscritotodosproyectos = models.BooleanField(db_column='SuscritoTodosProyectos')  # Field name made lowercase.
    enviarcomo = models.SmallIntegerField(db_column='EnviarComo')  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NotificacionesSuscripciones'


class Notificacionessuscripcionesproyectos(models.Model):
    idsuscripcion = models.ForeignKey(Notificacionessuscripciones, db_column='IDSuscripcion')  # Field name made lowercase.
    idproyecto = models.IntegerField(db_column='IDProyecto')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NotificacionesSuscripcionesProyectos'
        unique_together = (('idsuscripcion', 'idproyecto'),)


class Notificacionessuscriptores(models.Model):
    idsuscriptor = models.IntegerField(db_column='IDSuscriptor', primary_key=True)  # Field name made lowercase.
    suscriptor = models.CharField(db_column='Suscriptor', max_length=100)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=50)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NotificacionesSuscriptores'


class Pagos(models.Model):
    idpago = models.IntegerField(db_column='IDPago', primary_key=True)  # Field name made lowercase.
    idtiporemesa = models.SmallIntegerField(db_column='IDTipoRemesa')  # Field name made lowercase.
    anio = models.IntegerField(db_column='Anio')  # Field name made lowercase.
    numerosemana = models.SmallIntegerField(db_column='NumeroSemana')  # Field name made lowercase.
    idproyecto = models.IntegerField(db_column='IDProyecto')  # Field name made lowercase.
    idtipoempresa = models.IntegerField(db_column='IDTipoEmpresa')  # Field name made lowercase.
    idtipoenvio = models.SmallIntegerField(db_column='IDTipoEnvio')  # Field name made lowercase.
    fechapago = models.CharField(db_column='FechaPago', max_length=10)  # Field name made lowercase.
    referencia = models.CharField(db_column='Referencia', max_length=50)  # Field name made lowercase.
    concepto = models.TextField(db_column='Concepto')  # Field name made lowercase. This field type is a guess.
    montopagado = models.DecimalField(db_column='MontoPagado', max_digits=19, decimal_places=4)  # Field name made lowercase.
    idctaorigen = models.ForeignKey(Cuentasbancarias, db_column='IDCtaOrigen')  # Field name made lowercase.
    idctadestino = models.ForeignKey(Cuentasbancarias, db_column='IDCtaDestino')  # Field name made lowercase.
    observaciones = models.TextField(db_column='Observaciones', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Pagos'


class Pagoscomprobantes(models.Model):
    idpago = models.ForeignKey(Pagos, db_column='IDPago')  # Field name made lowercase.
    nombrearchivocomprobante = models.CharField(db_column='NombreArchivoComprobante', max_length=50)  # Field name made lowercase.
    comprobante = models.BinaryField(db_column='Comprobante')  # Field name made lowercase.
    mimetypearchivo = models.CharField(db_column='MIMETypeArchivo', max_length=50)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PagosComprobantes'


class Parametros(models.Model):
    nombreservidor = models.CharField(db_column='NombreServidor', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Parametros'


class Parametrosaplicacion(models.Model):
    diastoleranciabaja = models.SmallIntegerField(db_column='DiasToleranciaBaja')  # Field name made lowercase.
    dialimitesolicitudremesa = models.SmallIntegerField(db_column='DiaLimiteSolicitudRemesa')  # Field name made lowercase.
    horalimitesolicitudremesa = models.CharField(db_column='HoraLimiteSolicitudRemesa', max_length=8)  # Field name made lowercase.
    dialimitepropuestaautomatica = models.SmallIntegerField(db_column='DiaLimitePropuestaAutomatica', blank=True, null=True)  # Field name made lowercase.
    horalimitepropuestaautomatica = models.CharField(db_column='HoraLimitePropuestaAutomatica', max_length=8, blank=True, null=True)  # Field name made lowercase.
    permitirmovremesasanteriores = models.BooleanField(db_column='PermitirMovRemesasAnteriores')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ParametrosAplicacion'


class Parametrosaplicacion(models.Model):
    diastoleranciabaja = models.SmallIntegerField(db_column='DiasToleranciaBaja')  # Field name made lowercase.
    dialimitesolicitudremesa = models.SmallIntegerField(db_column='DiaLimiteSolicitudRemesa')  # Field name made lowercase.
    horalimitesolicitudremesa = models.CharField(db_column='HoraLimiteSolicitudRemesa', max_length=8)  # Field name made lowercase.
    dialimitepropuestaautomatica = models.SmallIntegerField(db_column='DiaLimitePropuestaAutomatica', blank=True, null=True)  # Field name made lowercase.
    horalimitepropuestaautomatica = models.CharField(db_column='HoraLimitePropuestaAutomatica', max_length=8, blank=True, null=True)  # Field name made lowercase.
    permitirmovremesasanteriores = models.BooleanField(db_column='PermitirMovRemesasAnteriores')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ParametrosAplicacion'


class Perfiles(models.Model):
    idperfil = models.SmallIntegerField(db_column='IDPerfil')  # Field name made lowercase.
    perfil = models.CharField(db_column='Perfil', max_length=50)  # Field name made lowercase.
    idperfil_0 = models.IntegerField(db_column='IDPerfil')  # Field name made lowercase. Field renamed because of name conflict.
    nombreperfil = models.CharField(db_column='NombrePerfil', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Perfiles'
        unique_together = (('idperfil_0', 'idperfil_0'),)


class Perfiles(models.Model):
    idperfil = models.SmallIntegerField(db_column='IDPerfil')  # Field name made lowercase.
    perfil = models.CharField(db_column='Perfil', max_length=50)  # Field name made lowercase.
    idperfil_0 = models.IntegerField(db_column='IDPerfil')  # Field name made lowercase. Field renamed because of name conflict.
    nombreperfil = models.CharField(db_column='NombrePerfil', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Perfiles'
        unique_together = (('idperfil_0', 'idperfil_0'),)


class Perfilesaplicacion(models.Model):
    idperfil = models.ForeignKey(Perfiles, db_column='IDPerfil')  # Field name made lowercase.
    idaplicacion = models.ForeignKey(Aplicaciones, db_column='IDAplicacion')  # Field name made lowercase.
    accesototal = models.BooleanField(db_column='AccesoTotal')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PerfilesAplicacion'
        unique_together = (('idperfil', 'idaplicacion'),)


class Perfilesaplicacionmenu(models.Model):
    idperfil = models.ForeignKey(Perfilesaplicacion, db_column='IDPerfil')  # Field name made lowercase.
    idaplicacion = models.ForeignKey(Perfilesaplicacion, db_column='IDAplicacion')  # Field name made lowercase.
    idnodomenu = models.ForeignKey(Aplicacionesmenu, db_column='IDNodoMenu')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PerfilesAplicacionMenu'
        unique_together = (('idperfil', 'idaplicacion', 'idnodomenu'),)


class Perfilesprocesos(models.Model):
    idperfil = models.ForeignKey(Perfiles, db_column='IDPerfil')  # Field name made lowercase.
    idproceso = models.ForeignKey('Procesos', db_column='IDProceso')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PerfilesProcesos'
        unique_together = (('idperfil', 'idproceso'),)


class Perfilesrubros(models.Model):
    idperfil = models.ForeignKey(Perfiles, db_column='IDPerfil')  # Field name made lowercase.
    idrubro = models.ForeignKey(Documentosrubro, db_column='IDRubro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PerfilesRubros'
        unique_together = (('idperfil', 'idrubro'),)


class Perfilestiposempresa(models.Model):
    idperfil = models.ForeignKey(Perfiles, db_column='IDPerfil')  # Field name made lowercase.
    idtipoempresa = models.SmallIntegerField(db_column='IDTipoEmpresa')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PerfilesTiposEmpresa'
        unique_together = (('idperfil', 'idtipoempresa'),)


class Perfilesusuarios(models.Model):
    idperfil = models.ForeignKey(Perfiles, db_column='IDPerfil')  # Field name made lowercase.
    idusuario = models.ForeignKey('Usuarios', db_column='IDUsuario')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PerfilesUsuarios'
        unique_together = (('idusuario', 'idperfil'),)


class Perfilesusuariosaplicacion(models.Model):
    idperfil = models.ForeignKey(Perfilesaplicacion, db_column='IDPerfil')  # Field name made lowercase.
    idaplicacion = models.ForeignKey(Perfilesaplicacion, db_column='IDAplicacion')  # Field name made lowercase.
    idusuario = models.ForeignKey('Usuarios', db_column='IDUsuario')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PerfilesUsuariosAplicacion'
        unique_together = (('idperfil', 'idaplicacion', 'idusuario'),)


class Porcentajesfacturacion(models.Model):
    idporcentaje = models.IntegerField(db_column='IDPorcentaje', unique=True)  # Field name made lowercase.
    idproyecto = models.IntegerField(db_column='IDProyecto')  # Field name made lowercase.
    vigencia = models.CharField(db_column='Vigencia', max_length=10)  # Field name made lowercase.
    imss = models.DecimalField(db_column='IMSS', max_digits=6, decimal_places=4)  # Field name made lowercase.
    impuestoestatal = models.DecimalField(db_column='ImpuestoEstatal', max_digits=6, decimal_places=4)  # Field name made lowercase.
    administracion = models.DecimalField(db_column='Administracion', max_digits=6, decimal_places=4)  # Field name made lowercase.
    iva = models.DecimalField(db_column='IVA', max_digits=6, decimal_places=4)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PorcentajesFacturacion'
        unique_together = (('idproyecto', 'vigencia'),)


class Procesos(models.Model):
    idproceso = models.SmallIntegerField(db_column='IDProceso', primary_key=True)  # Field name made lowercase.
    proceso = models.CharField(db_column='Proceso', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Procesos'


class Proyectos(models.Model):
    idproyecto = models.IntegerField(db_column='IDProyecto', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=100)  # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    idtipoproyecto = models.ForeignKey('Tiposproyecto', db_column='IDTipoProyecto', blank=True, null=True)  # Field name made lowercase.
    idlogotipo = models.ForeignKey(Logotipos, db_column='IDLogotipo', blank=True, null=True)  # Field name made lowercase.
    idempresa = models.ForeignKey(Empresas, db_column='IDEmpresa', blank=True, null=True)  # Field name made lowercase.
    idestado = models.ForeignKey(Estados, db_column='IDEstado', blank=True, null=True)  # Field name made lowercase.
    direccion = models.TextField(db_column='Direccion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fechainicio = models.CharField(db_column='FechaInicio', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechatermino = models.CharField(db_column='FechaTermino', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechainiciocontrato = models.CharField(db_column='FechaInicioContrato', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechaterminocontrato = models.CharField(db_column='FechaTerminoContrato', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pctparticipacion = models.DecimalField(db_column='PctParticipacion', max_digits=5, decimal_places=2)  # Field name made lowercase.
    pctmetautilidadcorporativo = models.DecimalField(db_column='PctMetaUtilidadCorporativo', max_digits=5, decimal_places=2)  # Field name made lowercase.
    pctmetautilidadobra = models.DecimalField(db_column='PctMetaUtilidadObra', max_digits=5, decimal_places=2)  # Field name made lowercase.
    montoventacontrato = models.DecimalField(db_column='MontoVentaContrato', max_digits=19, decimal_places=4)  # Field name made lowercase.
    montoactualcontrato = models.DecimalField(db_column='MontoActualContrato', max_digits=19, decimal_places=4)  # Field name made lowercase.
    montoinicialpio = models.DecimalField(db_column='MontoInicialPIO', max_digits=19, decimal_places=4)  # Field name made lowercase.
    montoactualpio = models.DecimalField(db_column='MontoActualPIO', max_digits=19, decimal_places=4)  # Field name made lowercase.
    estaactivo = models.BooleanField(db_column='EstaActivo')  # Field name made lowercase.
    visibleenreportes = models.BooleanField(db_column='VisibleEnReportes')  # Field name made lowercase.
    visibleenapps = models.BooleanField(db_column='VisibleEnApps')  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.
    logotipo = models.BinaryField(db_column='Logotipo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Proyectos'


class Proyectosempresas(models.Model):
    idproyecto = models.ForeignKey(Proyectos, db_column='IDProyecto')  # Field name made lowercase.
    idempresa = models.ForeignKey(Empresas, db_column='IDEmpresa')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ProyectosEmpresas'
        unique_together = (('idproyecto', 'idempresa'),)


class Proyectosunificados(models.Model):
    idproyecto = models.ForeignKey(Proyectos, db_column='IDProyecto')  # Field name made lowercase.
    idbasedatos = models.ForeignKey(Basesdatos, db_column='IDBaseDatos')  # Field name made lowercase.
    idproyectounificado = models.IntegerField(db_column='IDProyectoUnificado')  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ProyectosUnificados'
        unique_together = (('idproyecto', 'idbasedatos', 'idproyectounificado'),)


class Remesas(models.Model):
    idremesa = models.IntegerField(db_column='IDRemesa', primary_key=True)  # Field name made lowercase.
    idproyecto = models.ForeignKey('Remesasfolios', db_column='IDProyecto')  # Field name made lowercase.
    anio = models.ForeignKey('Remesasfolios', db_column='Anio')  # Field name made lowercase.
    numerosemana = models.ForeignKey('Remesasfolios', db_column='NumeroSemana')  # Field name made lowercase.
    folio = models.SmallIntegerField(db_column='Folio')  # Field name made lowercase.
    idtiporemesa = models.ForeignKey('Remesastiporemesa', db_column='IDTipoRemesa')  # Field name made lowercase.
    idestadoremesa = models.ForeignKey('Remesasestadoremesa', db_column='IDEstadoRemesa')  # Field name made lowercase.
    idusuarioregistro = models.IntegerField(db_column='IDUsuarioRegistro', blank=True, null=True)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Remesas'


class Remesasbitacoraeventos(models.Model):
    idremesa = models.ForeignKey(Remesas, db_column='IDRemesa')  # Field name made lowercase.
    idtipoevento = models.ForeignKey('Remesasbitacoratipoevento', db_column='IDTipoEvento')  # Field name made lowercase.
    idusuario = models.IntegerField(db_column='IDUsuario')  # Field name made lowercase.
    fechahoraevento = models.DateTimeField(db_column='FechaHoraEvento')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RemesasBitacoraEventos'


class Remesasbitacoratipoevento(models.Model):
    idtipoevento = models.SmallIntegerField(db_column='IDTipoEvento', primary_key=True)  # Field name made lowercase.
    tipoevento = models.CharField(db_column='TipoEvento', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RemesasBitacoraTipoEvento'


class Remesasestadoremesa(models.Model):
    idestadoremesa = models.SmallIntegerField(db_column='IDEstadoRemesa', primary_key=True)  # Field name made lowercase.
    estadoremesa = models.CharField(db_column='EstadoRemesa', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RemesasEstadoRemesa'


class Remesasfolios(models.Model):
    idproyecto = models.IntegerField(db_column='IDProyecto')  # Field name made lowercase.
    anio = models.ForeignKey('Remesassemanas', db_column='Anio')  # Field name made lowercase.
    numerosemana = models.ForeignKey('Remesassemanas', db_column='NumeroSemana')  # Field name made lowercase.
    ultimofolio = models.SmallIntegerField(db_column='UltimoFolio')  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RemesasFolios'
        unique_together = (('idproyecto', 'anio', 'numerosemana'),)


class Remesasliberadas(models.Model):
    idremesa = models.ForeignKey(Remesas, db_column='IDRemesa')  # Field name made lowercase.
    idtipoempresa = models.SmallIntegerField(db_column='IDTipoEmpresa')  # Field name made lowercase.
    idusuarioliberacion = models.IntegerField(db_column='IDUsuarioLiberacion')  # Field name made lowercase.
    fechahoraliberacion = models.DateTimeField(db_column='FechaHoraLiberacion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RemesasLiberadas'
        unique_together = (('idremesa', 'idtipoempresa'),)


class Remesassemanas(models.Model):
    anio = models.IntegerField(db_column='Anio')  # Field name made lowercase.
    numerosemana = models.SmallIntegerField(db_column='NumeroSemana')  # Field name made lowercase.
    fechainicial = models.CharField(db_column='FechaInicial', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechatermino = models.CharField(db_column='FechaTermino', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RemesasSemanas'
        unique_together = (('anio', 'numerosemana'),)


class Remesastiporemesa(models.Model):
    idtiporemesa = models.SmallIntegerField(db_column='IDTipoRemesa', primary_key=True)  # Field name made lowercase.
    tiporemesa = models.CharField(db_column='TipoRemesa', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RemesasTipoRemesa'


class Reportehoras(models.Model):
    idreporte = models.IntegerField(db_column='IDReporte', unique=True)  # Field name made lowercase.
    idproyecto = models.IntegerField(db_column='IDProyecto')  # Field name made lowercase.
    idmaquina = models.ForeignKey(Maquinas, db_column='IDMaquina')  # Field name made lowercase.
    fechareporte = models.CharField(db_column='FechaReporte', max_length=10)  # Field name made lowercase.
    enviadosao = models.BooleanField(db_column='EnviadoSAO')  # Field name made lowercase.
    idhoramensual = models.ForeignKey(Horasmensuales, db_column='IDHoraMensual', blank=True, null=True)  # Field name made lowercase.
    idtransaccionsao = models.IntegerField(db_column='IDTransaccionSAO', blank=True, null=True)  # Field name made lowercase.
    numerofoliosao = models.IntegerField(db_column='NumeroFolioSAO', blank=True, null=True)  # Field name made lowercase.
    fechahoraenvio = models.DateTimeField(db_column='FechaHoraEnvio', blank=True, null=True)  # Field name made lowercase.
    idusuarioenvio = models.ForeignKey('Usuarios', db_column='IDUsuarioEnvio', blank=True, null=True)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ReporteHoras'
        unique_together = (('idproyecto', 'idmaquina', 'fechareporte'),)


class Reportehorasdetalle(models.Model):
    idreportehora = models.IntegerField(db_column='IDReporteHora', primary_key=True)  # Field name made lowercase.
    idreporteturno = models.ForeignKey('Reportehorasturnos', db_column='IDReporteTurno')  # Field name made lowercase.
    idtipohora = models.ForeignKey('Tiposhora', db_column='IDTipoHora')  # Field name made lowercase.
    idactividad = models.IntegerField(db_column='IDActividad', blank=True, null=True)  # Field name made lowercase.
    rutaactividad = models.TextField(db_column='RutaActividad', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    unidadactividad = models.CharField(db_column='UnidadActividad', max_length=16, blank=True, null=True)  # Field name made lowercase.
    cantidadhoras = models.DecimalField(db_column='CantidadHoras', max_digits=4, decimal_places=2)  # Field name made lowercase.
    observaciones = models.TextField(db_column='Observaciones', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    aprobada = models.BooleanField(db_column='Aprobada')  # Field name made lowercase.
    enviadasao = models.BooleanField(db_column='EnviadaSAO')  # Field name made lowercase.
    iditemsao = models.IntegerField(db_column='IDItemSAO', blank=True, null=True)  # Field name made lowercase.
    cantidadhorasenviada = models.DecimalField(db_column='CantidadHorasEnviada', max_digits=4, decimal_places=2)  # Field name made lowercase.
    preciounitario = models.DecimalField(db_column='PrecioUnitario', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    numeroseriemaquina = models.CharField(db_column='NumeroSerieMaquina', max_length=64, blank=True, null=True)  # Field name made lowercase.
    fechahoraenvio = models.DateTimeField(db_column='FechaHoraEnvio', blank=True, null=True)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.
    idusuarioregistro = models.ForeignKey('Usuarios', db_column='IDUsuarioRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ReporteHorasDetalle'


class Reportehorasturnos(models.Model):
    idreporteturno = models.IntegerField(db_column='IDReporteTurno', unique=True)  # Field name made lowercase.
    idreporte = models.ForeignKey(Reportehoras, db_column='IDReporte')  # Field name made lowercase.
    idturno = models.ForeignKey('Turnos', db_column='IDTurno')  # Field name made lowercase.
    horometroinicial = models.DecimalField(db_column='HorometroInicial', max_digits=6, decimal_places=1)  # Field name made lowercase.
    horometrofinal = models.DecimalField(db_column='HorometroFinal', max_digits=6, decimal_places=1)  # Field name made lowercase.
    observaciones = models.TextField(db_column='Observaciones', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ReporteHorasTurnos'
        unique_together = (('idreporte', 'idturno'),)


class Subcontratos(models.Model):
    idsubcontrato = models.IntegerField(db_column='IDSubcontrato', primary_key=True)  # Field name made lowercase.
    idproyecto = models.IntegerField(db_column='IDProyecto')  # Field name made lowercase.
    idclasificador = models.ForeignKey(Clasificadores, db_column='IDClasificador')  # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    montosubcontrato = models.DecimalField(db_column='MontoSubcontrato', max_digits=19, decimal_places=4)  # Field name made lowercase.
    montoanticipo = models.DecimalField(db_column='MontoAnticipo', max_digits=19, decimal_places=4)  # Field name made lowercase.
    pctretencionfg = models.DecimalField(db_column='PctRetencionFG', max_digits=5, decimal_places=2)  # Field name made lowercase.
    fechainiciocliente = models.CharField(db_column='FechaInicioCliente', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechaterminocliente = models.CharField(db_column='FechaTerminoCliente', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechainicioproyecto = models.CharField(db_column='FechaInicioProyecto', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechaterminoproyecto = models.CharField(db_column='FechaTerminoProyecto', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechainiciocontratista = models.CharField(db_column='FechaInicioContratista', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechaterminocontratista = models.CharField(db_column='FechaTerminoContratista', max_length=10, blank=True, null=True)  # Field name made lowercase.
    montoventacliente = models.DecimalField(db_column='MontoVentaCliente', max_digits=19, decimal_places=4)  # Field name made lowercase.
    montoventaactualcliente = models.DecimalField(db_column='MontoVentaActualCliente', max_digits=19, decimal_places=4)  # Field name made lowercase.
    montoinicialpio = models.DecimalField(db_column='MontoInicialPIO', max_digits=19, decimal_places=4)  # Field name made lowercase.
    montoactualpio = models.DecimalField(db_column='MontoActualPIO', max_digits=19, decimal_places=4)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Subcontratos'


class Tiposagrupador(models.Model):
    idtipoagrupador = models.IntegerField(db_column='IDTipoAgrupador', primary_key=True)  # Field name made lowercase.
    tipoagrupador = models.CharField(db_column='TipoAgrupador', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TiposAgrupador'


class Tiposbasedatos(models.Model):
    idtipobasedatos = models.SmallIntegerField(db_column='IDTipoBaseDatos', primary_key=True)  # Field name made lowercase.
    tipobasedatos = models.CharField(db_column='TipoBaseDatos', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TiposBaseDatos'


class Tiposcosto(models.Model):
    idtipocosto = models.IntegerField(db_column='IDTipoCosto', primary_key=True)  # Field name made lowercase.
    tipocosto = models.CharField(db_column='TipoCosto', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TiposCosto'


class Tiposgasto(models.Model):
    idtipogasto = models.IntegerField(db_column='IDTipoGasto', primary_key=True)  # Field name made lowercase.
    tipogasto = models.CharField(db_column='TipoGasto', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TiposGasto'


class Tiposhora(models.Model):
    idtipohora = models.IntegerField(db_column='IDTipoHora', primary_key=True)  # Field name made lowercase.
    tipohora = models.CharField(db_column='TipoHora', max_length=50)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TiposHora'


class Tiposlistaasistencia(models.Model):
    idtipolistaasistencia = models.IntegerField(db_column='IDTipoListaAsistencia', primary_key=True)  # Field name made lowercase.
    tipolistaasistencia = models.CharField(db_column='TipoListaAsistencia', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TiposListaAsistencia'


class Tiposnaturaleza(models.Model):
    idnaturaleza = models.IntegerField(db_column='IDNaturaleza', primary_key=True)  # Field name made lowercase.
    naturaleza = models.CharField(db_column='Naturaleza', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TiposNaturaleza'


class Tiposproyecto(models.Model):
    idtipoproyecto = models.IntegerField(db_column='IDTipoProyecto', primary_key=True)  # Field name made lowercase.
    tipoproyecto = models.CharField(db_column='TipoProyecto', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TiposProyecto'


class Tipossistemaorigen(models.Model):
    idtiposistemaorigen = models.SmallIntegerField(db_column='IDTipoSistemaOrigen', primary_key=True)  # Field name made lowercase.
    tiposistemaorigen = models.CharField(db_column='TipoSistemaOrigen', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TiposSistemaOrigen'


class Turnos(models.Model):
    idturno = models.IntegerField(db_column='IDTurno', primary_key=True)  # Field name made lowercase.
    turno = models.CharField(db_column='Turno', max_length=50)  # Field name made lowercase.
    horainicio = models.CharField(db_column='HoraInicio', max_length=8)  # Field name made lowercase.
    horatermino = models.CharField(db_column='HoraTermino', max_length=8)  # Field name made lowercase.
    horasturno = models.IntegerField(db_column='HorasTurno', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Turnos'


class Unidad(models.Model):
    id_unidad = models.CharField(db_column='ID_Unidad', primary_key=True, max_length=10)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=140)  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Unidad'


class Unidadesinsumos(models.Model):
    idunidad = models.IntegerField(db_column='IDUnidad', primary_key=True)  # Field name made lowercase.
    unidad = models.CharField(db_column='Unidad', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UnidadesInsumos'


class Unificacionproyectoobra(models.Model):
    idbasedatos = models.IntegerField(db_column='IDBaseDatos')  # Field name made lowercase.
    idproyecto = models.IntegerField(db_column='IDProyecto')  # Field name made lowercase.
    id_obra = models.IntegerField()
    principal = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'UnificacionProyectoObra'
        unique_together = (('idbasedatos', 'idproyecto', 'id_obra'),)


class Usuarios(models.Model):
    idusuario = models.IntegerField(db_column='IDUsuario', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=100)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', unique=True, max_length=50)  # Field name made lowercase.
    password = models.BinaryField(db_column='Password')  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=60, blank=True, null=True)  # Field name made lowercase.
    inactivo = models.BooleanField(db_column='Inactivo')  # Field name made lowercase.
    accesotodosproyectos = models.BooleanField(db_column='AccesoTodosProyectos')  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Usuarios'


class Usuarios2(models.Model):
    idusuario = models.IntegerField(db_column='IDUsuario', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=50, blank=True, null=True)  # Field name made lowercase.
    password = models.TextField(db_column='Password', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    inactivo = models.NullBooleanField(db_column='Inactivo')  # Field name made lowercase.
    accesotodosproyectos = models.NullBooleanField(db_column='AccesoTodosProyectos')  # Field name made lowercase.
    fechahoraregistro = models.DateTimeField(db_column='FechaHoraRegistro', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50, blank=True, null=True)  # Field name made lowercase.
    passworddecrypted = models.CharField(db_column='PasswordDecrypted', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Usuarios2'


class Usuariosaplicaciones(models.Model):
    idusuario = models.ForeignKey(Usuarios, db_column='IDUsuario')  # Field name made lowercase.
    idaplicacion = models.ForeignKey(Aplicaciones, db_column='IDAplicacion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UsuariosAplicaciones'
        unique_together = (('idusuario', 'idaplicacion'),)


class Usuariosproyectos(models.Model):
    idusuario = models.ForeignKey(Usuarios, db_column='IDUsuario')  # Field name made lowercase.
    idproyecto = models.ForeignKey(Proyectos, db_column='IDProyecto')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UsuariosProyectos'
        unique_together = (('idusuario', 'idproyecto'),)


class BasesDatosCadeco(models.Model):
    nombre = models.CharField(unique=True, max_length=100)
    activa = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'bases_datos_cadeco'


class BasesDatosInterfaz(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    activa = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'bases_datos_interfaz'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128)
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)
