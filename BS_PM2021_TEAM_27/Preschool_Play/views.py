from django.shortcuts import render

from .models import *


def index(request):
    context = {}
    if request.user is not None:
        context['user'] = request.user
    if request.user.is_authenticated:
        context['profile'] = UserProfile.objects.get(user=request.user)
    return render(request, 'Preschool_Play/index.html', context)
