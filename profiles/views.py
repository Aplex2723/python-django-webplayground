from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from registration.models import Profile
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

# Create your views here.
class ProfilesListView(ListView):
    model = Profile
    template_name = "profiles/profile_list.html" #30 minustos buscando solucion a esto, es importante xd

    # Aplicando la paginacion  (Listas largas para separarlas por ganias, como en los perfiles)
    paginate_by = 3

class ProfilesDetailView(DetailView):
    model = Profile
    template_name = "profiles/profile_detail.html"
    
    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['username'])