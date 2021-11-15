from django.core.exceptions import ValidationError
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
        existing_ingredients = {}
        for ingredient in ingredients:
            if ingredient['amount'] <= 0:
                raise ValidationError(
                    'Количество ингридиента должно быть больше нуля'
                )
            if (
                instance := ingredient['ingredient']
            ) not in existing_ingredients:
                existing_ingredients[instance] = True
            else:
                raise ValidationError(
                    'Ингридиенты не должны повторяться'
                )
        if data['cooking_time'] <= 0:
            raise ValidationError(
                'Время готовки должно быть больше нуля'
            )
        # Валидировать теги на предмет дублей не визу смысла
        # т.к. при добавлении в m2m через set() все дубли сами отвалятся

        # valid_ingredient = {}
        # invalid_ingredient_idx = []
        # for idx in range(len(ingredients)):
        #     ingredient = ingredients[idx]['ingredient']
        #     amount = ingredients[idx]['amount']
        #     if ingredient not in valid_ingredient:
        #         valid_ingredient[ingredient] = idx
        #     else:
        #         origin_ingr_idx = valid_ingredient[ingredient]
        #         ingredients[origin_ingr_idx]['amount'] += amount
        #         invalid_ingredient_idx.append(idx)
        # if invalid_ingredient_idx:
        #     [ingredients.pop(idx) for idx in invalid_ingredient_idx[::-1]]
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
                ingredient=ingredient['ingredient'],
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
