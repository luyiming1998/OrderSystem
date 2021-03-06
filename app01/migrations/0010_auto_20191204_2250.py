# Generated by Django 2.2.7 on 2019-12-04 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0009_auto_20191204_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='good_status',
            field=models.IntegerField(default=1, verbose_name='商品状态'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='good_pic',
            field=models.ImageField(default='good_pic/default.png', upload_to='good_pic/%Y/%m', verbose_name='商品图片'),
        ),
    ]
