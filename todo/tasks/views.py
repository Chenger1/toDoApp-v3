from django.views.generic import ListView


from .models import Task


class TaskList(ListView):
    model = Task
    template_name = 'task/list.html'
