from django.shortcuts import render,get_object_or_404
from houses.models import Property
# Create your views here.
def index(request):
    is_featured = Property.objects.filter(available=True, is_featured=True)
    context={
        'is_featured':is_featured
    }

    return render(request,'index.html',context)

def advertisements(request):
    propertys = Property.objects.filter(available=True)
    context = {
        'propertys': propertys,

    }
    return render(request,'properties.html',context)
def house_detail(request,id,slug):
    house=get_object_or_404(Property,pk=id,slug=slug)
    context={
        'house':house
    }
    return render(request,'property-details.html',context)
def contact(request):
    return render(request,'contact.html')