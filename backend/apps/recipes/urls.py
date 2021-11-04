from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.recipes.views import TagRetrieveViewSet


router = DefaultRouter()

router.register('', TagRetrieveViewSet, basename='tags')


urlpatterns = [
    path('tags/', include(router.urls)),
]
