from django.urls import path

from task_manager.statuses import views

urlpatterns = [
    path('', views.StatusView.as_view(), name='statuses'),
    path('create/', views.StatusRegister.as_view(), name='status_create'),
    path('<int:id>/edit/', views.StatusEdit.as_view(), name='status_edit'),
    path('<int:id>/delete/', views.StatusDelete.as_view(), name='status_destroy'),
]
