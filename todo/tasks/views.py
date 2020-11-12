from django.views.generic import ListView


from .models import Task


class TaskList(ListView):
    queryset = None
    template_name = 'task/list.html'

    def get(self, request, *args, **kwargs):
        self.queryset = Task.objects.filter(author=request.user)
        return super().get(request, *args, **kwargs)
