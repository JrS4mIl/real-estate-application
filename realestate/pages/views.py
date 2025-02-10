from django.shortcuts import render
from houses.models import Property
# Create your views here.
def index(request):
    return render(request,'index.html')

def advertisements(request):
    propertys = Property.objects.filter(available=True)
    context = {
        'propertys': propertys
    }
    return render(request,'properties.html',context)

def contact(request):
    return render(request,'contact.html')