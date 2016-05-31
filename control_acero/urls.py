from django.conf.urls import url

from . import views

app_name = 'control_acero'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^home/$', views.HomeView.as_view(), name='home'),
    url(r'^principal/$', views.principalView, name='principalView'),
    url(r'^frenteTrabajo/$', views.frenteTrabajoView, name='frenteTrabajoView'),
    url(r'^controlAsignacion/$', views.controlAsignacionView, name='controlAsignacionView'),
    url(r'^controlAsignacion/nuevo/$', views.controlAsignacionNuevoView, name='controlAsignacionNuevoView'),
    url(r'^usuario/login/$', views.loginUsuario, name='loginUsuario'),
    url(r'^usuario/logout/$', views.logout, name='logout'),
    url(r'^acceso/$', views.AccesoView.as_view(), name='acceso'),
    #url(r'^suministro/$', views.SuministroView.as_view(), name='suministro'),
    url(r'^frente/$', views.FrenteView.as_view(), name='frente'),
    url(r'^control/$', views.ControlView.as_view(), name='control'),
    #url(r'^habilitado/$', views.HabilitadoView.as_view(), name='habilitado'),
    #url(r'^armado/$', views.ArmadoView.as_view(), name='armado'),
    #url(r'^colocado/$', views.ColocadoView.as_view(), name='colocado'),
    #"""------------------------------------------"""
    #""" RUTAS RELACIONADAS CON ORDEN DE TRABAJO """
    #"""------------------------------------------"""
    url(r'^ordenTrabajo/nuevo/$', views.ordenTrabajoNuevoView, name='ordenTrabajoNuevoView'),
    url(r'^ordenTrabajo/comboFuncion/$', views.ordenTrabajoComboFuncion, name='ordenTrabajoComboFuncion'),
    url(r'^ordenTrabajo/comboDespiece/$', views.ordenTrabajoComboDespiece, name='ordenTrabajoComboDespiece'),
    url(r'^ordenTrabajo/MaterialShow/$',views.ordenTrabajoMaterialShow, name='ordenTrabajoMaterialShow'),
    #url(r'^ordenTrabajo/ElementoDetalle/$', views.ordenTrabajoElementoDetalle, name='ordenTrabajoElementoDetalle'),
    #url(r'^ordenTrabajo/AsignarElemento/$',views.ordenTrabajoAsignarElemento, name='ordenTrabajoAsignarElemento'),

    #"""------------------------------------------"""
    #""" RUTAS RELACIONADAS CON FRENTE DE TRABAJO """
    #"""------------------------------------------"""
    url(r'^frenteTrabajo/$', views.frenteTrabajoView, name='frenteTrabajoView'),
    url(r'^frenteTrabajo/nuevo/$', views.frenteTrabajoNuevoView, name='frenteTrabajoNuevoView'),
    url(r'^frenteTrabajo/show/$', views.frenteTrabajoShow, name='frenteTrabajoShow'),

      #"""------------------------------------------"""
    #"""        RUTAS RELACIONADAS CON INVENTARIOS  """
    #"""--------------------------------------------"""
    url(r'^inventario/movimientos/$', views.movimientosView, name='movimientosView'),
    url(r'^inventario/movimientos/show/$', views.movimientosShow, name='movimientosShow'),
    #url(r'^inventario/cierre/$', views.cierresView, name='cierresView'),
    url(r'^inventario/fisico/busqueda/$', views.fisicoBusquedaView, name='fisicoBusquedaView'),
    url(r'^inventario/inventarioFisico/$', views.inventarioFisicoView, name='inventarioFisicoView'),
    url(r'^inventario/elemento/busqueda/$', views.elementoBusquedaView, name='elementoBusquedaView'),
    url(r'^inventario/material/busqueda/$', views.materialBusquedaView, name='materialBusquedaView'),
    url(r'^material/combo/$', views.materialCombo, name='materialCombo'),
    url(r'^inventario/despiece/busqueda/$', views.despieceBusquedaView, name='despieceBusquedaView'),
    url(r'^inventario/frente/combo/busqueda/$', views.frenteComboBusquedaViews, name='frenteComboBusquedaViews'),
    url(r'^inventario/apoyo/busqueda/$', views.apoyoBusquedaView, name='apoyoBusquedaView'),
    url(r'^inventario/save/$', views.inventarioSave, name='inventarioSave'),
    #"""------------------------------------------"""
    #"""        RUTAS RELACIONADAS CON APOYO      """
    #"""------------------------------------------"""
    url(r'^apoyo/combofiltrado/$', views.apoyoCombofiltrado, name='apoyoCombofiltrado'),

    url(r'^frente/show/$', views.frenteShow, name='frenteShow'),
    url(r'^frente/showelemento/$', views.frenteShowelemento, name='frenteShowelemento'),
    url(r'^frente/combo/$', views.frenteCombo, name='frenteCombo'),
    url(r'^frente/combofiltrado/$', views.frenteCombofiltrado, name='frenteCombofiltrado'),
    url(r'^frente/actualizaestatus/$', views.frenteActualizaestatus, name='frenteActualizaestatus'),
    #"""------------------------------------------"""
    #"""   RUTAS RELACIONADAS CON LAS FUNCIONES   """
    #"""------------------------------------------"""
    url(r'^funcion/show/$', views.funcionShow, name='funcionShow'),
    url(r'^funcion/combofiltrado/$', views.funcionComboFiltrado, name='funcionComboFiltrado'),
    #"""------------------------------------------"""
    #"""   RUTAS RELACIONADAS CATALOGO DE APOYOS  """
    #"""------------------------------------------"""
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




    url(r'^funcion/show/$', views.funcionShow, name='funcionShow'),
    url(r'^recepcion/$', views.RecepcionView.as_view(), name='recepcion'),
    url(r'^estructura/combo/$', views.estructuraCombo, name='estructuraCombo'),
    url(r'^elemento/combo/$', views.elementoCombo, name='elementoCombo'),
    url(r'^elemento/comboapoyoelmento/$', views.elementoComboApoyoElemento, name='elementoComboApoyoElemento'),
    url(r'^elemento/elementomaterial/$', views.elementoMaterial, name='elementoMaterial'),

    url(r'^programa/save/$', views.programaSave, name='programaSave'),
    url(r'^programa/combofiltrado/$', views.programaCombofiltrado, name='programaCombofiltrado'),

    url(r'^asignacion/save/$', views.asignacionSave, name='asignacionSave'),

    url(r'^asignacion/comboOrden/$', views.asignacionComboOrden, name='asignacionComboOrden'),
    url(r'^asignacion/comboFrente/$', views.asignacionComboFrente, name='asignacionComboFrente'),
    url(r'^asignacion/comboPrograma/$', views.asignacionComboPrograma, name='asignacionComboPrograma'),
    url(r'^asignacion/comboElementos/$', views.asignacionComboElementos, name='asignacionComboElementos'),

    #"""------------------------------------------"""
    #""" RUTAS RELACIONADAS CON SUMINISTRO """
    #"""------------------------------------------"""
    url(r'^suministro/recepcion/$', views.suministroRecepcionView, name='suministroRecepcionView'),
    url(r'^suministro/asignacion/$', views.suministroAsignacionView, name='suministroAsignacionView'),
    url(r'^suministro/asigna/comboPrograma/$', views.suministroAsignaComboPrograma, name='suministroAsignaComboPrograma'),
    url(r'^suministro/asigna/comboFuncion/$', views.suministroAsignaComboFuncion, name='suministroAsignaComboFuncion'),
    url(r'^suministro/asigna/elementos/$', views.suministroAsignaElementos, name='suministroAsignaElementos'),
    url(r'^suministro/asigna/save/$', views.suministroAsignaSave, name='suministroAsignaSave'),
    url(r'^suministro/asignar/comboPrograma/$', views.suministroAsignarComboPrograma, name='suministroAsignarComboPrograma'),
    url(r'^suministro/asignar/comboFuncion/$', views.suministroAsignarComboFuncion, name='suministroAsignarComboFuncion'),
    url(r'^suministro/asignar/comboTaller/$', views.suministroAsignarComboTaller, name='suministroAsignarComboTaller'),
    url(r'^suministro/asignar/comboTransporte/$', views.suministroAsignarComboTransporte, name='suministroAsignarComboTransporte'),
    url(r'^suministro/asignar/comboFuncionElegido/$', views.suministroAsignarcomboFuncionElegido, name='suministroAsignarcomboFuncionElegido'),
    url(r'^suministro/asignar/cantidades/$', views.suministroAsignarCantidades, name='suministroAsignarCantidades'),
    url(r'^suministro/asignar/save/$', views.suministroAsignarSave, name='suministroAsignarSave'),
    #"""------------------------------------------"""
    #""" RUTAS RELACIONADAS CON HABILITADO """
    #"""------------------------------------------"""
    url(r'^habilitado/recepcion/$', views.habilitadoRecepcionView, name='habilitadoRecepcionView'),
    url(r'^habilitado/asignacion/$', views.habilitadoAsignacionView, name='habilitadoAsignacionView'),
    url(r'^habilitado/cambioTaller/$', views.habilitadoCambioTallerView, name='habilitadoCambioTallerView'),
    url(r'^habilitado/asigna/comboPrograma/$', views.habilitadoAsignaComboPrograma, name='habilitadoAsignaComboPrograma'),
    url(r'^habilitado/asigna/comboFuncion/$', views.habilitadoAsignaComboFuncion, name='habilitadoAsignaComboFuncion'),
    url(r'^habilitado/recepcion/habilitado/$', views.habilitadoRecepcionHabilitado, name='habilitadoRecepcionHabilitado'),
    url(r'^habilitado/recepcion/save/$', views.habilitadoRecepcionSave, name='habilitadoRecepcionSave'),
    url(r'^habilitado/asignar/comboPrograma/$', views.habilitadoAsignarComboPrograma, name='habilitadoAsignarComboPrograma'),
    url(r'^habilitado/asignar/comboFuncion/$', views.habilitadoAsignarComboFuncion, name='habilitadoAsignarComboFuncion'),
    url(r'^habilitado/asignar/comboElemento/$', views.habilitadoAsignarComboElemento, name='habilitadoAsignarComboElemento'),
    url(r'^habilitado/asignar/cantidades/$', views.habilitadoAsignarCantidades, name='habilitadoAsignarCantidades'),
    url(r'^habilitado/asignar/elemento/$', views.habilitadoAsignarElemento, name='habilitadoAsignarElemento'),
    url(r'^habilitado/asignar/save/$', views.habilitadoAsignarSave, name='habilitadoAsignarSave'),
    url(r'^habilitado/asignar/despiece/save/$', views.habilitadoAsignarDespieceSave, name='habilitadoAsignarDespieceSave'),
    url(r'^habilitado/recepcion/comboOrden/$', views.habilitadoRecepcionComboOrden, name='habilitadoRecepcionComboOrden'),
    url(r'^habilitado/asignar/armado/$', views.habilitadoAsignarArmado, name='habilitadoAsignarArmado'),
    #"""------------------------------------------"""
    #""" RUTAS RELACIONADAS CON HABILITADO """
    #"""------------------------------------------"""
    url(r'^armado/recepcion/$', views.armadoRecepcionView, name='armadoRecepcionView'),
    url(r'^armado/recepcion/comboFrente/$', views.armadoRecepcionComboFrente, name='armadoRecepcionComboFrente'),
    url(r'^armado/asignacion/$', views.armadoAsignacionView, name='armadoAsignacionView'),
    url(r'^armado/asignar/comboPrograma/$', views.armadoAsignarComboPrograma, name='armadoAsignarComboPrograma'),
    url(r'^armado/asignar/comboFuncion/$', views.armadoAsignarComboFuncion, name='armadoAsignarComboFuncion'),
    url(r'^armado/asignar/comboElemento/$', views.armadoAsignarComboElemento, name='armadoAsignarComboElemento'),
    url(r'^armado/asignar/elemento/$', views.armadoAsignarElemento, name='armadoAsignarElemento'),
    url(r'^armado/asigna/save/$', views.armadoAsignaSave, name='armadoAsignaSave'),
    url(r'^armado/asignacion/comboPrograma/$', views.armadoAsignacionComboPrograma, name='armadoAsignacionComboPrograma'),
    url(r'^armado/asignacion/comboFuncion/$', views.armadoAsignacionComboFuncion, name='armadoAsignacionComboFuncion'),
    url(r'^armado/asignacion/comboElemento/$', views.armadoAsignacionComboElemento, name='armadoAsignacionComboElemento'),
    url(r'^armado/asignacion/elemento/$', views.armadoAsignacionElemento, name='armadoAsignacionElemento'),
    url(r'^armado/asignacion/save/$', views.armadoAsignacionSave, name='armadoAsignacionSave'),
    url(r'^armado/recepcion/armado/$', views.armadoRecepcionArmado, name='armadoRecepcionArmado'),
    #"""------------------------------------------"""
    #""" RUTAS RELACIONADAS CON COLOCADO """
    #"""------------------------------------------"""
    url(r'^colocado/recepcion/$', views.colocadoRecepcionView, name='colocadoRecepcionView'),
    url(r'^colocado/recepcion/comboPrograma/$', views.colocadoRecepcionComboPrograma, name='colocadoRecepcionComboPrograma'),
    url(r'^colocado/recepcion/comboFuncion/$', views.colocadoRecepcionComboFuncion, name='colocadoRecepcionComboFuncion'),
    url(r'^colocado/recepcion/comboApoyo/$', views.colocadoRecepcionComboApoyo, name='colocadoRecepcionComboApoyo'),
    url(r'^colocado/recepcion/detalle/$', views.colocadoRecepcionDetalle, name='colocadoRecepcionDetalle'),
    url(r'^colocado/recepcion/save/$', views.colocadoRecepcionSave, name='colocadoRecepcionSave'),
    #"""------------------------------------------"""
    #""" RUTAS RELACIONADAS CON IMAGENES """
    #"""------------------------------------------"""
    url(r'^imagenes/base64/$', views.imagenesBase64, name='imagenesBase64'),
]