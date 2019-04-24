from django import forms


class InformationForm(forms.Form):
    name = forms.CharField()
    personal_icon = forms.URLField()
    color = forms.CharField()
    banner_picture = forms.URLField()
    pic1 = forms.URLField()
    pic2 = forms.URLField()
    pic3 = forms.URLField()
    bio = forms.CharField()
    twitter = forms.URLField()
    facebook = forms.URLField()
    instagram = forms.URLField()
    github = forms.URLField()
    email = forms.EmailField()
