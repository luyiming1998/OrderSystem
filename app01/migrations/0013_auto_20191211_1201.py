# Generated by Django 2.2.7 on 2019-12-11 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0012_auto_20191206_1001'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Coments',
            new_name='Comment',
        ),
    ]