from apps.recipes.models import IngredientAmount


def generate_shopping_list(user):
    shopping_list = {}
    ingredients = IngredientAmount.objects.filter(
        recipe__carts__user=user
        ).values_list(
        'ingredient__name',
        'amount',
        'ingredient__measurement_unit',
        named=True
    )
    for row in ingredients:
        if row.ingredient__name in shopping_list:
            shopping_list[row.ingredient__name][0] += row.amount
        else:
            shopping_list[row.ingredient__name] = [
                row.amount, row.ingredient__measurement_unit
            ]
    return shopping_list
