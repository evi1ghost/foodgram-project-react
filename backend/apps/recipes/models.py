from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    hexcolor_regex = RegexValidator(
        regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$',
        message=(
            'Enter valid hex color number'
        )
    )
    hexcolor = models.CharField(
        max_length=7,
        unique=True,
        validators=[hexcolor_regex],
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Название для ссылки'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


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
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Cooking time could not be less than 1'
            )
        ],
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

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование'
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
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
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Amount could not be less than 1'
            )
        ],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'

    def __str__(self) -> str:
        return self.ingridient.name
