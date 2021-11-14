from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, status, views
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from apps.users.serializers import CustomAuthTokenSerializer


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.status_code = status.HTTP_201_CREATED
        return response


class DestroyTokenAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user:
            Response(
                {'detail': 'Authentication credentials were not provided.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            token = Token.objects.get(user=user)
        except ObjectDoesNotExist:
            Response(
                {'detail': 'Token does not exist.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        token.delete()
        return Response(status=status.HTTP_201_CREATED)
