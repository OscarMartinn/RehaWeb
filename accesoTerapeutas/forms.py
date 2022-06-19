from django.db.models.fields import DateField, DateTimeField
from django.db.models.query import QuerySet
from django.forms import ModelForm, widgets, Select
from django import forms
from django.forms.models import inlineformset_factory


from .models import Diagnosticos, Edad, Extremidades, Objetivo_Terapeutico, Pacientes, Ejercicios, Pci, Posicion, Sesiones, SesionesEjercicios, Terapeutas

##################################################################################################
#------------------------------------------- Formularios ----------------------------------------#
##################################################################################################


class PacienteForm(ModelForm):
    DOY = ('1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971',
       '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979',
       '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987',
       '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995',
       '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003',
       '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011',
       '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
       '2020','2021')
    fecha_Nacimiento = forms.DateField(widget=forms.SelectDateWidget(years = DOY))
    terapeuta = forms.ModelMultipleChoiceField(queryset=Terapeutas.objects.filter(usuario__groups__name__in=['terapeuta']))
    class Meta:
        model= Pacientes
        fields=('nombre','apellidos','fecha_Nacimiento','telefono','email','diagnostico','macs','gmfcs','calificacion5','calificacion50','calificacion500','usuario','contraseña', 'terapeuta','visible',)
        help_texts = {
            'nombre': (''),
            'apellidos': (''),
            'fecha_Nacimiento': (''),
            'telefono': (''),
            'email': (''),
            'diagnostico': (''),
            'macs': (''),
            'gmfcs': (''),
            'calificacion5': (''),
            'calificacion50': (''),    
            'calificacion500': (''),
            'usuario': (''),
            'contraseña': (''),
            'terapeuta': (''),
            'visible': (''),
        }


        
class EditarPacienteForm(ModelForm):
    class Meta:
        model= Pacientes
        fields=('nombre','apellidos','telefono','email','diagnostico','macs','gmfcs','calificacion5','calificacion50','calificacion500','usuario','contraseña', 'terapeuta','visible',)
        help_texts = {
            'nombre': (''),
            'apellidos': (''),
            'telefono': (''),
            'email': (''),
            'diagnostico': (''),
            'macs': (''),
            'gmfcs': (''),
            'calificacion5': (''),
            'calificacion50': (''),    
            'calificacion500': (''),
            'usuario': (''),
            'contraseña': (''),
            'terapeuta': (''),
            'visible': (''),
        }

class EjercicioForm(ModelForm):
    diagnostico = forms.ModelMultipleChoiceField(queryset=Diagnosticos.objects.all())
    posicion = forms.ModelMultipleChoiceField(queryset=Posicion.objects.all())
    extremidades = forms.ModelMultipleChoiceField(queryset=Extremidades.objects.all())
    edad = forms.ModelMultipleChoiceField(queryset=Edad.objects.all())
    objetivo_Terapeutico = forms.ModelMultipleChoiceField(queryset=Objetivo_Terapeutico.objects.all())
    pci = forms.ModelMultipleChoiceField(queryset=Pci.objects.all())
    class Meta:
        model= Ejercicios
        fields=('codigo','nombre', 'descripcion','edad', 'extremidades','lateralidad','monitoreo_Sensores','posicion','objetivo_Terapeutico','diagnostico','pci','visible')
        help_texts = {
            'codigo':(''),
            'nombre': (''),
            'descripcion': (''),
            'edad':(''),
            'extremidades':(''),
            'lateralidad':(''),
            'monitoreo_Sensores':(''),
            'posicion':(''),
            'objetivo_Terapeutico':(''),
            'diagnostico':(''),
            'pci':(''),
            'visible':(''),
            }

class EditarEjercicioForm(ModelForm):

    class Meta:
        model= Ejercicios
        fields=('codigo','nombre','descripcion','edad', 'extremidades','lateralidad','monitoreo_Sensores','posicion','objetivo_Terapeutico','diagnostico','pci', 'video','visible')
        help_texts = {
            'codigo':(''),
            'nombre': (''),
            'descripcion': (''),
            'edad':(''),
            'extremidades':(''),
            'lateralidad':(''),
            'monitoreo_Sensores':(''),
            'posicion':(''),
            'objetivo_Terapeutico':(''),
            'diagnostico':(''),
            'pci':(''),
            'video':(''),
            'visible':(''),
            }   


class SubirVideoForm(ModelForm):

    class Meta:
        model= Ejercicios
        fields=( 'video',)
        help_texts = {
            'video':(''),
            }         

class SesionForm(ModelForm):
    fecha_Inicial = forms.DateField(widget=forms.SelectDateWidget())
    fecha_Final = forms.DateField(widget=forms.SelectDateWidget())
    #ejercicios = forms.ModelMultipleChoiceField(queryset=Ejercicios.objects.all(),widget=forms.CheckboxSelectMultiple())
    #ejercicios = forms.ModelMultipleChoiceField(queryset=Ejercicios.objects.all())
    #ejercicios = forms.ModelMultipleChoiceField(queryset=Ejercicios.objects.all())
    terapeuta = forms.ModelMultipleChoiceField(queryset=Terapeutas.objects.filter(usuario__groups__name__in=['terapeuta']))
    class Meta:
        model = Sesiones
        exclude = ('ejercicios',)
        fields=('paciente','periodicidad','fecha_Inicial', 'fecha_Final', 'terapeuta',  'visible')
        help_texts = {
            'paciente': (''),
            'periodicidad': ('Especifique las veces por semana que debe hacer los ejercicios.'),
            'fecha_Inicial': (''),
            'fecha_Final': (''),
            'terapeuta': (''),
            'visible': (''),
            }

class EditarSesionForm(ModelForm):

    
    class Meta:
        model= Sesiones
        fields=('paciente','periodicidad', 'fecha_Inicial', 'fecha_Final','ejercicios','terapeuta','visible')
        help_texts = {
            'paciente': (''),
            'ejercicios': (''),
            'periodicidad': (''),
            'fecha_Inicial': (''),
            'fecha_Final': (''),
            'terapeuta': (''),
            'visible': (''),
            }

class SesionEjerciciosForm(ModelForm):
    

    class Meta:
        model= SesionesEjercicios
        fields=('ejercicios','repeticiones')
        exclude = ('sesiones',)
        help_texts = {
            'ejercicios': (''),
            'repeticiones': (''),
            }

