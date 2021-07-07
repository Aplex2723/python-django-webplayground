from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #Se le asigna a user, los usuarios registrados y si se elimina uno, borraria todo lo relacionado a el.
    content = models.TextField()    
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

#Creando un manager para pruebas en TDD, en pocas palabras estamos creando un filtro
class ThreadManager(models.Manager):
    def find(self, user1, user2):
        quaryset = self.filter(users=user1).filter(users=user2)
        if len(quaryset) > 0:
            return quaryset[0]
        else:
            return None
    
    def find_or_create(self, user1, user2):
        thread = self.find(user1, user2) #Buscando si existen, si no existe, habra un None
        if thread is None:  #Comprovamos si no exite el usuario
            thread = Thread.objects.create()    #Creando el usuario en caso de no existir
            thread.users.add(user1, user2)  #Anadiendo los usuarios al hilo nuevo
        return thread   #devolviendo el hilo


class Thread(models.Model): #Este hilo es el punto de encuentro que almacena: 
    users = models.ManyToManyField(User, related_name='threads') #Los Usuarios, con un identificador users.threads
    messages = models.ManyToManyField(Message) #Los mensajes escritos por los usuarios
    updated = models.DateTimeField(auto_now=True)

    objects = ThreadManager() #Para asignarle el filtro.

    class Meta:
        ordering = ['-updated']

#   Esta funcion esta conectada a Thread.messages para detectar cualquier cambio en su interior
#   Los valores que se optienen son varios, un ejemplo podria ser el pk_set el cual asigna o borra un identificador antes de crear un mensaje o despues de borrar
#   Mas info de distintos valores que se pueden sacar con el .pop() https://docs.djangoproject.com/en/2.0/ref/signals/#m2m-changed
def message_change(sender, **kwargs):  
    instance = kwargs.pop("instance", None) #La funcion pop() lo que hace es que saca elementos del diccionario
    action = kwargs.pop("action", None)
    pk_set = kwargs.pop("pk_set", None)
    print(instance, action, pk_set)

    false_pk_set = set()    #Aqui se guardaran los mensajes no deseados
    if action is "pre_add": #Comprovando si la accion fue un pre_add
        for msg_pk in pk_set:   #Iterando cada mensaje
            msg = Message.objects.get(pk=msg_pk)    #Asignando a la variable msg los mensajes por su clave principal
            if msg.user not in instance.users.all(): #Comprovando si el mensaje del usuario no esta en la lista de usuarios asignados
                print("Ups, ({}) no forma parte del hilo (thread)".format(msg.user))    #Si no esta, slatara un error y el usuario que no fue guardado
                false_pk_set.add(msg_pk)    #Anadiendo los mensajes no deseados a esta variable

    #   Buscar los mensajes que si estan en pk_set y los borramos
    pk_set.difference_update(false_pk_set)  #Esto lo que hace es como si le restara el mensaje no deseado, en este caso el pk_set tiene 3 usuarios y solo quemos 2
                                            #para eso es esta parte, ya que le estaria restando el dalse_pk_set que en este caso seria el 3er usuario dejando el pk_set con 2
    #   Forzando la actualizacion haciendo un save
    instance.save()


#   Con esta funcion conectamos la senal m2m_changed a la calse Thread.messages
m2m_changed.connect(message_change, sender=Thread.messages.through)