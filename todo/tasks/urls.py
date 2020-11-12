from django.urls import path

from .views import TaskList

app_name = 'tasks'

urlpatterns =[
    path('', TaskList.as_view(), name='task_list'),
]
