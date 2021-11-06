from rest_framework import serializers

from apps.recipes.models import IngredientAmount


class IngredientsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='name',
        read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='measurement_unit',
        read_only=True
    )

    class Meta:
        model = IngredientAmount
        fields = ['id', 'name', 'measurement_unit', 'amount']
