from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('tasks/', views.TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/members/', views.ViewTaskMembersView.as_view(), name='task-members'),
    path('tasks/<int:pk>/members/add-remove/', views.AddRemoveTaskMemberView.as_view(), name='add-remove-task-member'),
    path('tasks/<int:pk>/status/', views.UpdateTaskStatusView.as_view(), name='update-task-status'),
    path('create-user/', views.CreateUserView.as_view(), name='create-user'),
]