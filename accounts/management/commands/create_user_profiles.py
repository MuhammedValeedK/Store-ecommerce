from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Create user profiles for users that do not have one'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            UserProfile.objects.get_or_create(user=user)
        self.stdout.write('Created missing user profiles')