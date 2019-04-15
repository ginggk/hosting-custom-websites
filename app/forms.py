from django import forms


class InformationForm(forms.Form):
    name = forms.CharField()
