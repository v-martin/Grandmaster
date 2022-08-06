import json

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from .models import Event
from .serializers import EventSerializer
from authentication.models import User
from rest_framework.decorators import action


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class EventViewSet(ModelViewSet):
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = EventSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if User.Group.ADMINISTRATOR in user or User.Group.MODERATOR in user:
                return Event.objects.all()
        else:
            return Event.objects.filter(hidden=False)

    @action(detail=True, methods=['put'])
    def add_member(self, request, *args, **kwargs):
        user = User.objects.get(self.request.data['pk'])
        instance = self.get_object()
        instance.members.add(user)
        instance.save()
        serializer = EventSerializer(instance=instance)
        return Response(serializer.data)
