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
        'name': form.cleaned_data['name']
        # form data
    }

    html_rendered_template = html_template.render(html_context)

    zip.writestr("index.html", html_rendered_template)
    # zip.writestr("styles.css", css_rendered_template)

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
