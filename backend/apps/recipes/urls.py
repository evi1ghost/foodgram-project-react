from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.recipes.views import IngredientReadOnlyViewSet, TagRetrieveViewSet


router = DefaultRouter()

router.register(
    'tags',
    TagRetrieveViewSet,
    basename='tags'
)
router.register(
    'ingredients',
    IngredientReadOnlyViewSet,
    basename='ingredients'
)


urlpatterns = [
    path('', include(router.urls)),
]
