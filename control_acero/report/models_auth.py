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


class Departamento(models.Model):
    iddepartamento = models.AutoField(primary_key=True)
    departamento = models.CharField(max_length=254)
    departamento_estado = models.SmallIntegerField()
    departamento_abreviatura = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = 'departamento'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Empresa(models.Model):
    idempresa = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=500)
    empresa_abreviatura = models.CharField(max_length=45)
    empresa_rfc = models.CharField(max_length=45, blank=True, null=True)
    empresa_direccion = models.TextField(blank=True, null=True)
    empresa_estado = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'empresa'


class Genero(models.Model):
    idgenero = models.AutoField(primary_key=True)
    genero = models.CharField(max_length=45)
    genero_abreviatura = models.CharField(max_length=45)
    genero_estado = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'genero'


class MaquinariaMigrations(models.Model):
    migration = models.CharField(max_length=255)
    batch = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'maquinaria_migrations'


class PermissionRole(models.Model):
    permission = models.ForeignKey('Permissions')
    role = models.ForeignKey('Roles')

    class Meta:
        managed = False
        db_table = 'permission_role'
        unique_together = (('permission', 'role'),)


class Permissions(models.Model):
    name = models.CharField(unique=True, max_length=255)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'permissions'


class RoleUser(models.Model):
    user = models.ForeignKey('Users')
    role = models.ForeignKey('Roles')

    class Meta:
        managed = False
        db_table = 'role_user'
        unique_together = (('user', 'role'),)


class Roles(models.Model):
    name = models.CharField(unique=True, max_length=255)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'roles'


class Titulo(models.Model):
    idtitulo = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=45)
    titulo_abreviatura = models.CharField(max_length=45, blank=True, null=True)
    titulo_estado = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'titulo'


class Ubicacion(models.Model):
    idubicacion = models.AutoField(primary_key=True)
    ubicacion = models.CharField(max_length=500)
    ubicacion_abreviatura = models.CharField(max_length=45, blank=True, null=True)
    ubicacion_direccion = models.TextField()
    ubicacion_estado = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'ubicacion'


class Usuario(models.Model):
    idusuario = models.AutoField(primary_key=True)
    usuario = models.CharField(unique=True, max_length=45, blank=True, null=True)
    clave = models.CharField(max_length=45, blank=True, null=True)
    nombre = models.CharField(max_length=45)
    apaterno = models.CharField(max_length=45)
    amaterno = models.CharField(max_length=45)
    correo = models.CharField(max_length=45, blank=True, null=True)
    extension = models.CharField(max_length=45, blank=True, null=True)
    fnacimiento = models.DateField(blank=True, null=True)
    foto = models.CharField(max_length=200, blank=True, null=True)
    soporte = models.CharField(max_length=200, blank=True, null=True)
    usuario_estado = models.SmallIntegerField()
    timestamp = models.DateTimeField()
    idubicacion = models.ForeignKey(Ubicacion, db_column='idubicacion')
    idempresa = models.ForeignKey(Empresa, db_column='idempresa')
    iddepartamento = models.ForeignKey(Departamento, db_column='iddepartamento')
    idtitulo = models.ForeignKey(Titulo, db_column='idtitulo')
    idgenero = models.ForeignKey(Genero, db_column='idgenero')
    rfc = models.CharField(max_length=20, blank=True, null=True)
    idpuesto = models.IntegerField()
    remember_token = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'
        unique_together = (('nombre', 'apaterno', 'amaterno'),)
