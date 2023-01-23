from django.urls import path

from task_manager.tasks import views

urlpatterns = [
    path('', views.TaskView.as_view(), name='tasks'),
    path('create/', views.TaskRegister.as_view(), name='task_create'),
    path('<int:id>/update/', views.TaskEdit.as_view(), name='task_edit'),
    path('<int:id>/delete/', views.TaskDelete.as_view(), name='task_destroy'),
    path('<int:id>/', views.OneTaskView.as_view(), name='task_see'),
]
