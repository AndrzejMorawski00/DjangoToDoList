from django.urls import path
from . import views

app_name='todo'

urlpatterns = [
    path('', views.index, name="home-view"),
    path('<order>', views.task_sorting, name='sort-tasks'),
    path('add-new/', views.add_new, name='add-new'),
    path('edit-task/<slug:task_slug>', views.edit_task, name="edit-task"),
    path("task-operation/<slug:task_slug>/<operation>/", views.task_operation, name='task-operation'),
]
