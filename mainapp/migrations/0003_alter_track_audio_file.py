# Generated by Django 5.0.4 on 2024-06-08 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_playlist_cover_alter_track_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='audio_file',
            field=models.FileField(upload_to='static/audio/'),
        ),
    ]
