from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db.models import Avg, Max, Min
from Preschool_Play.models import *
import random


class Command(BaseCommand):
    help = 'Average number of messages per user'

    def handle(self, *args, **options):
        messages_amount = Message.objects.all().count()
        users_amount = User.objects.all().count()
        print(f'Number of users: {users_amount}')
        print(f'Average number of messages per user: {messages_amount/users_amount}')
