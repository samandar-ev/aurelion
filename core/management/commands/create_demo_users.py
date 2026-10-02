from django.core.management.base import BaseCommand

from core.models import Location, User

DEMO_USERS = [
    ('owner', User.Role.OWNER),
    ('cashier', User.Role.CASHIER),
    ('associate', User.Role.SALES_ASSOCIATE),
]


class Command(BaseCommand):
    help = 'Create one demo account per role and a default store location (local testing only).'

    def add_arguments(self, parser):
        parser.add_argument('--password', default='aurelion-demo', help='Password for all demo accounts.')

    def handle(self, *args, password, **options):
        Location.objects.get_or_create(code='MAIN', defaults={'name': 'Flagship Store', 'address': 'N/A'})
        for username, role in DEMO_USERS:
            user, created = User.objects.get_or_create(username=username, defaults={'role': role})
            user.role = role
            user.is_staff = user.is_superuser = role == User.Role.OWNER
            user.set_password(password)
            user.save()
            self.stdout.write(f"{'Created' if created else 'Updated'} {username} ({role.label})")
        self.stdout.write(self.style.SUCCESS(f'Demo users ready. Password: {password}'))
