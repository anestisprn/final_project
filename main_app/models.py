from wsgiref.validate import validator
from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.
from django.core import validators


class EndUser(User):
    userDateOfBirth = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'EndUser'


class TourGuide(User):
    guideDescription = models.CharField(max_length=300, blank=True, null=True)
    numberOfActivities = models.IntegerField(blank=True, null=True)
    income = models.IntegerField(blank=True, null=True)
    ratings = models.IntegerField(blank=True, null=True)
    approvalChoices = (
        ('Approved', True),
        ('Non-approved', False)
    )
    isGuideApproved = models.CharField(max_length=12, choices=approvalChoices)

    class Meta:
        verbose_name = 'TourGuide'


class TourExperience(models.Model):
    tourTitle = models.CharField(max_length=100, verbose_name='Tour Title')
    tourLocation = models.CharField(
        max_length=50, verbose_name='Tour Location')
    tourDuration = models.IntegerField(verbose_name='Tour Duration')
    tourPrice = models.FloatField(verbose_name='Tour Price',  validators=[
                                  validators.MinValueValidator(1), validators.MaxValueValidator(10000)])
    tourAvailableDate = models.DateField(verbose_name='Tour Available Date')
    tourMaxNumberOfPeople = models.IntegerField(verbose_name='Tour Max Number of People', validators=[
                                                validators.MinValueValidator(1), validators.MaxValueValidator(20)])
    tourDescription = models.TextField(
        max_length=500, verbose_name='Tour Title')
    tourImage = models.ImageField(
        upload_to="static/media/images/", height_field=None, width_field=None, max_length=100, blank=True, null=True, verbose_name='Tour Image')

    endUser = models.ManyToManyField(
        EndUser, related_name="tourExperiences", blank=True)
    tourGuide = models.ForeignKey(
        TourGuide, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.tourTitle

    class Meta:
        verbose_name = 'TourExperience'


class OrderDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    # You can change as a Foreign Key to the user model
    customer_email = models.EmailField(verbose_name='Customer Email')
    tourExperience = models.ForeignKey(
        to=TourExperience, verbose_name='TourExperience', on_delete=models.PROTECT)
    amount = models.IntegerField(verbose_name='Amount')
    stripe_payment_intent = models.CharField(max_length=200)
    # This field can be changed as status
    has_paid = models.BooleanField(
        default=False, verbose_name='Payment Status')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)


class Booking(models.Model):
    tourExperience = models.ForeignKey(
        TourExperience, on_delete=models.CASCADE, blank=True)
    endUser = models.ForeignKey(EndUser, on_delete=models.CASCADE, blank=True)
    orderDetail = models.OneToOneField(
        OrderDetail, on_delete=models.CASCADE, null=True)
