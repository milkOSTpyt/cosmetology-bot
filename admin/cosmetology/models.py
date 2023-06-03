from django.db import models


class Owner(models.Model):
    full_name = models.CharField(max_length=100)
    description = models.TextField()
    telegram_id = models.IntegerField()
    location_latitude = models.FloatField(default=0)
    location_longitude = models.FloatField(default=0)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if Owner.objects.count() <= 1:
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Информация администратора"
        verbose_name_plural = "Информация администратора"


class Client(models.Model):
    telegram_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    telegram_username = models.CharField(max_length=70, null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    chat_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} {self.telegram_id}'

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Service(models.Model):
    title = models.CharField(max_length=80)
    link = models.CharField(max_length=250)
    description = models.TextField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_discount = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
