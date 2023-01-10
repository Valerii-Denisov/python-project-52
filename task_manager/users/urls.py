from django.urls import path

from task_manager.users import views

urlpatterns = [
    path('', views.UsersView.as_view(), name='users'),
    path('user_create/', views.UserRegister.as_view(), name='user_create'),
    path('<int:id>/edit/', views.UserEdit.as_view(), name='user_edit'),
    path('<int:id>/delete/', views.UserDelete.as_view(), name='user_destroy'),
]
