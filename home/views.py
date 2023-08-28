from typing import Any
from django import http
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from . forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib import messages



class Home(View):
    template_name = 'home/home.html'
    def get(self, request):
        return render(request, self.template_name)
    

class About(View):
    template_name = 'home/home.html'
    def get(self, request):
        return render(request, self.template_name)
    


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'home/register.html'


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})
    

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, 'Registered', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})
            