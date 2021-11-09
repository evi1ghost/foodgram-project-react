from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.carts.utilities import generate_pdf_response, generate_shopping_list
from apps.recipes.models import Recipe
from apps.recipes.permissions import IsAuthorOrReadOnly
from apps.recipes.serializers import RecipeSerializer
from apps.users.serializers import UserRecipeSerializer

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=['get', 'delete'],
        url_path=r'(?P<id>[\d]+)/favorite',
        url_name='favorite',
        pagination_class=None,
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, *args, **kwargs):
        user = request.user
        recipe = get_object_or_404(Recipe, id=kwargs['id'])
        like = User.objects.filter(id=user.id, favourite_recipes=recipe)
        if request.method == 'GET' and not like:
            recipe.who_likes_it.add(user)
            serializer = UserRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE' and like:
            recipe.who_likes_it.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['get', 'delete'],
        url_path=r'(?P<id>[\d]+)/shopping_cart',
        url_name='shopping_cart',
        pagination_class=None,
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, *args, **kwargs):
        user = request.user
        recipe = get_object_or_404(Recipe, id=kwargs['id'])
        is_added = User.objects.filter(id=user.id, cart__recipes=recipe)
        if request.method == 'GET' and not is_added:
            user.cart.recipes.add(recipe)
            serializer = UserRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE' and is_added:
            user.cart.recipes.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        pagination_class=None,
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request, *args, **kwargs):
        user = request.user
        shopping_list = generate_shopping_list(user)
        return generate_pdf_response(shopping_list)
