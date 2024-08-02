from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from todoapp.views import *
urlpatterns = [
    path('api/create-task/', create_task, name='api-create-task'),#for creating task
    path('tasks/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),#delting task by id
    path('api/login/', LoginView.as_view(), name='login'),# user and super user login
    path('api/register/', register, name='api-register'),# user and super user SignUp
    path('users/', UserListView.as_view(), name='user_name_list'),# user and super user Details
    path('update-desc/<int:pk>/', UpdateDescriptionView.as_view(), name='update-desc'),# Task Update Desc
    path('update-status/<int:pk>/', UpdateStatusView.as_view(), name='update-status'),# Task Update Status
    path('update-name/<int:pk>/', UpdateNameView.as_view(), name='update_taskname'),# Task Update Task Name
    path('save-data/<int:id>/', save_data_view, name='category_save_data'),# Task Update Checklist
    path('file-upload/<int:pk>/', ImageUpdateView.as_view(), name='image_update'),# Task Update fileupload
    path('userdelete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),# User Delete
    path('tasks/', TaskListView.as_view(), name='login'),# All Tasks
    path('task/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),#Task Detail By ID
    path('cover_update/<int:pk>/',CoverUpdateView.as_view(),name='update_cover'),# Task Update Cover
    path('api/create_group/', create_group, name='api_create_group'),# Create Group
    path('users_update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_profile_update'),#Update UserDetails
    path('cardname/', CardListView.as_view(), name='card_name_list'),#sending card names to user get method
    path('api/createcard/', create_card, name='api_create_task'),#for storing card name into database,
    path('api/update_user/<int:user_id>/', UpdateUserView.as_view(), name='update_user'),#for updating User Details
    path('attachments/<int:pk>/download/', DownloadAttachmentView.as_view(), name='download_attachment'),#Download Attachment
    path('attachments/<int:pk>/delete/', attachment_delete_view.as_view(), name='delete_attachment'),# Delete attachment by Task ID
    path('api/create_project/', create_project, name='api-create-project'),#for creating project
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('api/projects/', ProjectsListView.as_view(), name='projects-list'),
    path('api/projects/<int:pk>/update/', ProjectUpdateAPIView.as_view(), name='project-update'),
    path('api/projects/<int:pk>/delete/', ProjectDeleteAPIView.as_view(), name='project-delete'),
    path('update-priority/<int:card_id>/', views.update_priority, name='update_priority'),
    path('update-enddate/<int:card_id>/', views.update_enddate, name='update_enddate'),
    path('api/get-users/', UserProfileListView.as_view(), name='user-list'),
    path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('projectper/', ProjectListAPIView.as_view(), name='project_list_api'),
    path('user/tasks/<int:user_id>/', UserProjectTasksView.as_view(), name='user-project-tasks'),
    path('api/deletecard/<int:card_id>/', delete_card, name='delete_card'),
    path('project/tasks/<str:projname>/', ProjectTasksView.as_view(), name='project-tasks'),
    path('comment/tasks/<str:task_name>/', TaskMessagesView.as_view(), name='tasks_Comment'),#Comment App
    # path('comment/tasks/<int:task_id>/', TaskMessagesView.as_view(), name='tasks_Comment'),
    path('user/tasks/<str:user_name>/', UserTaskView.as_view(), name='tasks_user'),#User Specific Tasks
    path('update-date/<int:pk>/', UpdateDateView.as_view(), name='update-date'),# Task Update Date
 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
