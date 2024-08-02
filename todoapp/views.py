import json
from django.http import FileResponse,HttpResponseRedirect,HttpResponse
from django.core.serializers import serialize
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view
from todoapp.serializers import *
from django.contrib.auth.decorators import login_required, user_passes_test
from todoapp.models import Task,Card
from .utils import save_project_data_as_text
from .decorators import manager_required
from rest_framework import permissions
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Count, Prefetch, Q
from urllib.parse import urlencode
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Projects, User, Task, Card, Message
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.mail import send_mail

@csrf_exempt
@api_view(['POST'])
def create_task(request):
    if request.method == 'POST':
        data = request.data
        auto_assign = data.get('auto_assign', False)

        assigned_user_id = None
        if auto_assign:
            project_name = data.get('project')
            tech_stack = data.get('techStack', [])

            try:
                project = Projects.objects.get(name=project_name)
            except Projects.DoesNotExist:
                return Response({"detail": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

            # Create a Q object for tech stack filtering
            tech_stack_filter = Q()
            for tech in tech_stack:
                tech_stack_filter |= Q(userprofile__tech_stack__icontains=tech)

            project_users = User.objects.filter(userprofile__assigned_project=project).filter(tech_stack_filter)

            if project_users.exists():
                assigned_user = project_users.annotate(task_count=Count('tasks')).order_by('task_count').first()
            else:
                tech_stack_users = User.objects.filter(tech_stack_filter)

                if tech_stack_users.exists():
                    assigned_user = tech_stack_users.annotate(task_count=Count('tasks')).order_by('task_count').first()
                else:
                    assigned_user = User.objects.annotate(task_count=Count('tasks')).order_by('task_count').first()

            if assigned_user:
                assigned_user_id = assigned_user.id

        tech_stack = data.get('techStack', [])
        if isinstance(tech_stack, list):
            data['tech_stack'] = ', '.join(tech_stack)  

        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            task = serializer.save()  

            if assigned_user_id:
                task.assignedTo.set([assigned_user_id])
                task.save()  

            task.refresh_from_db()
            serializer = TaskSerializer(task)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['PUT'])
def update_priority(request, card_id):
    try:
        task = Task.objects.get(id=card_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
    priority = request.data.get('priority')
    
    if priority not in dict(Task.MY_CHOICES).keys(): 
        return Response({'error': 'Invalid priority value'}, status=status.HTTP_400_BAD_REQUEST)
    
    task.priority = priority
    task.save()
    
    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_enddate(request, card_id):
    try:
        task = Task.objects.get(id=card_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
    enddate = request.data.get('enddate')
    
    try:
        task.enddate = enddate  
        task.save()
    except ValueError:
        return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)

class ProjectListAPIView(APIView):
    def get(self, request):
        projects = Projects.objects.all()
        project_data = []

        for project in projects:
            # Filter tasks related to this project
            tasks = Task.objects.filter(project=project)

            # Count the total number of tasks
            total_tasks = tasks.count()

            # Count tasks by status
            completed_tasks = tasks.filter(taskStatus__card_name='Completed').count()
            # in_progress_tasks = tasks.filter(taskStatus__card_name='In Progress').count()
            # test_tasks = tasks.filter(taskStatus__card_name='Test').count()
            # other_tasks = tasks.filter(taskStatus__card_name='Other').count()

            # Calculate completion percentage
            if total_tasks == 0:
                completion_percentage = 0
            else:
                completion_percentage = round((completed_tasks / total_tasks) * 100.0)

            # Append project data to the list
            project_data.append({
                'id': project.id,
                'name': project.name,
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                # 'in_progress_tasks': in_progress_tasks,
                # 'test_tasks': test_tasks,
                # 'other_tasks': other_tasks,
                'completion_percentage': completion_percentage,
            })

        return Response(project_data, status=status.HTTP_200_OK)

class UserProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        profiles = self.get_queryset()
        serializer = self.get_serializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # permission_classes = [permissions.IsAdminUser]  # Only admin users can delete tasks
    # @method_decorator(manager_required) #for manager
    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_mail(
                'User Created Successfully',
                f'''Hi {user.username},

Welcome to Bourntec ToDo Application!

We’re excited to have you on board. Below are your login credentials:

Username: {user.username}
Password: {user.password}

Please make sure to change your password upon your first login for security purposes. If you have any questions or need assistance, feel free to reach out to our support team.

Thank you for choosing Bourntec!

Best regards,
The Bourntec Team''',

                'Bourntec Solutions',
                [user.email],
                fail_silently=False,
            )
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

admin_required = user_passes_test(lambda user: user.is_superuser)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# @api_view(['POST'])
# def register(request):
#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# admin_required = user_passes_test(lambda user: user.is_superuser)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_superuser:
                # Redirect for superuser
                query_params = urlencode({
                    'username': user.username,
                    'email': user.email,
                    'role': user.userprofile.role,
                    'designation':user.userprofile.designation,
                })
                redirect_url = f'http://localhost:3000/?{query_params}'
                return JsonResponse({"msg": "superuserlogin", "url": redirect_url})
            elif user.userprofile.role == "Manager":
                # Redirect for Manager
                query_params = urlencode({
                    'username': user.username,
                    'email': user.email,
                    'role': user.userprofile.role,
                    'designation':user.userprofile.designation,
                })
                redirect_url = f'http://localhost:3000/?{query_params}'
                return JsonResponse({"msg": "managerlogin", "url": redirect_url})
            else:
                # Redirect for other users
                query_params = urlencode({
                    'username': user.username,
                    'email': user.email,
                    'role': user.userprofile.role,
                    'designation':user.userprofile.designation,
                })
                redirect_url = f'http://localhost:3000/?{query_params}'
                return JsonResponse({"msg": "userlogin", "url": redirect_url})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
# class UpdateDateView(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Task.objects.all()
#     serializer_class = MyModelSerializer

class UpdateDescriptionView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = Update_Description

class UpdateStatusView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = Update_Status

class UpdateNameView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = Update_Name

# @api_view(['PUT'])
# def create_or_update_tasks(request):
#     if request.method == 'PUT':
#         data = json.loads(request.body)  # Assuming JSON data is sent in the request body
#         task = Task.objects.get(pk=data["project_id"])
#         d = {}
#         for k,v in data.items():
#             d[k]=v
#         task.checklist = str(d)
#         task.save()
#     return JsonResponse({'message': 'Tasks created/updated successfully'}, status=200)
# # else:
#     return JsonResponse({'error': 'Invalid request method'}, status=400)
# class create_or_update_tasks(generics.UpdateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = Update_Checklist
#views for save checklists

@api_view(['PUT'])
def save_data_view(request,id):
    if request.method == 'PUT':
        try:
            # Assume the JSON data is sent in the body of the request
            json_data = json.loads(request.body)
            save_project_data_as_text(id,json_data)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)})
    else:
        return JsonResponse({'status': 'failed', 'message': 'Only POST requests are allowed'})

class ImageUpdateView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def put(self, request, pk):
        try:
            image_instance = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UploadedFileSerializer(image_instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#Delete User
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDeleteSerializer
    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response({"msg":"User Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)
class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
class TaskDetailView(APIView):
    def get(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task)
        return Response(serializer.data)
class CoverUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = UpdateCoverColorSerializer

@api_view(['POST'])
# @admin_required
# @login_required
def create_group(request):
    if request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CardListView(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

@api_view(['POST'])
# @login_required
def create_card(request):
    if request.method == 'POST':
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def delete_card(request, card_id):
    try:
        card = Card.objects.get(id=card_id)
    except Card.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    card.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class UpdateUserView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DownloadAttachmentView(APIView):

    def get(self, request, pk, format=None):
        attachment = get_object_or_404(Task, pk=pk)
        response = FileResponse(attachment.file.open(), as_attachment=True, filename=attachment.taskName)
        return response

class attachment_delete_view(APIView):
    def delete(self, request, pk, format=None):
        attachment = get_object_or_404(Task, pk=pk)
        attachment.file.delete()  # Delete the file from the storage
        return Response(status=status.HTTP_204_NO_CONTENT)
# @api_view(['POST'])
# def create_project(request):
#     if request.method == 'POST':
#         serializer = ProjectSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectsListView(generics.ListAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer

class ProjectUpdateAPIView(APIView):
    # permission_classes=[IsAdminUser]
    def put(self, request, pk):
        project = get_object_or_404(Projects, pk=pk)
        serializer = ProjectsSerializer(instance=project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDeleteAPIView(APIView):
    # permission_classes=[IsAdminUser]
    def delete(self, request, pk):
        project = get_object_or_404(Projects, pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            user = User.objects.get(username=username)
            token = default_token_generator.make_token(user)
            reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': user.pk, 'token': token}))
            send_mail(
                'Password Reset Request',
                f'Use the link below to reset your password:\n{reset_url}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        serializer = PasswordResetConfirmSerializer(data={
            'uidb64': uidb64,
            'token': token,
            'new_password': request.data.get('new_password')
        })
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_project(request):
    serializer = ProjectsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_users(request):
    users = User.objects.prefetch_related(
        Prefetch('userprofile', queryset=UserProfile.objects.only('designation'))
    ).values('username', 'userprofile__designation')
    
    users_list = list(users)
    return JsonResponse(users_list, safe=False)

class ProjectTasksView(APIView):
    def get(self, request, projname):
        project = get_object_or_404(Projects, name=projname)
        tasks = Task.objects.filter(project=project)

        task_data = []

        for task in tasks:
            task_serializer = TaskSerializer(task)
            task_info = task_serializer.data
            task_info['project_name'] = task.project.name
            task_data.append(task_info)

        return Response(task_data, status=status.HTTP_200_OK)

class UserProjectTasksView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        tasks = Task.objects.filter(assignedTo=user)

        task_data = []

        for task in tasks:
            task_serializer = TaskSerializer(task)
            task_info = task_serializer.data
            task_info['project_name'] = task.project.name
            task_data.append(task_info)

        return Response(task_data, status=status.HTTP_200_OK)
    
# class TaskMessagesView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, task_id, format=None):
#         task = get_object_or_404(Task, id=task_id)
#         messages = Message.objects.filter(task=task)
#         serializer = MessageSerializer(messages, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, task_id, format=None):
#         if not request.user.is_authenticated:
#             return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

#         task = get_object_or_404(Task, id=task_id)
#         serializer = MessageSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save(task=task, user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskMessagesView(APIView):
    def get(self, request, task_name, format=None):
        task = get_object_or_404(Task, taskName=task_name)
        messages = Message.objects.filter(task=task)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
 
 
class UserTaskView(APIView):
    def get(self, request, user_name, format=None):
        user = get_object_or_404(User, username=user_name)
        task = Task.objects.filter(assignedTo=user)
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UpdateDateView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    queryset = Task.objects.all()
    serializer_class = MyModelSerializer