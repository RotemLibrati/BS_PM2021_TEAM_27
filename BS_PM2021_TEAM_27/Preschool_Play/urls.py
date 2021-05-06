from django.urls import path

from . import views

app_name = 'Preschool_Play'

urlpatterns = [
    path('', views.index, name='index'),
    path('scoregraphs', views.score_graphs, name='scoregraphs'),
    path('scoregraphs/<str:name>', views.score_graphs, name='scoregraphs'),
    path('show-suspend-user', views.show_suspend_user, name='show-suspend-user'),
    path('filter-suspension', views.filter_suspension, name='filter-suspension'),
    path('show-users', views.show_users, name='show-users'),
    path('search-user', views.search_user, name='search-user'),
    path('add-media', views.add_media, name='add-media'),
    path('delete-media', views.delete_media, name='delete-media'),
    path('login', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/<int:message_id>/', views.view_message, name='view-message'),
    path('inbox/delete/<int:message_id>/', views.delete_message, name='delete-message'),
    path('inbox/new-message/', views.new_message, name='new-message'),
    path('inbox/new-message/<str:reply>', views.new_message, name='new-message'),
    path('parent', views.parent, name='parent'),
    path('suspension-teacher', views.suspension_for_teacher, name='suspension_teacher'),
    path('message-board/', views.message_board, name='message-board'),
    path('message-board/<int:delete_message>', views.message_board, name='message-board'),
    path('scoretable_teacher', views.scoretable, name='scoretable_teacher'),
    path('sort-child', views.sort_child_according_kindergarten, name='sort-child'),
    path('show-kindergarten', views.sort_child_according_kindergarten, name='show-kindergarten'),
    path('<str:username>/new-profile/', views.new_profile, name='new-profile'),
    path('new-user', views.new_user, name='new-user'),
    path('my-students', views.my_students, name='my-students'),
    path('find-student-of-teacher', views.find_student_of_teacher, name='find-student-of-teacher'),
    path('find-student-of-teacher/<str:teacher_fname>/<str:teacher_lname>', views.find_student_of_teacher, name='find-student-of-teacher'),
    path('create-child', views.add_child, name='create-child'),
    path('delete-user', views.delete_user, name='delete-user'),
    path('delete-primary-user', views.delete_primary_user, name='delete-primary-user'),
    path('FAQ', views.FAQ, name='FAQ'),
    path('view-note/<int:note_id>/', views.view_note, name='view-note'),
    path('notes', views.notes, name='notes'),
    path('new-note', views.new_note, name='new-note'),
]

