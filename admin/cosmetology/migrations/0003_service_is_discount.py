# Generated by Django 4.2.1 on 2023-05-08 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmetology', '0002_delete_promotion_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='is_discount',
            field=models.BooleanField(default=False),
        ),
    ]
