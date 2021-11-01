from django.contrib.auth import get_user_model
from rest_framework import serializers

# from apps.users.models import Follow

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
