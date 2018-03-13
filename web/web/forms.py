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
