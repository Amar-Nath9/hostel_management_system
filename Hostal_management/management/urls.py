from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dashboard'),
    path('management-login/', views.management_login, name='management_login'),
    path('management/', views.management_dashboard, name="management_dashboard"),
    path('amar_profile/', views.amar_profile, name='amar_profile'),
    path('management/update/<int:user_id>/', views.update_student, name='update_student'),
    path('management/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('management/add-payment/<int:user_id>/', views.add_payment, name='add_payment'),  
    path('management/approve-payment/<int:payment_id>/', views.approve_payment, name='approve_payment'),
    path('management/disapprove-payment/<int:payment_id>/', views.disapprove_payment, name='disapprove_payment'),
]
