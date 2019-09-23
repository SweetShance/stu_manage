"""intelligent_form URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static   # 新加入 
from django.conf import settings             # 新加入 
from .views import Index, Welcome, AdminManagement, RoleManagement, Permiclassify, PermiManagement, Login

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', Login.as_view(), name="login"),
    path('index', Index.as_view(), name="index"),
    path('welcome', Welcome.as_view(), name="welcome"),
    path('manage/', include('stu_table.urls')),
    path('adminManagement/', AdminManagement.as_view(), name="management"),
    path('role/', RoleManagement.as_view(), name="rolemanagement"),
    path('permiclassify', Permiclassify.as_view(), name='permiclassify'),
    path('permiManagement', PermiManagement.as_view(), name="permiManagement"),
    path('error', include('myUtils.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
