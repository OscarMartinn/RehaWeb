from django.db.models.fields import DateField, DateTimeField
from django.db.models.query import QuerySet
from django.forms import ModelForm, widgets, Select
from django import forms
from django.forms.models import inlineformset_factory

from englishAccess.models import Ages, Diagnostics, Exercices, Extremities, Patients, PciEnglish, Position, Sessions, SessionsExercices, Therapeutic_Objective, Therapists

class EnglishPacienteForm(ModelForm):
    DOY = ('1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971',
       '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979',
       '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987',
       '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995',
       '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003',
       '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011',
       '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
       '2020','2021')
    birth_Date = forms.DateField(widget=forms.SelectDateWidget(years = DOY))
    terapeuta = forms.ModelMultipleChoiceField(queryset=Therapists.objects.filter(user__groups__name__in=['terapeuta']))
    class Meta:
        model = Patients
        fields=('nombre','apellidos','birth_Date','telefono','email','diagnostico','macs','gmfcs','calificacion5','calificacion50','calificacion500','usuario','contraseña', 'terapeuta','visible',)
        help_texts = {
            'nombre': (''),
            'apellidos': (''),
            'birth_Date': (''),
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



class EnglishEditarPacienteForm(ModelForm):
    class Meta:
        model = Patients
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




class EnglishEjercicioForm(ModelForm):
    #diagnostic = forms.ModelMultipleChoiceField(queryset=Diagnostics.objects.all())
    #position = forms.ModelMultipleChoiceField(queryset=Position.objects.all())
    #extremities = forms.ModelMultipleChoiceField(queryset=Extremities.objects.all())
    #ages = forms.ModelMultipleChoiceField(queryset=Ages.objects.all())
    #therapeuticobjective = forms.ModelMultipleChoiceField(queryset=TherapeuticObjective.objects.all())
    #pci = forms.ModelMultipleChoiceField(queryset=PciEnglish.objects.all())
    class Meta:
        model= Exercices
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




class EnglishEditarEjercicioForm(ModelForm):

    class Meta:
        model = Exercices
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



class EnglishSubirVideoForm(ModelForm):

    class Meta:
        model = Exercices
        fields=( 'video',)
        help_texts = {
            'video':(''),
            }   



class EnglishSesionForm(ModelForm):
    initial_Date = forms.DateField(widget=forms.SelectDateWidget())
    final_Date = forms.DateField(widget=forms.SelectDateWidget())
    terapeuta = forms.ModelMultipleChoiceField(queryset=Therapists.objects.filter(user__groups__name__in=['terapeuta']))
    class Meta:
        model = Sessions
        exclude = ('ejercicios',)
        fields=('paciente','periodicidad','initial_Date', 'final_Date', 'terapeuta',  'visible')
        help_texts = {
            'paciente': (''),
            'periodicidad': (''),
            'initial_Date': (''),
            'final_Date': (''),
            'terapeuta': (''),
            'visible': (''),
            }


class EnglishSesionEjerciciosForm(ModelForm):
    
    class Meta:
        model = SessionsExercices
        fields=('ejercicios','repeticiones')
        exclude = ('sesiones',)
        help_texts = {
            'ejercicios': (''),
            'repeticiones': (''),
            }
