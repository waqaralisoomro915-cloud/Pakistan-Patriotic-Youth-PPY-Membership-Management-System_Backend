
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from .models import Positions
from .serializers import PositionSerializer
from .permissions import CanManagePositions


class PositionsViewSet(ModelViewSet):
    queryset = Positions.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [CanManagePositions]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["name", "level"]
    search_fields = ["name"]
    ordering_fields = ["name", "level", "created_at"]
    ordering = ["-created_at"]
