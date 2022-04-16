from django.db import models
from django.contrib.auth.models import User, AbstractUser
import uuid
# Create your models here.





# class EndUser(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     userFirstName = models.CharField(max_length=50)
#     userLastName = models.CharField(max_length=50)
#     user_registration = models.DateField()
#     userDateOfBirth = models.DateField()
#     # user = models.ForeignKey(
#     #     CustomUser,  on_delete=models.CASCADE, null=True)

#     def __str__(self):
#         return self.userFirstName

# #sign up as a tour guide
class TourGuide(User):
    guideDescription = models.CharField(max_length=300)
    # guideDob = models.DateField(null=True)
    numberOfActivities = models.IntegerField(blank=True, null=True)
    income = models.IntegerField(blank=True, null=True)
    ratings = models.IntegerField(blank=True, null=True)
    isGuideApproved = models.BooleanField(default=False)


#     # def __str__(self):
#     #     return self.guideFirstName

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
