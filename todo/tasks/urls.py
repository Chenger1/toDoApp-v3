from django.urls import path

from .views import TaskList, CreateCategoryView, CreateTaskView, TaskRemoveView, TaskUpdateView, TaskDetailView

app_name = 'tasks'

urlpatterns =[
    path('', TaskList.as_view(), name='task_list'),
    path('category/<int:category_id>/', TaskList.as_view(), name='task_list_in_category'),
    path('create-category/', CreateCategoryView.as_view(), name='create_category'),
    path('create-task/', CreateTaskView.as_view(), name='create_task'),
    path('remove-task/<slug:slug>/', TaskRemoveView.as_view(), {'status': True}, name='remove_task'),
    path('update-task/<slug:slug>/', TaskUpdateView.as_view(), name='update_task'),
    path('task-detail/<slug:slug>/', TaskDetailView.as_view(), name='task_detail'),
]
