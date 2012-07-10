# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

def homepage(request):
    return HttpResponse("Welcome to our homepage!")