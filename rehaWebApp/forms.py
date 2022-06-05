from django import forms

class formularioContacto(forms.Form):

	asunto = forms.CharField() # Le indicamos que es un campo de caracteres
	email = forms.EmailField()
	mensaje = forms.CharField()