from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from car.models import Category, Comment, Reservation
from home.models import UserProfile, Setting
from user.forms import UserUpdateForm, ProfileUpdateForm


def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user

    profile = UserProfile.objects.get(user_id=current_user.id)
    name = profile.user_name
    context = {
        'category': category,
        'profile': profile,
        'name': name,
        'setting': setting,
    }
    return render(request, 'user_profile.html', context)

def user_update(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('/user')

    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        if request.user.is_authenticated:
            current_user = request.user
            profile = UserProfile.objects.get(user_id=current_user.id)
            context = {
                'category': category,
                'user_form': user_form,
                'profile_form': profile_form,
                'profile': profile,
                'setting': setting,
            }
            return render(request, 'user_update.html', context)
        else:
            context = {
                'category': category,
                'user_form': user_form,
                'profile_form': profile_form,
                'setting': setting,
            }
            return render(request, 'user_update.html', context)

def change_password(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password/')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        if request.user.is_authenticated:
            current_user = request.user
            profile = UserProfile.objects.get(user_id=current_user.id)
            return render(request, 'change_password.html', {
                'form': form,
                'category': category,
                'profile': profile,
                'setting': setting,
            })
        else:
            return render(request, 'change_password.html', {
                'form': form,
                'category': category,
                'setting': setting,
            })

@login_required(login_url='/login')
def comments(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id = current_user.id)
    if current_user.is_authenticated:
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {
            'category': category,
            'comments': comments,
            'profile': profile,
            'setting': setting,
        }
        return render(request, 'user_comments.html', context)
    else:
        context = {
            'category': category,
            'comments': comments,
            'setting': setting,
        }
        return render(request, 'user_comments.html', context)

@login_required(login_url='/login')
def deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id = id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted...')
    return HttpResponseRedirect('/user/comments')

@login_required(login_url='/login')
def reservations(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    reservations = Reservation.objects.filter(user_id = current_user.id)
    if current_user.is_authenticated:
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {
            'category': category,
            'reservations': reservations,
            'profile': profile,
            'setting': setting,
        }
        return render(request, 'user_reservations.html', context)
    else:
        context = {
            'category': category,
            'reservations': reservations,
            'setting': setting,
        }
        return render(request, 'user_reservations.html', context)

@login_required(login_url='/login')
def deletereservation(request, id):
    current_user = request.user
    Reservation.objects.filter(id = id, user_id=current_user.id).delete()
    messages.success(request, 'Rezervation deleted...')
    return HttpResponseRedirect('/user/reservations')