# Generated by Django 3.0.8 on 2020-07-23 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muscle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainlog',
            name='used_date',
            field=models.DateField(verbose_name='日付'),
        ),
    ]