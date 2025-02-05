from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

def advertisements(request):
    return render(request,'properties.html')

def contact(request):
    return render(request,'contact.html')