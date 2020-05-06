from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from car.models import Category
from home.models import UserProfile
from user.forms import UserUpdateForm, ProfileUpdateForm


def index(request):
    category = Category.objects.all()
    current_user = request.user

    profile = UserProfile.objects.get(user_id=current_user.id)
    name = profile.user_name
    context = {
        'category': category,
        'profile': profile,
        'name': name,
    }
    return render(request, 'user_profile.html', context)

def user_update(request):
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
            }
            return render(request, 'user_update.html', context)
        else:
            context = {
                'category': category,
                'user_form': user_form,
                'profile_form': profile_form,
            }
            return render(request, 'user_update.html', context)

def change_password(request):
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
            })
        else:
            return render(request, 'change_password.html', {
                'form': form,
                'category': category,
            })