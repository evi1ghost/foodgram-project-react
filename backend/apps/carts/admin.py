from django.contrib import admin

from apps.carts.models import Cart


class RecipesInline(admin.StackedInline):
    model = Cart.recipes.through
    extra = 1
    verbose_name = 'Рецепт'
    verbose_name_plural = 'Рецепты'


class CartAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'user',
    ]
    exclude = [
        'recipes',
    ]
    inlines = [
        RecipesInline,
    ]
    list_filter = [
        'user',
    ]
    search_fields = [
        'user',
    ]
    empty_value_display = '-пусто-'


admin.site.register(Cart, CartAdmin)
