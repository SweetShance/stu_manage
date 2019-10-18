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
from .views import Index, Welcome, AdminManagement, RoleManagement, Permiclassify, PermiManagement, \
    Login, PermissionAdd, PermissionDelete, PermissionEdit, RoleDelete, RoleAdd, RoleEdit, LogOut, Register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view(), name="login"),
    path('logout', LogOut.as_view(), name="logout"),
    path('register', Register.as_view(), name="register" ),
    path('index', Index.as_view(), name="index"),
    path('welcome', Welcome.as_view(), name="welcome"),
    path('manage/', include('stu_table.urls')),
    path('adminManagement/', AdminManagement.as_view(), name="management"),
    path('user/', include('user.urls')),
    path('role', RoleManagement.as_view(), name="rolemanagement"),
    path('roledelete', RoleDelete.as_view(), name="roledelete"),
    path('roleadd', RoleAdd.as_view(), name="roleadd"),
    path('roleedit', RoleEdit.as_view(), name='roleedit'),
    path('permiclassify', Permiclassify.as_view(), name='permiclassify'),
    path('permiManagement', PermiManagement.as_view(), name="permiManagement"),
    path('permissionadd', PermissionAdd.as_view(), name='permissionadd'),
    path('permissiondelete', PermissionDelete.as_view(), name='permissiondelete'),
    path('permissionedit', PermissionEdit.as_view(), name="permissionedit"),
    path('error', include('myUtils.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
