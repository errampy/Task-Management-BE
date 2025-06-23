from pyexpat.errors import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from task_manager_app.serializers import UserRegistrationSerializer, TaskStatusSerializer, TaskSerializer, TaskCreateUpdateSerializer
from rest_framework import permissions
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from task_manager_app.models import TaskStatus, Task
from django.db.models import Q
from django.shortcuts import get_object_or_404


# Create your views here.
class UserRegistrationAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                # Manually hash the password before saving
                password = make_password(serializer.validated_data['password'])
                user_data = serializer.validated_data
                user_data['password'] = password

                # Create the user with hashed password
                User.objects.create(**user_data)
                return Response(data="Successfully", status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(data={"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)


class TaskStatusAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TaskStatusSerializer

    @swagger_auto_schema(responses={200: TaskStatusSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = TaskStatus.objects.all()
            serializer = TaskStatusSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(data={"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=TaskStatusSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = TaskStatusSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data="Successfully", status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(data={"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)


class TaskAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer

    @swagger_auto_schema(responses={200: TaskSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            status_id = request.GET.get('status', None)
            task_id = request.GET.get('task_id', None)
            if task_id is not None:
                try:
                    obj = Task.objects.get(pk=task_id)
                    serializer = TaskCreateUpdateSerializer(obj)
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                except Task.DoesNotExist:
                    return Response(data=None, status=status.HTTP_400_BAD_REQUEST)
            if status_id:
                records = Task.objects.filter(
                    Q(user=request.user) & Q(status_id=status_id))
            else:
                records = Task.objects.filter(user=request.user)

            serializer = TaskSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(data={"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=TaskSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = TaskCreateUpdateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(data="Successfully", status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(data={"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=TaskSerializer)
    def put(self, request, *args, **kwargs):
        try:
            task_id = kwargs.get('pk')
            task = get_object_or_404(Task, id=task_id, user=request.user)
            serializer = TaskCreateUpdateSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data="Updated Successfully", status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(data={"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            task_id = kwargs.get('pk')
            task = get_object_or_404(Task, id=task_id, user=request.user)
            task.delete()
            return Response(data="Deleted Successfully", status=status.HTTP_204_NO_CONTENT)
        except Exception as error:
            return Response(data={"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
