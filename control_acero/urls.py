from django.conf.urls import url

from . import views

app_name = 'control_acero'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^home/$', views.HomeView.as_view(), name='home'),
    url(r'^principal/$', views.principalView, name='principalView'),
    url(r'^frenteTrabajo/$', views.frenteTrabajoView, name='frenteTrabajoView'),
    url(r'^frente/guardaFrente/$', views.frenteGuardaFrenteView, name='frenteGuardaFrenteView'),
    url(r'^controlAsignacion/$', views.controlAsignacionView, name='controlAsignacionView'),
    url(r'^controlAsignacion/nuevo/$', views.controlAsignacionNuevoView, name='controlAsignacionNuevoView'),
    url(r'^usuario/login/$', views.loginUsuario, name='loginUsuario'),
    url(r'^acceso/$', views.AccesoView.as_view(), name='acceso'),
    #url(r'^suministro/$', views.SuministroView.as_view(), name='suministro'),
    url(r'^frente/$', views.FrenteView.as_view(), name='frente'),
    url(r'^control/$', views.ControlView.as_view(), name='control'),
    #url(r'^habilitado/$', views.HabilitadoView.as_view(), name='habilitado'),
    #url(r'^armado/$', views.ArmadoView.as_view(), name='armado'),
    #url(r'^colocado/$', views.ColocadoView.as_view(), name='colocado'),
    #"""------------------------------------------"""
    #""" RUTAS RELACIONADAS CON ARMADO """
    #"""------------------------------------------"""
    url(r'^armado/$', views.armadoView, name='armadoView'),
    #"""------------------------------------------"""
    #""" RUTAS RELACIONADAS CON COLOCADO """
    #"""------------------------------------------"""
    url(r'^colocado/$', views.colocadoView, name='colocadoView'),
    #"""------------------------------------------"""
    #""" RUTAS RELACIONADAS CON FRENTE DE TRABAJO """
    #"""------------------------------------------"""
    url(r'^frenteTrabajo/$', views.frenteTrabajoView, name='frenteTrabajoView'),
    url(r'^frenteTrabajo/nuevo/$', views.frenteTrabajoNuevoView, name='frenteTrabajoNuevoView'),
    url(r'^frenteTrabajo/show/$', views.frenteTrabajoShow, name='frenteTrabajoShow'),
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
    url(r'^catologos/apoyos/$', views.apoyosView, name='apoyosView'),
    url(r'^catologos/apoyos/new/$', views.apoyosNewView, name='apoyosNewView'),
    url(r'^catologos/apoyos/(?P<pk>[0-9]+)/edit/$', views.apoyosEditView, name='apoyosEditView'),
    url(r'^catologos/apoyos/delete/(?P<pk>[0-9]+)/$', views.apoyosLogicalDelete, name='apoyosLogicalDelete'),
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
]