from django import forms
from emoji_picker.widgets import EmojiPickerTextareaAdmin

from admin.cosmetology.models import Owner, Service, Promotion


class OwnerForm(forms.ModelForm):
    description = forms.CharField(widget=EmojiPickerTextareaAdmin)

    class Meta:
        model = Owner
        fields = ("full_name", "description", "telegram_id")


class ServiceForm(forms.ModelForm):
    description = forms.CharField(widget=EmojiPickerTextareaAdmin)
    link = forms.URLField(empty_value=False)

    class Meta:
        model = Service
        fields = ("title", "link", "description", "category_id")


class PromotionForm(forms.ModelForm):
    description = forms.CharField(widget=EmojiPickerTextareaAdmin)
    link = forms.URLField(empty_value=False)

    class Meta:
        model = Promotion
        fields = ("title", "link", "description", "is_active")
