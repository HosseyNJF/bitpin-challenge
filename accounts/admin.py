from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import BlogUser


@admin.register(BlogUser)
class BlogUserAdmin(UserAdmin):
    pass
