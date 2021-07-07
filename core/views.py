from django.shortcuts import render
from django.views.generic.base import TemplateView

class HomePageView(TemplateView):
    template_name = 'core/home.html'
#   def get_context_data(self, **kwargs):
#       context = super().get_context_data(**kwargs)
#      context['title'] = "Mi superweb playground"
#      return context
    def get(self, request, *arg, **kwargs):
        return render(request, self.template_name, {'title':"Mi super Web playground"})
    
class SamplePageView(TemplateView):
  template_name = 'core/sample.html'

