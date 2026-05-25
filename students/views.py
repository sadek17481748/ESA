"""
students/views.py
Students CRUD + bulk CSV import for school admin.
"""
import csv
import io

from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from audit.services import log_action
from core_app.mixins import TenantScopedQuerySetMixin
from core_app.permissions import IsSchoolAdminOnly, IsSchoolAdminOrReadOnlyStaff
from .models import StudentProfile
from .serializers import StudentProfileSerializer

User = get_user_model()


class StudentViewSet(TenantScopedQuerySetMixin, viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy', 'import_csv'):
            return [IsAuthenticated(), IsSchoolAdminOnly()]
        return [IsAuthenticated(), IsSchoolAdminOrReadOnlyStaff()]

    def get_queryset(self):
        return super().get_queryset().select_related('school', 'user')

    def perform_create(self, serializer):
        user = self.request.user
        school = user.school
        if user.role == 'super_admin':
            school = serializer.validated_data.get('school') or school
        instance = serializer.save(school=school)
        log_action(user=user, action='create', resource='StudentProfile',
                   resource_id=instance.pk, request=self.request)

    def perform_update(self, serializer):
        instance = serializer.save()
        log_action(user=self.request.user, action='update', resource='StudentProfile',
                   resource_id=instance.pk, request=self.request)

    @action(detail=False, methods=['post'])
    def import_csv(self, request):
        """
        POST multipart file field `file` — columns: first_name,last_name,year_group,admission_number
        """
        upload = request.FILES.get('file')
        if not upload:
            return Response({'file': 'CSV file required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not upload.name.lower().endswith('.csv'):
            return Response({'file': 'Must be a .csv file.'}, status=status.HTTP_400_BAD_REQUEST)

        school = request.user.school
        created = 0
        errors = []
        text = upload.read().decode('utf-8-sig')
        reader = csv.DictReader(io.StringIO(text))
        required = {'first_name', 'last_name'}
        if not required.issubset(set(reader.fieldnames or [])):
            return Response(
                {'file': 'CSV needs columns: first_name, last_name (optional: year_group, admission_number)'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        for i, row in enumerate(reader, start=2):
            fn = (row.get('first_name') or '').strip()
            ln = (row.get('last_name') or '').strip()
            if not fn or not ln:
                errors.append(f'Row {i}: missing name')
                continue
            adm = (row.get('admission_number') or '').strip()
            yg = (row.get('year_group') or '').strip()
            if adm and StudentProfile.objects.filter(school=school, admission_number=adm).exists():
                errors.append(f'Row {i}: duplicate admission_number {adm}')
                continue
            StudentProfile.objects.create(
                school=school,
                first_name=fn,
                last_name=ln,
                year_group=yg,
                admission_number=adm,
            )
            created += 1
        return Response({'created': created, 'errors': errors}, status=status.HTTP_201_CREATED)


# ---------------------------------------------------------------------------
# BUGGY CODE (commented out) — CSV import ignored school and wrote to wrong tenant
# ---------------------------------------------------------------------------
# StudentProfile.objects.create(
#     first_name=fn, last_name=ln, year_group=yg, admission_number=adm,
# )

# ---------------------------------------------------------------------------
# BUGGY CODE (commented out) — teacher saw students from every school
# ---------------------------------------------------------------------------
# class StudentViewSet(TenantScopedQuerySetMixin, viewsets.ModelViewSet):
#     def get_queryset(self):
#         return StudentProfile.objects.all()
