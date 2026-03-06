from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.upload_page, name='upload_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/dashboard/<str:category>/', views.api_dashboard_data, name='api_dashboard_data'),
    path('upload/', views.process_upload, name='process_upload'),
]