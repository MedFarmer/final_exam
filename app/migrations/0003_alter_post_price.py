# Generated by Django 5.0 on 2023-12-07 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_post_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='price',
            field=models.IntegerField(verbose_name='Цена'),
        ),
    ]
