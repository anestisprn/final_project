from django.db import models
from django.contrib.auth.models import User, AbstractUser
import uuid
# Create your models here.

# #sign up as a tour guide
class TourGuide(User):
    guideDescription = models.CharField(max_length=300)
    # guideDob = models.DateField(null=True)
    numberOfActivities = models.IntegerField(blank=True, null=True)
    income = models.IntegerField(blank=True, null=True)
    ratings = models.IntegerField(blank=True, null=True)
    approvalChoices = (
        ('Approved', True), 
        ('Non-approved', False)
    )
    isGuideApproved = models.CharField(max_length=12, choices=approvalChoices)


    def __str__(self):
        return f"{User.first_name} {User.last_name}"


class TourExperience(models.Model):
    tourTitle = models.CharField(max_length=100)
    tourLocation = models.CharField(max_length=50)
    tourDuration = models.IntegerField()
    tourPrice = models.FloatField()
    tourAvailableDate = models.DateField()
    tourMaxNumberOfPeople = models.IntegerField()
    tourDescription = models.TextField(max_length=499)
    tourGuide = models.ForeignKey(TourGuide, on_delete=models.CASCADE, related_name='tourexperience')
    tourImage = models.ImageField(
        upload_to="static/media/images/", height_field=None, width_field=None, max_length=100, null=True)

    def __str__(self):
        return self.tourTitle

class EndUser(User):
    userDateOfBirth = models.DateField()
    tourExperiences = models.ManyToManyField(TourExperience)
    # user = models.ForeignKey(
    #     CustomUser,  on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{User.first_name} {User.last_name}"