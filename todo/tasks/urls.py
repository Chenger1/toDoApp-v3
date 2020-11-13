from django.urls import path

from .views import TaskList, CreateCategoryView

app_name = 'tasks'

urlpatterns =[
    path('', TaskList.as_view(), name='task_list'),
    path('create-category/', CreateCategoryView.as_view(), name='create_category'),
]
