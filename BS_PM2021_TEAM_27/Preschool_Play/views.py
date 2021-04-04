from datetime import timezone

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import *
import json
from .forms import AddMediaForm, DeleteMediaForm




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

@login_required
def parent_page(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.type == 'parent':
            context = {}
            context['user'] = request.user
            context['profile'] = user_profile
            context['children'] = list(Child.objects.filter(parent=request.user))
            return render(request, 'Preschool_Play/parent-page.html', context)
    except (UserProfile.DoesNotExist):
        pass
    return render(request, 'Preschool_Play/error.html', {'message': 'Unauthorized user'})
