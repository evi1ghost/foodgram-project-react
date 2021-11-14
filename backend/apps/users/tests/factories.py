import factory
from faker import Faker

from apps.users.models import Follow, User

fake = Faker(locale='ru_RU')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ['email', 'username']

    first_name = factory.Faker('first_name', locale='ru_RU')
    last_name = factory.Faker('last_name', locale='ru_RU')
    email = factory.Faker('email', locale='en_US')
    username = factory.Faker('user_name', locale='en_US')


class FollowFactory(factory.django.DjangoModelFactory):
    '''
    Creates Follow object. User.objects.first() is used as author.
    You should create at least two users before use this factory.
    '''
    class Meta:
        model = Follow
        django_get_or_create = ['subscriber']

    subscriber = factory.Iterator(
        User.objects.all().exclude(id=User.objects.first().id)
    )
    author = factory.LazyFunction(lambda: User.objects.first())
