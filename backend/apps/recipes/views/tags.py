from rest_framework import viewsets

from apps.recipes.models import Tag
from apps.recipes.serializers import TagSerializer


class TagRetrieveViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
