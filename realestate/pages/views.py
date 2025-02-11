from django.shortcuts import render, get_object_or_404, redirect
from houses.models import Property,Category
from .models import Contact
from .forms import ContactForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.
def index(request):
    is_featured = Property.objects.filter(available=True, is_featured=True)
    random_houses = Property.objects.filter(available=True).order_by("?")[:6]
    context = {
        'is_featured': is_featured,
        'random_houses': random_houses
    }

    return render(request, 'index.html', context)


def advertisements(request):
    propertys = Property.objects.filter(available=True)
    category=Category.objects.all()
    context = {
        'propertys': propertys,
        'category':category

    }
    return render(request, 'properties.html', context)


def house_detail(request, id, slug):
    house = get_object_or_404(Property, pk=id, slug=slug)
    context = {
        'house': house
    }
    return render(request, 'property-details.html', context)


def contact(request):
    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message success send')
            return redirect('contact')
        else:
            print(form.errors)
    else:
        form=ContactForm()
    context={
        'form':form
    }
    return render(request,'contact.html',context)
def category_list(request, category_slug):
    propertys = Property.objects.all().filter(category__slug=category_slug)
    category = Category.objects.all()
    context = {
        'propertys': propertys,
        'category': category
    }
    return render(request, 'properties.html', context)