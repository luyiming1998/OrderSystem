# Generated by Django 2.2.7 on 2019-12-04 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0008_auto_20191204_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='good_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.GoodType', verbose_name='商品类型'),
        ),
    ]
