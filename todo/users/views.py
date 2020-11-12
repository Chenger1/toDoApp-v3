from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


class UserRegistrationView(CreateView):
    template_name = 'users/user/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('tasks.task_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password'])
        login(self.request, user)
        return result
