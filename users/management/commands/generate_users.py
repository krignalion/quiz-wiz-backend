from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from datetime import timedelta
from random import randint

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Generate random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']

        for i in range(total):
            username = fake.user_name()
            email = fake.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            password = fake.password()
            created_at = fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None) + timedelta(days=randint(1, 30))

            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )

            user.created_at = created_at
            user.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully created user: {username}'))