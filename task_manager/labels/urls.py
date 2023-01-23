from django.urls import path

from task_manager.labels import views

urlpatterns = [
    path('', views.LabelView.as_view(), name='labels'),
    path('create/', views.LabelRegister.as_view(), name='label_create'),
    path('<int:id>/update/', views.LabelEdit.as_view(), name='label_edit'),
    path('<int:id>/delete/', views.LabelDelete.as_view(), name='label_destroy'),
]
