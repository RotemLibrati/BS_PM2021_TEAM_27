from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db.models import Avg, Max, Min
from Preschool_Play.models import *
import random


class Command(BaseCommand):
    help = 'Average score improvement over time'

    def handle(self, *args, **options):
        children = Child.objects.all()
        score_diffs = []
        for c in children:
            first_score_amount = Score.objects.filter(child=c).order_by('date')[0].amount
            avg_score_amount = Score.objects.filter(child=c).aggregate(Avg('amount'))['amount__avg']
            score_diffs.append(avg_score_amount - first_score_amount)
        print(f'Number of children: {len(children)}')
        print(f'Average score improvement over time: {sum(score_diffs) / len(score_diffs)}')
