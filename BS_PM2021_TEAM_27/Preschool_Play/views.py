from datetime import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


from .models import *
import json
# from .forms import DeleteMediaForm, LoginForm, MessageForm, AddMediaForm


def index(request):
    context = {}
    if request.user is not None:
        context['user'] = request.user
    if request.user.is_authenticated:
        context['profile'] = UserProfile.objects.get(user=request.user)
    return render(request, 'Preschool_Play/index.html', context)


@login_required
def admin_graphs(request):
    context = {}
    context['user'] = request.user
    if request.user.is_authenticated:
        context['profile'] = UserProfile.objects.get(user=request.user)
    if context['profile'].is_admin:
        context['scoreData'] = list(Score.objects.values(d=ExtractDay('date'), m=ExtractMonth('date'), y=ExtractYear('date')).annotate(
            Sum('amount')))
        return render(request, 'Preschool_Play/admin-graphs.html', context)
    return render(request, 'Preschool_Play/error.html', {'message': 'Unauthorized user'})


@login_required
def send_game_info(request):
    data = request.body.decode('utf-8')
    received_json_data = json.loads(data)
    child_name = received_json_data['child']
    _amount = received_json_data['amount']
    _comment = received_json_data['comment']
    try:
        connected_user = request.user
        child = Child.objects.get(name=child_name)
        if child.parent == connected_user:
            sc = Score(child=child, amount=_amount, comment=_comment)
            sc.save()
            return HttpResponse("Score saved")
    except (Child.DoesNotExist):
        pass
    return HttpResponse('Failed')


def show_suspend_user(request):
    user_profile = UserProfile.objects.all()
    users = [] # List of unsuspended users
    suspend_user = [] # lost of suspended users
    for user in user_profile:
        if user.suspension_time >= timezone.now():
            suspend_user.append(user)
        else:
            users.append(user)
    context = {'users': users, 'suspend_user': suspend_user}
    return render(request, 'Preschool_Play/show-suspend-user.html', context)


def filter_suspension(request):
    user_profile = UserProfile.objects.all()
    suspend_user = [] # list of suspended users
    for user in user_profile:
        if user.suspension_time >= timezone.now():
            suspend_user.append(user)
    suspend_user.sort(key=lambda r: r.suspension_time) # filter by time left and keeping track of the time user has been suspended.
    context = {'suspend_user': suspend_user}
    return render(request, 'Preschool_Play/filter-suspension.html', context)


# def add_media(request):
#     if request.method == 'POST':
#         form = AddMediaForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             path = form.cleaned_data['path']
#             type = form.cleaned_data['type']
#             media = Media.objects.all()
#             for m in media:
#                 if m.name == name:
#                     return HttpResponse("This name is already exist")
#             new = Media.objects.create(name=name, path=path, type=type)
#             new.save()
#             return HttpResponseRedirect(reverse('Preschool_Play:index'))
#     else:
#         form = AddMediaForm()
#         context = {'form': form}
#     return render(request, 'Preschool_Play/add-media.html', context)


# def delete_media(request):
#     if request.method == 'POST':
#         form = DeleteMediaForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             media_delete = Media.objects.filter(name=name).delete()
#             return HttpResponseRedirect(reverse('Preschool_Play:index'))
#     else:
#         form = DeleteMediaForm()
#     context = {'form': form}
#     return render(request, 'Preschool_Play/delete-media.html', context)


def show_users(request):
    user_profile = UserProfile.objects.all()
    context = {'up': user_profile}
    return render(request, 'Preschool_Play/show-users.html', context)


def search_user(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
    if user_profile.is_admin:
        unconfirmed_users = list(UserProfile.objects.filter(auth=False))
        context = {}
        for x in unconfirmed_users:
            if x.user.first_name == fname and x.user.last_name == lname:
                context['profile'] = x
                return render(request, 'Preschool_Play/search-user.html', context)
    return render(request, 'Preschool_Play/error.html', {'message': 'unauthorized'})


# def login_view(request):  # login view
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             user = authenticate(username=form.cleaned_data['user_name'], password=form.cleaned_data['password'])
#             if user is not None:
#                 login(request, user)
#                 user = request.user
#                 userprofile = UserProfile.objects.get(user=user)
#                 if userprofile.last_login.date() < timezone.now().date():
#                     userprofile.daily_minutes = 0
#                 userprofile.last_login = timezone.now()
#                 userprofile.save()
#                 return HttpResponseRedirect(reverse('Preschool_Play:index'))
#     else:
#         form = LoginForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'Preschool_Play/login.html', context)

@login_required
def logout(request):  # logout view
    userprofile = UserProfile.objects.get(user=request.user)
    td = timezone.now() - userprofile.last_login
    userprofile.total_minutes += (td.total_seconds() / 60)
    userprofile.save()
    request.session.flush()

    if hasattr(request, 'user'):
        request.user = AnonymousUser()
    return HttpResponseRedirect(reverse('Preschool_Play:index'))


def inbox(request):  # TODO: fix links menu in template
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    current_user = request.user
    messages_received = list(
        Message.objects.filter(receiver=current_user, deleted_by_receiver=False).order_by('-sent_date'))
    messages_sent = list(Message.objects.filter(sender=current_user, deleted_by_sender=False).order_by('-sent_date'))
    return render(request, 'Preschool_Play/inbox.html', {'user': current_user,
                                                       'messages_received': messages_received,
                                                       'messages_sent': messages_sent
                                                       })


def view_message(request, message_id):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    try:
        message = Message.objects.get(id=message_id)
    except (TypeError, Message.DoesNotExist):
        error = "Message getting failed."
        return render(request, 'Preschool_Play/failure.html', {'error': error})
    return render(request, 'Preschool_Play/message.html', {'user': request.user,
                                                         'message': message,
                                                         })


def delete_message(request, message_id):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    try:
        message = Message.objects.get(id=message_id)
        if request.user == message.receiver:
            message.deleted_by_receiver = True
        if request.user == message.sender:
            message.deleted_by_sender = True

        message.save()

        if message.deleted_by_sender and message.deleted_by_receiver:
            message.delete()
    except (TypeError, Message.DoesNotExist):
        error = "Message deletion failed."
        render(request, 'Preschool_Play/failure.html', {'error': error})
    return HttpResponseRedirect(reverse('Preschool_Play:inbox'))


# def new_message(request, **kwargs):
#     if request.user is None or not request.user.is_authenticated:
#         return HttpResponse("Not logged in")
#     user_profile = UserProfile.objects.get(user=request.user)
#     user_list = User.objects.all()
#     profile_list = UserProfile.objects.all()
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         request.user.reply = None
#         if form.is_valid():
#             sender = request.user
#             receiver_name = form.cleaned_data['receiver']
#             try:
#                 receiver = User.objects.get(username=receiver_name)
#             except (TypeError, User.DoesNotExist):
#                 error = "Could not find user."
#                 render(request, 'Preschool_Play/failure.html', {'error': error})
#             subject = form.cleaned_data['subject']
#             body = form.cleaned_data['body']
#             sent_date = timezone.now()
#             message = Message(sender=sender, receiver=receiver, subject=subject, body=body, sent_date=sent_date)
#             message.save()
#             return HttpResponseRedirect(reverse('Preschool_Play:inbox'))
#             return HttpResponseRedirect(reverse('Preschool_Play:success-message'))
#     else:
#         form = MessageForm()
#         if kwargs:
#             if kwargs['reply']:
#                 form = MessageForm({'receiver': kwargs['reply']})
#     return render(request, 'Preschool_Play/new-message.html', {
#         'form': form, 'users': user_list, 'user': request.user, 'user_profile': user_profile, 'profiles': profile_list
#     })


def parent(request):
    children = Child.objects.filter(parent=request.user)
    context = {'children': children}
    return render(request, 'Preschool_Play/parent.html', context)


def suspension_for_teacher(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if user_profile.type != 'teacher':
        return HttpResponse("You are not teacher !!")

    child = Child.objects.filter(teacher=user)
    suspended_child = []
    for c in child:
        if c.suspension_time >= timezone.now():
            suspended_child.append(c)
    context = {'user_profile': user_profile, 'suspended_child': suspended_child}
    return render(request, 'Preschool_Play/suspension-teacher.html', context)


@login_required
def message_board(request, **kwargs):
    context = {}
    usrprof = UserProfile.objects.get(user=request.user)
    context['is_teacher'] = False
    if usrprof.type == 'teacher':
        context['is_teacher'] = True
        if kwargs:
            Message.objects.get(id=kwargs['delete_message']).delete()
    context['messages'] = Message.objects.filter(is_public=True)
    return render(request, 'Preschool_Play/message-board.html', context)


