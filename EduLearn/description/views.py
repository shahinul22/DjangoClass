from django.shortcuts import render

# Create your views here.

def des(request):
    return render(request, "description/description.html")
