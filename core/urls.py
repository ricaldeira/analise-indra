from django.urls import path
from . import views
from .api import DashboardAPIView, DashboardCategoriesAPIView

app_name = 'core'

urlpatterns = [
    path('', views.upload_page, name='upload_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Legacy API endpoint (keeping for compatibility)
    path('api/dashboard/<str:category>/', views.api_dashboard_data, name='api_dashboard_data'),
    # New REST API endpoints
    path('api/v1/dashboard/<str:category>/', DashboardAPIView.as_view(), name='dashboard_api'),
    path('api/v1/dashboard/', DashboardCategoriesAPIView.as_view(), name='dashboard_categories_api'),
    path('upload/', views.process_upload, name='process_upload'),
]