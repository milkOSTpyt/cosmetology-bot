from django.contrib import admin
from django.contrib.auth.models import Group

from . import models
from .forms import OwnerForm, ServiceForm, PromotionForm


@admin.register(models.Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "telegram_id")
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


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title",)
    list_filter = ("category_id__title",)
    search_fields = ("title",)
    form = ServiceForm


@admin.register(models.Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active")
    list_filter = ("title", "is_active")
    search_fields = ("title",)
    form = PromotionForm


admin.site.site_header = "Nastassia COSMETOLOGY"
admin.site.site_title = "Панель администрирования"
admin.site.index_title = "Админка"
admin.site.unregister(Group)
