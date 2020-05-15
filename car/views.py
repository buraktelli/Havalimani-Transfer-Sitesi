from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from car.models import CommentForm, Comment, ReservationForm, Reservation


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


def addreservation(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            current_user = request.user

            data = Reservation()
            data.user_id = current_user.id
            data.car_id = id
            data.name = current_user.first_name
            data.surname = current_user.last_name
            data.start_hour = form.cleaned_data['start_hour']
            data.hours = form.cleaned_data['hours']
            data.check_in = form.cleaned_data['check_in']

            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            messages.success(request, "Rezervasyon başarı ile kaydedilmiştir. Teşekkür ederiz....")

            return HttpResponseRedirect('/')

    messages.warning(request, "Rezervasyon kaydedilemedi... Kontrol ediniz...")
    return HttpResponseRedirect(url)