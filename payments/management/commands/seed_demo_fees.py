"""
Management command: seed_demo_fees
Demo school, parent_demo user, and two sample fees for Stripe checkout testing.
Run: python manage.py seed_demo_fees
"""
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from schools.models import School
from payments.models import FeeItem

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates demo school, parent user, and sample fees for stripe testing'

    def handle(self, *args, **options):
        school, _ = School.objects.get_or_create(
            name='Al-Noor Academy',
            defaults={
                'contact_email': 'admin@alnoor.example',
                'subscription_tier': School.TIER_STANDARD,
            },
        )

        parent, created = User.objects.get_or_create(
            username='parent_demo',
            defaults={
                'email': 'parent@esa.demo',
                'role': 'parent',
                'school': school,
            },
        )
        if created:
            parent.set_password('demo1234')
            parent.save()

        if not FeeItem.objects.filter(parent=parent).exists():
            FeeItem.objects.create(
                school=school,
                parent=parent,
                child_name='Ahmed Hussain',
                title='Term 3 tuition',
                amount_pence=25000,
                due_date=date.today() + timedelta(days=14),
                status=FeeItem.STATUS_OUTSTANDING,
            )
            FeeItem.objects.create(
                school=school,
                parent=parent,
                child_name='Ahmed Hussain',
                title='School trip',
                amount_pence=3500,
                due_date=date.today() - timedelta(days=3),
                status=FeeItem.STATUS_OVERDUE,
            )

        self.stdout.write(self.style.SUCCESS(
            'Demo ready. Log in as parent_demo / demo1234 then open /payments/'
        ))
