from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Material(models.Model):
	nombre = models.CharField(blank=True, max_length=100)
	proveedor = models.CharField(default=0, max_length=20)
	ESTATUSTIPO = (
	    (1, 'Recto'),
	    (2, 'Rollo'),
	)
	tipo = models.IntegerField(choices=ESTATUSTIPO, default=1)
	diametro = models.FloatField(default=0)
	peso = models.FloatField(default=0)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.nombre

class Despiece(models.Model):
	nombre = models.CharField(max_length=100)
	pieza = models.CharField(default=0, max_length=20)
	calibre = models.CharField(default=0, max_length=20)
	pija = models.FloatField(default=0)
	longitud = models.FloatField(default=0)
	material = models.ManyToManyField(
		'material',
		blank=True,
	)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.nombre

class Elemento(models.Model):
	nombre = models.CharField(max_length=100)
	tipo = models.CharField(max_length=10)
	peso = models.FloatField(default=0)
	material = models.ManyToManyField(
		'material',
		blank=True,
	)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True, null=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.nombre

class Ingenieria(models.Model):
	ubicacion = models.CharField(max_length=100)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.ubicacion

class Transporte(models.Model):
	TIPOTRANSPORTE = (
	    (1, 'Local'),
	    (2, 'Foraneo'),
	)
	tipo = models.IntegerField(choices=TIPOTRANSPORTE, default=1)
	capacidad = models.IntegerField()
	placas = models.CharField(max_length=20)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.tipo

class Taller(models.Model):
	nombre = models.CharField(max_length=100)
	responsable = models.CharField(max_length=100, default=0)
	proveedor = models.CharField(default=0, max_length=20)
	ubicacion = models.CharField(max_length=100)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.nombre

class Funcion(models.Model):
	TIPOFUNCION = (
	    (1, 'Suministrador'),
	    (2, 'Habilitador'),
	    (3, 'Armador'),
	    (3, 'Colocador'),
	)
	tipo = models.IntegerField(choices=TIPOFUNCION, default=1)
	proveedor = models.CharField(default=0, max_length=20)
	tonelajeMaximo = models.FloatField(default=0)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.proveedor

class Frente(models.Model):
	nombre = models.CharField(max_length=100)
	identificacion = models.IntegerField()
	ubicacion = models.CharField(max_length=100)
	kilometros = models.FloatField(default=0)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.nombre

class ControlAsignacion(models.Model):
	cantidad = models.IntegerField()
	tiempoEntrega = models.IntegerField()
	funcion = models.ForeignKey(Funcion)
	frente = models.ForeignKey(Frente)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.nombre

class AsignacionEtapa(models.Model):
	funcion = models.ForeignKey(Funcion)
	ControlAsignacion = models.ForeignKey(ControlAsignacion)
	estatusEtapa = models.IntegerField()
	etapa = models.IntegerField()

class FrenteAsigna(models.Model):
	idOrden = models.IntegerField(null=True, blank=True)
	idFrente = models.IntegerField(blank=True)
	tipo = models.IntegerField()
	idEstructuraElemento = models.IntegerField()
	fechaRegistro = models.DateTimeField(auto_now_add=True)

class Apoyo(models.Model):
	numero = models.CharField(max_length=100)
	elemento = models.ManyToManyField(
		'elemento',
	)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.numero