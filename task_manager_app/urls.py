from django.urls import path
from task_manager_app.views import *

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name="register"),
    path('task-status/', TaskStatusAPIView.as_view(), name="task_status"),
    path('task/', TaskAPIView.as_view(), name="task"),
    path('task/<int:pk>/', TaskAPIView.as_view(), name="task_update_delete"),
]

