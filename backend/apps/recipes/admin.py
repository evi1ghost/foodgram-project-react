from django.contrib import admin

from apps.recipes.models import Ingredient, IngredientAmount, Recipe


class IngredientAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
        'measurement_unit',
    ]
    list_filter = [
        'name',
    ]
    search_fields = [
        'name',
    ]
    empty_value_display = '-пусто-'


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'amount',
        'ingredient',
        'recipe',
    ]
    list_filter = [
        'ingredient',
        'recipe',
    ]
    search_fields = [
        'recipe',
    ]
    empty_value_display = '-пусто-'


class TagInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1
    verbose_name = 'Тег'
    verbose_name_plural = 'Теги'


class LikesInline(admin.TabularInline):
    model = Recipe.who_likes_it.through
    extra = 1
    verbose_name = 'Пользователь'
    verbose_name_plural = 'Добавили в избранное'


class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
        'image',
        'text',
        'cooking_time',
        'author',
    ]
    exclude = [
        'tags',
        'who_likes_it',
    ]
    inlines = [
        TagInline,
        LikesInline,
    ]
    list_filter = [
        'name',
        'cooking_time',
        'author',
    ]
    search_fields = [
        'name',
        'author',
    ]
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(Recipe, RecipeAdmin)
