from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User

# Create your tests here.

class ProfileTestCase(TestCase):
    def setUp(self): #Se sobrescribe esta funcion que esta adentro de TestCase para preparar la prueba
        User.objects.create_user('test', 'test@test.com', 'test1234') #El metodo create_user se encarga de pasar una contrasena e incriptarla automaticamente

    def test_profile_exists(self): #Esta es la funcion de la prueba, se le puede asignar cualquier nombre siempre y cuando lleve test_profile
        exists = Profile.objects.filter(user__username='test').exists() # Filtra si en los perfiles hay un usuario con nombre 'test'
        self.assertEqual(exists, True)# Si existe, devolvera true
        