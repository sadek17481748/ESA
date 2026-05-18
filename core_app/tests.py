"""
core_app/tests.py
TenantMiddleware sets request.tenant_school from the logged-in user.
"""
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from core_app.middleware import TenantMiddleware
from schools.models import School

User = get_user_model()


class TenantMiddlewareTests(TestCase):
    def test_sets_tenant_school_on_request(self):
        school = School.objects.create(name='Test')
        user = User.objects.create_user(
            username='u1', password='x', role='teacher', school=school,
        )
        user.backend = 'django.contrib.auth.backends.ModelBackend'

        factory = RequestFactory()
        request = factory.get('/')
        request.user = user

        def get_response(req):
            return req

        middleware = TenantMiddleware(get_response)
        middleware(request)
        self.assertEqual(request.tenant_school, school)
