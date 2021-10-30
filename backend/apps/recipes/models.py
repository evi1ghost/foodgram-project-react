from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    hexcolor = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Название для ссылки'
    )


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    image = models.ImageField(verbose_name='Изображение')
    text = models.TextField(
        max_length=3000,
        verbose_name='Описание'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэги'
    )
    who_likes_it = models.ManyToManyField(
        User,
        related_name='favourite_recipes',
        verbose_name='Кому понравилось'
    )


class Ingridient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование'
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения'
    )


class IngridientAmount(models.Model):
    ingridient = models.ForeignKey(
        Ingridient,
        on_delete=models.CASCADE,
        related_name='ingridient_amount',
        verbose_name='Ингридиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingridients',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(verbose_name='Количество')
