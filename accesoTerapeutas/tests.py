from urllib import response
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rehaWeb import settings
from rehaWeb.settings import LOGIN_REDIRECT_URL

# Create your tests here.
User = get_user_model()

class UsuarioTestCase(TestCase):

    def setUp(self):
        user = User(username = 'prueba', email = 'prueba@mail.es')
        user.is_staff = True
        user.is_superuser = True
        user_pass = 'pass123456'
        self.user_pass = user_pass
        user.set_password(user_pass)
        user.save()
        self.user = user


    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count,1)

    def test_user_password(self):
        self.assertTrue(self.user.check_password(self.user_pass))

    def test_login_url(self):
        # url_login = "/apps/baremacion/local/accounts/login/"
        # self.assertEqual(settings.LOGIN_URL, url_login)
        url_login = settings.LOGIN_REDIRECT_URL
        print(url_login)
        # python requests - manage.py runserver
        # self.client.get, self.client.post
        # response = self.client.post(url, {}, follow=True)
        data = {'username':'prueba', 'password': self.user_pass}
        response = self.client.post("/accesoTerapeutas/", data, follow=True)
        #print(response.request)
        # print(dir(response))
        status_code = response.status_code
        self.assertEqual(status_code,200)