# Generated by Django 4.0.1 on 2022-04-24 21:17

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import location_field.models.plain


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='EndUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('userDateOfBirth', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'EndUser',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='TourExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tourTitle', models.CharField(max_length=100, verbose_name='Tour Title')),
                ('tourCity', models.CharField(blank=True, max_length=255)),
                ('tourCategory', models.CharField(choices=[('Food Experience', 'food_experience'), ('Activities in Nature', 'activities_in_nature'), ('Drinking experience', 'drinking_experience'), ('Spiritual experience', 'spiritual_experience'), ('Sightseeing experience', 'sightseeing_experience')], max_length=50)),
                ('tourLocation', location_field.models.plain.PlainLocationField(blank=True, max_length=63)),
                ('tourDuration', models.IntegerField(verbose_name='Tour Duration')),
                ('tourPrice', models.FloatField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10000)], verbose_name='Tour Price')),
                ('tourRating', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Tour Rating')),
                ('tourAvailableDate', models.DateField(verbose_name='Tour Available Date')),
                ('tourMaxNumberOfPeople', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)], verbose_name='Tour Max Number of People')),
                ('tourDescription', models.TextField(max_length=500, verbose_name='Tour Title')),
                ('tourImage', models.ImageField(blank=True, null=True, upload_to='static/media/images/', verbose_name='Tour Image')),
                ('endUser', models.ManyToManyField(blank=True, related_name='tourExperiences', to='main_app.EndUser')),
            ],
            options={
                'verbose_name': 'TourExperience',
            },
        ),
        migrations.CreateModel(
            name='TourGuide',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('guideDescription', models.CharField(blank=True, max_length=300, null=True)),
                ('numberOfActivities', models.IntegerField(blank=True, null=True)),
                ('income', models.IntegerField(blank=True, null=True)),
                ('ratings', models.IntegerField(blank=True, null=True)),
                ('isGuideApproved', models.CharField(choices=[('Approved', True), ('Non-approved', False)], max_length=12)),
            ],
            options={
                'verbose_name': 'TourGuide',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endUser', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.enduser')),
                ('tourExperience', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.tourexperience')),
            ],
        ),
        migrations.AddField(
            model_name='tourexperience',
            name='tourGuide',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.tourguide'),
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('customer_email', models.EmailField(max_length=254, verbose_name='Customer Email')),
                ('amount', models.IntegerField(verbose_name='Amount')),
                ('stripe_payment_intent', models.CharField(max_length=200)),
                ('has_paid', models.BooleanField(default=False, verbose_name='Payment Status')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('tourExperience', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main_app.tourexperience', verbose_name='Tour Experience')),
            ],
        ),
    ]
