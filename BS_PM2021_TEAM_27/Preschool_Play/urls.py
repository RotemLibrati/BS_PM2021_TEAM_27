from django.urls import path

from . import views

app_name = 'Preschool_Play'

urlpatterns = [
    path('', views.index, name='index'),
    path('admingraphs', views.admin_graphs, name='admingraphs'),
    # path('parentpage', views.parent_page, name='parentpage'),
    path('show-suspend-user', views.show_suspend_user, name='show-suspend-user'),
    path('filter-suspension', views.filter_suspension, name='filter-suspension'),
    path('show-users', views.show_users, name='show-users'),
    path('search-user', views.search_user, name='search-user'),
    path('add-media', views.add_media, name='add-media'),
    path('delete-media', views.delete_media, name='delete-media'),
    path('login', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
]