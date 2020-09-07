# Generated by Django 3.1 on 2020-09-06 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20200906_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='tag',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='api.category'),
        ),
        migrations.AddField(
            model_name='tag',
            name='name',
            field=models.CharField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.CharField(default='', max_length=50),
        ),
    ]
