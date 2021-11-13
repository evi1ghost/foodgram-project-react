from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.recipes.models import Recipe

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        subscriptions = user.subscriptions.filter(author=obj).exists()
        return subscriptions

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
        ]
        extra_kwargs = {'password': {'write_only': True}}


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        min_length=8,
        max_length=128,
        write_only=True,
    )
    current_password = serializers.CharField(write_only=True)


class UserRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']
        read_only_fields = ['name', 'image', 'cooking_time']


class UserSubscriptionSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        recipes_limit = self.context[
            'request'].query_params.get('recipes_limit')
        if recipes_limit and recipes_limit.isdigit():
            recipes_limit = int(recipes_limit)
        queryset = obj.recipes.all()[:recipes_limit]
        serializer = UserRecipeSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
            'recipes',
            'recipes_count'
        ]
        extra_kwargs = {'password': {'write_only': True}}
