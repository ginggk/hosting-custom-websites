from django.shortcuts import render, redirect
from django.views import View
from app import forms
from . import models

# Create your views here.


class WebsiteInfo(View):
    def get(self, request):
        return render(request, 'information.html',
                      {'InformationForm': forms.InformationForm()})

    # def post(self, request):
    #     form = forms.InformationForm(data=request.POST)
    #     if form.is_valid():
    #         name = form.cleaned_data['name']
    #         return redirect('information')
    #     else:
    #         return render(request, 'index.html', {'InformationForm': form})
