from django import forms
from .models import Apoyo

class ApoyoForm(forms.ModelForm):
	class Meta:
		model = Apoyo
		fields = ['numero', 'estatus']