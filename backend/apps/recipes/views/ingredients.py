from rest_framework import viewsets

from apps.recipes.filters import IngredientFilter
from apps.recipes.models import IngredientAmount
from apps.recipes.serializers import IngredientsSerializer


class IngredientReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IngredientAmount.objects.select_related('ingredient').all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    filterset_class = IngredientFilter
