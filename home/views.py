from django.shortcuts import render, HttpResponse
from django.views import View


class Home(View):
    template_name = 'home/home.html'
    def get(self, request):
        return render(request, self.template_name)