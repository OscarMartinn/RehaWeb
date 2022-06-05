from django.views.decorators.csrf import csrf_exempt
from gettext import gettext
from django.shortcuts import render, HttpResponse
from django.core.mail import send_mail
from rehaWebApp.forms import formularioContacto
from rehaWeb import settings
from django.shortcuts import redirect
from django.utils import translation


# Create your views here.
def index(request):

	#user_language = 'en'
	#translation.activate(user_language)
	#request.session[translation.LANGUAGE_SESSION_KEY] = user_language
	#if translation.LANGUAGE_SESSION_KEY in request.session:
	#	del request.session[translation.LANGUAGE_SESSION_KEY]


	#from django.utils.translation import gettext
	#title = gettext('Pagina de inicio')
	#context = {'title':title,}
	#return render(request, "rehaWebApp/index.html", context)
	print(translation.get_language())
	
	return render(request, "rehaWebApp/index.html", {"idioma": translation.get_language()})

def setLanguage(request, idLanguage=None):

	if idLanguage == 1:
		user_language = 'es' 
	else: 
		user_language = 'en'

	translation.activate(user_language)
	#request.session[translation.LANGUAGE_SESSION_KEY] = user_language
	#if translation.LANGUAGE_SESSION_KEY in request.session:
	#	del request.session[translation.LANGUAGE_SESSION_KEY]

	return redirect("index") 

def setLanguage2(request, idLanguage=None):

	if idLanguage == 1:
		user_language = 'es'
	else: 
		user_language = 'en'

	translation.activate(user_language)
	#request.session[translation.LANGUAGE_SESSION_KEY] = user_language
	#if translation.LANGUAGE_SESSION_KEY in request.session:
	#	del request.session[translation.LANGUAGE_SESSION_KEY]

	return redirect("login") 


def login(request):

	print(request)
	from django.urls import resolve
	current_url = resolve(request.path_info)
	print("Login:", current_url.route)

	print(translation.get_language())
	return render(request, "registration/login.html")

def contacto(request):
	if request.method == "POST":
		nameIntro = request.POST["name"]
		emailIntro = request.POST["email"]
		mensajeIntro = nameIntro + "\nCon correo electrónico: "+ emailIntro + "\n" + "Mensaje: " + request.POST["message"]
		emailFrom = settings.EMAIL_HOST_USER 
		dondeLlega = ["omartincas@gmail.com"]
		send_mail(nameIntro, mensajeIntro, emailFrom, dondeLlega)
	
	return render(request,"rehaWebApp/index.html",{"idioma": translation.get_language()}) 
		
