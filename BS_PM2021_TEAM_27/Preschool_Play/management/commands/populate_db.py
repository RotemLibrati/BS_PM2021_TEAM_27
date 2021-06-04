from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from Preschool_Play.models import *
import random


class Command(BaseCommand):
    help = 'Populate db'

    def handle(self, *args, **options):
        admin_user = User.objects.create_user('admin2', 'admin@test.com')
        admin_user.set_password('qwerty246')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        admin_profile = UserProfile(user=admin_user, is_admin=True)
        admin_profile.save()

        teacher_users = []
        kindergartens = []
        parents = []
        children = []
        for t in range(random.randint(3, 6)):
            u = User(username=f'Teacher{t}')
            u.set_password('qwerty246')
            u.save()
            teacher_users.append(u)
            UserProfile(user=u, type='teacher', auth=True).save()
            k = Kindergarten(name=f'Kindergarten{t}', teacher=u.profile)
            k.save()
            kindergartens.append(k)

        for x in range(random.randint(6, 10)):
            p = User(username=f'parent{x}')
            p.set_password('qwerty246')
            p.save()
            parents.append(p)
            UserProfile(user=p, type='parent', auth=True).save()
            for c in range(random.randint(1, 3)):
                r = random.randint(0, len(teacher_users) - 1)
                rand_teacher = teacher_users[r]
                child = Child(name=f'child{x}.{c}', parent=p.profile,
                              teacher=rand_teacher.profile, kindergarten=kindergartens[r], auth=True)
                child.save()
                children.append(child)
        for ch in children:
            d = datetime.today() - timedelta(days=random.randint(1, 30))
            Score(child=ch, amount=random.randint(1, 30), date=d).save()
    #
    #     parent1 = self.create_parent1()
    #     teacher1 = self.create_teacher1()
    #     kindergarten = Kindergarten(name='Flower', teacher=teacher1.profile)
    #     kindergarten.save()
    #     for i in range(random.randint(5, 20)):
    #         Child(name=f'child{i},')
    #     child1 = Child(name='Dani', parent=parent1.profile,
    #                    teacher=teacher1.profile, auth=True, kindergarten=kindergarten)
    #     child1.save()
    #     child2 = Child(name='Ron', parent=parent1.profile,
    #                    teacher=teacher1.profile, auth=True, kindergarten=kindergarten)
    #     child2.save()
    #     for _ in range(random.randint(3, 6)):
    #         d = datetime.today() - timedelta(days=random.randint(1, 30))
    #         d2 = datetime.today() - timedelta(days=random.randint(1, 30))
    #         Score(child=child1, amount=random.randint(1, 30), date=d).save()
    #         Score(child=child2, amount=random.randint(1, 30), date=d2).save()
    #
    # @staticmethod
    # def create_parent1():
    #     parent_user = User(username='parent1', first_name='John',
    #                        last_name='Smith')
    #     parent_user.set_password('qwerty246')
    #     parent_user.save()
    #     parent_profile = UserProfile(user=parent_user, address='Beersheba',
    #                                  age=30, type='parent', is_admin=False,
    #                                  auth=True)
    #     parent_profile.save()
    #     return parent_user
    #
    # @staticmethod
    # def create_teacher1():
    #     teacher_user = User(username='teacher1', first_name='Orna',
    #                         last_name='Katz')
    #     teacher_user.set_password('qwerty246')
    #     teacher_user.save()
    #     teacher_profile = UserProfile(user=teacher_user, address='Beersheba',
    #                                   age=25, type='teacher', is_admin=False,
    #                                   auth=True)
    #     teacher_profile.save()
    #     return teacher_user
