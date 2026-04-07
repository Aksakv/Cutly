

from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
     path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('<str:code>', RedirectURLView.as_view(), name='redirect'),
   
]