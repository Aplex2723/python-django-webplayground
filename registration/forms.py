from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido, 254 caracteres como maximo y debe de ser valido")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


    def clean_email(self):
        email = self.cleaned_data.get("email") #Recuperando el emailk
        if User.objects.filter(email=email).exists(): #Comprueba si existe algun correo duplicado
            raise forms.ValidationError("El email ya esta registrado, prueba con otro.") #si esta registrado, no deja registrar al usuario
        return email #En caso de que no este registrado, hace la validacion


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'link']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class':'form-control-file mt-3'}),
            'bio': forms.Textarea(attrs={'class':'form-control mt-3', 'rows':3, 'placeholder':'Biografia'}),
            'link': forms.URLInput(attrs={'class':'form-control mt-3', 'placeholder':'Enlace'}),
        }


class EmailForm(forms.ModelForm):
        email = forms.EmailField(required=True, help_text="Requerido, 254 caracteres como maximo y debe de ser valido")
        
        class Meta:
            model = User
            fields = ['email']

        def clean_email(self):
            email = self.cleaned_data.get("email") #Recuperando el emailk

            if 'email' in self.changed_data: #change_data es una lista que almacena todos los campos editados en el formulario
                if User.objects.filter(email=email).exists(): #Comprueba si existe algun correo duplicado
                    raise forms.ValidationError("El email ya esta registrado, prueba con otro.") #si esta registrado, no deja registrar al usuario
            return email #En caso de que no este registrado, hace la validacion
