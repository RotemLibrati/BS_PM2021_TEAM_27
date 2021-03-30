from django.urls import path

from . import views

app_name = 'Preschool_Play'

urlpatterns = [
    path('', views.index, name='index'),
    path('admingraphs', views.admin_graphs, name='admingraphs'),
    path('parentpage', views.parent_page, name='parentpage'),
]