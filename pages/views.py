from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from .forms import PageForm
from .models import Page 

class StaffRequieredMixin(object):

    #Este Mixin requerirar que el usuario se amiembro del staff
    #Evitando que usuarios no identificados, modifiquen la pagina desde las urls

    #El siguiente metodos(decorador) nos servira para pedir una autentificacion
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
            #Verificando si es usuario es staff, y reedireccionandolo al panel de control, esto no es necesario si tenemos un decorador
            #if not request.user.is_staff:
                #return redirect(reverse_lazy('admin:login'))
            return super(StaffRequieredMixin, self).dispatch(request, *args, **kwargs)

# Create your views here.
class PageListView(ListView):
    model = Page  

class PageDetailView(DetailView):
    model = Page

#Los decoradores se pueden usar en cualquier clase para pedir una condicion.
@method_decorator(staff_member_required, name="dispatch")
class PageCreate(CreateView):
    model = Page 
    form_class = PageForm
    #Forma con medoto reverse_lazy
    success_url = reverse_lazy('pages:pages')

    #Forma normal
    #    def get_success_url(self):
            #success_url = reverse('pages:pages')
            #return success_url

@method_decorator(staff_member_required, name="dispatch")
class PageUpdate(UpdateView):
    model = Page 
    template_name_suffix = '_update_form'
    fields = ['title', 'content', 'order']
    def get_success_url(self):
        return reverse_lazy('pages:update', args=[self.object.id]) + '?ok'

class PageDelete(StaffRequieredMixin ,DeleteView):
    model = Page
    success_url = reverse_lazy('pages:pages')