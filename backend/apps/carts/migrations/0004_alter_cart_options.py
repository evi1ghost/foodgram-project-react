# Generated by Django 3.2.8 on 2021-10-30 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_cart_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Список покупок', 'verbose_name_plural': 'Списки покупок'},
        ),
    ]
