# Generated by Django 4.0.1 on 2022-04-20 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourexperience',
            name='endUser',
            field=models.ManyToManyField(blank=True, related_name='tourExperiences', to='main_app.EndUser'),
        ),
    ]
