from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='dashboard'),

    path('management-login/',views.management_login, name='management_login'),
    path('management/',views.management_dashboard,name="management_dashboard"),
    path('amar_profile/',views.amar_profile, name='amar_profile'),
    path('student/update/<int:user_id>/', views.update_student, name='update_student'),

]