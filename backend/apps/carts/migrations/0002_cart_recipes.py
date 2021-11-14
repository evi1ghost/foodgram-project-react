# Generated by Django 3.2.8 on 2021-11-14 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carts', '0001_initial'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='recipes',
            field=models.ManyToManyField(related_name='carts', to='recipes.Recipe', verbose_name='Рецепты'),
        ),
    ]
