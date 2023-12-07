from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from accountapp.decorators import account_ownership_required
from accountapp.forms import CustomUserCreationForm, CustomUserUpdateForm , CustomUserDeleteForm


# Create your views here.


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accountapp/create.html'
    success_url = reverse_lazy('main')


has_ownership = [login_required, account_ownership_required]

@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class UserUpdateView(UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    context_object_name = 'target_user'
    template_name = 'accountapp/update.html'
    success_url = reverse_lazy('accountapp:logout')


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class UserDeleteView(DeleteView):
    model = User
    form_class = CustomUserDeleteForm
    context_object_name = 'target_user'
    success_url = reverse_lazy('main')
    template_name = 'accountapp/delete.html'
