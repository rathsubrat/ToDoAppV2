"""
URL configuration for todoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from todoapp.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('todo/', include('todoapp.urls')),
    # path('api/create-task/', create_task, name='api-create-task'),
    # path('tasks/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
    # path('api/login/', LoginView.as_view(), name='login'),
    # path('api/register/', register, name='api-register'),
    # path('users/', UserListView.as_view(), name='user-list'),
    # path('update-date/<int:pk>/', UpdateDateView.as_view(), name='update-date'),
    # path('update-desc/<int:pk>/', UpdateDescriptionView.as_view(), name='update-desc'),
    # path('update-status/<int:pk>/', UpdateStatusView.as_view(), name='update-status'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)