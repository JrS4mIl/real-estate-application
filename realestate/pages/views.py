from django.shortcuts import render, get_object_or_404, redirect
from houses.models import Property,Category
from .models import Contact
from .forms import ContactForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.
from accounts.models import Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def index(request):
    is_featured = Property.objects.filter(available=True, is_featured=True,status='published')
    random_houses = Property.objects.filter(available=True).order_by("?")[:6]
    is_featured_profile=Profile.objects.filter(is_featured=True)
    context = {
        'is_featured': is_featured,
        'random_houses': random_houses,
        'is_featured_profile':is_featured_profile
    }

    return render(request, 'index.html', context)


def advertisements(request):
    propertys = Property.objects.filter(available=True,status='published').order_by('-created_at')
    category=Category.objects.all()
    paginator = Paginator(propertys, 3)  # Her sayfada 2 öğe gösterir
    page = request.GET.get('page')
    paged_propertys = paginator.get_page(page)

    context = {
        'propertys': propertys,
        'category':category,
        'paged_propertys': paged_propertys,


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
    paged_propertys = Property.objects.all().filter(category__slug=category_slug,available=True,status='published')
    category = Category.objects.all()
    context = {
        'paged_propertys': paged_propertys,
        'category': category
    }
    return render(request, 'properties.html', context)
def profile_show(request,id):
    properties_status = Property.objects.filter(owner=id, status='published',available=True).order_by('-created_at')
    paginator = Paginator(properties_status, 4)  # Her sayfada 2 öğe gösterir
    page = request.GET.get('page')
    paged_propertys = paginator.get_page(page)
    context={
        'properties_status':properties_status,
        'paged_propertys':paged_propertys
    }

    return render(request,'profile.html',context)