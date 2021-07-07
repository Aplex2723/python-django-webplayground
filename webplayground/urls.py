"""webplayground URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pages.urls import pages_patterns
from profiles.urls import profiles_patterns
from messenger.urls import messenger_patterns
from django.conf import settings

urlpatterns = [
        path('admin/', admin.site.urls),
        path('pages/', include(pages_patterns)),
        path('', include('core.urls')),

        #Paths de auth
        path('accounts/', include('django.contrib.auth.urls')),
        path('accounts/', include('registration.urls')),

        path('profiles/', include(profiles_patterns)),

        #Paths de messenger
        path('messenger/', include(messenger_patterns)),
]

#Haciendo posible poder guardar imagenes localmente, es necesario tener el mode DEBUG en True en Settings.py
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        