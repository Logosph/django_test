# Generated by Django 5.1.3 on 2024-11-28 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_client_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='style',
            name='style_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]