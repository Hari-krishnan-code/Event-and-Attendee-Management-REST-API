"""
URL configuration for eventmanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from eventcore import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.RegisterView.as_view()),
    path('login/', obtain_auth_token),
    path('users/', views.UserListView.as_view()),

    path('jwt_login/', TokenObtainPairView.as_view()),
    path('api/refresh/', TokenRefreshView.as_view()),

    path('events/', views.EventListCreateView.as_view()),
    path('events/<pk>/', views.EventRetrieveUpdateDeleteView.as_view()),
    path('events/<event_id>/attendees/', views.EventAttendeeListCreateView.as_view()),
    path('events/<event_id>/attendees/<attendee_id>/', views.AttendeeDeleteView.as_view()),

    path('jwt_logout/', views.JWT_logout.as_view()),
]
