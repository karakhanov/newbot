# Generated by Django 3.2.6 on 2021-08-30 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0003_alter_profile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='l_name',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Last Name'),
        ),
    ]
