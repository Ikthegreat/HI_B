# Generated by Django 3.2.13 on 2023-05-18 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='vote_count',
        ),
    ]
