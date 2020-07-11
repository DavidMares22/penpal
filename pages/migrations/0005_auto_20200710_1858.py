# Generated by Django 3.0.8 on 2020-07-10 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20200709_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_learning',
            field=models.CharField(blank=True, choices=[('1', 'Enlgish'), ('2', 'Spanish'), ('3', 'French'), ('4', 'German')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='speaks',
            field=models.CharField(blank=True, choices=[('1', 'Enlgish'), ('2', 'Spanish'), ('3', 'French'), ('4', 'German')], max_length=10, null=True),
        ),
    ]
