from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # path('', views.dashboard, name='dashboard'),
    path('register/',views.register,name='register'),
    path('login/',views.login_page,name='login'),
    path('student_dashboard/',views.student_dashboard,name='student_dashboard'),
    path('update_user/<id>/',views.update_user,name='update_user'),
    path('logout/',views.logout_page,name='logout'),



]


# if settings.DEBUG :
#     urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

# urlpatterns += staticfiles_urlpatterns()