
from django.urls import path
from rehaWebApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.index, name = "index"),
    path('login/', views.login, name = "login"),
    path('contacto/', views.contacto),
    path('setLanguage/<int:idLanguage>', views.setLanguage, name = "setLanguage"),
    path('setLanguage2/<int:idLanguage>', views.setLanguage2, name = "setLanguage2"), 
     
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)