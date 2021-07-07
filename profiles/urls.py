from django.urls import path
from profiles.views import ProfilesListView, ProfilesDetailView

profiles_patterns = ([
    path('', ProfilesListView.as_view(), name='list'),
    path('<username>/', ProfilesDetailView.as_view(), name='detail'),
], "profiles")
