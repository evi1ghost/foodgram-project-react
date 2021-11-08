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
        subscribtions = user.subscribtions.filter(author=obj).exists()
        return subscribtions

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
        read_only_fields = ['is_subscribed']
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
    recipes = UserRecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()

    def get_is_subscribed(self, obj):
        return True

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
        read_only_fields = ['is_subscribed']
        extra_kwargs = {'password': {'write_only': True}}
