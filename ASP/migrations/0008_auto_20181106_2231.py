# Generated by Django 2.2 on 2018-11-06 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ASP', '0007_auto_20181106_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='priority',
            field=models.CharField(choices=[('1', 'High'), ('2', 'Medium'), ('3', 'Low')], default='3', max_length=1),
        ),
    ]