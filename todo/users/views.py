from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from tasks.models import Task, Category


class UserRegistrationView(CreateView):
    template_name = 'users/user/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self.request, user)
        return result


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user/detail.html'
    user = None

    def get(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, pk=kwargs['pk'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        task_queryset = Task.objects.filter(author=self.user)
        task_counter = task_queryset.count()
        category_queryset = Category.objects.filter(author=self.user)

        result['tasks'] = task_queryset
        result['counter'] = task_counter
        result['categories'] = category_queryset

        return result
