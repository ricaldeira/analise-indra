from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .views import get_dashboard_data

class DashboardAPIView(APIView):
    """
    API endpoint for dashboard data by category
    """

    def get(self, request, category):
        """
        Get dashboard data for a specific category
        """
        try:
            data = get_dashboard_data(category.upper())
            return Response(data)
        except Exception as e:
            return Response(
                {'error': f'Erro ao obter dados do dashboard: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DashboardCategoriesAPIView(APIView):
    """
    API endpoint for all dashboard categories
    """

    def get(self, request):
        """
        Get dashboard data for all categories
        """
        try:
            categories = ['AAPP', 'Sanidad', 'Consolidado']
            data = {}

            for category in categories:
                data[category.lower()] = get_dashboard_data(category)

            return Response(data)
        except Exception as e:
            return Response(
                {'error': f'Erro ao obter dados do dashboard: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )