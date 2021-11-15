from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .ingredients import IngredientAmountSerializer
from .tags import TagSerializer
from apps.recipes.models import IngredientAmount, Recipe
from apps.users.serializers import UserSerializer


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        if obj.who_likes_it.filter(id=request.user.id).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        if obj.carts.filter(user=request.user).exists():
            return True
        return False

    def to_representation(self, instance):
        self.fields['tags'] = TagSerializer(many=True)
        return super().to_representation(instance)

    def validate(self, data):
        ingredients = data['ingredients']
        ingr_ids = {}
        for i in range(len(ingredients)):
            id = ingredients[i]['id']
            if id not in ingr_ids:
                ingr_ids[id] = i
            else:
                ingredients[ingr_ids[id]]['amount'] += (
                    ingredients[i]['amount']
                )
                ingredients.pop(i)
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients_from_request = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.add(*tags)
        for ingredient in ingredients_from_request:
            IngredientAmount.objects.create(
                ingredient_id=ingredient['id'],
                amount=ingredient['amount'],
                recipe=recipe
            )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients_from_request = validated_data.pop('ingredients')
        super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.add(*tags)
        IngredientAmount.objects.filter(recipe=instance).delete()
        for ingredient in ingredients_from_request:
            IngredientAmount.objects.get_or_create(
                ingredient_id=ingredient['id'],
                amount=ingredient['amount'],
                recipe=instance
            )
        return instance

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        ]
