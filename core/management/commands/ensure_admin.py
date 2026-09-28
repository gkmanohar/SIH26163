import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

DEMO_USERNAME = 'demo'
DEMO_PASSWORD = 'Demo@1234'


class Command(BaseCommand):
    help = (
        "Create the public demo user (no admin rights) and, if the "
        "DJANGO_SUPERUSER_* env vars are set, create/update the private "
        "admin superuser. Safe to run on every deploy."
    )

    def handle(self, *args, **options):
        User = get_user_model()

        # Public demo account: not staff, not superuser -> cannot open /admin/
        demo, _ = User.objects.get_or_create(username=DEMO_USERNAME)
        demo.is_staff = False
        demo.is_superuser = False
        demo.set_password(DEMO_PASSWORD)
        demo.save()
        self.stdout.write(self.style.SUCCESS(f'Demo user "{DEMO_USERNAME}" ready.'))

        # Private admin account (from env vars)
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')

        if not username or not password:
            self.stdout.write(
                'DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_PASSWORD not '
                'set — skipping admin user creation.'
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_staff': True, 'is_superuser': True},
        )
        user.email = email or user.email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created superuser "{username}".'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated existing superuser "{username}".'))