from django import forms
from .models import Apoyo, Elemento

class ApoyoForm(forms.ModelForm):
	class Meta:
		model = Apoyo
		fields = ['numero', 'estatus']
		exclude = ['estatus']