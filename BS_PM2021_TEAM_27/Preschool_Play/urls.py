from django.urls import path

from . import views

app_name = 'Preschool_Play'

urlpatterns = [
    path('', views.index, name='index'),
]