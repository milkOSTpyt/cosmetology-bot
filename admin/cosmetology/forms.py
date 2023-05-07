from django import forms
from emoji_picker.widgets import EmojiPickerTextareaAdmin, EmojiPickerTextInputAdmin

from admin.cosmetology.models import Owner, Service, Category


class OwnerForm(forms.ModelForm):
    full_name = forms.CharField(label='Имя')
    description = forms.CharField(widget=EmojiPickerTextareaAdmin, label='Описание')
    telegram_id = forms.IntegerField(label='Telegram id')

    class Meta:
        model = Owner
        fields = ("full_name", "description", "telegram_id")


class ServiceForm(forms.ModelForm):
    title = forms.CharField(widget=EmojiPickerTextInputAdmin, label='Название')
    description = forms.CharField(widget=EmojiPickerTextareaAdmin, label='Описание')
    link = forms.URLField(empty_value=False, label='Ссылка для записи')
    category_id = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория')
    is_active = forms.BooleanField(label='Запись открыта', required=False)

    class Meta:
        model = Service
        fields = ("title", "link", "description", "category_id", "is_active")


class CategoryForm(forms.ModelForm):
    title = forms.CharField(widget=EmojiPickerTextInputAdmin, label='Название')

    class Meta:
        model = Category
        fields = ("title",)
