from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('payments/', include('payments.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

# wireframe css lives at repo root /css — serve in dev only
if settings.DEBUG:
    urlpatterns += [
        path('css/<path:path>', serve, {'document_root': settings.BASE_DIR / 'css'}),
    ]
