from django.urls import path
from .views import SignUpView
<<<<<<< HEAD
from django.contrib.auth import views as auth_views
=======
>>>>>>> 83291be23de4ee3ca6cf180de73b752c7840ca55


urlpatterns = [
    
    path('', SignUpView.as_view(), name='signup'),
<<<<<<< HEAD
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
=======
>>>>>>> 83291be23de4ee3ca6cf180de73b752c7840ca55
]
