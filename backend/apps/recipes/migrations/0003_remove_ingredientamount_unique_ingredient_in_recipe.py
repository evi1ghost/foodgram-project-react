# Generated by Django 3.2.8 on 2021-11-14 23:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='ingredientamount',
            name='unique_ingredient_in_recipe',
        ),
    ]
