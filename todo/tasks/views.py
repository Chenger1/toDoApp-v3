from django.views.generic import ListView
from django.views.generic import View
from django.shortcuts import render, redirect

from .forms import CreateCategoryForm, CreateSubTaskFormSet, CreateTaskForm


from .models import Task, Category, Subtask


class TaskList(ListView):
    queryset = None
    template_name = 'task/list.html'

    def get(self, request, *args, **kwargs):
        category = kwargs.get('category_id')
        try:
            if category:
                task_queryset = Task.objects.filter(author=request.user, category=category)
            else:
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


class CreateTaskView(View):
    template = 'task/create_task.html'

    def get(self, request):
        task_form = CreateTaskForm(request.user)
        subtask_form = CreateSubTaskFormSet()
        return render(request, self.template, {'form': task_form,
                                               'subtasks': subtask_form})

    def post(self, request):
        task_form = CreateTaskForm(request.user, request.POST)
        subtask_form = CreateSubTaskFormSet(request.POST)

        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.author = request.user
            task.save()

            cd = list(filter(lambda x: len(x) > 0, subtask_form.cleaned_data))
            if subtask_form.is_valid() and cd:
                for form in cd:
                    subtask = Subtask.objects.create(title=form['title'],
                                                     task=task)
                    subtask.save()

        return redirect('tasks:task_list')
