from datetime import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models.signals import post_save
from django import forms
from profanity import *

from .models import *
import json
from .forms import DeleteMediaForm, LoginForm, MessageForm, AddMediaForm, KindergartenListForm, \
    CreateUserForm, ProfileForm, ChildForm, DeleteUserForm, DeletePrimaryUserForm, VideoForm, ScoreDataForm
from django.shortcuts import render, get_object_or_404


def index(request):
    context = {}
    if request.user is not None:
        context['user'] = request.user
    if request.user.is_authenticated:
        context['profile'] = UserProfile.objects.get(user=request.user)
        unread_messages_amount = Message.objects.filter(receiver=request.user, is_unread=True).count()
        if unread_messages_amount > 0:
            context['unread'] = unread_messages_amount
    if request.user.is_authenticated:
        message = Notification.objects.filter(receiver=request.user, seen=False)
        context['message'] = message
        for m in message:
            m.seen = True
            m.save()
    return render(request, 'Preschool_Play/index.html', context)


@login_required
def score_graphs(request):
    context = {'user': request.user}
    if request.method == 'POST':
        form = ScoreDataForm(request.POST)
        if form.is_valid():
            pair = form.cleaned_data['child_parent_pair']
            pair = pair.split(':')
            user_is_admin = False
            if request.user.profile.is_admin:
                children = list(Child.objects.all().order_by('parent__user__username', 'name'))
                user_is_admin = True
            elif request.user.profile.type == 'teacher':
                children = list(Child.objects.filter(teacher=request.user.profile).order_by('parent__user__username', 'name'))
            else:
                children = list(Child.objects.filter(parent=request.user.profile).order_by('name'))
            if pair[0] == 'All' and user_is_admin:
                context['scoreData'] = list(
                    Score.objects.values(d=ExtractDay('date'), m=ExtractMonth('date'), y=ExtractYear('date')).annotate(
                        Sum('amount')))
                context['child_name'] = 'All'
            else:
                parent_user_of_chosen_child = User.objects.get(username=pair[1])
                chosen_child = Child.objects.get(name=pair[0], parent=parent_user_of_chosen_child.profile)
                context['child_name'] = chosen_child.name
                if user_is_admin or request.user == parent_user_of_chosen_child or request.user.profile == chosen_child.teacher:
                    context['scoreData'] = list(
                        Score.objects.filter(child=chosen_child).values(d=ExtractDay('date'), m=ExtractMonth('date'), y=ExtractYear('date')).annotate(
                            Sum('amount')))
                else:
                    return render(request, 'Preschool_Play/error.html', {'message': 'Unauthorized user'})
            form = ScoreDataForm()
            pairs_choices = [(f'{c.name}:{c.parent.user.username}', f'P: {c.parent.user.username}. C: {c.name}.') for c in
                             children]
            if user_is_admin:
                pairs_choices.insert(0, ('All:All', 'All'))
            form.fields['child_parent_pair'] = forms.CharField(widget=forms.Select(choices=pairs_choices))
            form.fields['child_parent_pair'].initial = pairs_choices[0][0]
            context['form'] = form
            return render(request, 'Preschool_Play/score-graphs.html', context)
    else:
        user_is_admin = False
        if request.user.profile.is_admin:
            children = list(Child.objects.all().order_by('parent__user__username', 'name'))
            user_is_admin = True
        elif request.user.profile.type == 'teacher':
            children = list(Child.objects.filter(teacher=request.user.profile).order_by('parent__user__username', 'name'))
        else:
            children = list(Child.objects.filter(parent=request.user.profile).order_by('name'))
        if user_is_admin:
            context['scoreData'] = list(
                Score.objects.values(d=ExtractDay('date'), m=ExtractMonth('date'), y=ExtractYear('date')).annotate(
                    Sum('amount')))
        else:
            context['scoreData'] = list(
                Score.objects.filter(child=children[0]).values(d=ExtractDay('date'), m=ExtractMonth('date'),
                                                               y=ExtractYear('date')).annotate(
                    Sum('amount')))
        form = ScoreDataForm()
        pairs_choices = [(f'{c.name}:{c.parent.user.username}', f'P: {c.parent.user.username}. C: {c.name}.') for c in children]
        if user_is_admin:
            pairs_choices.insert(0, ('All:All', 'All'))
            context['child_name'] = 'All'
        else:
            context['child_name'] = children[0].name
        form.fields['child_parent_pair'] = forms.CharField(widget=forms.Select(choices=pairs_choices))
        form.fields['child_parent_pair'].initial = pairs_choices[0][0]
        context['form'] = form
        return render(request, 'Preschool_Play/score-graphs.html', context)
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
    users = []  # List of unsuspended users
    suspend_user = []  # lost of suspended users
    for user in user_profile:
        if user.suspension_time >= timezone.now():
            suspend_user.append(user)
        else:
            users.append(user)
    context = {'users': users, 'suspend_user': suspend_user}
    return render(request, 'Preschool_Play/show-suspend-user.html', context)


def filter_suspension(request):
    user_profile = UserProfile.objects.all()
    suspend_user = []  # list of suspended users
    for user in user_profile:
        if user.suspension_time >= timezone.now():
            suspend_user.append(user)
    suspend_user.sort(
        key=lambda r: r.suspension_time)  # filter by time left and keeping track of the time user has been suspended.
    context = {'suspend_user': suspend_user}
    return render(request, 'Preschool_Play/filter-suspension.html', context)


def add_media(request):
    if request.method == 'POST':
        form = AddMediaForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            path = form.cleaned_data['path']
            type = form.cleaned_data['type']
            media = Media.objects.all()
            for m in media:
                if m.name == name:
                    return HttpResponse("This name is already exist")
            new = Media.objects.create(name=name, path=path, type=type)
            new.save()
            return HttpResponseRedirect(reverse('Preschool_Play:index'))
    else:
        form = AddMediaForm()
        context = {'form': form}
    return render(request, 'Preschool_Play/add-media.html', context)


def delete_media(request):
    if request.method == 'POST':
        form = DeleteMediaForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            media_delete = Media.objects.filter(name=name).delete()
            return HttpResponseRedirect(reverse('Preschool_Play:index'))
    else:
        form = DeleteMediaForm()
    context = {'form': form}
    return render(request, 'Preschool_Play/delete-media.html', context)


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


def login_view(request):  # login view
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['user_name'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                user = request.user
                userprofile = UserProfile.objects.get(user=user)
                if userprofile.last_login.date() < timezone.now().date():
                    userprofile.daily_minutes = 0
                userprofile.last_login = timezone.now()
                userprofile.save()
                return HttpResponseRedirect(reverse('Preschool_Play:index'))
    else:
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'Preschool_Play/login.html', context)


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


@login_required
def inbox(request):
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
        message.is_unread = False
        message.save()
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
        return render(request, 'Preschool_Play/failure.html', {'error': error})
    return HttpResponseRedirect(reverse('Preschool_Play:inbox'))


def new_message(request, **kwargs):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    user_profile = UserProfile.objects.get(user=request.user)
    teachers_users = None
    parents_users = None
    if user_profile.type == 'teacher':
        teachers_users = User.objects.all()
        parents_users = User.objects.filter(profile__type='parent', profile__child__teacher=request.user,
                                            profile__is_admin=False)
    if user_profile.type == 'parent':
        teachers_users = User.objects.filter(profile__student__parent=request.user.profile)
        parents_users = User.objects.filter(profile__type='parent', child__teacher__in=list(teachers_users),
                                            profile__is_admin=False)
    if user_profile.is_admin:
        teachers_users = User.objects.filter(profile__type='teacher')
        parents_users = User.objects.filter(profile__is_admin=False)
    admin_users = User.objects.filter(profile__is_admin=True)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        request.user.reply = None
        if form.is_valid():
            sender = request.user
            receiver_name = form.cleaned_data['receiver']
            try:
                receiver = User.objects.get(username=receiver_name)
            except (TypeError, User.DoesNotExist):
                error = "Could not find user."
                render(request, 'Preschool_Play/failure.html', {'error': error})
            message_is_profane = False
            subject = form.cleaned_data['subject']
            subject_is_profane = has_profanity(subject)
            if subject_is_profane:
                subject = censor_profanity(subject)
            body = form.cleaned_data['body']
            body_is_profane = has_profanity(body)
            if body_is_profane:
                body = censor_profanity(body)
            message_is_profane = subject_is_profane or body_is_profane
            if message_is_profane and not user_profile.is_admin:
                if user_profile.profanity_warning:
                    s_time = datetime.now() + timedelta(hours=48)
                    user_profile.suspension_time = s_time
                    user_profile.save()
                    admin_notification = Notification(receiver=admin_users[0],
                                                      message=f'User {request.user.username} has been suspended for '
                                                              f'48 hours - until {s_time}.')
                    admin_notification.save()
                else:
                    user_notification = Notification(receiver=request.user,
                                                     message='WARNING: profanity is not allowed. '
                                                             'If you receive another warning in '
                                                             'the future hours you will be '
                                                             'suspended for 48 hours.')
                    user_notification.save()
                    admin_notification = Notification(receiver=admin_users[0],
                                                      message=f'User {request.user.username} has '
                                                              f'received a profanity warning.')
                    admin_notification.save()
                user_profile.profanity_warning = True
                user_profile.save()
            sent_date = timezone.now()
            message = Message(sender=sender, receiver=receiver, subject=subject, body=body, sent_date=sent_date)
            message.save()
            return HttpResponseRedirect(reverse('Preschool_Play:inbox'))
    else:
        form = MessageForm()
        if kwargs:
            if kwargs['reply']:
                form = MessageForm({'receiver': kwargs['reply']})
        all_users = list(teachers_users) + list(parents_users) + list(admin_users)
        form.fields['receiver'] = forms.CharField(
            widget=forms.Select(choices=[(u.username, u.username) for u in all_users]))
        form.fields['receiver'].initial = all_users[0].username
    return render(request, 'Preschool_Play/new-message.html', {
        'form': form, 'teachers': teachers_users, 'parents': parents_users, 'user': request.user, 'admins': admin_users
    })


def parent(request):
    user_parent = request.user
    user_profile = UserProfile.objects.get(user=user_parent)
    children = Child.objects.filter(parent=user_profile)
    context = {'children': children}
    return render(request, 'Preschool_Play/parent.html', context)


def child_area(request, name):
    user_parent = request.user
    user_profile = UserProfile.objects.get(user=user_parent)
    child = Child.objects.get(parent=user_profile, name=name)
    teacher = child.teacher
    videos = Video.objects.filter(create=teacher)
    context = {'child': child, 'videos': videos}
    return render(request, 'Preschool_Play/child-area.html', context)


def scoretable(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if user_profile.type == 'teacher':
        user_list = Score.objects.filter(child__teacher=user)
        context = {'user_list': user_list}
    return render(request, 'Preschool_Play/scoretable_teacher.html', context)


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


def sort_child_according_kindergarten(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if user_profile.is_admin:
        if request.method == 'POST':
            form = KindergartenListForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                temp = Child.objects.all()
                children = []
                for c in temp:
                    if str(c.kindergarten) == str(name):
                        children.append(c)
                context = {'name': name, 'children': children}
                return render(request, 'Preschool_Play/sort-child.html', context)
        else:
            form = KindergartenListForm()
            return render(request, 'Preschool_Play/show-kindergarten.html', {'form': form})
    else:
        return render(request, 'Preschool_Play/error.html', {'message': 'You don\'t have access'})


def new_user(request):
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            user = get_object_or_404(User, username=user_form.cleaned_data['username'])
            return HttpResponseRedirect(reverse('Preschool_Play:new-profile', args=[str(user.username)]))
    else:
        user_form = CreateUserForm()
        context = {'user_form': user_form}
        return render(request, 'Preschool_Play/new-user.html', context)


def new_profile(request, username):
    def attach_user(sender, **kwargs):
        userprofile = kwargs['instance']
        userprofile.user = user
        post_save.disconnect(attach_user, sender=UserProfile)
        userprofile.save()

    if request.method == 'POST':
        user = User.objects.get(username=username)
        form = ProfileForm(request.POST)
        if form.is_valid():
            post_save.connect(attach_user, sender=UserProfile)
            form.save()
            alert = Notification(receiver=User.objects.get(username='admin'),
                                 message=f'New user sign up to your system {user}')
            alert.save()
            return HttpResponseRedirect(reverse('Preschool_Play:index'))
    else:
        user = User.objects.get(username=username)
        form = ProfileForm()
    context = {'user': user, 'form': form}
    return render(request, 'Preschool_Play/new-profile.html', context)


@login_required
def add_child(request, **kwargs):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    teachers_users = None
    kindergarten = None
    teachers_users = UserProfile.objects.filter(type='teacher')
    kindergarten = Kindergarten.objects.all()
    if user_profile.type != 'parent':
        return render(request, 'Preschool_Play/error.html', {'message': 'You don\'t parent'})
    else:
        if request.method == 'POST':
            form = ChildForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name_child']
                teacher = form.cleaned_data['teacher']
                child_names = Child.objects.all()
                child_list = list(child_names)
                print(child_list)
                for n in child_list:
                    print(n)
                    if name == n.name:
                        return render(request, 'Preschool_Play/error.html',
                                      {'message': 'You try to add name exist'})
                kindergarten = form.cleaned_data['kindergarten']
                chosen_teacher = UserProfile.objects.filter(type='teacher')
                for t in chosen_teacher:
                    if str(t.user) == teacher:
                        finally_chosen_teacher = UserProfile.objects.get(user=t.user)
                        temp = UserProfile.objects.get(user=t.user)
                        chosen_kindergarten = Kindergarten.objects.get(teacher=temp)
                        if chosen_kindergarten.name != kindergarten:
                            return render(request, 'Preschool_Play/error.html',
                                          {'message': 'The teacher and the kindergarten are not suitable'})
                        new_child = Child(name=name, parent=user_profile, teacher=finally_chosen_teacher,
                                          kindergarten=chosen_kindergarten)
                        new_child.save()
                        alert = Notification(receiver=User.objects.get(username='admin'),
                                             message=f'{user} has registered his child to the system')
                        alert.save()
                        return HttpResponseRedirect(reverse('Preschool_Play:index'))
        else:
            form = ChildForm()
            all_users = list(teachers_users)
            all_kindergarten = list(kindergarten)
            form.fields['teacher'] = forms.CharField(
                widget=forms.Select(choices=[(u.user, u.user) for u in all_users]))
            form.fields['teacher'].initial = all_users[0].user
            form.fields['kindergarten'] = forms.CharField(
                widget=forms.Select(choices=[(n.name, n.name) for n in kindergarten]))
            form.fields['kindergarten'].initial = kindergarten[0].name
        return render(request, 'Preschool_Play/create-child.html', {
            'form': form, 'teachers': teachers_users
        })


def delete_user(request):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    child = Child.objects.filter(parent=user_profile)
    if request.method == 'POST':
        form = DeleteUserForm(child, request.POST)
        if form.is_valid():
            if "_make-unique" in request.POST:
                name = form.cleaned_data['child']
                password = form.cleaned_data['password']
                if user.check_password(password):
                    name.delete()
                else:
                    alert = Notification(receiver=user,
                                         message='The password is incorrect, you are passed to the home page')
                    alert.save()
                    return HttpResponseRedirect(reverse('Preschool_Play:index'))
        return HttpResponseRedirect(reverse('Preschool_Play:index'))
    else:
        form = DeleteUserForm(child)
    context = {'form': form}
    return render(request, 'Preschool_Play/delete-user.html', context)


def delete_primary_user(request):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = DeletePrimaryUserForm(request.POST)
        if form.is_valid():
            if "_make-unique" in request.POST:
                password = form.cleaned_data['password']
                if user.check_password(password):
                    user_profile.delete()
                    request.user.delete()
                else:
                    alert = Notification(receiver=user,
                                         message='The password is incorrect, you are passed to the home page')
                    alert.save()
                    return HttpResponseRedirect(reverse('Preschool_Play:index'))
        return HttpResponseRedirect(reverse('Preschool_Play:index'))
    else:
        form = DeletePrimaryUserForm()
    context = {'form': form, 'user_profile': user_profile}
    return render(request, 'Preschool_Play/delete-primary-user.html', context)


def show_video(request):
    # videos = Video.objects.all()
    # context = {
    #     'videos': videos,
    # }
    return render(request, 'Preschool_Play/videos.html')


def upload_video(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if user_profile.type != 'teacher':
        return render(request, 'Preschool_Play/error.html',
                      {'message': 'You are cant upload media because you are not a teacher !'})
    if request.method == 'POST':
        form = VideoForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            form.save()
            last = Video.objects.last()
            last.create = user_profile
            last.save()
            return HttpResponseRedirect(reverse('Preschool_Play:index'))
    else:
        form = VideoForm(request.POST or None, request.FILES or None)
        context = {'form': form}
    return render(request, 'Preschool_Play/upload.html', context)
