from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from car.models import Car, Category, Images
from home.models import Setting, ContactFormMessage, ContactFormu


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Car.objects.all()[:5]
    category = Category.objects.all()
    randomcars = Car.objects.all().order_by('?')[:4]
    lastcars = Car.objects.all().order_by('-id')[:8]

    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'sliderdata': sliderdata,
               'randomcars': randomcars,
               'lastcars': lastcars}
    return render(request, 'index.html', context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting':setting, 'page':'hakkimizda'}
    return render(request,'hakkimizda.html',context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting':setting, 'page':'referanslar'}
    return render(request,'referanslar.html',context)

def iletisim(request):
    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız başarıyla gönderilmiştir. Teşekkür ederiz.")
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting':setting, 'form':form}
    return render(request,'iletisim.html',context)

def category_cars(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    cars = Car.objects.filter(category_id=id)
    context = {'cars': cars,
               'category': category,
               'categorydata': categorydata,
               }
    return render(request, 'cars.html', context)

def car_detail(request, id, slug):
    category = Category.objects.all()
    car = Car.objects.get(pk=id)
    images = Images.objects.filter(car_id=id)
    context = {'category': category,
               'car': car,
               'images': images,
               }
    return render(request, 'car_detail.html', context)