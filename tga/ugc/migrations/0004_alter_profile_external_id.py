# Generated by Django 3.2.6 on 2021-08-24 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0003_alter_message_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='external_id',
            field=models.PositiveIntegerField(unique=True, verbose_name='Account ID'),
        ),
    ]