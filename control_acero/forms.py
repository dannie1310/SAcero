from django import forms
from .models import Apoyo, Elemento, Despiece,Material,Funcion, Frente, Taller, Transporte

class ApoyoForm(forms.ModelForm):
	class Meta:
		model = Apoyo
		fields = ['numero', 'estatus', 'elemento']
		exclude = ['estatus']

class ElementoForm(forms.ModelForm):
	class Meta:
		model = Elemento
		fields = ['nombre', 'tipo','estatus', 'peso']
		exclude = ['estatus']

class DespieceForm(forms.ModelForm):
	class Meta:
		model = Despiece
		fields = ['nomenclatura', 'estatus', 'longitud','cantidad','figura','peso']
		exclude = ['estatus']

class MaterialForm(forms.ModelForm):
	class Meta:
		model = Material
		fields = ['nombre', 'estatus', 'diametro','peso','longitud','proveedor','tipo','numero']
		exclude = ['estatus']

class FrenteForm(forms.ModelForm):
	class Meta:
		model = Frente
		fields = ['nombre', 'estatus', 'identificacion','ubicacion','kilometros']
		exclude = ['estatus']

class FuncionForm(forms.ModelForm):
	class Meta:
		model = Funcion
		fields = ['tipo', 'proveedor', 'tonelajeMaximo','estatus']
		exclude = ['estatus']

class TallerForm(forms.ModelForm):
	class Meta:
		model = Taller
		fields = ['nombre', 'estatus', 'proveedor','ubicacion','responsable']
		exclude = ['estatus']

class TransporteForm(forms.ModelForm):
	class Meta:
		model = Transporte
		fields = ['tipo', 'estatus', 'placas','capacidad']
		exclude = ['estatus']
