from django.urls import path

from . import views

app_name = 'Preschool_Play'

urlpatterns = [
    path('', views.index, name='index'),
    path('admingraphs', views.admin_graphs, name='admingraphs'),
    path('show-suspend-user', views.show_suspend_user, name='show-suspend-user'),
]