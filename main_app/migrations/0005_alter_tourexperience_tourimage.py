# Generated by Django 4.0.3 on 2022-04-13 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_tourexperience_tourimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourexperience',
            name='tourImage',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
