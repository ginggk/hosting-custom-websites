from django.shortcuts import render, redirect
from django.views import View
from app import forms
from . import models
from io import BytesIO
from zipfile import ZipFile
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.utils.encoding import smart_bytes, force_text


# Create your views here.
def ZipResponse(zip_string, zip_name):
    response = HttpResponse(zip_string, content_type='application/zip')
    response["Content-Disposition"] = f"attachment; filename={zip_name}.zip"
    return response


def build_zip(form):
    in_memory = BytesIO()

    zip = ZipFile(in_memory, "a")

    html_template = get_template('index.html')
    html_context = {
        'name': form.cleaned_data['name'],
        'personal_icon': form.cleaned_data['personal_icon'],
        'banner_picture': form.cleaned_data['banner_picture'],
        'pic1': form.cleaned_data['pic1'],
        'pic2': form.cleaned_data['pic2'],
        'pic3': form.cleaned_data['pic3'],
        'bio': form.cleaned_data['bio'],
        'twitter': form.cleaned_data['twitter'],
        'facebook': form.cleaned_data['facebook'],
        'instagram': form.cleaned_data['instagram'],
        'github': form.cleaned_data['github'],
        'email': form.cleaned_data['email'],
        'color': form.cleaned_data['color']
        # form data
    }

    css_template = get_template('style.css')
    css_context = {'color': form.cleaned_data['color']}

    html_rendered_template = html_template.render(html_context)
    css_rendered_template = css_template.render(css_context)

    zip.writestr("index.html", html_rendered_template)
    zip.writestr("style.css", css_rendered_template)

    # fix for Linux zip files read in Windows
    for file in zip.filelist:
        file.create_system = 0

    zip.close()

    in_memory.seek(0)
    return in_memory.read()


class WebsiteInfo(View):
    def get(self, request):
        return render(request, 'information.html',
                      {'InformationForm': forms.InformationForm()})

    def post(self, request):
        form = forms.InformationForm(request.POST)

        if form.is_valid():
            zip_string = build_zip(form)
            return ZipResponse(zip_string, "your_fancy_new_website")
        else:
            print(form.is_valid())
            print(form.cleaned_data)
            print(form.errors)
            return render(request, 'information.html',
                          {'InformationForm': form})
