"""
URL configuration for string_analyzer project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('strings_app.urls')),
]
