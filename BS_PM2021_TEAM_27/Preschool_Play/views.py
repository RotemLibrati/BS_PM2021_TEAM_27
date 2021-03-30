from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import json


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
