from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer, TaskCreateUpdateSerializer, UserSerializer


class Index(APIView):
    def get(self, request):
        return Response({'Status': "Success"})


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if username and password:
            user = User.objects.create_user(username=username, password=password, email=email)
            return Response({"message": "User created successfully"}, status=200)
        return Response({"error": "Invalid data"}, status=400)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=401)


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save()


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateUpdateSerializer


class CreateUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({"error": "Username, email, and password are required."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"message": "User created successfully", "user_id": user.id}, status=201)


class AddRemoveTaskMemberView(APIView):
    def post(self, request, pk):
        task = Task.objects.get(pk=pk)
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({"error": "User ID is required."}, status=400)

        user = User.objects.get(pk=user_id)
        
        if user in task.members.all():
            return Response({"status": "User is already a member of this task."}, status=400)
        else:
            task.members.add(user)
            return Response({"status": "User added to task successfully."})

    def delete(self, request, pk):
        task = Task.objects.get(pk=pk)
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({"error": "User ID is required."}, status=400)

        user = User.objects.get(pk=user_id)
        
        if user in task.members.all():
            task.members.remove(user)
            return Response({"status": "User removed from task successfully."})
        else:
            return Response({"error": "User is not a member of this task."}, status=400)


class ViewTaskMembersView(APIView):
    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        members = task.members.all()
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data)


class UpdateTaskStatusView(APIView):
    def patch(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.status = request.data.get('status')
        task.save()
        return Response({"status": "success"})
