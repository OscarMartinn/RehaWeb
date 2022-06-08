from gettext import gettext
from multiprocessing import context
from operator import index
import os
from posixpath import split
from webbrowser import get
from django.urls import resolve
import re
from django.db.models.fields.related import ManyToManyField
from django.shortcuts import render
from rehaWeb.settings import MEDIA_ROOT
from .models import Calificaciones, Diagnosticos, Extremidades, Gmfcs, Lateralidad, Macs, Edad, ObjetivoTerapeutico, Pci, Posicion, Sesiones, Ejercicios, Pacientes, SesionesEjercicios, Terapeutas, ValoracionPacientes, EjerciciosRealizados, RegistroSesiones, FormularioPacientes
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import   EditarSesionForm, PacienteForm, EjercicioForm, EditarPacienteForm, EditarEjercicioForm, SesionEjerciciosForm, SesionForm, SubirVideoForm
from django.utils import timezone
from django.shortcuts import redirect
from datetime import date, datetime
from django.core.files import File
from django.utils import translation
from englishAccess.models import Ages, AssessmentPatiens, Exercices, ExercisesDone, Extremities, Laterality, Patients, Diagnostics, GmfcsEnglish, MacsEnglish, PciEnglish, Position, RegistrationSession, Sessions, PatientForm, SessionsExercices, Classifications, TherapeuticObjective, Therapists
from englishAccess.forms import EnglishPacienteForm, EnglishEditarPacienteForm, EnglishEjercicioForm, EnglishEditarEjercicioForm, EnglishSesionEjerciciosForm, EnglishSesionForm, EnglishSubirVideoForm
from django_xhtml2pdf.utils import generate_pdf as gen_pdf, render_to_pdf_response
from rehaWeb import settings
from rehaWeb.settings import workingOnServer
from django.contrib.auth.models import Group


# Create your views here.

#Esta vista mostrara un menu con opciones comunes a todos los terapeutas pero cada un o tendrá un contenido diferente
@login_required
def acceso(request):

    current_url = resolve(request.path_info)
    print("AccesoTerapeutas:", current_url.route)
    terapeuta = Terapeutas.objects.get(usuario = request.user)
    translation.activate(terapeuta.idioma.code)
    return render(request, "accesoTerapeutas/indexTerapeutas.html") 

@login_required
def setLanguage(request, idLanguage=None, idSeccion=None):

    if idSeccion == 1:
        direccion = "Acceso"
    if idSeccion == 2:
        direccion = "Pacientes"
    if idSeccion == 3:
        direccion = "Ejercicios"
    if idSeccion == 4:
        direccion = "Sesiones"


    if idLanguage == 1:
	    user_language = 'es'
    else: 
	    user_language = 'en'

    translation.activate(user_language)
    #request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    #if translation.LANGUAGE_SESSION_KEY in request.session:
	#    del request.session[translation.LANGUAGE_SESSION_KEY]

    return redirect(direccion) 


@login_required
def pacientes(request):

    terapeuta = Terapeutas.objects.get(usuario = request.user)
    
    grupoPermisos = Group.objects.get(user = request.user)
    print(grupoPermisos)
    if str(grupoPermisos) == 'clinica':
        pacientes = Pacientes.objects.all()
    else:
        if terapeuta.idioma.code == 'en':
            pacientes = Patients.objects.filter(terapeuta = terapeuta)
        else:
            pacientes = Pacientes.objects.filter(terapeuta = terapeuta)

    if terapeuta.idioma.code == 'en':
        diagnosticos = Diagnostics.objects.all()
        macs = MacsEnglish.objects.all()
        gmfcs = GmfcsEnglish.objects.all()

    else:
        diagnosticos = Diagnosticos.objects.all()
        macs = Macs.objects.all()
        gmfcs = Gmfcs.objects.all()

    current_url = resolve(request.path_info)
    if(current_url.route == 'en/accesoTerapeutas/pacientes'): 
        idioma = "en"
    elif(current_url.route == 'es/accesoTerapeutas/pacientes' or current_url.route == 'accesoTerapeutas/pacientes'):  
        idioma = "es"
    
    #Creo un diccionario con los filtros
    seleccionados1 = {}
    seleccionados2 = {}
    seleccionados3 = {}
    queries = None
    
    #Para las calificaciones me tengo que coger los pacientes.calificacion5 == a X
    ################################ FILTRADO EN PACIENTES ##############################
    if request.POST:
        
        #        Para hacer comprobaciones       #
        for key, value in request.POST.items():
           if key != 'csrfmiddlewaretoken':
                valores = key + ":" + value
                print(valores)
        ##########################################

        for d in diagnosticos:
            seleccionados1[d.nombre] = 'false'
        for m in macs:
            seleccionados2[m.autoAlias()] = 'false'
        for g in gmfcs:
            seleccionados3[g.autoAlias()] = 'false'

        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                for e in diagnosticos:
                    if e.nombre == key and queries is None:
                        queries = Q(diagnostico__nombre__icontains = key)
                        seleccionados1[e.nombre] = 'true'
                    elif e.nombre == key and queries is not None:
                        queries |= Q(diagnostico__nombre__icontains = key)
                        seleccionados1[e.nombre] = 'true'

        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                for e in macs:
                    if e.autoAlias() == value and queries is None:
                        queries = Q(macs__nombre__icontains = key)
                        seleccionados2[e.autoAlias()] = 'true'
                    elif e.autoAlias() == value and queries is not None:
                        queries |= Q(macs__nombre__icontains = key)
                        seleccionados2[e.autoAlias()] = 'true'

        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                for e in gmfcs:
                    if e.autoAlias() == value and queries is None:
                        queries = Q(gmfcs__nombre__icontains = key)
                        seleccionados3[e.autoAlias()] = 'true'
                    elif e.autoAlias() == value and queries is not None:
                        queries |= Q(gmfcs__nombre__icontains = key)
                        seleccionados3[e.autoAlias()] = 'true'
        
        
        #En el caso en el que se envie el POST sin aplicar ningun filtro 
        if queries == None:
            return render(request, "accesoTerapeutas/pacientes.html", {"pacientes": pacientes, "diagnosticos": diagnosticos, 
                "macs":macs, "gmfcs":gmfcs, "seleccionados1":seleccionados1,"seleccionados2":seleccionados2,"seleccionados3":seleccionados3,"idioma":idioma})
    
        if terapeuta.idioma.code == 'en':
            pacientes = Patients.objects.filter(queries)
        else:
            pacientes = Pacientes.objects.filter(queries)

        return render(request, "accesoTerapeutas/pacientes.html", {"pacientes": pacientes, "diagnosticos": diagnosticos, 
            "macs":macs, "gmfcs":gmfcs, "seleccionados1":seleccionados1, "seleccionados2":seleccionados2, "seleccionados3":seleccionados3,"idioma":idioma})

 # Lo que estamos haciendo es crear un diccionario con el nombre "sesiones" 
 # que nos recoge los objetos de la lista de sesiones que previamete hemos recogido
    return render(request, "accesoTerapeutas/pacientes.html", {"pacientes": pacientes, "diagnosticos": diagnosticos, 
            "macs":macs, "gmfcs":gmfcs, "seleccionados1":seleccionados1, "seleccionados2":seleccionados2, "seleccionados3":seleccionados3,"idioma":idioma})


@login_required
#Info Pacientes
def infoPaciente(request, idPaciente):

    #print(idPaciente)
    #queries = (Q(id__iexact = idPaciente))
    #pacientes = Pacientes.objects.filter(queries)
    

    #queries1 = (Q(paciente__id__iexact = idPaciente) & Q(visible = True))
    #sesiones = Sesiones.objects.filter(queries1).order_by('-actualizado')[:5]
    
    #formulario = FormularioPacientes.objects.all()

    #sesionesEjercicios = SesionesEjercicios.objects.all()

    terapeuta = Terapeutas.objects.get(usuario = request.user)
    translation.activate(terapeuta.idioma.code)

    if terapeuta.idioma.code == 'en':
        paciente = Patients.objects.filter(id = idPaciente)
        sesion = Sessions.objects.filter(paciente__id = idPaciente)
        ejerciciosSesion = SessionsExercices.objects.filter(sesiones__paciente__id = idPaciente)
        formulario = PatientForm.objects.filter(paciente__id = idPaciente)
    
    else:   
        paciente = Pacientes.objects.filter(id = idPaciente)
        sesion = Sesiones.objects.filter(paciente__id = idPaciente)
        ejerciciosSesion = SesionesEjercicios.objects.filter(sesiones__paciente__id = idPaciente)
        formulario = FormularioPacientes.objects.filter(paciente__id = idPaciente)

    current_url = resolve(request.path_info)
    if(current_url.route == 'en/accesoTerapeutas/infoPaciente/<int:idPaciente>'):  #just taking a look
        idioma = "en"
    elif(current_url.route == 'es/accesoTerapeutas/infoPaciente/<int:idPaciente>' or current_url.route == 'accesoTerapeutas/infoPaciente/<int:idPaciente>'):  #can edit
        idioma = "es"
    #print(paciente)
    #print(formulario)
    #print(sesion)
    #print(ejerciciosSesion)
    
    return render(request, "accesoTerapeutas/pacientesInfo.html", {"paciente": paciente, "sesion":sesion, "sesionesEjercicios":ejerciciosSesion, "formulario":formulario,"idioma":idioma})
    #return render(request, "accesoTerapeutas/pacientesInfo.html", {"paciente": paciente})
    
@login_required
#Busqueda en pacientes
def busquedaPacientes(request):

    paciente = request.GET.get('pacientes','')
    
    queries = (Q(nombre__icontains = paciente) | Q(diagnostico__nombre__icontains = paciente) | Q(apellidos__icontains = paciente))

    current_url = resolve(request.path_info)
    if(current_url.route == 'en/accesoTerapeutas/busquedaPacientes'):  #just taking a look
        idioma = "en"
    elif(current_url.route == 'es/accesoTerapeutas/busquedaPacientes' or current_url.route == 'accesoTerapeutas/busquedaPacientes'):  #can edit
        idioma = "es"

    terapeuta = Terapeutas.objects.get(usuario = request.user)

    if terapeuta.idioma.code == 'en':
        #En el caso en el que se envie el POST sin escribir nada en el cajon de buscar
        if queries == None:
            pacientes = Patients.objects.all()
            return render(request, "accesoTerapeutas/pacientes.html", {"pacientes": pacientes,"idioma":idioma})

        terapeuta = Terapeutas.objects.get(usuario = request.user)
        pacientes = Patients.objects.filter(queries, terapeuta = terapeuta)
        return render(request, "accesoTerapeutas/busquedaPacientes.html", {"pacientes": pacientes,"idioma":idioma})
    else:
        #En el caso en el que se envie el POST sin escribir nada en el cajon de buscar
        if queries == None:
            pacientes = Pacientes.objects.all()
            return render(request, "accesoTerapeutas/pacientes.html", {"pacientes": pacientes,"idioma":idioma})

        terapeuta = Terapeutas.objects.get(usuario = request.user)
        pacientes = Pacientes.objects.filter(queries, terapeuta = terapeuta)
        return render(request, "accesoTerapeutas/busquedaPacientes.html", {"pacientes": pacientes,"idioma":idioma})

@login_required
#Añadir en pacientes
def nuevoPaciente(request):

    terapeuta = Terapeutas.objects.get(usuario = request.user)

    if terapeuta.idioma.code == 'en':
        if request.method == 'POST': # si el usuario está enviando el formulario con datos
            form = EnglishPacienteForm(request.POST) # Bound form
            if form.is_valid():
                pacientes = form.save()
                #pacientes.terapeuta = request.user
                pacientes.creado = timezone.now()
                pacientes.actualizado = timezone.now()
                pacientes.save()
                pacientes = Patients.objects.all()
                #return render(request, "accesoTerapeutas/pacientes.html", {"pacientes": pacientes})
                return redirect('Pacientes')

        else:
            form = EnglishPacienteForm() # Unbound form
            return render(request, 'accesoTerapeutas/nuevoPaciente.html', {'form': form})
    
    else:
        if request.method == 'POST': # si el usuario está enviando el formulario con datos
            form = PacienteForm(request.POST) # Bound form
            if form.is_valid():
                pacientes = form.save()
                #pacientes.terapeuta = request.user
                pacientes.creado = timezone.now()
                pacientes.actualizado = timezone.now()
                pacientes.save()
                pacientes = Pacientes.objects.all()
                #return render(request, "accesoTerapeutas/pacientes.html", {"pacientes": pacientes})
                return redirect('Pacientes')

        else:
            form = PacienteForm() # Unbound form
            return render(request, 'accesoTerapeutas/nuevoPaciente.html', {'form': form})

@login_required
#Editar en pacientes
def editarPaciente(request, idPaciente):

    terapeuta = Terapeutas.objects.get(usuario = request.user)

    if terapeuta.idioma.code == 'en':
        p = Patients.objects.get(pk=idPaciente) #aqui tienen tu objeto de tipo Empleado
        if request.method == "POST":
            form = EnglishEditarPacienteForm(request.POST,instance=p)
            if form.is_valid():
                
                p.nombre = request.POST['nombre']
                p.apellidos = request.POST['apellidos']
                p.telefono = request.POST['telefono']
                p.email = request.POST['email']
    
                diagnostico = request.POST['diagnostico']
                d = Diagnostics.objects.get(id=diagnostico)
                p.diagnostico = d
    
                macs = request.POST['macs']
                d = MacsEnglish.objects.get(id=macs)
                p.macs = d
    
                gmfcs = request.POST['gmfcs']
                d = GmfcsEnglish.objects.get(id=gmfcs)
                p.gmfcs = d
                
                calificacion5 = request.POST['calificacion5']
                d = Classifications.objects.get(id=calificacion5)
                p.calificacion5 = d
    
                calificacion50 = request.POST['calificacion50']
                d = Classifications.objects.get(id=calificacion50)
                p.calificacion50 = d
    
                calificacion500 = request.POST['calificacion500']
                d = Classifications.objects.get(id=calificacion500)
                p.calificacion500 = d
                
                p.usuario = request.POST['usuario']
                p.contraseña = request.POST['contraseña']
                
                terapeuta = request.POST['terapeuta']
                d = Terapeutas.objects.get(id=terapeuta)
                p.terapeuta = d
                
                p.visible = request.POST['visible']
                if p.visible == "on":
                    p.visible = True
                else:
                    p.visible = False
    
                p.actualizado = timezone.now()
                form.save() #aqui estas guardando diractamente el formulario en la base de datos
                return redirect('Pacientes')
            else:
                form = EnglishEditarPacienteForm(instance=p) 
                return render(request,"accesoTerapeutas/editarPaciente.html",{'form' : form})
        else:
            form = EnglishEditarPacienteForm(instance=p) 
    
        return render(request, "accesoTerapeutas/editarPaciente.html",{'form' : form})

    else:
        p = Pacientes.objects.get(pk=idPaciente) #aqui tienen tu objeto de tipo Empleado
        if request.method == "POST":
            form = EditarPacienteForm(request.POST,instance=p)
            if form.is_valid():

                p.nombre = request.POST['nombre']
                p.apellidos = request.POST['apellidos']
                p.telefono = request.POST['telefono']
                p.email = request.POST['email']

                diagnostico = request.POST['diagnostico']
                d = Diagnosticos.objects.get(id=diagnostico)
                p.diagnostico = d

                macs = request.POST['macs']
                d = Macs.objects.get(id=macs)
                p.macs = d

                gmfcs = request.POST['gmfcs']
                d = Gmfcs.objects.get(id=gmfcs)
                p.gmfcs = d

                calificacion5 = request.POST['calificacion5']
                d = Calificaciones.objects.get(id=calificacion5)
                p.calificacion5 = d

                calificacion50 = request.POST['calificacion50']
                d = Calificaciones.objects.get(id=calificacion50)
                p.calificacion50 = d

                calificacion500 = request.POST['calificacion500']
                d = Calificaciones.objects.get(id=calificacion500)
                p.calificacion500 = d

                p.usuario = request.POST['usuario']
                p.contraseña = request.POST['contraseña']

                terapeuta = request.POST['terapeuta']
                d = Terapeutas.objects.get(id=terapeuta)
                p.terapeuta = d

                p.visible = request.POST['visible']
                if p.visible == "on":
                    p.visible = True
                else:
                    p.visible = False

                p.actualizado = timezone.now()
                form.save() #aqui estas guardando diractamente el formulario en la base de datos
                return redirect('Pacientes')
            else:
                form = EditarPacienteForm(instance=p) 
                return render(request,"accesoTerapeutas/editarPaciente.html",{'form' : form})
        else:
            form = EditarPacienteForm(instance=p) 

        return render(request, "accesoTerapeutas/editarPaciente.html",{'form' : form})

@login_required
#Ocultar en pacientes
def ocultarPaciente(request, idPaciente):
    
    terapeuta = Terapeutas.objects.get(usuario = request.user)

    if terapeuta.idioma.code == 'en':
        p = Patients.objects.get(pk=idPaciente) #aqui tienen tu objeto de tipo Empleado
        p.visible = False
        p.save()
        return  redirect('Pacientes')
    else:
        p = Pacientes.objects.get(pk=idPaciente) #aqui tienen tu objeto de tipo Empleado
        p.visible = False
        p.save()
        return  redirect('Pacientes')

#Esta vista mostrara un listado de los pacientes que tiene el TERAPEUTA en NO VISIBLE
@login_required
def pacientesNoVisibles(request):

    terapeuta = Terapeutas.objects.get(usuario = request.user)

    if terapeuta.idioma.code == 'en':
        pacientes = Patients.objects.filter(visible=False, terapeuta = terapeuta).order_by('-actualizado')
        diagnosticos = Diagnostics.objects.all()
        macs = MacsEnglish.objects.all()
        gmfcs = GmfcsEnglish.objects.all()
    else:
        pacientes = Pacientes.objects.filter(visible=False, terapeuta = terapeuta).order_by('-actualizado')
        diagnosticos = Diagnosticos.objects.all()
        macs = Macs.objects.all()
        gmfcs = Gmfcs.objects.all()

    current_url = resolve(request.path_info)
    if(current_url.route == 'en/accesoTerapeutas/pacientesNoVisibles'):  #just taking a look
        idioma = "en"
    elif(current_url.route == 'es/accesoTerapeutas/pacientesNoVisibles' or current_url.route == 'accesoTerapeutas/pacientesNoVisibles'):  #can edit
        idioma = "es"
    
    #Creo un diccionario con los filtros
    seleccionados1 = {}
    seleccionados2 = {}
    seleccionados3 = {}
    queries = None
    
    #Para las calificaciones me tengo que coger los pacientes.calificacion5 == a X
    ################################ FILTRADO EN PACIENTES ##############################
    if request.POST:
        
        #        Para hacer comprobaciones       #
        for key, value in request.POST.items():
           if key != 'csrfmiddlewaretoken':
                valores = key + ":" + value
                print(valores)
        ##########################################

        for d in diagnosticos:
            seleccionados1[d.nombre] = 'false'
        for m in macs:
            seleccionados2[m.autoAlias()] = 'false'
        for g in gmfcs:
            seleccionados3[g.autoAlias()] = 'false'

        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                for e in diagnosticos:
                    if e.nombre == key and queries is None:
                        queries = Q(diagnostico__nombre__icontains = key)
                        seleccionados1[e.nombre] = 'true'
                    elif e.nombre == key and queries is not None:
                        queries |= Q(diagnostico__nombre__icontains = key)
                        seleccionados1[e.nombre] = 'true'

        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                for e in macs:
                    if e.autoAlias() == value and queries is None:
                        queries = Q(macs__nombre__icontains = key)
                        seleccionados2[e.autoAlias()] = 'true'
                    elif e.autoAlias() == value and queries is not None:
                        queries |= Q(macs__nombre__icontains = key)
                        seleccionados2[e.autoAlias()] = 'true'

        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                for e in gmfcs:
                    if e.autoAlias() == value and queries is None:
                        queries = Q(gmfcs__nombre__icontains = key)
                        seleccionados3[e.autoAlias()] = 'true'
                    elif e.autoAlias() == value and queries is not None:
                        queries |= Q(gmfcs__nombre__icontains = key)
                        seleccionados3[e.autoAlias()] = 'true'

        

        #En el caso en el que se envie el POST sin aplicar ningun filtro 
        if queries == None:
            return render(request, "accesoTerapeutas/pacientesNoVisibles.html", {"pacientes": pacientes, "diagnosticos": diagnosticos, 
                "macs":macs, "gmfcs":gmfcs, "seleccionados1":seleccionados1,"seleccionados2":seleccionados2,"seleccionados3":seleccionados3,"idioma":idioma})

        if terapeuta.idioma.code == 'en':
            pacientes = Patients.objects.filter(queries)
        else:
            pacientes = Pacientes.objects.filter(queries)

        return render(request, "accesoTerapeutas/pacientesNoVisibles.html", {"pacientes": pacientes, "diagnosticos": diagnosticos, 
            "macs":macs, "gmfcs":gmfcs, "seleccionados1":seleccionados1, "seleccionados2":seleccionados2, "seleccionados3":seleccionados3,"idioma":idioma})

 # Lo que estamos haciendo es crear un diccionario con el nombre "sesiones" 
 # que nos recoge los objetos de la lista de sesiones que previamete hemos recogido
    return render(request, "accesoTerapeutas/pacientesNoVisibles.html", {"pacientes": pacientes, "diagnosticos": diagnosticos, 
            "macs":macs, "gmfcs":gmfcs, "seleccionados1":seleccionados1, "seleccionados2":seleccionados2, "seleccionados3":seleccionados3,"idioma":idioma})







































########################################################################################## 
#-------------------------------------- EJERCICIOS --------------------------------------#
########################################################################################## 
#Esta vista mostrara un listado de los ejercicios disponibles
@login_required
def ejercicios(request):

    terapeuta = Terapeutas.objects.get(usuario = request.user)

    if terapeuta.idioma.code == 'en':
        ejercicios = Exercices.objects.all()
        edades = Ages.objects.all()
        extremidades = Extremities.objects.all()
        lateralidad = Laterality.objects.all()
        posiciones = Position.objects.all()
        objetivos = TherapeuticObjective.objects.all()
        diagnosticos = Diagnostics.objects.all()
        pci = PciEnglish.objects.all()
    
    else: 
        ejercicios = Ejercicios.objects.all()
        edades = Edad.objects.all()
        extremidades = Extremidades.objects.all()
        lateralidad = Lateralidad.objects.all()
        posiciones = Posicion.objects.all()
        objetivos = ObjetivoTerapeutico.objects.all()
        diagnosticos = Diagnosticos.objects.all()
        pci = Pci.objects.all()

    current_url = resolve(request.path_info)
    if(current_url.route == 'en/accesoTerapeutas/ejercicios'):  #just taking a look
        idioma = "en"
    elif(current_url.route == 'es/accesoTerapeutas/ejercicios' or current_url.route == 'accesoTerapeutas/ejercicios'):  #can edit
        idioma = "es"


    #Filtrado en ejercicios 
    #Creo un diccionario con los filtros
    seleccionados1 = {}
    seleccionados2 = {}
    seleccionados3 = {}
    seleccionados4 = {}
    seleccionados5 = {}
    seleccionados6 = {}
    seleccionados7 = {}
    queries = None

    ################################ FILTRADO EN EJERCICIOS ##############################
    if request.POST:

        #        Para hacer comprobaciones       #
        for key, value in request.POST.items():
           if key != 'csrfmiddlewaretoken':
                valores = key + ":" + value
                #print(valores)
        ##########################################

        for e in edades:
            seleccionados1[e.autoAlias()] = 'false'
        for e in extremidades:
            seleccionados2[e.nombre] = 'false'
        for l in lateralidad:
            seleccionados3[l.nombre] = 'false'
        for p in posiciones:
            seleccionados4[p.nombre] = 'false'
        for o in objetivos:
            seleccionados5[o.autoAlias()] = 'false'
        for d in diagnosticos:
            seleccionados6[d.nombre] = 'false'
        for p in pci:
            seleccionados7[p.nombre] = 'false'

        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                for e in edades:
                    if e.autoAlias() == value and queries is None:
                        queries = Q(edad__nombre__icontains = key)
                        seleccionados1[e.autoAlias()] = 'true'
                    elif e.autoAlias() == value and queries is not None:
                        queries |= Q(edad__nombre__icontains = key)
                        seleccionados1[e.autoAlias()] = 'true'

        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                for e in extremidades:
                    if e.nombre == key and queries is None:
                        queries = Q(extremidades__nombre__icontains = key)
                        seleccionados2[e.nombre] = 'true'
                    elif e.nombre == key and queries is not None:
                        queries |= Q(extremidades__nombre__icontains = key)
                        seleccionados2[e.nombre] = 'true'

        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                for e in lateralidad:
                    if e.nombre == key and queries is None:
                        queries = Q(lateralidad__nombre__icontains = key)
                        seleccionados3[e.nombre] = 'true'
                    elif e.nombre == key and queries is not None:
                        queries |= Q(lateralidad__nombre__icontains = key)
                        seleccionados3[e.nombre] = 'true' 

        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                for e in posiciones:
                    if e.nombre == key and queries is None:
                        queries = Q(posicion__nombre__icontains = key)
                        seleccionados4[e.nombre] = 'true'
                    elif e.nombre == key and queries is not None:
                        queries |= Q(posicion__nombre__icontains = key)
                        seleccionados4[e.nombre] = 'true'

        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                for e in objetivos:
                    if e.autoAlias() == value and queries is None:
                        queries = Q(objetivoTerapeutico__nombre__icontains = key)
                        seleccionados5[e.autoAlias()] = 'true'
                    elif e.autoAlias() == value and queries is not None:
                        queries |= Q(objetivoTerapeutico__nombre__icontains = key)
                        seleccionados5[e.autoAlias()] = 'true'

        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                for e in diagnosticos:
                    if e.nombre == key and queries is None:
                        queries = Q(diagnostico__nombre__icontains = key)
                        seleccionados6[e.nombre] = 'true'
                    elif e.nombre == key and queries is not None:
                        queries |= Q(diagnostico__nombre__icontains = key)
                        seleccionados6[e.nombre] = 'true'

        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                for e in pci:
                    if e.nombre == key and queries is None:
                        queries = Q(pci__nombre__icontains = key)
                        seleccionados7[e.nombre] = 'true'
                    elif e.nombre == key and queries is not None:
                        queries |= Q(pci__nombre__icontains = key)
                        seleccionados7[e.nombre] = 'true'

        #En el caso en el que se envie el POST sin aplicar ningun filtro 
        if queries == None:
            return render(request, "accesoTerapeutas/ejercicios.html", {"ejercicios": ejercicios, "edades": edades,"extremidades": extremidades,
            "lateralidad": lateralidad,"posiciones": posiciones,"objetivos": objetivos, "pci": pci, "diagnosticos": diagnosticos, "seleccionados1":seleccionados1,
            "seleccionados2":seleccionados2,"seleccionados3":seleccionados3,"seleccionados4":seleccionados4,"seleccionados5":seleccionados5,"seleccionados6":seleccionados6,"seleccionados7":seleccionados7,"idioma":idioma})
        

        if terapeuta.idioma.code == 'en':
            ejercicios = Exercices.objects.filter(queries)
        else:
            ejercicios = Ejercicios.objects.filter(queries)
        return render(request, "accesoTerapeutas/ejercicios.html", {"ejercicios": ejercicios, "edades": edades,"extremidades": extremidades,
            "lateralidad": lateralidad,"posiciones": posiciones,"objetivos": objetivos, "pci": pci, "diagnosticos": diagnosticos, "seleccionados1":seleccionados1,
            "seleccionados2":seleccionados2,"seleccionados3":seleccionados3,"seleccionados4":seleccionados4,"seleccionados5":seleccionados5,"seleccionados6":seleccionados6,"seleccionados7":seleccionados7,"idioma":idioma})


    # Lo que estamos haciendo es crear un diccionario con el nombre "ejercicios" 
    # que nos recoge los objetos de la lista de sesiones que previamete hemos recogido
    return render(request, "accesoTerapeutas/ejercicios.html", {"ejercicios": ejercicios, "edades": edades,"extremidades": extremidades,
            "lateralidad": lateralidad,"posiciones": posiciones,"objetivos": objetivos, "pci": pci, "diagnosticos": diagnosticos, "seleccionados1":seleccionados1,
            "seleccionados2":seleccionados2,"seleccionados3":seleccionados3,"seleccionados4":seleccionados4,"seleccionados5":seleccionados5,"seleccionados6":seleccionados6,"seleccionados7":seleccionados7,"idioma":idioma})


@login_required
#Info ejercicios
def infoEjercicio(request, idEjercicio):

    terapeuta = Terapeutas.objects.get(usuario = request.user)

    if terapeuta.idioma.code == 'en':
        ejercicio = Exercices.objects.filter(pk = idEjercicio)
    else:
        ejercicio = Ejercicios.objects.filter(pk = idEjercicio)

    current_url = resolve(request.path_info)
    if(current_url.route == 'en/accesoTerapeutas/infoEjercicio/<int:idEjercicio>'):  #just taking a look
        idioma = "en"
    elif(current_url.route == 'es/accesoTerapeutas/infoEjercicio/<int:idEjercicio>' or current_url.route == 'accesoTerapeutas/infoEjercicio/<int:idEjercicio>'):  #can edit
        idioma = "es"

    return render(request, "accesoTerapeutas/ejercicioInfo.html", {"ejercicio": ejercicio,"idioma":idioma})


@login_required
#Busqueda en ejercicios
def busquedaEjercicios(request):
    
    ejercicios = request.GET.get('ejercicios','')
    queries = ( Q(nombre__icontains = ejercicios) | Q(descripcion__icontains = ejercicios) | Q(codigo__icontains = ejercicios))

    current_url = resolve(request.path_info)
    if(current_url.route == 'en/accesoTerapeutas/busquedaEjercicios'):  #just taking a look
        idioma = "en"
    elif(current_url.route == 'es/accesoTerapeutas/busquedaEjercicios' or current_url.route == 'accesoTerapeutas/busquedaEjercicios'):  #can edit
        idioma = "es"


    terapeuta = Terapeutas.objects.get(usuario = request.user)
    
    if terapeuta.idioma.code == 'en':
        #En el caso en el que se envie el POST con el cajon de buscar en blanco 
        if queries == None:
            ejercicios = Exercices.objects.all()
            return render(request, "accesoTerapeutas/ejercicios.html", {"ejercicios": ejercicios, "idioma":idioma})

        ejercicios = Exercices.objects.filter(queries)
        return render(request, "accesoTerapeutas/busquedaEjercicios.html", {"ejercicios": ejercicios, "idioma":idioma})

    else:
        #En el caso en el que se envie el POST con el cajon de buscar en blanco 
        if queries == None:
            ejercicios = Ejercicios.objects.all()
            return render(request, "accesoTerapeutas/ejercicios.html", {"ejercicios": ejercicios, "idioma":idioma})

        ejercicios = Ejercicios.objects.filter(queries)
        return render(request, "accesoTerapeutas/busquedaEjercicios.html", {"ejercicios": ejercicios, "idioma":idioma})

@login_required
#Añadir en ejercicios
def nuevoEjercicio(request):

    terapeuta = Terapeutas.objects.get(usuario = request.user)
    
    if terapeuta.idioma.code == 'en':
        if request.method == 'POST': # si el usuario está enviando el formulario con datos
            form = EnglishEjercicioForm(request.POST) # Bound form
            if form.is_valid():
                ejercicios = form.save(commit=False)
                ejercicios.creado = timezone.now()
                ejercicios.actualizado = timezone.now()
                ejercicios.save()
                form.save()
                ejercicios = Exercices.objects.all()
                return redirect('Ejercicios')

        else:
            form = EnglishEjercicioForm() # Unbound form
            return render(request, 'accesoTerapeutas/nuevoEjercicio.html', {'form': form})
    else:
        if request.method == 'POST': # si el usuario está enviando el formulario con datos
            form = EjercicioForm(request.POST) # Bound form
            if form.is_valid():
                ejercicios = form.save(commit=False)
                ejercicios.creado = timezone.now()
                ejercicios.actualizado = timezone.now()
                ejercicios.save()
                form.save()
                ejercicios = Ejercicios.objects.all()
                return redirect('Ejercicios')

        else:
            form = EjercicioForm() # Unbound form
            return render(request, 'accesoTerapeutas/nuevoEjercicio.html', {'form': form})


@login_required
#Editar en ejercicio
def editarEjercicio(request, idEjercicio):

    terapeuta = Terapeutas.objects.get(usuario = request.user)
    
    if terapeuta.idioma.code == 'en':
        e = Exercices.objects.get(pk=idEjercicio) #aqui tienen tu objeto de tipo Empleado

        if request.method == "POST":
            form = EnglishEditarEjercicioForm(request.POST,request.FILES,instance=e)
            if form.is_valid():

                e.nombre = request.POST['nombre']
                e.descripcion = request.POST['descripcion']

                edad = request.POST['edad']
                edad1 = Ages.objects.get(id=edad)
                e.edad.add(edad1)

                extremidad = request.POST['extremidades']
                extremidad1 = Extremities.objects.get(id=extremidad)
                e.extremidades.add(extremidad1)

                ############### Foreign Key ################
                lateralidad = request.POST['lateralidad']
                l = Laterality.objects.get(id=lateralidad)
                l.lateralidad = l

                posicion = request.POST['posicion']
                posicion1 = Position.objects.get(id=posicion)
                e.posicion.add(posicion1)

                objetivo = request.POST['objetivoTerapeutico']
                objetivo1 = TherapeuticObjective.objects.get(id=objetivo)
                e.objetivoTerapeutico.add(objetivo1)

                diagnostico = request.POST['diagnostico']
                diagnostico1 = Diagnostics.objects.get(id=diagnostico)
                e.diagnostico.add(diagnostico1)

                pci = request.POST['pci']
                pci1 = PciEnglish.objects.get(id=pci)
                e.pci.add(pci1)

                #e.video = request.FILES['video']
                e.actualizado = timezone.now()
                form.save() #aqui estas guardando diractamente el formulario en la base de datos
                return redirect('Ejercicios')
            else:

                form = EnglishEditarEjercicioForm(instance=e) 
                return render(request,"accesoTerapeutas/editarEjercicio.html",{'form' : form})
        else:

            form = EnglishEditarEjercicioForm(instance=e) 

        return render(request, "accesoTerapeutas/editarEjercicio.html",{'form' : form})
    else:
        e = Ejercicios.objects.get(pk=idEjercicio) #aqui tienen tu objeto de tipo Empleado

        if request.method == "POST":
            form = EditarEjercicioForm(request.POST,request.FILES,instance=e)
            if form.is_valid():

                e.nombre = request.POST['nombre']
                e.descripcion = request.POST['descripcion']

                edad = request.POST['edad']
                edad1 = Edad.objects.get(id=edad)
                e.edad.add(edad1)

                extremidad = request.POST['extremidades']
                extremidad1 = Extremidades.objects.get(id=extremidad)
                e.extremidades.add(extremidad1)

                ############### Foreign Key ################
                lateralidad = request.POST['lateralidad']
                l = Lateralidad.objects.get(id=lateralidad)
                l.lateralidad = l

                posicion = request.POST['posicion']
                posicion1 = Posicion.objects.get(id=posicion)
                e.posicion.add(posicion1)

                objetivo = request.POST['objetivoTerapeutico']
                objetivo1 = ObjetivoTerapeutico.objects.get(id=objetivo)
                e.objetivoTerapeutico.add(objetivo1)

                diagnostico = request.POST['diagnostico']
                diagnostico1 = Diagnosticos.objects.get(id=diagnostico)
                e.diagnostico.add(diagnostico1)

                pci = request.POST['pci']
                pci1 = Pci.objects.get(id=pci)
                e.pci.add(pci1)

                #e.video = request.FILES['video']
                e.actualizado = timezone.now()
                form.save() #aqui estas guardando diractamente el formulario en la base de datos
                return redirect('Ejercicios')
            else:

                form = EditarEjercicioForm(instance=e) 
                return render(request,"accesoTerapeutas/editarEjercicio.html",{'form' : form})
        else:

            form = EditarEjercicioForm(instance=e) 

        return render(request, "accesoTerapeutas/editarEjercicio.html",{'form' : form})

@login_required
#SubirVideo
def subirVideo(request, idEjercicio):

    terapeuta = Terapeutas.objects.get(usuario = request.user)
    
    if terapeuta.idioma.code == 'en':
        e = Exercices.objects.get(pk=idEjercicio) #aqui tienen tu objeto de tipo Empleado

        if request.method == "POST":
            form = EnglishSubirVideoForm(request.POST,request.FILES,instance=e)
            if form.is_valid():
            
                #e.video = request.FILES['video']
                e.actualizado = timezone.now()
                form.save() #aqui estas guardando diractamente el formulario en la base de datos
                return redirect('Ejercicios')
            else:

                form = EnglishSubirVideoForm(instance=e) 
                return render(request,"accesoTerapeutas/subirVideo.html",{'form' : form})
        else:

            form = EnglishSubirVideoForm(instance=e) 

        return render(request, "accesoTerapeutas/subirVideo.html",{'form' : form})

    else:
        e = Ejercicios.objects.get(pk=idEjercicio) #aqui tienen tu objeto de tipo Empleado

        if request.method == "POST":
            form = SubirVideoForm(request.POST,request.FILES,instance=e)
            if form.is_valid():
            
                #e.video = request.FILES['video']
                e.actualizado = timezone.now()
                form.save() #aqui estas guardando diractamente el formulario en la base de datos
                return redirect('Ejercicios')
            else:

                form = SubirVideoForm(instance=e) 
                return render(request,"accesoTerapeutas/subirVideo.html",{'form' : form})
        else:

            form = SubirVideoForm(instance=e) 

        return render(request, "accesoTerapeutas/subirVideo.html",{'form' : form})


@login_required
#Ocultar en ejercicios
def ocultarEjercicio(request, idEjercicio):

    terapeuta = Terapeutas.objects.get(usuario = request.user)
    
    if terapeuta.idioma.code == 'en':
        e = Exercices.objects.get(pk=idEjercicio) 
    else:
        e = Ejercicios.objects.get(pk=idEjercicio) 
    e.visible = False
    e.save()
    return  redirect('Ejercicios')



#Esta vista mostrara un listado de los ejercicios que tiene el TERAPEUTA en NO VISIBLE
@login_required
def ejerciciosNoVisibles(request):

    terapeuta = Terapeutas.objects.get(usuario = request.user)
    
    if terapeuta.idioma.code == 'en':
        ejercicios = Exercices.objects.all()
        edades = Ages.objects.all()
        extremidades = Extremities.objects.all()
        lateralidad = Laterality.objects.all()
        posiciones = Position.objects.all()
        objetivos = TherapeuticObjective.objects.all()
        diagnosticos = Diagnostics.objects.all()
        pci = PciEnglish.objects.all()
    else:
        ejercicios = Ejercicios.objects.all()
        edades = Edad.objects.all()
        extremidades = Extremidades.objects.all()
        lateralidad = Lateralidad.objects.all()
        posiciones = Posicion.objects.all()
        objetivos = ObjetivoTerapeutico.objects.all()
        diagnosticos = Diagnosticos.objects.all()
        pci = Pci.objects.all()

    current_url = resolve(request.path_info)
    if(current_url.route == 'en/accesoTerapeutas/ejerciciosNoVisibles'):  #just taking a look
        idioma = "en"
    elif(current_url.route == 'es/accesoTerapeutas/ejerciciosNoVisibles' or current_url.route == 'accesoTerapeutas/ejerciciosNoVisibles'):  #can edit
        idioma = "es"

    #Filtrado en ejercicios 
    #Creo un diccionario con los filtros
    seleccionados1 = {}
    seleccionados2 = {}
    seleccionados3 = {}
    seleccionados4 = {}
    seleccionados5 = {}
    seleccionados6 = {}
    seleccionados7 = {}
    queries = None

    ################################ FILTRADO EN EJERCICIOS ##############################
    if request.POST:

        #        Para hacer comprobaciones       #
        for key, value in request.POST.items():
           if key != 'csrfmiddlewaretoken':
                valores = key + ":" + value
                #print(valores)
        ##########################################

        for e in edades:
            seleccionados1[e.autoAlias()] = 'false'
        for e in extremidades:
            seleccionados2[e.nombre] = 'false'
        for l in lateralidad:
            seleccionados3[l.nombre] = 'false'
        for p in posiciones:
            seleccionados4[p.nombre] = 'false'
        for o in objetivos:
            seleccionados5[o.autoAlias()] = 'false'
        for d in diagnosticos:
            seleccionados6[d.nombre] = 'false'
        for p in pci:
            seleccionados7[p.nombre] = 'false'

        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                for e in edades:
                    if e.autoAlias() == value and queries is None:
                        queries = Q(edad__nombre__icontains = key)
                        seleccionados1[e.autoAlias()] = 'true'
                    elif e.autoAlias() == value and queries is not None:
                        queries |= Q(edad__nombre__icontains = key)
                        seleccionados1[e.autoAlias()] = 'true'

        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                for e in extremidades:
                    if e.nombre == key and queries is None:
                        queries = Q(extremidades__nombre__icontains = key)
                        seleccionados2[e.nombre] = 'true'
                    elif e.nombre == key and queries is not None:
                        queries |= Q(extremidades__nombre__icontains = key)
                        seleccionados2[e.nombre] = 'true'

        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                for e in lateralidad:
                    if e.nombre == key and queries is None:
                        queries = Q(lateralidad__nombre__icontains = key)
                        seleccionados3[e.nombre] = 'true'
                    elif e.nombre == key and queries is not None:
                        queries |= Q(lateralidad__nombre__icontains = key)
                        seleccionados3[e.nombre] = 'true' 

        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                for e in posiciones:
                    if e.nombre == key and queries is None:
                        queries = Q(posicion__nombre__icontains = key)
                        seleccionados4[e.nombre] = 'true'
                    elif e.nombre == key and queries is not None:
                        queries |= Q(posicion__nombre__icontains = key)
                        seleccionados4[e.nombre] = 'true'

        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                for e in objetivos:
                    if e.autoAlias() == value and queries is None:
                        queries = Q(objetivoTerapeutico__nombre__icontains = key)
                        seleccionados5[e.autoAlias()] = 'true'
                    elif e.autoAlias() == value and queries is not None:
                        queries |= Q(objetivoTerapeutico__nombre__icontains = key)
                        seleccionados5[e.autoAlias()] = 'true'

        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                for e in diagnosticos:
                    if e.nombre == key and queries is None:
                        queries = Q(diagnostico__nombre__icontains = key)
                        seleccionados6[e.nombre] = 'true'
                    elif e.nombre == key and queries is not None:
                        queries |= Q(diagnostico__nombre__icontains = key)
                        seleccionados6[e.nombre] = 'true'

        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                for e in pci:
                    if e.nombre == key and queries is None:
                        queries = Q(pci__nombre__icontains = key)
                        seleccionados7[e.nombre] = 'true'
                    elif e.nombre == key and queries is not None:
                        queries |= Q(pci__nombre__icontains = key)
                        seleccionados7[e.nombre] = 'true'

        #En el caso en el que se envie el POST sin aplicar ningun filtro 
        if queries == None:
            return render(request, "accesoTerapeutas/ejerciciosNoVisibles.html", {"ejercicios": ejercicios, "edades": edades,"extremidades": extremidades,
            "lateralidad": lateralidad,"posiciones": posiciones,"objetivos": objetivos, "pci": pci, "diagnosticos": diagnosticos, "seleccionados1":seleccionados1,
            "seleccionados2":seleccionados2,"seleccionados3":seleccionados3,"seleccionados4":seleccionados4,"seleccionados5":seleccionados5,"seleccionados6":seleccionados6,"seleccionados7":seleccionados7,"idioma":idioma})
        
        ejercicios = Ejercicios.objects.filter(queries)
        return render(request, "accesoTerapeutas/ejerciciosNoVisibles.html", {"ejercicios": ejercicios, "edades": edades,"extremidades": extremidades,
            "lateralidad": lateralidad,"posiciones": posiciones,"objetivos": objetivos, "pci": pci, "diagnosticos": diagnosticos, "seleccionados1":seleccionados1,
            "seleccionados2":seleccionados2,"seleccionados3":seleccionados3,"seleccionados4":seleccionados4,"seleccionados5":seleccionados5,"seleccionados6":seleccionados6,"seleccionados7":seleccionados7,"idioma":idioma})


    # Lo que estamos haciendo es crear un diccionario con el nombre "ejercicios" 
    # que nos recoge los objetos de la lista de sesiones que previamete hemos recogido
    return render(request, "accesoTerapeutas/ejerciciosNoVisibles.html", {"ejercicios": ejercicios, "edades": edades,"extremidades": extremidades,
            "lateralidad": lateralidad,"posiciones": posiciones,"objetivos": objetivos, "pci": pci, "diagnosticos": diagnosticos, "seleccionados1":seleccionados1,
            "seleccionados2":seleccionados2,"seleccionados3":seleccionados3,"seleccionados4":seleccionados4,"seleccionados5":seleccionados5,"seleccionados6":seleccionados6,"seleccionados7":seleccionados7,"idioma":idioma})
    






















########################################################################################## 
#-------------------------------------- SESIONES ----------------------------------------#
########################################################################################## 
@login_required
def nuevaSesion(request):

    terapeuta = Terapeutas.objects.get(usuario = request.user)
    
    if terapeuta.idioma.code == 'en':
        if request.method == 'POST': # si el usuario está enviando el formulario con datos
            form = EnglishSesionForm(request.POST) # Bound form
            if form.is_valid():

                sesiones = form.save(commit=False)
                sesiones.creado = timezone.now()
                sesiones.actualizado = timezone.now()
                sesiones.save()
                idSesion = sesiones.id
                print(idSesion)
                form.save()
                sesiones = Sessions.objects.all()
                return redirect('ejerciciosSesion', idSesion)

        else:
            form = EnglishSesionForm() # Unbound form
            return render(request, 'accesoTerapeutas/nuevaSesion.html', {'form': form})

    else:
        if request.method == 'POST': # si el usuario está enviando el formulario con datos
            form = SesionForm(request.POST) # Bound form
            if form.is_valid():

                sesiones = form.save(commit=False)
                sesiones.creado = timezone.now()
                sesiones.actualizado = timezone.now()
                sesiones.save()
                idSesion = sesiones.id
                print(idSesion)
                form.save()
                sesiones = Sesiones.objects.all()
                return redirect('ejerciciosSesion', idSesion)

        else:
            form = SesionForm() # Unbound form
            return render(request, 'accesoTerapeutas/nuevaSesion.html', {'form': form})

@login_required
def ejerciciosSesion(request,idSesion):

    terapeuta = Terapeutas.objects.get(usuario = request.user)
    
    if terapeuta.idioma.code == 'en':
        if request.method == 'POST': # si el usuario está enviando el formulario con datos
            form2 = EnglishSesionEjerciciosForm(request.POST) 
            if form2.is_valid():
                sesionEjercicios = form2.save(commit=False)
                sesionEjercicios.sesiones_id = idSesion
                form2.save()
                sesionEjercicios = SessionsExercices.objects.all()

                form2 = EnglishSesionEjerciciosForm() # Unbound form
                sesion = Sessions.objects.get(pk=idSesion) #aqui tienen tu objeto de tipo Empleado
                return render(request, 'accesoTerapeutas/ejerciciosSesion.html', {'form2': form2, "sesion":sesion})

        else:
            form2 = EnglishSesionEjerciciosForm() # Unbound form
            sesion = Sessions.objects.get(pk=idSesion) #aqui tienen tu objeto de tipo Empleado

            return render(request, 'accesoTerapeutas/ejerciciosSesion.html', {'form2': form2, "sesion":sesion})
    else:
        if request.method == 'POST': # si el usuario está enviando el formulario con datos
            form2 = SesionEjerciciosForm(request.POST) 
            if form2.is_valid():
                sesionEjercicios = form2.save(commit=False)
                sesionEjercicios.sesiones_id = idSesion
                #sesionEjercicios.sesiones.id = idSesion
                form2.save()
                sesionEjercicios = SesionesEjercicios.objects.all()

                form2 = SesionEjerciciosForm() # Unbound form
                sesion = Sesiones.objects.get(pk=idSesion) #aqui tienen tu objeto de tipo Empleado
                return render(request, 'accesoTerapeutas/ejerciciosSesion.html', {'form2': form2, "sesion":sesion})

        else:
            form2 = SesionEjerciciosForm() # Unbound form
            sesion = Sesiones.objects.get(pk=idSesion) #aqui tienen tu objeto de tipo Empleado

            return render(request, 'accesoTerapeutas/ejerciciosSesion.html', {'form2': form2, "sesion":sesion})

@login_required
#Editar en sesiones
def editarSesion(request, idSesion):
    
    s = Sesiones.objects.get(pk=idSesion) #aqui tienen tu objeto de tipo Empleado
    if request.method == "POST":
        form = EditarSesionForm(request.POST,instance=s)
        if form.is_valid():
            
            print(request)
            paciente = request.POST['paciente']
            d = Pacientes.objects.get(id=paciente)
            s.paciente = d

            #e = Ejercicios.objects.get(id)
            #s.ejercicios = e


            s.periodicidad = request.POST['periodicidad']


            #s.fechaInicial = request.POST['fechaInicial']
            #s.fechaFinal = request.POST['fechaFinal']
            #fechaIn = datetime.strptime(request.POST['fechaInicial'], '%d/%m/%Y')
            #fechaIn2 = datetime.strftime(fechaIn, '%Y-%m-%d')
            #fechaFin = datetime.strptime(request.POST['fechaFinal'], '%d/%m/%Y')
            #fechaFin2 = datetime.strftime(fechaFin, '%Y-%m-%d')
            #s.fechaInicial = fechaIn2
            #s.fechaFinal = fechaFin2

            terapeuta = request.POST['terapeuta']
            d = Terapeutas.objects.get(id=terapeuta)
            s.terapeuta = d

            s.visible = request.POST['visible']
            if s.visible == "on":
                s.visible = True
            else:
                s.visible = False
           

            s.actualizado = timezone.now()
            form.save() #aqui estas guardando diractamente el formulario en la base de datos
            return redirect('Sesiones')
        else:
            form = EditarSesionForm(instance=s) 
            return render(request,"accesoTerapeutas/editarSesion.html",{'form' : form})
    else:
        form = EditarSesionForm(instance=s) 

    return render(request, "accesoTerapeutas/editarSesion.html",{'form' : form})

@login_required
def sesiones(request):

    terapeuta = Terapeutas.objects.get(usuario = request.user)

    if terapeuta.idioma.code == 'en':
        ejercicios = Exercices.objects.all()
        sesiones = Sessions.objects.filter(terapeuta = terapeuta) 
        sesionesEjercicios = SessionsExercices.objects.all()
        realizados = ExercisesDone.objects.all()
        registro = RegistrationSession.objects.all()
        valoracion = AssessmentPatiens.objects.all()
    else:
        ejercicios = Ejercicios.objects.all()
        sesiones = Sesiones.objects.filter(terapeuta = terapeuta) 
        sesionesEjercicios = SesionesEjercicios.objects.all()
        realizados = EjerciciosRealizados.objects.all()
        registro = RegistroSesiones.objects.all()
        valoracion = ValoracionPacientes.objects.all()

    fechaActual = datetime.now()
    actual = fechaActual.strftime("%d-%m-%Y")

    current_url = resolve(request.path_info)
    if(current_url.route == 'en/accesoTerapeutas/sesiones'):  #just taking a look
        idioma = "en"
    elif(current_url.route == 'es/accesoTerapeutas/sesiones' or current_url.route == 'accesoTerapeutas/sesiones'):  #can edit
        idioma = "es"
    
 # Lo que estamos haciendo es crear un diccionario con el nombre "sesiones" 
 # que nos recoge los objetos de la lista de sesiones que previamete hemos recogido
    return render(request, "accesoTerapeutas/sesiones.html", {"actual":actual, "sesiones": sesiones, "ejercicios": ejercicios, "sesionesEjercicios": sesionesEjercicios, "valoracion": valoracion, "registro": registro, "realizados": realizados, "idioma":idioma})
    

@login_required
#Busqueda en sesiones
def busquedaSesiones(request):
    
    sesion = request.GET.get('sesiones','')
    terapeuta = Terapeutas.objects.get(usuario = request.user)

    if terapeuta.idioma.code == 'en':
        sesionesEjercicios = SessionsExercices.objects.all()
        realizados = ExercisesDone.objects.all()
        registro = RegistrationSession.objects.all()
        valoracion = AssessmentPatiens.objects.all()
    else:
        sesionesEjercicios = SesionesEjercicios.objects.all()
        realizados = EjerciciosRealizados.objects.all()
        registro = RegistroSesiones.objects.all()
        valoracion = ValoracionPacientes.objects.all()
    
    queries = ( Q(paciente__nombre__icontains = sesion) | Q(paciente__apellidos__icontains = sesion))

    
    print(sesionesEjercicios)

    current_url = resolve(request.path_info)
    if(current_url.route == 'en/accesoTerapeutas/busquedaSesiones'):  #just taking a look
        idioma = "en"
    elif(current_url.route == 'es/accesoTerapeutas/busquedaSesiones' or current_url.route == 'accesoTerapeutas/busquedaSesiones'):  #can edit
        idioma = "es"
    #En el caso en el que se envie el POST con el cajon de buscar en blanco 
    if queries == None:
        if terapeuta.idioma.code == 'en':
            sesiones = Sessions.objects.all()
            ejercicios = ExercisesDone.objects.all()
        else:
            sesiones = Sesiones.objects.all()
            ejercicios = Ejercicios.objects.all()
        
        return render(request, "accesoTerapeutas/busquedaSesiones.html", {"sesiones": sesiones, "ejercicios": ejercicios, "sesionesEjercicios": sesionesEjercicios, "valoracion": valoracion, "registro": registro, "realizados": realizados, "idioma":idioma})
    if terapeuta.idioma.code == 'en':
        ejercicios = Exercices.objects.all()
        sesiones = Sessions.objects.filter(queries)
    else:
        ejercicios = Ejercicios.objects.all()
        sesiones = Sesiones.objects.filter(queries)
    return render(request, "accesoTerapeutas/busquedaSesiones.html", {"sesiones": sesiones, "ejercicios": ejercicios, "sesionesEjercicios": sesionesEjercicios, "valoracion": valoracion, "registro": registro, "realizados": realizados, "idioma":idioma})


@login_required
#Enviar sesion. Se usa para crear un fichero con todos los datos que va a tener la sesion y sera ese el fichero qeu se envia a la raspberry
def sesionEnviada(request, sesionId):

    terapeuta = Terapeutas.objects.get(usuario = request.user)
    
    if terapeuta.idioma.code == 'en':
        s = Sessions.objects.get(pk=sesionId) #aqui tienen tu objeto de tipo Sesion
        sEj = SessionsExercices.objects.filter(sesiones__id=sesionId) #aqui tienen tu objeto de tipo Sesion
    else:
        s = Sesiones.objects.get(pk=sesionId) #aqui tienen tu objeto de tipo Sesion
        sEj = SesionesEjercicios.objects.filter(sesiones__id=sesionId) #aqui tienen tu objeto de tipo Sesion
    print(sEj)
    pacienteId = s.paciente.id
    #Ruta para almacenar el fichero con la sesion
    if workingOnServer:
        ruta = '/home/ubuntu/Web/django/rehaWeb/datosEnviados/sesiones/'
    else:
        ruta = '/Users/oscarmartincasares/Desktop/Working_www...com/rehaweb/rehaweb/datosEnviados/sesiones/'
    nombre = ruta + str(s.paciente.usuario) + ".txt"
    
    
    with open(nombre, 'w') as f:
        myfile = File(f)
        myfile.write('Fecha de inicio: '+ str(s.fechaInicial))
        myfile.write('\nFecha de finalizacion: '+ str(s.fechaFinal))
        for sesion in sEj:
            if sesion.sesiones.id == sesionId:
                myfile.write('\nCodigo: ' + str(sesion.ejercicios.codigo))
                ejercicio = sesion.ejercicios.nombre
                myfile.write('\nEjercicio: ' + str(ejercicio))
                repeticiones = sesion.repeticiones
                myfile.write('\nRepeticiones: ' + str(repeticiones))
#                if sesion.ejercicios.descripcion:
#                    myfile.write('\nDescripcion: ' + unicode(sesion.ejercicios.descripcion).encode('utf-8))
        myfile.write('\nPeriodicidad: ' + str(s.periodicidad))
        myfile.write('\nSesion: ' + str(sesionId))
        myfile.write('\nPaciente Id: ' + str(pacienteId))
    
    myfile.closed
    f.closed
    #Cambiamos el campo del modelo indicando que esa sesion ha sido ya enviada
    s.enviado=True
    s.save()
    print(ruta)
    #return render(request, "accesoTerapeutas/sesiones.html")
    return redirect('Sesiones')

def safe_str(obj):
    try: return str(obj)
    except UnicodeEncodeError:
        return obj.encode('ascii', 'ignore').decode('ascii')
    return ""

#Esta vista mostrara un listado de los pacientes que tiene el TERAPEUTA en NO VISIBLE
@login_required
def sesionesNoVisibles(request):

    terapeuta = Terapeutas.objects.get(usuario = request.user)
    if terapeuta.idioma.code == 'en':
        realizados = ExercisesDone.objects.all()
        registro = RegistrationSession.objects.all()
        valoracion = AssessmentPatiens.objects.all()
        sesionesEjercicios = SessionsExercices.objects.all()
        sesiones = Sessions.objects.filter(visible=False).order_by('-actualizado')
    else:
        realizados = EjerciciosRealizados.objects.all()
        registro = RegistroSesiones.objects.all()
        valoracion = ValoracionPacientes.objects.all()
        sesionesEjercicios = SesionesEjercicios.objects.all()
        sesiones = Sesiones.objects.filter(visible=False).order_by('-actualizado')

    current_url = resolve(request.path_info)
    if(current_url.route == 'en/accesoTerapeutas/sesionesNoVisibles'):  #just taking a look
        idioma = "en"
    elif(current_url.route == 'es/accesoTerapeutas/sesionesNoVisibles' or current_url.route == 'accesoTerapeutas/sesionesNoVisibles'):  #can edit
        idioma = "es"

    return render(request, "accesoTerapeutas/sesionesNoVisibles.html", {"sesiones": sesiones,"sesionesEjercicios": sesionesEjercicios, "valoracion": valoracion, "registro": registro, "realizados": realizados,"idioma":idioma})


@login_required
#Ocultar en pacientes
def ocultarSesion(request, idSesion):
    
    terapeuta = Terapeutas.objects.get(usuario = request.user)
    if terapeuta.idioma.code == 'en':
        s = Sessions.objects.get(pk=idSesion) #aqui tienen tu objeto de tipo Empleado
    else:
        s = Sesiones.objects.get(pk=idSesion) #aqui tienen tu objeto de tipo Empleado
    s.visible = False
    s.save()
    return  redirect('Sesiones')


















########################################################################################## 
#-------------------------------------- INFORMES ----------------------------------------#
########################################################################################## 
def getDays(sesionId,paciente):

    days = []
    valoraciones = ValoracionPacientes.objects.filter(usuario = paciente, sesion = sesionId)
    for valoracion in valoraciones:
        if valoracion.fecha not in days:
            days.append(valoracion.fecha)

    return days

@login_required
def informes(request, sesionId,showFilters=False):
    print(sesionId)
    terapeuta = Terapeutas.objects.get(usuario = request.user)
    if terapeuta.idioma.code == 'en':
        s = Sessions.objects.get(pk=sesionId) #aqui tienen tu objeto de tipo Sesion
        idioma = 'en'
    else:
        s = Sesiones.objects.get(pk=sesionId) #aqui tienen tu objeto de tipo Sesion
        idioma = 'es'

    try:
        if workingOnServer:
            #aws s3 sync s3:://ficherosrehabot2/sesiones
            pass
        pacienteId = s.paciente.id
        if workingOnServer == True:
            ruta = '/home/ubuntu/Web/django/rehaWeb/datosRecibidos/valoracionIndividual/'
        else:
            ruta = '/Users/oscarmartincasares/Desktop/Working_www...com/rehaWeb/rehaWeb/datosRecibidos/valoracionIndividual/'
        nombre = ruta + "valoracionIndividual" + str(s.paciente.usuario) + "_" + str(sesionId) + ".csv"  

        import csv
        with open(nombre) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            ejs = []
            val1 = []
            val2 = []
            val3 = []
            val4 = []
            val5 = []
            fecha = []
            sesionId = []

            for row in csv_reader:
                ejs.append(row[2])
                val1.append(row[3])
                val2.append(row[4])
                val3.append(row[5])
                val4.append(row[6])
                val5.append(row[7])
                fecha.append(row[8].split(" ")[0])
                sesionId.append(row[9])
        
            ejercicios_readed = len(ejs)

        if terapeuta.idioma.code == 'en':
            exist = AssessmentPatiens.objects.filter(sesion = sesionId[1])
            paciente = Patients.objects.get(id = pacienteId)
            if len(exist) == 0:
                for i in range(len(ejs)):
                    v = AssessmentPatiens()
                    v.usuario = paciente
                    v.ejercicio = ejs[i]
                    v.valoracion1 = val1[i]
                    v.valoracion2 = val2[i]
                    v.valoracion3 = val3[i]
                    v.valoracion4 = val4[i]
                    v.valoracion5 = val5[i]
                    v.fecha = fecha[i]
                    v.sesion = sesionId[i]
                    v.save()
            elif len(exist) > 0:
                initial = len(exist)
                for i in range(ejercicios_readed - initial):
                    v = AssessmentPatiens()
                    v.usuario = paciente
                    v.ejercicio = ejs[i+initial]
                    v.valoracion1 = val1[i+initial]
                    v.valoracion2 = val2[i+initial]
                    v.valoracion3 = val3[i+initial]
                    v.valoracion4 = val4[i+initial]
                    v.valoracion5 = val5[i+initial]
                    v.fecha = fecha[i+initial]
                    v.sesion = sesionId[i+initial]
                    v.save()

            valoracion = AssessmentPatiens.objects.filter(sesion = sesionId[1])  
        else:
            exist = ValoracionPacientes.objects.filter(sesion = sesionId[1])
            paciente = Pacientes.objects.get(id = pacienteId)
            if len(exist) == 0:
                for i in range(len(ejs)):
                    v = ValoracionPacientes()
                    v.usuario = paciente
                    v.ejercicio = ejs[i]
                    v.valoracion1 = val1[i]
                    v.valoracion2 = val2[i]
                    v.valoracion3 = val3[i]
                    v.valoracion4 = val4[i]
                    v.valoracion5 = val5[i]
                    v.fecha = fecha[i]
                    v.sesion = sesionId[i]
                    v.save()
            elif len(exist) > 0:
                initial = len(exist)
                for i in range(ejercicios_readed - initial):
                    v = ValoracionPacientes()
                    v.usuario = paciente
                    v.ejercicio = ejs[i+initial]
                    v.valoracion1 = val1[i+initial]
                    v.valoracion2 = val2[i+initial]
                    v.valoracion3 = val3[i+initial]
                    v.valoracion4 = val4[i+initial]
                    v.valoracion5 = val5[i+initial]
                    v.fecha = fecha[i+initial]
                    v.sesion = sesionId[i+initial]
                    v.save()

            valoracion = ValoracionPacientes.objects.filter(sesion = sesionId[1])

        days = getDays(sesionId[1],paciente)

        notinform = False
        context = {
            "valoracion": valoracion, 
            "idioma":idioma, 
            "notinform":notinform,
            "sesion":s, 
            "paciente":paciente,
            "dias":days,
            "showFilters": showFilters,
        }
        
        return render(request, "accesoTerapeutas/informes.html", context)
    except:
        notinform = True
        return render(request, "accesoTerapeutas/informes.html", {"notinform":notinform,"sesion":s})



''' 
@login_required
def informes(request, sesionId, showFilters=False):
    print(sesionId)

    terapeuta = Terapeutas.objects.get(usuario = request.user)
    if terapeuta.idioma.code == 'en':
        s = Sessions.objects.get(pk=sesionId) #aqui tienen tu objeto de tipo Sesion
        idioma = 'en'
    else:
        s = Sesiones.objects.get(pk=sesionId) #aqui tienen tu objeto de tipo Sesion
        idioma = 'es'

    if workingOnServer:
        #aws s3 sync s3:://ficherosrehabot2/sesiones
        pass

    try:
        pacienteId = s.paciente.id
        if workingOnServer == True:
            ruta = '/home/ubuntu/Web/django/rehaWeb/datosRecibidos/valoracionIndividual/'
        else:
            ruta = '/Users/oscarmartincasares/Desktop/Working_www...com/rehaWeb/rehaWeb/datosRecibidos/valoracionIndividual/'
        nombre = ruta + "valoracionIndividual" + str(s.paciente.usuario) + ".csv"


        import csv
        with open(nombre) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            ejs = []
            val1 = []
            val2 = []
            val3 = []
            val4 = []
            val5 = []
            fecha = []
            sesionId = []

            for row in csv_reader:
                ejs.append(row[2])
                val1.append(row[3])
                val2.append(row[4])
                val3.append(row[5])
                val4.append(row[6])
                val5.append(row[7])
                fecha.append(row[8].split(" ")[0])
                sesionId.append(row[9])
        
            ejercicios_readed = len(ejs)

        if terapeuta.idioma.code == 'en':
            exist = AssessmentPatiens.objects.filter(sesion = sesionId[1])
            paciente = Patients.objects.get(id = pacienteId)
            if len(exist) == 0:
                for i in range(len(ejs)):
                    v = AssessmentPatiens()
                    v.usuario = paciente
                    v.ejercicio = ejs[i]
                    v.valoracion1 = val1[i]
                    v.valoracion2 = val2[i]
                    v.valoracion3 = val3[i]
                    v.valoracion4 = val4[i]
                    v.valoracion5 = val5[i]
                    v.fecha = fecha[i]
                    v.sesion = sesionId[i]
                    v.save()
            elif len(exist) > 0:
                initial = len(exist)
                for i in range(ejercicios_readed - initial):
                    v = AssessmentPatiens()
                    v.usuario = paciente
                    v.ejercicio = ejs[i+initial]
                    v.valoracion1 = val1[i+initial]
                    v.valoracion2 = val2[i+initial]
                    v.valoracion3 = val3[i+initial]
                    v.valoracion4 = val4[i+initial]
                    v.valoracion5 = val5[i+initial]
                    v.fecha = fecha[i+initial]
                    v.sesion = sesionId[i+initial]
                    v.save()

            valoracion = AssessmentPatiens.objects.filter(sesion = sesionId[1])  
        else:
            exist = ValoracionPacientes.objects.filter(sesion = sesionId[1])
            paciente = Pacientes.objects.get(id = pacienteId)
            if len(exist) == 0:
                for i in range(len(ejs)):
                    v = ValoracionPacientes()
                    v.usuario = paciente
                    v.ejercicio = ejs[i]
                    v.valoracion1 = val1[i]
                    v.valoracion2 = val2[i]
                    v.valoracion3 = val3[i]
                    v.valoracion4 = val4[i]
                    v.valoracion5 = val5[i]
                    v.fecha = fecha[i]
                    v.sesion = sesionId[i]
                    v.save()
            elif len(exist) > 0:
                initial = len(exist)
                for i in range(ejercicios_readed - initial):
                    v = ValoracionPacientes()
                    v.usuario = paciente
                    v.ejercicio = ejs[i+initial]
                    v.valoracion1 = val1[i+initial]
                    v.valoracion2 = val2[i+initial]
                    v.valoracion3 = val3[i+initial]
                    v.valoracion4 = val4[i+initial]
                    v.valoracion5 = val5[i+initial]
                    v.fecha = fecha[i+initial]
                    v.sesion = sesionId[i+initial]
                    v.save()

            valoracion = ValoracionPacientes.objects.filter(sesion = sesionId[1])

        days = getDays(sesionId[1],paciente)

        notinform = False
        context = {
            "valoracion": valoracion, 
            "idioma":idioma, 
            "notinform":notinform,
            "sesion":s, 
            "paciente":paciente,
            "dias":days,
            "showFilters": showFilters,
        }
        
        return render(request, "accesoTerapeutas/informes.html", context)
    except:
        notinform = True
        return render(request, "accesoTerapeutas/informes.html", {"notinform":notinform,"sesion":s})
'''

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def filtrarInforme(request, idPaciente, sesionId):

    terapeuta = Terapeutas.objects.get(usuario = request.user)
    if terapeuta.idioma.code == 'en':
        s = Sessions.objects.get(pk=sesionId) #aqui tienen tu objeto de tipo Sesion
        idioma = 'en'
    else:
        s = Sesiones.objects.get(pk=sesionId) #aqui tienen tu objeto de tipo Sesion
        idioma = 'es'

    dolores = request.GET.getlist('dolor')
    fechas = request.GET.getlist('fechas')

    kwargs_dolor = []
    for sel in dolores:
        if sel == 'Menor a 3':
            kwargs_dolor.append(0)
            kwargs_dolor.append(1)
            kwargs_dolor.append(2)
        elif sel == 'Entre 3 y 5':
            kwargs_dolor.append(3)
            kwargs_dolor.append(4)
            kwargs_dolor.append(5)
        elif sel == 'Entre 6 y 8':
            kwargs_dolor.append(6)
            kwargs_dolor.append(7)
            kwargs_dolor.append(8)
        elif sel == 'Mas de 8':
            kwargs_dolor.append(9)
            kwargs_dolor.append(10)

    vals = []
    if terapeuta.idioma.code == 'en':
        paciente = Patients.objects.get(id = idPaciente)
        if len(dolores) != 0:
            valoraciones = AssessmentPatiens.objects.filter(usuario = paciente, valoracion4__in = kwargs_dolor)
        else:
            valoraciones = AssessmentPatiens.objects.filter(usuario = paciente)
    else:
        paciente = Pacientes.objects.get(id = idPaciente)
        if len(dolores) != 0:
            valoraciones = ValoracionPacientes.objects.filter(usuario = paciente, valoracion4__in = kwargs_dolor)
        else:
            valoraciones = ValoracionPacientes.objects.filter(usuario = paciente)

    if len(fechas) != 0:
        for fecha in fechas:
            for valoracion in valoraciones:
                if valoracion.fecha == fecha:
                    vals.append(valoracion)
    else:
        vals = valoraciones
    
    if len(dolores) == 0 and len(fechas) == 0:
        return redirect('Informes',sesionId)

    days = getDays(sesionId,paciente)

    notinform = False
    context = {
        "valoracion": vals, 
        "idioma":idioma, 
        "notinform":notinform,
        "sesion":s, 
        "paciente":paciente,
        "dias":days,
    }
    return render(request, "accesoTerapeutas/informes.html", context)


def get_join_pdf_file_name(file_name):
    path=os.path.join(settings.MEDIA_ROOT, "informes")
    if not os.path.exists(path):
        os.makedirs(path)
    full_filename=os.path.join(path, file_name)
    return full_filename

from PyPDF2 import PdfFileWriter, PdfFileReader

def join_pdf(pdf, final_name):
    output_path=get_join_pdf_file_name(final_name)
    pdf_writer=PdfFileWriter()

    pdf_reader=PdfFileReader(pdf)
    for page in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(page))

    #pdf_reader=PdfFileReader(pdf2.file.name)
    #for page in range(pdf_reader.getNumPages()):
    #    pdf_writer.addPage(pdf_reader.getPage(page))

    with open(output_path, 'wb') as fh:
        pdf_writer.write(fh)

    # fh = open(output_path, 'r')
    # return fh
    with open(output_path, 'rb') as f:
        return f.read()
    return ""

from django.http import HttpResponse
def generarPDF (request, sesionId):
    terapeuta = Terapeutas.objects.get(usuario = request.user)
    
    if terapeuta.idioma.code == 'en':
        s = Sessions.objects.get(pk=sesionId) #aqui tienen tu objeto de tipo Sesion
        idioma = 'en'
    else:
        s = Sesiones.objects.get(pk=sesionId) #aqui tienen tu objeto de tipo Sesion
        idioma = 'es'

    pacienteId = s.paciente.id

    if terapeuta.idioma.code == 'en':
        valoracion = AssessmentPatiens.objects.filter(sesion = sesionId)  
        paciente = Patients.objects.get(id = pacienteId)

        context = {"valoracion": valoracion, "idioma":idioma,"paciente":paciente}
        pdf_file = 'accesoTerapeutas/generacionPdf/genPdf.html'
        pdf = gen_pdf(pdf_file,context = context)
        final_filename = paciente.nombre + "_" + paciente.apellidos + "_report_session.pdf"
        f = join_pdf(pdf, final_filename)
        response = HttpResponse(f, content_type='application/pdf')
        attach = 'attachment; filename=' + final_filename
        response['Content-Disposition'] = attach
        return response

    else:
        valoracion = ValoracionPacientes.objects.filter(sesion = sesionId)
        paciente = Pacientes.objects.get(id = pacienteId)

        context = {"valoracion": valoracion, "idioma":idioma,"paciente":paciente}
        print(context)
        pdf_file = 'accesoTerapeutas/generacionPdf/genPdf.html'
        pdf = gen_pdf(pdf_file,context = context)
        final_filename = paciente.nombre + "_" + paciente.apellidos + "_informe_sesion_" + str(sesionId) + ".pdf"
        f = join_pdf(pdf, final_filename)
        response = HttpResponse(f, content_type='application/pdf')
        attach = 'attachment; filename=' + final_filename
        response['Content-Disposition'] = attach
        return response




