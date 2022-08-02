from __future__ import unicode_literals
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib import admin

from .models import PhoneOTP
User = get_user_model()


admin.site.register(PhoneOTP)


class UserAdmin(BaseUserAdmin):
    # То, что отображается в просмотре в виде списка
    list_display = ('full_name', 'phone', 'admin',)
    # То, по чему можно фильтровать этот список
    list_filter = ('active', 'admin',)
    # Поля при просмотре конкретного объекта
    fieldsets = (
        (None, {'fields': ('phone', 'password', 'full_name')}),
        ('Permissions', {'fields': ('admin', 'active', 'groups')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2')}
         ),
    )

    # Поля, по которым можно сортировать при просмотре в виде списка
    search_fields = ('phone', 'full_name')
    # Поля, по которым идет порядок просмотра в виде списка
    ordering = ('phone', 'full_name')
    filter_horizontal = ()

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


admin.site.register(User, UserAdmin)