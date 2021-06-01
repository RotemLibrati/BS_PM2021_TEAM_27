from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from Preschool_Play.models import *
from django.conf import settings
from django.core.mail import send_mail
import random


class Command(BaseCommand):
    help = 'Send an email of the tests report'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--subject', type=str, help='Subject of the email')
        parser.add_argument('-b', '--body', type=str, help='Body of the email')

    def handle(self, *args, **options):
        subject = "no subject"
        if options['subject']:
            subject = options['subject']
        body = "no body"
        if options['body']:
            body = options['body']

        send_mail(
            subject,
            body,
            'team27@django.com',
            ['eilonco@ac.sce.ac.il'],
            fail_silently=False,
        )
