# Generated by Django 2.2 on 2018-11-06 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ASP', '0008_auto_20181106_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='priority',
            field=models.CharField(choices=[('3', 'High'), ('2', 'Medium'), ('1', 'Low')], default='3', max_length=1),
        ),
    ]