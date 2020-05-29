from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from car.models import CommentForm, Comment, ReservationForm, Reservation, Category, Car, ReservationListForm
from home.models import Setting, UserProfile


def index(request):
    return HttpResponse("Product Page")


@login_required(login_url='/login')
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user

            data = Comment()
            data.user_id = current_user.id
            data.car_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            messages.success(request, "Yorumunuz başarı ile kaydedilmiştir. Teşekkür ederiz....")

            return HttpResponseRedirect(url)

    messages.warning(request, "Yorumunuz kaydedilemedi... Kontrol ediniz...")
    return HttpResponseRedirect(url)

@login_required(login_url='/login')
def addreservation(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            current_user = request.user

            #Bankadan ödeme onayı gelirse devam et
            data = Reservation()
            data.user_id = current_user.id
            data.car_id = id
            data.name = current_user.first_name
            data.surname = current_user.last_name
            data.distance = form.cleaned_data['distance']
            data.date = form.cleaned_data['date']
            data.time = form.cleaned_data['time']
            data.phone = form.cleaned_data['phone']
            data.start_from = form.cleaned_data['start_from']
            data.destination_to = form.cleaned_data['destination_to']
            data.kisi_sayisi = form.cleaned_data['kisi_sayisi']
            data.address = form.cleaned_data['address']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            messages.success(request, "Rezervasyon başarı ile kaydedilmiştir. Teşekkür ederiz....")

            return HttpResponseRedirect('/')

    messages.warning(request, "Rezervasyon kaydedilemedi... Kontrol ediniz...")
    return HttpResponseRedirect(url)

@login_required(login_url='/login')
def reservation_list(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    categorydata = Category.objects.all()
    if request.method == 'POST':
        form = ReservationListForm(request.POST)
        if form.is_valid():
            kisi_sayisi = form.cleaned_data['kisi_sayisi']
            start_from = form.cleaned_data['start_from']
            destination_to = form.cleaned_data['destination_to']

    cars = Car.objects.filter(kisi_sayisi=kisi_sayisi)
    if request.user.is_authenticated:
        current_user = request.user
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {'cars': cars,
                   'category': category,
                   'categorydata': categorydata,
                   'setting': setting,
                   'profile': profile,
                   'kisi_sayisi': kisi_sayisi,
                   'start_from': start_from,
                   'destination_to': destination_to,
                   }
    else:
        context = {'cars': cars,
                   'category': category,
                   'categorydata': categorydata,
                   'setting': setting,
                   'kisi_sayisi': kisi_sayisi,
                   'start_from': start_from,
                   }
    return render(request, 'rezerv_list.html', context)

def reservation(request, id):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    categorydata = Category.objects.all()
    car = Car.objects.get(pk=id)
    if request.method == 'POST':
        form = ReservationListForm(request.POST)
        if form.is_valid():
            kisi_sayisi = form.cleaned_data['kisi_sayisi']
            date = form.cleaned_data['date']
            distance = form.cleaned_data['distance']
            start_from = form.cleaned_data['start_from']
            destination_to = form.cleaned_data['destination_to']

        total = distance*car.price

    if request.user.is_authenticated:
        current_user = request.user
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {'car': car,
                   'category': category,
                   'categorydata': categorydata,
                   'setting': setting,
                   'profile': profile,
                   'kisi_sayisi': kisi_sayisi,
                   'date': date,
                   'start_from': start_from,
                   'destination_to': destination_to,
                   'total': total,
                   'distance': distance,
                   }
    else:
        context = {'car': car,
                   'category': category,
                   'categorydata': categorydata,
                   'setting': setting,
                   'kisi_sayisi': kisi_sayisi,
                   'date': date,
                   'start_from': start_from,
                   'destination_to': destination_to,
                   'total': total,
                   'distance': distance,
                   }
    return render(request, 'reservation.html', context)