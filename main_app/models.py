from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User, AbstractUser
import uuid
# Create your models here.


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('end_user', 'end_user'),
        ('tour_guide', 'tour_guide'),
        ('moderator', 'moderator'),
    )
    user_type = models.CharField(max_length=50,
                                 choices=USER_TYPE_CHOICES, null=True)


class EndUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userFirstName = models.CharField(max_length=50)
    userLastName = models.CharField(max_length=50)
    user_registration = models.DateField()
    userDateOfBirth = models.DateField()
    user = models.ForeignKey(
        CustomUser,  on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.userFirstName


class TourGuide(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guideFirstName = models.CharField(max_length=50)
    guideLastName = models.CharField(max_length=50)
    guideDescription = models.TextField(max_length=300)

    def __str__(self):
        return self.guideFirstName


class TourExperience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tourTitle = models.CharField(max_length=100)
    tourLocation = models.CharField(max_length=50)
    tourDuration = models.IntegerField()
    tourPrice = models.FloatField()
    tourAvailableDate = models.DateField()
    tourMaxNumberOfPeople = models.IntegerField()
    tourDescription = models.TextField(max_length=499)
    tourGuide = models.ForeignKey(TourGuide, on_delete=models.CASCADE)
    tourImage = models.ImageField(
        upload_to="static/media/images/", height_field=None, width_field=None, max_length=100, null=True)

    def __str__(self):
        return self.tourTitle
