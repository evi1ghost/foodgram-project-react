import factory
from faker import Faker

from apps.users.models import User

fake = Faker(locale='ru_RU')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ['email', 'username']

    first_name = factory.Faker('first_name', locale='ru_RU')
    last_name = factory.Faker('last_name', locale='ru_RU')
    email = factory.Faker('email', locale='en_US')
    username = factory.Faker('last_name', locale='en_US')
