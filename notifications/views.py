"""notifications/views.py — list and mark read for current user."""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        note = self.get_object()
        note.is_read = True
        note.save(update_fields=['is_read'])
        return Response(NotificationSerializer(note).data)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'ok': True})


# ---------------------------------------------------------------------------
# BUGGY CODE (commented out) — listed every notification in the database
# ---------------------------------------------------------------------------
# def get_queryset(self):
#     return Notification.objects.all().order_by('-created_at')
