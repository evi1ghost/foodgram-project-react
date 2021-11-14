from django.contrib import admin
from django.urls import include, path

apps_urlpatterns = [
    path('', include('apps.users.urls')),
    path('', include('apps.recipes.urls')),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(apps_urlpatterns)),
]
