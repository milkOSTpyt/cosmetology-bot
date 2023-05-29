from django.contrib import admin
from django.contrib.auth.models import Group

from . import models
from .forms import OwnerForm, ServiceForm, CategoryForm


@admin.register(models.Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "telegram_id", "location_latitude", "location_longitude")
    form = OwnerForm


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "telegram_username", "phone_number", "created_at")
    list_filter = ("name",)
    search_fields = ("name",)
    readonly_fields = ('telegram_id', 'name', 'telegram_username', 'phone_number')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
    list_filter = ("title",)
    search_fields = ("title",)
    form = CategoryForm


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "is_discount")
    list_filter = ("category_id__title", "is_active", "is_discount")
    search_fields = ("title",)
    form = ServiceForm


admin.site.site_header = "Nastassia COSMETOLOGY"
admin.site.site_title = "Панель администрирования"
admin.site.index_title = "Админка"
admin.site.unregister(Group)
