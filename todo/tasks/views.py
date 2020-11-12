from django.views.generic import ListView


from .models import Task, Category


class TaskList(ListView):
    queryset = None
    template_name = 'task/list.html'

    def get(self, request, *args, **kwargs):
        task_queryset = Task.objects.filter(author=request.user)
        categories_queryset = Category.objects.filter(author=request.user)

        self.queryset = {
            'tasks': task_queryset,
            'categories': categories_queryset
        }
        return super().get(request, *args, **kwargs)
