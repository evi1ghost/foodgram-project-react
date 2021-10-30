from django.db import models
from django.contrib.auth import get_user_model

from apps.recipes.models import Recipe

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    recipes = models.ManyToManyField(
        Recipe,
        related_name='carts',
        verbose_name='Рецепты'
    )
