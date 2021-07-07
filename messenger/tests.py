from django.test import TestCase
from django.contrib.auth.models import User
from .models import Thread, Message

# Create your tests here.
class ThreadTestCase(TestCase):
    def setUp(self):    #Montando entorno de pruebas
        self.user1 = User.objects.create_user('user1', None, 'test1234')    #Asignando los usuarios a usar, en este caso son 2.
        self.user2 = User.objects.create_user('user2', None, 'test1234')
        self.user3 = User.objects.create_user('user3', None, 'test1234')

        self.thread = Thread.objects.create()   #Creando un Hilo(Thread) el cual nos permite almacenar los mensajes escritos

    def test_add_users_to_thread(self):
        self.thread.users.add(self.user1, self.user2)   #El metodo 'add' nos sirve para anadir objetos, ya sean individuales o varias siempre y cuando esten separados con comas
        self.assertEqual(len(self.thread.users.all()), 2)   #El metodo 'assertEqual' somprueva si 2 valores son equivalentes, en esta caso se va a comprovar la longitud de los usuarios.

    def test_filter_thread_by_users(self):
        self.thread.users.add(self.user1, self.user2)   #Se vulve a anadir ya que si se ejecuta indivudualmente, no leera el test anterior.
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2) #Con esto ya tendiramos todos los Hilos donde esta el user1, para obtener tambien el usuario 2, agregamos otro filtro
        self.assertEqual(self.thread, threads[0])

    def test_filter_non_existent_thread(self):
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2) #Con esto ya tendiramos todos los Hilos donde esta el user1, para obtener tambien el usuario 2, agregamos otro filtro
        self.assertEqual(len(threads), 0)

    def test_add_message_to_thread(self):   #Haciendo test con los mensajes
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(user=self.user1, content="Muy buenas")    #Creamos los mensajes llamando a la clase 'Message' y asignandole un usuario y el contenido del mensaje
        message2 = Message.objects.create(user=self.user2, content="Hola")
        self.thread.messages.add(message1, message2)    #Anadimos los mensajes al Hilo(Thread)
        self.assertEqual(len(self.thread.messages.all()), 2)    #Comprovamos si la longitud de los mensajes son 2, en este caso es correcto ya que solo asignamos message1 y message2

        for message in self.thread.messages.all():  #Con este for, estamos comprobando si realmente se han guardado los usuarios junto al mensaje
            print("({}): {}".format(message.user, message.content))
        
    def test_add_message_from_user_not_in_thread(self): #Comprovbacion de mensaje no asignado pero aplicado
        self.thread.users.add(self.user1, self.user2)   #Anadiendo el usuario 1 y 2 al thread
        message1 = Message.objects.create(user=self.user1, content="Mensaje de la primera persona")  #Creando los mensajes para que se guarden en la duncion 'Message'
        message2 = Message.objects.create(user=self.user2, content="Mensaje de la segunda persona")
        message3 = Message.objects.create(user=self.user3, content="Mensaje de la tercera persona, soy un espia")    #Dandole un 3er mensaje.
        self.thread.messages.add(message1, message2, message3)
        self.assertEqual(len(self.thread.messages.all()), 2)
        #   En este caso da error ya que aun que nadamas le estamos diciendo que hay unicamente 2 usuarios, automaticamente se agrega el 3ero

    def test_find_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        threads = Thread.objects.find(self.user1, self.user2)   #Creando nuestro porpio metodo 'find'
        self.assertEqual(self.thread, threads)

    def test_find_or_create_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        threads = Thread.objects.find_or_create(self.user1, self.user2)
        self.assertEqual(self.thread, threads)
        threads = Thread.objects.find_or_create(self.user1, self.user3)   #Como el usuario 'user3' no ha sido creado anteriormente, el metodo 'find_or_create' debera de crearlo
        self.assertIsNotNone(threads)   #Este assert debera validar de que threads no hay ningun valor none

