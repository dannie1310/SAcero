from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'control_acero'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^home/$', views.HomeView.as_view(), name='home'),
    url(r'^principal/$', views.principalView, name='principalView'),
    url(r'^usuario/login/$', views.loginUsuario, name='loginUsuario'),
    url(r'^usuario/logout/$', views.logout_view, name='logout'),

    url(r'^recepcion/material/$', views.recepcionMaterialView, name='recepcionMaterialView'),
    url(r'^salida/habilitado/$', views.salidaHabilitadoView, name='salidaHabilitadoView'),
    url(r'^salida/habilitado/material/$', views.salidaHabilitadoMaterial, name='salidaHabilitadoMaterial'),
    url(r'^salida/habilitado/save/$', views.salidaHabilitadoSave, name='salidaHabilitadoSave'),

    url(r'^entrada/armado/$', views.entradaArmadoView, name='entradaArmadoView'),
    url(r'^entrada/armado/combo/apoyo/$', views.entradaArmadoComboApoyo, name='entradaArmadoComboApoyo'),
    url(r'^entrada/armado/combo/elemento/$', views.entradaArmadoComboElemento, name='entradaArmadoComboElemento'),
    url(r'^entrada/armado/material/$', views.entradaArmadoMaterial, name='entradaArmadoMaterial'),
    url(r'^entrada/armado/save/$', views.entradaArmadoSave, name='entradaArmadoSave'),


    url(r'^elemento/elementomaterial/$', views.elementoMaterial, name='elementoMaterial'),

    url(r'^reportes/reporte/$', views.reporteView, name='reporteView'),
    url(r'^reportes/reporteConsulta/$', views.reporteConsulta, name='reporteConsulta'),

    

    url(r'^programa/save/$', views.programaSave, name='programaSave'),

    #"""------------------------------------------"""
    #"""   RUTAS RELACIONADAS CON COMBOS          """
    #"""------------------------------------------"""
    url(r'^combo/funcion/$', views.comboFuncion, name='comboFuncion'),
    url(r'^combo/frente/$', views.comboFrente, name='comboFrente'),
    url(r'^combo/apoyo/$', views.comboApoyo, name='comboApoyo'),
    url(r'^combo/elemento/$', views.comboElemento, name='comboElemento'),
    url(r'^combo/funciongeneral/$', views.comboFuncionGeneral, name='comboFuncionGeneral'),
    url(r'^combo/taller/$', views.comboTaller, name='comboTaller'),


    #"""------------------------------------------"""
    #"""   RUTAS RELACIONADAS CATALOGO DE APOYOS  """
    #"""------------------------------------------"""
    url(r'^catalogos/usuarios/new/$', views.usuariosNewView, name='usuariosNewView'),
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
]