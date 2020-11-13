from django.views.generic import ListView
from django.views.generic import View
from django.shortcuts import render, redirect

from .forms import CreateCategoryForm


from .models import Task, Category


class TaskList(ListView):
    queryset = None
    template_name = 'task/list.html'

    def get(self, request, *args, **kwargs):
        try:
            task_queryset = Task.objects.filter(author=request.user)
            categories_queryset = Category.objects.filter(author=request.user)
        except TypeError:
            # If request.user == AnonymousUser
            return redirect('users:login')

        else:
            self.queryset = {
                'tasks': task_queryset,
                'categories': categories_queryset
            }
            return super().get(request, *args, **kwargs)


class CreateCategoryView(View):
    template = 'task/create_category.html'

    def get(self, request):
        form = CreateCategoryForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = CreateCategoryForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.author = request.user
            new_category.save()
            return redirect('tasks:task_list')

        return render(request, self.template, {'form': form})
