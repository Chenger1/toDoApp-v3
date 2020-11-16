from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskList.as_view(), name='task_list'),
    path('category/<int:category_id>/', views.TaskList.as_view(), name='task_list_in_category'),
    path('create-category/', views.CreateCategoryView.as_view(), name='create_category'),
    path('create-task/', views.CreateTaskView.as_view(), name='create_task'),
    path('remove-task/<slug:slug>/', views.TaskRemoveView.as_view(), {'status': True}, name='remove_task'),
    path('update-task/<slug:slug>/', views.TaskUpdateView.as_view(), name='update_task'),
    path('task-detail/<slug:slug>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('mark-as-done/<slug:slug>/<str:model_name>/<str:template>/', views.MarkAsDoneMixin.as_view(),
         {'status': True}, name='mark_as_done'),
    path('mark-as-not-done/<slug:slug>/<str:model_name>/<str:template>/', views.MarkAsDoneMixin.as_view(),
         {'status': False}, name='mark_as_not_done'),
]
