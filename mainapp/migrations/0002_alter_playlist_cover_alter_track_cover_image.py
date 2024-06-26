# Generated by Django 5.0.4 on 2024-06-08 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='cover',
            field=models.ImageField(blank=True, default='static/img/default-cover.png', upload_to='static/img/'),
        ),
        migrations.AlterField(
            model_name='track',
            name='cover_image',
            field=models.ImageField(blank=True, default='static/img/default-cover.png', null=True, upload_to='static/img/'),
        ),
    ]
