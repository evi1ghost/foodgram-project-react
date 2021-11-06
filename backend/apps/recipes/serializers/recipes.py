from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from apps.recipes.models import IngredientAmount, Recipe, Tag
from apps.users.serializers import UserSerializer
from .tags import TagSerializer
from .ingredients import IngredientsSerializer


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientsSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shoping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(max_length=None, use_url=True)

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        if user in obj.who_likes_it.all():
            return True
        return False

    def get_is_in_shoping_cart(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        if obj in user.cart.recipes.all():
            return True
        return False

    def create(self, validated_data):
        tags_from_request = validated_data.pop('tags')
        ingredients_from_request = validated_data.pop('ingredients')

        tag_ids = [tag['id'] for tag in tags_from_request]
        tags = Tag.objects.filter(id__in=tag_ids)

        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.add(*tags)

        for ingredient in ingredients_from_request:
            IngredientAmount.objects.create(
                ingredient_id=ingredient['id'],
                amount=ingredient['amount'],
                recipe=recipe
            )
        return recipe

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shoping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        ]
