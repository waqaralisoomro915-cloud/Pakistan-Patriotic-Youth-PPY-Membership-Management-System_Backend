from rest_framework.viewsets import ModelViewSet
from .serializers import BaseModelSerializer
class BaseModelViewSet(ModelViewSet):
    """
    Reusable base ViewSet for PPY applications.
    """
    serializer_class = BaseModelSerializer
    def get_queryset(self):
        """
        Child ViewSets must define their own queryset.
        """
        if not hasattr(self, "queryset") or self.queryset is None:
            raise NotImplementedError(
                "Define queryset in the child ViewSet."
            )

        return super().get_queryset()
