from django import forms

class CreateForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    price = forms.IntegerField(required=True)

class UpdateForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    price = forms.IntegerField(required=True)

class CommentForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5, required=True)
    comment = forms.CharField(max_length=100, required=True)

class SignupForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    email = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=30, required=True)
    passwordConfirm = forms.CharField(max_length=30, required=True)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=30, required=True)

