# Generated by Django 4.0.7 on 2023-02-12 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0009_alter_ad_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='text',
            field=models.TextField(max_length=2000),
        ),
    ]
