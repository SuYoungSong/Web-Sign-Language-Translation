from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accountapp.forms import CustomAuthenticationForm
from accountapp.views import UserCreateView, UserDetailView, UserUpdateView, UserDeleteView

app_name = 'accountapp'

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='create'),
    path('detail/<int:pk>', UserDetailView.as_view(), name='detail'),
    path('update/<int:pk>', UserUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', UserDeleteView.as_view(), name='delete'),
    path('login/', LoginView.as_view(authentication_form=CustomAuthenticationForm , template_name='accountapp/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
