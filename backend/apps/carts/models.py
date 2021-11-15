from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save

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

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self) -> str:
        return self.user.username


def create_cart(sender, instance, **kwargs):
    Cart.objects.get_or_create(user=instance)


post_save.connect(create_cart, sender=User)
