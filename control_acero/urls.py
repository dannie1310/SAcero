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
    url(r'^control/nuevo/$', views.controlNuevo, name='controlNuevo'),
    #url(r'^habilitado/$', views.HabilitadoView.as_view(), name='habilitado'),
    #url(r'^armado/$', views.ArmadoView.as_view(), name='armado'),
    #url(r'^colocado/$', views.ColocadoView.as_view(), name='colocado'),
    #"""------------------------------------------"""
    #""" RUTAS RELACIONADAS CON SUMINISTRO """
    #"""------------------------------------------"""
    url(r'^suministro/$', views.suministroView, name='suministroView'),
    #"""------------------------------------------"""
    #""" RUTAS RELACIONADAS CON HABILITADO """
    #"""------------------------------------------"""
    url(r'^habilitado/$', views.habilitadoView, name='habilitadoView'),
    url(r'^habilitado/cambioTaller/$', views.habilitadoCambioTallerView, name='habilitadoCambioTallerView'),
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
    url(r'^recepcion/registros/$', views.recepcionRegistros, name='recepcionRegistros'),
    url(r'^estructura/combo/$', views.estructuraCombo, name='estructuraCombo'),
    url(r'^elemento/combo/$', views.elementoCombo, name='elementoCombo'),
    url(r'^elemento/comboapoyoelmento/$', views.elementoComboApoyoElemento, name='elementoComboApoyoElemento'),
    url(r'^elemento/elementomaterial/$', views.elementoMaterial, name='elementoMaterial'),

    url(r'^programa/save/$', views.programaSave, name='programaSave'),
    url(r'^programa/combofiltrado/$', views.programaCombofiltrado, name='programaCombofiltrado'),

    url(r'^asignacion/save/$', views.asignacionSave, name='asignacionSave'),
]
