from django.urls import path
from .views import RegisterationView,LoginView 

urlpatterns = [
    path("register/",RegisterationView.as_view(),name="register"),
    path("login/",LoginView.as_view(),name="login"),
]

# vSgGF158EWT0Xs7v