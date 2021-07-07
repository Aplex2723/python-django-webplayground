from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver #Importando decorador 
from django.db.models.signals import post_save #Importando senal

#Funcion para ahorar espacio (Al actualizar la foto de perfil borra la antigua y pone la nueva)
def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)# Se recupera la instancia justo antes de actualizarla
    old_instance.avatar.delete()# Borramos la foto de avatar anterior
    return 'profiles/' + filename # Guardamos la nueva foto en la carpeta que le asignemos, junto al nommbre del archivo

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True) #Para anadir imagenes, es necesario tener instalada la libreria pilow y configurar en setting.py
    bio = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)

    class Meta: #Esta clase va a ordenar los objetos, primero numeros y luego letras
        ordering = ['user__username'] 

#               RELACIONES ENTRE MODELOS
#      -OneToOneField (1:1) 1 usuario - 1 perfil
#      -ForeigneyField (1:N) 1 autor <- N entradas
#      -ManyToManyField (N:M) N entradas <-> M categorias
#

@receiver(post_save, sender=User)# Definiendo la senal para que se guarde despues de crear el usuario
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
        #print("Se acaba de crear un usuario y su perfil enlazado")