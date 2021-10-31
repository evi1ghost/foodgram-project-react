from django.contrib import admin

from apps.users.models import Follow, User


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'username',
        'email',
        'first_name',
        'last_name'
    ]
    list_filter = [
        'username',
        'email',
        'first_name',
        'last_name',
    ]
    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name',
    ]
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'subscriber',
        'author',
    ]
    list_filter = [
        'subscriber',
        'author',
    ]
    search_fields = [
        'subscriber',
        'author',
    ]
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
