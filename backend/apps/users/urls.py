from django.urls import include, path

from apps.users.views import CustomAuthToken, DestroyTokenAPIView


auth_urlpatterns = [
    path('login/', CustomAuthToken.as_view()),
    path('logout/', DestroyTokenAPIView.as_view()),
]


urlpatterns = [
    path('auth/token/', include(auth_urlpatterns)),
]
