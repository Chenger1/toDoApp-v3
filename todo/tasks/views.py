from django.views.generic import ListView
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CreateCategoryForm, CreateSubTaskFormSet, CreateTaskForm

from .models import Task, Category, Subtask


class TaskList(ListView):
    queryset = None
    template_name = 'task/list.html'

    def get(self, request, *args, **kwargs):
        category = kwargs.get('category_id')
        try:
            if category:
                task_queryset = Task.objects.filter(author=request.user, category=category, removed=False)
            else:
                task_queryset = Task.objects.filter(author=request.user, removed=False)
            categories_queryset = Category.objects.filter(author=request.user)
        except TypeError:
            # If request.user == AnonymousUser
            return redirect('users:login')

        else:
            self.queryset = {
                'tasks': task_queryset,
                'categories': categories_queryset,
                'current_category': category
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
        task_form = CreateTaskForm(request.user, data=request.POST)
        subtask_form = CreateSubTaskFormSet(data=request.POST)

        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.author = request.user
            task.save()
            request.user.total_tasks += 1
            request.user.save()

            cd = list(filter(lambda x: len(x) > 0, subtask_form.cleaned_data))
            if subtask_form.is_valid() and cd:
                for form in cd:
                    subtask = Subtask.objects.create(title=form['title'],
                                                     task=task)
                    subtask.save()

        return redirect('tasks:task_list')


class TaskRemoveView(View):
    def post(self, request, slug, status):
        task = get_object_or_404(Task, slug__iexact=slug,
                                 author=request.user)
        task.removed = status
        task.save()

        return redirect('tasks:task_list')


class TaskUpdateView(View):
    template = 'task/update_task.html'

    def get(self, request, slug):
        task = get_object_or_404(Task,
                                 slug__iexact=slug, author=request.user)

        task_form = CreateTaskForm(request.user, instance=task)
        subtasks_forms = CreateSubTaskFormSet(instance=task)

        return render(request, self.template, {'task_form': task_form,
                                               'subtasks_forms': subtasks_forms})

    def post(self, request, slug):
        task = get_object_or_404(Task,
                                 slug__iexact=slug, author=request.user)
        task_form = CreateTaskForm(request.user, request.POST, instance=task)
        subtask_form = CreateSubTaskFormSet(data=request.POST, instance=task)

        if task_form.is_valid():
            updated_task = task_form.save(commit=False)

            if subtask_form.is_valid():
                subtask_form.save()
                updated_task.save()

        return redirect('tasks:task_list')


class TaskDetailView(DetailView):
    model = Task
    template_name = 'task/detail.html'


class MarkAsDoneMixin(View):
    models = {
        'Task': Task,
        'Subtask': Subtask
    }

    def post(self, request, slug, model_name, template, status):
        model = self.models[model_name]
        obj = get_object_or_404(model,
                                slug__iexact=slug)
        obj.status = status
        obj.save()

        if template == 'list':
            return redirect('tasks:task_list')
        elif template == 'detail':
            if model_name == 'Subtask':
                slug = obj.task.slug
            return redirect('tasks:task_detail', slug=slug)


class TaskHistoryView(ListView):
    model = Task
    template_name = 'task/history.html'

    def get(self, request, *args, **kwargs):
        task_queryset = Task.objects.filter(author=request.user)
        self.queryset = {
            'tasks': task_queryset
        }
        return super().get(request, *args, **kwargs)


class ObjectDeleteMixin(View):
    models = {
        'Task': Task,
        'Subtask': Subtask
    }
    model = None

    def post(self, request, slug, model_name, template):
        self.model = self.models[model_name]
        obj = get_object_or_404(self.model,
                                slug__iexact=slug)
        obj.delete()

        if template == 'detail':
            slug = obj.task.slug
            return redirect('tasks:task_detail', slug=slug)
        elif template == 'history':
            return redirect('tasks:task_history')
