from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import models, forms
import re


# Create your views here.
def sign_in(request):
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('accounts:profile', kwargs={'username': user.username}))
    return render(request, 'accounts/sign_in.html', {'form' : form})


@login_required
def sign_out(request):
    logout(request)
    return render(request, 'home.html')


def sign_up(request):
    user_form = forms.UserForm()
    if request.method == 'POST':
        user_form = forms.UserForm(request.POST)
        if user_form.is_valid():
            user = User.objects.create_user(
                username=user_form.cleaned_data.get('username'),
                email=user_form.cleaned_data.get('email'),
                password=user_form.cleaned_data.get('password')
            )
            models.Profile.create_profile(user=user)
            login(request, user)
            return HttpResponseRedirect(reverse('accounts:profile', kwargs={'username': user.username}))
    return render(request, "accounts/signup.html", {'user_form' : user_form})


@login_required
def change_password(request, username):
    user = get_object_or_404(User, username=username)
    form = forms.ChangePasswordForm()
    if request.method == 'POST':
        form = forms.ChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')
            if user.check_password(password):
                if new_password == confirm_password:
                    if re.match(new_password, user.first_name, re.I):
                        raise forms.ValidationError("Password shouldn't match with the first name")

                    if re.match(new_password, user.last_name, re.I):
                        raise forms.ValidationError("Password shouldn't match with the last name")
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                    return HttpResponseRedirect(reverse('accounts:profile', kwargs={'username': user.username}))
    return render(request, 'accounts/change_password.html', {'form' : form})


@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(models.Profile, user=user)
    profile_form = forms.ProfileForm(instance=profile)
    if request.method == 'POST':
        profile_form = forms.ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            # profile.first_name = profile_form.cleaned_data.get('first_name')
            # profile.last_name = profile_form.cleaned_data.get('last_name')
            # profile.dob = profile_form.cleaned_data.get('dob')
            # profile.bio = profile_form.cleaned_data.get('bio')
            # profile.avatar = profile_form.cleaned_data.get('avatar')
            # profile.hobbies = profile_form.cleaned_data.get('hobbies')
            # profile.city = profile_form.cleaned_data.get('city')
            # profile.favorite_pet = profile_form.cleaned_data.get('favorite_pet')
            # profile.save()
            profile_form.save()

            user.first_name = profile_form.cleaned_data.get('first_name')
            user.last_name = profile_form.cleaned_data.get('last_name')
            user.save()
            return HttpResponseRedirect(reverse('accounts:profile', kwargs={'username': user.username}))
    return render(request, "accounts/edit_profile.html", {'profile_form' : profile_form})


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "accounts/profile.html", {"user" : user})