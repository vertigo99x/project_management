from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser 
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Project
from .serializers import ProjectSerializer
from django.shortcuts import get_object_or_404

class CustomPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'
    max_page_size = 100 
    
    
class ProjectView(APIView):
    parser_classes = [JSONParser]
    serializer_class = ProjectSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        
        search_query = request.query_params.get('search')
        project_status = request.query_params.get('status')
        project_priority = request.query_params.get('priority')
        assigned_to_id = request.query_params.get('assigned_to')
        
        filters = {}
        
        
        if search_query:
            search_filter = Q(project_name__icontains=search_query) | Q(project_description__icontains=search_query)
        else:
            search_filter = Q()

        if project_status:
            filters['status'] = project_status
        if project_priority:
            filters['priority'] = project_priority
        if assigned_to_id:
            filters['assigned_to__uuid'] = assigned_to_id

        if user.role == 'admin':
            filters['created_by'] = user
        else:
            filters['assigned_to'] = user

        projects = Project.objects.filter(search_filter, **filters)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(projects, request)
        serializer = self.serializer_class(page, many=True)

        response_data = {
            "status": True,
            "message": "Projects retrieved successfully",
            "data": serializer.data,
            "pagination": {
                "current_page": paginator.page.number,
                "total_pages": paginator.page.paginator.num_pages,
                "page_size": paginator.page_size,
                "total_items": paginator.page.paginator.count,
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            response_data = {
                "status": True,
                "message": "Project created successfully.",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, uuid, *args, **kwargs):
        project = get_object_or_404(Project, uuid=uuid)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            response_data = {
                "status": True,
                "message": "Project Updated successfully.",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, uuid, *args, **kwargs):
        project = get_object_or_404(Project, uuid=uuid)
        project.delete()
        response_data = {
                "status": True,
                "message": "Project was Deleted successfully.",
                "data": None,
            }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)