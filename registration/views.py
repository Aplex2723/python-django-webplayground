from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
#from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Profile


# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail 
    #success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    #Comprobando si el usuario se registro correctamente
    def get_success_url(self):
        return reverse_lazy('login') + '?register'

    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        #Modificando los campos en tiempo real para evitar eliminar valores no deseados
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'Nombre de usuario'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder':'Direccion email'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Constrasena'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Repita la contrasena'})
        return form

#     Comprobando y mostrando si el usuario esta logeado
@method_decorator(login_required, name="dispatch")
class ProfileUpdate(UpdateView):
    form_class = ProfileForm
        # model = Profile
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_form.html'

    def get_object(self):
        #Recuperando el objeto que se va a editar
        profile, created = Profile.objects.get_or_create(user=self.request.user) 
        #   Busca a partir del filtro y si no lo encuentra lo crea
        #   Esta funcion no se puede devolver asi nadamas, ya que
        #   es guardado como una tupla, para esto es necesario
        #   asignarle 2 valores, una el cual es el propio objeto
        #   en este caso "profile" y una variable de tipo bool
        #   donde se almacena si se a creado o no en este momento
        return profile
        
        
#     Comprobando y mostrando si el usuario esta logeado
@method_decorator(login_required, name="dispatch")
class EmailUpdate(UpdateView):
    form_class = EmailForm
        # model = Profile
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_email_form.html'

    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
         form = super(EmailUpdate, self).get_form()
        #Modificando los campos en tiempo real para evitar eliminar valores no deseados
         form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder':'Email'})

         return form