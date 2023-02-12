from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import render, redirect


class SignUpView(View):
    model = User
    template_name = "registration/signup.html"
    success_url = reverse_lazy('login')

    def get(self, request):
        return render(request, self.template_name, {'form': UserCreationForm()})

    def post(self, request):
        form = UserCreationForm(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        form.save()

        return redirect(self.success_url)
