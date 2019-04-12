from django.shortcuts import get_object_or_404
from django import forms
from django.contrib.auth.models import User
from .models import Profile
import re
import datetime


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=255)
    email = forms.CharField(max_length=255)
    verify_email = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        cleaned_data = super().clean()
        email = str(cleaned_data.get('email')).strip()
        verify_email = str(cleaned_data.get('verify_email')).strip()
        password = str(cleaned_data.get('password')).strip()
        confirm_password = str(cleaned_data.get('confirm_password')).strip()

        if email != verify_email:
            raise forms.ValidationError("Email doesn't match!")

        if password != confirm_password:
            raise forms.ValidationError("Password doesn't match!")


    # If email does not exist then raise a validation error
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            account = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        if account:
            raise forms.ValidationError("Email already taken. Try something else!")

    # must not have the password length less than 14 characters.
    # must use of both uppercase and lowercase letters
    # must include one or more numerical digits
    # must include one or more of special characters such as @, #, $
    def clean_password(self):
        value = self.cleaned_data.get('password')
        if len(value) < 14 :
            raise forms.ValidationError("Password Length must be atleast 14")
        if not re.findall(r'[a-z]+', value):
            raise forms.ValidationError("Password must contain lower case character")
        if not re.findall(r'[A-Z]+', value):
            raise forms.ValidationError("Password must contain upper case character")
        if not re.findall(r'[0-9]+', value):
            raise forms.ValidationError("Password must contain atleast one digit")
        if not re.findall(r'[@#$]+', value):
            raise forms.ValidationError("Password must contain atleast one special character such as @, #, $")
        return value


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'dob', 'bio', 'avatar', 'city', 'favorite_pet', 'hobbies']


    # If the bio data should be at least 10 words.
    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        verify_bio = bio.split()
        if len(verify_bio) < 10:
            raise forms.ValidationError("Please write at least 10 words.")
        return bio

    # To verify whether date of birth accept below format:
    # YYYY-MM-DD, MM/DD/YYYY, or MM/DD/YY.
    def clean_dob(self):
        formats = ("%Y-%m-d", "%m/%d/%Y", "%d/%m/%Y")
        dob = self.cleaned_data.get('dob')
        index = 3
        for item in formats:
            try:
                datetime.datetime.strptime(str(dob), item)
            except ValueError:
                index -= 1

        if index == 0:
            raise forms.ValidationError("Date of Birth not in valid format")
        else:
            return dob


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    # New password must not match with the old one.
    # new password and confirm password should match
    # must not contain the user name or parts of the user’s full name
    def clean(self):
        cleaned_data = super().clean()

        password = str(cleaned_data.get('password')).strip()
        new_password = str(cleaned_data.get('new_password')).strip()
        confirm_password = str(cleaned_data.get('confirm_password')).strip()

        if new_password == password:
            raise forms.ValidationError("New password must be same as old!")

        if new_password != confirm_password:
            raise forms.ValidationError("Password doesn't match!")

        # if re.match(new_password, cleaned_data['first_name'], re.I):
        #     raise forms.ValidationError("Password shouldn't match with the first name")
        #
        # if re.match(new_password, cleaned_data['last_name'], re.I):
        #     raise forms.ValidationError("Password shouldn't match with the last name")

    # must not have the password length less than 14 characters.
    # must use of both uppercase and lowercase letters
    # must include one or more numerical digits
    # must include one or more of special characters such as @, #, $
    def clean_new_password(self):
        value = self.cleaned_data.get('new_password')
        if len(value) < 14 :
            raise forms.ValidationError("Password Length must be atleast 14")
        if not re.findall(r'[a-z]+', value):
            raise forms.ValidationError("Password must contain lower case character")
        if not re.findall(r'[A-Z]+', value):
            raise forms.ValidationError("Password must contain upper case character")
        if not re.findall(r'[0-9]+', value):
            raise forms.ValidationError("Password must contain atleast one digit")
        if not re.findall(r'[@#$]+', value):
            raise forms.ValidationError("Password must contain atleast one special character such as @, #, $")
        return value


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = get_object_or_404(User, username=username)

        if len(username) == 0:
            raise forms.ValidationError("username field is Empty!")

        if user:
            return username
        else:
            raise forms.ValidationError("username does not exist!")

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = get_object_or_404(User, username=username)

        if len(password) == 0:
            raise forms.ValidationError("Password field Empty!")

        if user:
            if user.check_password(password):
                return password
            else:
                raise forms.ValidationError("username or Password incorrect")
        else:
            raise forms.ValidationError("username does not exist!")
