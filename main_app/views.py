from django.shortcuts import render

from .models import *

# Create your views here.


def homepage(request):
    context = {'allToursList': TourExperience.objects.all()}
    return render(request, 'main_app/homepage.html', context)
