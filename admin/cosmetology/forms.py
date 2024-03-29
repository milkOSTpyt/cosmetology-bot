from django import forms
from emoji_picker.widgets import EmojiPickerTextareaAdmin, EmojiPickerTextInputAdmin

from admin.cosmetology.models import Owner, Service, Category


class OwnerForm(forms.ModelForm):
    full_name = forms.CharField(label='Имя')
    description = forms.CharField(widget=EmojiPickerTextareaAdmin, label='Описание')
    telegram_id = forms.IntegerField(label='Telegram id')
    location_longitude = forms.FloatField(label='Месторасположение - долгота')
    location_latitude = forms.FloatField(label='Месторасположение - широта')

    class Meta:
        model = Owner
        fields = ("full_name", "description", "telegram_id", "location_longitude", "location_latitude")


class ServiceForm(forms.ModelForm):
    title = forms.CharField(widget=EmojiPickerTextInputAdmin, label='Название')
    price = forms.FloatField(label='Цена', required=False)
    description = forms.CharField(widget=EmojiPickerTextareaAdmin, label='Описание')
    link = forms.URLField(empty_value=False, label='Ссылка для записи')
    category_id = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория')
    is_active = forms.BooleanField(label='Запись открыта', required=False)
    is_discount = forms.BooleanField(label='Акции', required=False)

    class Meta:
        model = Service
        fields = ("title", "price", "link", "description", "category_id", "is_active", "is_discount")


class CategoryForm(forms.ModelForm):
    title = forms.CharField(widget=EmojiPickerTextInputAdmin, label='Название')

    class Meta:
        model = Category
        fields = ("title",)
