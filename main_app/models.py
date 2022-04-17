from django.db import models
from django.contrib.auth.models import User, AbstractUser
import uuid
# Create your models here.


# sign up as a tour guide
class EndUser(User):
    userDateOfBirth = models.DateField(blank=True, null=True)


class TourGuide(User):
    guideDescription = models.CharField(max_length=300, blank=True, null=True)
    # guideDob = models.DateField(null=True)
    numberOfActivities = models.IntegerField(blank=True, null=True)
    income = models.IntegerField(blank=True, null=True)
    ratings = models.IntegerField(blank=True, null=True)
    approvalChoices = (
        ('Approved', True), 
        ('Non-approved', False)
    )
    isGuideApproved = models.CharField(max_length=12, choices=approvalChoices)


class TourExperience(models.Model):
    endUsers = models.ManyToManyField(EndUser, through="Booking")
    tourGuide = models.ForeignKey(TourGuide, on_delete=models.CASCADE)

    tourTitle = models.CharField(max_length=100)
    tourLocation = models.CharField(max_length=50)
    tourDuration = models.IntegerField()
    tourPrice = models.FloatField()
    tourAvailableDate = models.DateField()
    tourMaxNumberOfPeople = models.IntegerField()
    tourDescription = models.TextField(max_length=500)
    tourImage = models.ImageField(
        upload_to="static/media/images/", height_field=None, width_field=None, max_length=100, blank=True, null=True)

    def __str__(self):
        return self.tourTitle


class Booking(models.Model):
    tourExperience = models.ForeignKey(TourExperience, on_delete=models.CASCADE)
    endUser = models.ForeignKey(EndUser, on_delete=models.CASCADE)
    transactionDate = models.DateField(auto_now=True)
