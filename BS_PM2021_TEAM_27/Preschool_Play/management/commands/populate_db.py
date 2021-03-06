from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from Preschool_Play.models import *
import random


class Command(BaseCommand):
    help = 'Populate db'

    def handle(self, *args, **options):
        admin_user = User.objects.create_user('admin', 'admin@test.com')
        admin_user.set_password('1234')
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
            for m in range(random.randint(0, 3)):
                Message(sender=p, receiver=random.choice(parents + teacher_users), subject=f'm{x}.{m}',
                        body=f'Hello').save()
            for c in range(random.randint(1, 3)):
                r = random.randint(0, len(teacher_users) - 1)
                rand_teacher = teacher_users[r]
                child = Child(name=f'child{x}.{c}', parent=p.profile,
                              teacher=rand_teacher.profile, kindergarten=kindergartens[r], auth=True)
                child.save()
                children.append(child)
        for ch in children:
            for _ in range(random.randint(1, 5)):
                d = datetime.today() - timedelta(days=random.randint(1, 30))
                Score(child=ch, amount=random.randint(1, 30), date=d).save()
        FAQs = []
        faq = FAQ(question='Can I write masseges for the theacher of my child?',
                  answer='Yes. go to the main menu and press on Inbox, and follow the instructions.')
        faq.save()
        FAQs.append(faq)

        faq = FAQ(question='How can I see messages from the teacher?',
                  answer='Go to the main menu and press on Inbox, and follow the instructions.')
        faq.save()
        FAQs.append(faq)

        faq = FAQ(question='How do I get to my childs personal area?', answer='Go to the main menu and press on My Children.')
        faq.save()
        FAQs.append(faq)

        faq = FAQ(question='How do I add my child to the system?',
                  answer='Go to the main menu and press on Create Child, and follow the instructions.')
        faq.save()
        FAQs.append(faq)

        faq = FAQ(question='Is it possible to open a personal area for my sons friend?',
                  answer='No. The system is open only for the Registered kindergartens. If the friend is in the same kindergarten he can open a personal area by his mother.')
        faq.save()
        FAQs.append(faq)

