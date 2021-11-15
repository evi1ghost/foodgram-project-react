from rest_framework import viewsets

from apps.recipes.filters import IngredientFilter
from apps.recipes.models import Ingredient
from apps.recipes.serializers import IngredientSerializer


class IngredientReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filterset_class = IngredientFilter
