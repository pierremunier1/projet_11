from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

<<<<<<< HEAD
from .forms import CustomUserCreationForm, CustomUserChangeForm
=======
from .forms import CustomUserCreationForm
>>>>>>> 83291be23de4ee3ca6cf180de73b752c7840ca55

class SignUpView(CreateView):
    """signupview"""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
<<<<<<< HEAD
    

=======
>>>>>>> 83291be23de4ee3ca6cf180de73b752c7840ca55
