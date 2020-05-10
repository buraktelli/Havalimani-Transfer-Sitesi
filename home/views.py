import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from car.models import Car, Category, Images, Comment
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormMessage, ContactFormu, UserProfile, UserProfileForm


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Car.objects.all()[:5]
    category = Category.objects.all()
    randomcars = Car.objects.all().order_by('?')[:4]
    lastcars = Car.objects.all().order_by('-id')[:8]
    if request.user.is_authenticated:
        current_user = request.user

        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {'setting': setting,
                   'category': category,
                   'page': 'home',
                   'sliderdata': sliderdata,
                   'randomcars': randomcars,
                   'lastcars': lastcars,
                   'profile': profile,
                   }
    else:
        context = {'setting': setting,
                   'category': category,
                   'page': 'home',
                   'sliderdata': sliderdata,
                   'randomcars': randomcars,
                   'lastcars': lastcars,
                   }
    return render(request, 'index.html', context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    if request.user.is_authenticated:
        current_user = request.user
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {'setting':setting, 'page':'hakkimizda', 'category':category, 'profile': profile}
    else:
        context = {'setting': setting, 'page': 'hakkimizda', 'category': category}
    return render(request,'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    if request.user.is_authenticated:
        current_user = request.user
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {'setting':setting, 'page':'referanslar', 'category':category, 'profile': profile}
    else:
        context = {'setting': setting, 'page': 'referanslar', 'category': category}
    return render(request,'referanslar.html', context)

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
    category = Category.objects.all()
    if request.user.is_authenticated:
        current_user = request.user
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {'setting':setting, 'form':form, 'category':category, 'profile': profile}
    else:
        context = {'setting': setting, 'form': form, 'category': category}
    return render(request,'iletisim.html', context)

def category_cars(request, id, slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    cars = Car.objects.filter(category_id=id)
    if request.user.is_authenticated:
        current_user = request.user
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {'cars': cars,
               'category': category,
               'categorydata': categorydata,
               'setting': setting,
               'profile': profile,
               }
    else:
        context = {'cars': cars,
                   'category': category,
                   'categorydata': categorydata,
                   'setting': setting,
                   }
    return render(request, 'cars.html', context)

def car_detail(request, id, slug):
    category = Category.objects.all()
    car = Car.objects.get(pk=id)
    images = Images.objects.filter(car_id=id)
    comments = Comment.objects.filter(car_id=id, status='True')
    if request.user.is_authenticated:
        current_user = request.user
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {'category': category,
               'car': car,
               'images': images,
               'comments': comments,
               'profile': profile,
               }
    else:
        context = {'category': category,
                   'car': car,
                   'images': images,
                   'comments': comments,
                   }
    return render(request, 'car_detail.html', context)

def car_search(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()

            query = form.cleaned_data['queryyy']
            catid = form.cleaned_data['catid']
            print(catid)
            if catid == 0:
                cars = Car.objects.filter(title__icontains=query)
            else:
                cars = Car.objects.filter(title__icontains=query, category_id=catid)
            if request.user.is_authenticated:
                current_user = request.user
                profile = UserProfile.objects.get(user_id=current_user.id)
                context = {
                    'cars': cars,
                    'category': category,
                    'setting': setting,
                    'profile': profile,
                }
            else:
                context = {
                    'cars': cars,
                    'category': category,
                    'setting': setting,
                }
            return render(request, 'cars_search.html', context)

    return HttpResponseRedirect('/')

def car_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        places = Car.objects.filter(title__icontains=q)
        results = []
        for pl in places:
            place_json = {}
            place_json = pl.title
            results.append(place_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.error(request, "Login Hatası ! Kullanıcı adı veya şifre yanlış. ")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    if request.user.is_authenticated:
        current_user = request.user
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {
            'category': category,
            'profile': profile,
        }
    else:
        context = {
            'category': category,
        }
    return render(request, 'login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            form = UserProfileForm()
            category = Category.objects.all()
            context = {
                'category': category,
                'form': form,
            }
            #return render(request, 'addprofile.html', context)
            return render(request, 'signup.html', context)


    if request.user.is_authenticated:
        current_user = request.user
        profile = UserProfile.objects.get(user_id=current_user.id)
        form = SignUpForm()
        category = Category.objects.all()
        context = {
            'category': category,
            'form': form,
            'profile': profile,
        }
    else:
        form = SignUpForm()
        category = Category.objects.all()
        context = {
            'category': category,
            'form': form,
        }
    return render(request, 'signup.html', context)


def addprofile(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        data = UserProfile
        #profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid():# and profile_form.is_valid():
            user_form.save()
            data = user_form
            data.save()
            #profile_form.save()
            messages.success(request, 'Your account has been created!')
            form = UserProfileForm()
            category = Category.objects.all()
            context = {
                'category': category,
                'form': form,
            }
            return render(request, 'addprofile.html', context)

    form = UserProfileForm()
    category = Category.objects.all()
    context = {
        'category': category,
        'form': form,
    }

    return render(request, 'addprofile.html', context)