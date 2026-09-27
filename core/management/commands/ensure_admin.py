import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Create (or update the password of) an admin superuser from "
        "DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_EMAIL / "
        "DJANGO_SUPERUSER_PASSWORD env vars. Safe to run on every deploy — "
        "does nothing if those vars are not set, and does not error if the "
        "user already exists."
    )

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')

        if not username or not password:
            self.stdout.write(
                'DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_PASSWORD not '
                'set — skipping admin user creation.'
            )
            return

        User = get_user_model()
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