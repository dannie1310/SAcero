# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_acero', '0174_inventariofisicodetalle_referencia'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='remision',
            options={'permissions': (('add_materiales', 'Puede Agregar Materiales'), ('change_materiales', 'Puede Actualizar Materiales'), ('delete_materiales', 'Puede Borrar Materiales'), ('add_despieces', 'Puede Agregar Despieces'), ('change_despieces', 'Puede Actualizar Despieces'), ('delete_despieces', 'Puede Borrar Despieces'), ('add_elementos', 'Puede Agregar Elementos'), ('change_elementos', 'Puede Actualizar Elementos'), ('delete_elementos', 'Puede Borrar Elementos'), ('add_apoyos', 'Puede Agregar Apoyos'), ('change_apoyos', 'Puede Actualizar Apoyos'), ('delete_apoyos', 'Puede Borrar Apoyos'), ('add_frentes', 'Puede Agregar Frentes'), ('change_frentes', 'Puede Actualizar Frentes'), ('delete_frentes', 'Puede Borrar Frentes'), ('add_proveedores', 'Puede Agregar Proveedores'), ('change_proveedores', 'Puede Actualizar Proveedores'), ('delete_proveedores', 'Puede Borrar Proveedores'), ('add_talleres', 'Puede Agregar Talleres'), ('change_talleres', 'Puede Actualizar Talleres'), ('delete_talleres', 'Puede Borrar Talleres'), ('add_transportes', 'Puede Agregar Transportes'), ('change_transportes', 'Puede Actualizar Transportes'), ('delete_transportes', 'Puede Borrar Transportes'), ('view_recepcion_material', 'Puede Visualizar Recepcion del Material del Fabricante'), ('view_salida_habilitado', 'Puede Visualizar Salida de Habilitado'), ('view_armado_recepcion', 'Puede Visualizar Armado Recepcion'), ('view_inventario_fisico', 'Puede Visualizar el Inventario Fisico'), ('view_reportes', 'Puede Visualizar Reportes'), ('view_movimientos', 'Puede Visualizar los Movimientos Realizados'), ('closing_inventarios', 'Puede Ajustar un Inventario Fisico'))},
        ),
    ]
