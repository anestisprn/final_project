from django.db import models
from django.contrib.auth.models import User, AbstractUser
import uuid
# Create your models here.


class TourExperience(models.Model):
    tourTitle = models.CharField(max_length=100)
    tourLocation = models.CharField(max_length=50)
    tourDuration = models.IntegerField()
    tourPrice = models.FloatField()
    tourAvailableDate = models.DateField()
    tourMaxNumberOfPeople = models.IntegerField()
    tourDescription = models.TextField(max_length=500)
    tourImage = models.ImageField(
        upload_to="static/media/images/", height_field=None, width_field=None, max_length=100, null=True)

    def __str__(self):
        return self.tourTitle


class EndUser(User):
    userDescription = models.CharField(max_length=300, blank=True, null=True)
    tourExperiences = models.ManyToManyField(TourExperience)
    # userDateOfBirth = models.DateField()

    # def __str__(self):
    #     return self.userFirstName


class TourGuide(User):
    guideDescription = models.CharField(max_length=300, blank=True, null=True)
    # guideDateOfBirth = models.DateField()
    numberOfActivities = models.IntegerField(blank=True, null=True)
    income = models.IntegerField(blank=True, null=True)
    ratings = models.IntegerField(blank=True, null=True)
    approvalChoices = (
        ('Approved', True), 
        ('Non-approved', False)
    )
    isGuideApproved = models.CharField(max_length=12, choices=approvalChoices)
    tourExperience = models.ForeignKey(TourExperience, on_delete=models.CASCADE, related_name='tourexperience', null = True)

    # def __str__(self):
    #     return "TourGuide"
