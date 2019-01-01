from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse('Blog home')

def about(request):
    return HttpResponse('Blog about')
