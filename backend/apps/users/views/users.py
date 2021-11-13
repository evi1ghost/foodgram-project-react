from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.models import Follow, User
from apps.users.serializers import (
    SetPasswordSerializer,
    UserSerializer,
    UserSubscriptionSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(
        methods=['get'],
        detail=False,
        url_path='me',
        url_name='me',
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['post'],
        detail=False,
        url_path='set_password',
        url_name='set_password',
        permission_classes=[permissions.IsAuthenticated],
    )
    def set_password(self, request, *args, **kwargs):
        user = request.user
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if user.check_password(
            serializer.validated_data.get('current_password')
        ):
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'current_password': 'Введен неверный пароль.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=['get'],
        detail=False,
        url_path='subscriptions',
        url_name='subscriptions',
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscription(self, request, *args, **kwargs):
        user = request.user
        queryset = User.objects.filter(subscribers__subscriber=user)
        serializer = UserSubscriptionSerializer(
            queryset,
            context={'request': request},
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get', 'delete'],
        url_path=r'(?P<id>[\d]+)/subscribe',
        url_name='subscribe',
        pagination_class=None,
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, *args, **kwargs):
        user = request.user
        author = get_object_or_404(User, id=kwargs['id'])
        subscribtion = Follow.objects.filter(
            subscriber=user,
            author=author
        )
        if (
            request.method == 'GET'
            and not subscribtion
            and user != author
        ):
            Follow.objects.create(
                subscriber=user,
                author=author
            )
            serializer = UserSubscriptionSerializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE' and subscribtion:
            subscribtion.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'detail': 'Действие уже выполнено'},
            status=status.HTTP_400_BAD_REQUEST
        )
