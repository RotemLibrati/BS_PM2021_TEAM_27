from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from Preschool_Play.models import *
import random


class Command(BaseCommand):
    help = 'Populate db'

    def handle(self, *args, **options):
        parent1 = self.create_parent1()
        teacher1 = self.create_teacher1()
        kindergarten = Kindergarten(name='Flower', teacher=teacher1.profile)
        kindergarten.save()
        child1 = Child(name='Dani', parent=parent1.profile,
                       teacher=teacher1.profile, auth=True, kindergarten=kindergarten)
        child1.save()
        child2 = Child(name='Ron', parent=parent1.profile,
                       teacher=teacher1.profile, auth=True, kindergarten=kindergarten)
        child2.save()
        for _ in range(random.randint(3, 6)):
            d = datetime.today() - timedelta(days=random.randint(1, 30))
            d2 = datetime.today() - timedelta(days=random.randint(1, 30))
            Score(child=child1, amount=random.randint(1, 30), date=d).save()
            Score(child=child2, amount=random.randint(1, 30), date=d2).save()

    @staticmethod
    def create_parent1():
        parent_user = User(username='parent1', first_name='John',
                           last_name='Smith')
        parent_user.set_password('qwerty246')
        parent_user.save()
        parent_profile = UserProfile(user=parent_user, address='Beersheba',
                                     age=30, type='parent', is_admin=False,
                                     auth=True)
        parent_profile.save()
        return parent_user

    @staticmethod
    def create_teacher1():
        teacher_user = User(username='teacher1', first_name='Orna',
                            last_name='Katz')
        teacher_user.set_password('qwerty246')
        teacher_user.save()
        teacher_profile = UserProfile(user=teacher_user, address='Beersheba',
                                      age=25, type='teacher', is_admin=False,
                                      auth=True)
        teacher_profile.save()
        return teacher_user
