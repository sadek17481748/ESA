"""
Post-deploy smoke check — demo accounts, URLs, and seed data.
Run: python manage.py verify_deploy
"""
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.test import Client, override_settings
from django.urls import reverse

User = get_user_model()

CHECKS = (
    ('test_parent', 'test1234', 'messaging:inbox'),
    ('test_student', 'test1234', 'pages:worksheets'),
    ('mr_mohammed', 'teacher1234', 'messaging:inbox'),
    ('schooladmin', 'admin1234', 'lms:hub'),
    ('super', 'super1234', 'messaging:inbox'),
)


class Command(BaseCommand):
    help = 'Smoke-test demo logins and key portal URLs after deploy'

    def handle(self, *args, **options):
        call_command('ensure_platform_seed')
        client = Client()
        passed = 0
        failed = 0

        with override_settings(ALLOWED_HOSTS=['testserver', 'localhost', '127.0.0.1', '.herokuapp.com']):
            for username, password, url_name in CHECKS:
                user = User.objects.filter(username=username).first()
                if not user:
                    self.stdout.write(self.style.ERROR(f'FAIL — user missing: {username}'))
                    failed += 1
                    continue
                if not client.login(username=username, password=password):
                    self.stdout.write(self.style.ERROR(f'FAIL — login: {username}'))
                    failed += 1
                    continue
                response = client.get(reverse(url_name))
                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS(f'OK — {username} → {url_name}'))
                    passed += 1
                else:
                    self.stdout.write(self.style.ERROR(
                        f'FAIL — {username} → {url_name} ({response.status_code})',
                    ))
                    failed += 1

            if client.login(username='schooladmin', password='admin1234'):
                r = client.get(reverse('messaging:student_search'), {'q': 'Amina'})
                if r.status_code == 200 and b'Amina' in r.content:
                    self.stdout.write(self.style.SUCCESS('OK — student search'))
                    passed += 1
                else:
                    self.stdout.write(self.style.ERROR('FAIL — student search'))
                    failed += 1

        self.stdout.write('')
        if failed:
            self.stdout.write(self.style.ERROR(f'Verify deploy: {passed} passed, {failed} failed'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Verify deploy: all {passed} checks passed'))
