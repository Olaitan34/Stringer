"""
URL configuration for strings_app.
"""
from django.urls import path
from . import views

app_name = 'strings_app'

urlpatterns = [
    # GET /strings/filter-by-natural-language - Natural language filter (must come before /<string_value>)
    path('strings/filter-by-natural-language', views.filter_by_natural_language, name='filter_by_natural_language'),
    
    # POST /strings - Create a new string analysis
    path('strings', views.create_string, name='create_string'),
    
    # GET /strings/ - List all strings with optional filters
    path('strings/', views.list_strings, name='list_strings'),
    
    # GET /strings/<string_value> - Get string by value
    # DELETE /strings/<string_value> - Delete string by value
    path('strings/<path:string_value>', views.string_detail, name='string_detail'),
]
