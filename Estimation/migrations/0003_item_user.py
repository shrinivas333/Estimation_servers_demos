# Generated by Django 2.2 on 2021-02-04 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Estimation', '0002_auto_20210129_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='User',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Estimation.User'),
        ),
    ]
