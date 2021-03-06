from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'control_acero'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^home/$', views.HomeView.as_view(), name='home'),
    url(r'^principal/$', views.principalView, name='principalView'),
    url(r'^perfil/$', views.perfilView, name='perfilView'),
    url(r'^usuario/login/$', views.loginUsuario, name='loginUsuario'),
    url(r'^usuario/logout/$', views.logout_view, name='logout'),
    url(r'^mail/$', views.mail, name='mail'),

    url(r'^recepcion/material/$', views.recepcionMaterialView, name='recepcionMaterialView'),
    
    url(r'^folios/mostrar/$', views.foliosMostrar, name='foliosMostrar'),
    url(r'^folios/salida/habilitado/$', views.foliosSalidaHabilitado, name='foliosSalidaHabilitado'),

    url(r'^salida/habilitado/$', views.salidaHabilitadoView, name='salidaHabilitadoView'),
    url(r'^salida/habilitado/material/$', views.salidaHabilitadoMaterial, name='salidaHabilitadoMaterial'),
    url(r'^salida/habilitado/save/$', views.salidaHabilitadoSave, name='salidaHabilitadoSave'),

    url(r'^entrada/armado/$', views.entradaArmadoView, name='entradaArmadoView'),
    url(r'^entrada/armado/combo/apoyo/$', views.entradaArmadoComboApoyo, name='entradaArmadoComboApoyo'),
    url(r'^entrada/armado/combo/elemento/$', views.entradaArmadoComboElemento, name='entradaArmadoComboElemento'),
    url(r'^entrada/armado/material/$', views.entradaArmadoMaterial, name='entradaArmadoMaterial'),
    url(r'^entrada/armado/save/$', views.entradaArmadoSave, name='entradaArmadoSave'),

    url(r'^fecha/$', views.fecha, name='fecha'),
    url(r'^elemento/elementomaterial/$', views.elementoMaterial, name='elementoMaterial'),

    url(r'^recepcion/material/save/$', views.recepcionMaterialSave, name='recepcionMaterialSave'),
    url(r'^reportes/reporte/$', views.reporteView, name='reporteView'),
    url(r'^reportes/reporteConsulta/$', views.reporteConsulta, name='reporteConsulta'),
    #"""------------------------------------------"""
    #"""        RUTAS RELACIONADAS CON INVENTARIOS  """
    #"""--------------------------------------------"""
    #url(r'^inventario/cierre/$', views.cierresView, name='cierresView'),
    #url(r'^inventario/fisico/busqueda/$', views.fisicoBusquedaView, name='fisicoBusquedaView'),
    url(r'^inventario/inventarioFisico/$', views.inventarioFisicoView, name='inventarioFisicoView'),
    url(r'^inventario/elemento/busqueda/$', views.elementoBusquedaView, name='elementoBusquedaView'),
    url(r'^inventario/material/busqueda/$', views.materialBusquedaView, name='materialBusquedaView'),
    url(r'^material/combo/$', views.materialCombo, name='materialCombo'),
    url(r'^inventario/frente/combo/busqueda/$', views.frenteComboBusquedaViews, name='frenteComboBusquedaViews'),
    url(r'^inventario/apoyo/busqueda/$', views.apoyoBusquedaView, name='apoyoBusquedaView'),
    url(r'^inventario/save/$', views.inventarioSave, name='inventarioSave'),
    url(r'^apoyo/combofiltrado/$', views.apoyoCombofiltrado, name='apoyoCombofiltrado'),
    url(r'^elemento/combo/$', views.comboElemento, name='comboElemento'),
    url(r'^frente/combo/$', views.comboFrente, name='comboFrente'),

    #"""------------------------------------------"""
    #"""   RUTAS RELACIONADAS CON COMBOS          """
    #"""------------------------------------------"""
    url(r'^combo/funcion/$', views.comboFuncion, name='comboFuncion'),
    url(r'^combo/frente/$', views.comboFrente, name='comboFrente'),
    url(r'^combo/apoyo/$', views.comboApoyo, name='comboApoyo'),
    url(r'^combo/elemento/$', views.comboElemento, name='comboElemento'),
    url(r'^combo/funciongeneral/$', views.comboFuncionGeneral, name='comboFuncionGeneral'),
    url(r'^combo/taller/$', views.comboTaller, name='comboTaller'),
    url(r'^combo/tallerG/$', views.comboTallerG, name='comboTallerG'),

    #"""------------------------------------------"""
    #"""   RUTAS RELACIONADAS CATALOGO DE APOYOS  """
    #"""------------------------------------------"""
    url(r'^catalogos/usuarios/$', views.usuariosView, name='usuariosView'),
    url(r'^catalogos/usuarios/new/$', views.usuariosNewView, name='usuariosNewView'),
    url(r'^catalogos/usuarios/(?P<pk>[0-9]+)/edit/$', views.usuariosEditView, name='usuariosEditView'),
    url(r'^catalogos/usuarios/(?P<pk>[0-9]+)/update/$', views.usuariosUpdateView, name='usuariosUpdateView'),
    url(r'^catalogos/grupos/new/$', views.gruposNewView, name='gruposNewView'),

    url(r'^catalogos/apoyos/$', views.apoyosView, name='apoyosView'),
    url(r'^catalogos/apoyos/new/$', views.apoyosNewView, name='apoyosNewView'),
    url(r'^catalogos/apoyos/(?P<pk>[0-9]+)/edit/$', views.apoyosEditView, name='apoyosEditView'),
    url(r'^catalogos/apoyos/(?P<pk>[0-9]+)/delete/$', views.apoyosLogicalDelete, name='apoyosLogicalDelete'),

    url(r'^catalogos/elementos/$', views.elementosView, name='elementosView'),
    url(r'^catalogos/elementos/new/$', views.elementosNewView, name='elementosNewView'),
    url(r'^catalogos/elementos/(?P<pk>[0-9]+)/edit/$', views.elementosEditView, name='elementosEditView'),

    url(r'^catalogos/despieces/$', views.despiecesView, name='despiecesView'),
    url(r'^catalogos/despieces/new/$', views.despiecesNewView, name='despiecesNewView'),
    url(r'^catalogos/despieces/(?P<pk>[0-9]+)/edit/$',views.despiecesEditView, name='despiecesEditView'),

    url(r'^catalogos/materiales/$', views.materialesView, name='materialesView'),
    url(r'^catalogos/materiales/new/$', views.materialesNewView, name='materialesNewView'),
    url(r'^catalogos/materiales/(?P<pk>[0-9]+)/edit/$', views.materialesEditView, name='materialesEditView'),

    url(r'^catalogos/frentes/$', views.frentesView, name='frentesView'),
    url(r'^catalogos/frentes/new/$', views.frentesNewView, name='frentesNewView'),
    url(r'^catalogos/frentes/(?P<pk>[0-9]+)/edit/$', views.frentesEditView, name='frentesEditView'),


    url(r'^catalogos/funciones/$', views.funcionesView, name='funcionesView'),
    url(r'^catalogos/funciones/new/$', views.funcionesNewView, name='funcionesNewView'),
    url(r'^catalogos/funciones/(?P<pk>[0-9]+)/edit/$', views.funcionesEditView, name='funcionesEditView'),

    url(r'^catalogos/talleres/$', views.talleresView, name='talleresView'),
    url(r'^catalogos/talleres/new/$', views.talleresNewView, name='talleresNewView'),
    url(r'^catalogos/talleres/(?P<pk>[0-9]+)/edit/$', views.talleresEditView, name='talleresEditView'),

    url(r'^catalogos/transportes/$', views.transportesView, name='transportesView'),
    url(r'^catalogos/transportes/new/$', views.transportesNewView, name='transportesNewView'),
    url(r'^catalogos/transportes/(?P<pk>[0-9]+)/edit/$', views.transportesEditView, name='transportesEditView'),

    url(r'^catalogos/movimientos/$', views.movimientosView, name='movimientosView'),
    url(r'^catalogos/movimientos/fecha/$', views.movimientosFecha, name='movimientosFecha'),
    url(r'^catalogos/movimientos/(?P<pk>[0-9]+)/detalle/$', views.movimientosDetalleView, name='movimientosDetalleView'),

    url(r'^inventario/$', views.inventario, name='inventario'),
    url(r'^inventario/remision/$', views.inventarioRemision, name='inventarioRemision'),
    url(r'^inventario/fisico/save/$', views.inventarioFisicoSave, name='inventarioFisicoSave'),
    url(r'^inventario/fisico/(?P<pk>[0-9]+)/edit/$', views.inventarioFisicoEditView, name='inventarioFisicoEditView'),
    url(r'^inventario/fisico/cierre/$', views.inventarioFisicoCierreView, name='inventarioFisicoCierreView'),
    url(r'^inventario/fisico/cierre/detalle/$', views.inventarioFisicoCierreDetalle, name='inventarioFisicoCierreDetalle'),
    url(r'^descarga/excel/(?P<filename>[\w\-]+)/$', views.descargaExcel, name='descargaExcel'),
    url(r'^inventario/fisico/cierre/save/$', views.inventarioFisicoCierreSave, name='inventarioFisicoCierreSave'),
    url(r'^inventario/fisico/cierre/ajuste/$', views.inventarioFisicoCierreAjusteView, name='inventarioFisicoCierreAjusteView'),

    url(r'^eliminar/folio/$', views.eliminarView, name='eliminarView'),
    url(r'^eliminar/buscar/folio/$', views.buscarFolio, name='buscarFolio'),
   # url(r'^leer/datos/$', views.leerArchivo, name='leerArchivo'),

   url(r'^buscar/funcion/$', views.buscarFuncion, name='buscarFuncion'),
   url(r'^buscar/elemento/$', views.buscarElemento, name='buscarElemento'),
   url(r'^buscar/frente/$', views.buscarFrente, name='buscarFrente'), 
   url(r'^buscar/apoyo/$', views.buscarApoyo, name='buscarApoyo'),
]