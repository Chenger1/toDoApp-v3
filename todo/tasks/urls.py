from django.urls import path

from .views import TaskList, CreateCategoryView, CreateTaskView, TaskRemoveView

app_name = 'tasks'

urlpatterns =[
    path('', TaskList.as_view(), name='task_list'),
    path('category/<int:category_id>/', TaskList.as_view(), name='task_list_in_category'),
    path('create-category/', CreateCategoryView.as_view(), name='create_category'),
    path('create-task/', CreateTaskView.as_view(), name='create_task'),
    path('remove-task/<slug:slug>/', TaskRemoveView.as_view(), {'status': True}, name='remove_task'),
]
