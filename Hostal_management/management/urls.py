from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='dashboard'),

    path('login_page/',views.login_page),
    # path('register/',views.register,name="register"),
    path('amar_profile/',views.amar_profile, name='amar_profile'),


]