"""
core/urls.py
Root URL config — admin, JWT auth, REST APIs, parent payments, session auth.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core_app.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    # JWT — used by API clients and Postman
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/accounts/', include('accounts.urls')),
    path('api/schools/', include('schools.urls')),
    path('api/students/', include('students.urls')),
    path('api/teachers/', include('teachers.urls')),
    path('api/classes/', include('academics.urls')),
    path('api/parents/', include('parents.urls')),
    path('api/subjects/', include('subjects.urls')),
    path('api/timetable/', include('timetable.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/homework/', include('homework.urls')),
    path('api/notifications/', include('notifications.urls')),
    # parent fee pages (session login)
    path('payments/', include('payments.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # shared wireframe stylesheet (login, payments, home)
    path('css/<path:path>', serve, {'document_root': settings.BASE_DIR / 'css'}),
]

# dev only — uploaded media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ---------------------------------------------------------------------------
# BUGGY CODE (commented out) — uploaded files 404 in local dev (no media route)
# ---------------------------------------------------------------------------
# if settings.DEBUG:
#     urlpatterns += [
#         path('css/<path:path>', serve, {'document_root': settings.BASE_DIR / 'css'}),
#     ]
