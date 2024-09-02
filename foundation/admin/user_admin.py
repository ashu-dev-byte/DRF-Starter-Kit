from django.contrib import admin

from foundation import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "role", "last_login", "is_active")
    raw_id_fields = ("user_permissions", "groups")
    search_fields = ["id", "name", "email"]
    list_filter = ("role",)
    list_per_page = 50
