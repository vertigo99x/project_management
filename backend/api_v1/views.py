from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser 
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Project, Activities
from .serializers import ProjectSerializer, ActivitySerializer
from django.shortcuts import get_object_or_404
from django.utils.timezone import now, timedelta
from django.db.models import Count



class CustomPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'
    max_page_size = 100 
    
    

class CustomAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        if request.resolver_match.url_name == 'docs' or request.resolver_match.url_name == 'api_schema':  #to allow swagger show docs for Views with IsAuthenticated
            return True
        return super().has_permission(request, view)



class ProjectView(APIView):
    parser_classes = [JSONParser]
    serializer_class = ProjectSerializer
    pagination_class = CustomPagination
    permission_classes = [CustomAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        
        role = getattr(user, 'role', 'user') 
        
        search_query = request.query_params.get('search')
        project_status = request.query_params.get('status')
        project_priority = request.query_params.get('priority')
        assigned_to_id = request.query_params.get('assigned_to')
        order = request.query_params.get('order')
        
        order_list = ['date_created','-date_created']
        if order not in order_list:
            order = 'date_created'
            
    
        filters = {}
        
        
        if search_query:
            search_filter = Q(project_name__icontains=search_query) | Q(project_description__icontains=search_query)
        else:
            search_filter = Q()

        if project_status:
            filters['status'] = project_status
            
            if project_status == 'pending':
                filters['status'] = None
        if project_priority:
            filters['priority'] = project_priority
        if assigned_to_id:
            filters['assigned_to__id'] = assigned_to_id

        if role == 'admin':
            filters['created_by'] = user
        else:
            filters['assigned_to'] = user
        
        if search_filter:
            projects = Project.objects.filter(search_filter, **filters).order_by(order)
        else:
            projects = Project.objects.filter(**filters).order_by(order)
            
            
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

    
    
    
    
    
class CreateProjectView(APIView):
    parser_classes = [JSONParser]
    serializer_class = ProjectSerializer
    pagination_class = CustomPagination
    permission_classes = [CustomAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            
            instance = Activities.objects.create(
                    user = request.user,
                    message = f"You Created a Project: {request.data.get('project_name')}",
                    status ='success',
                ) 
            instance.save()

            response_data = {
                "status": True,
                "message": "Project created successfully.",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
  
class UpdateProjectView(APIView):
    parser_classes = [JSONParser]
    serializer_class = ProjectSerializer
    pagination_class = CustomPagination
    permission_classes = [CustomAuthenticated]
    authentication_classes = [JWTAuthentication]
    def put(self, request, uuid, *args, **kwargs):
        project = get_object_or_404(Project, uuid=uuid)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            
            if project and not project.assigned_to and request.data.get('assigned_to'):
                instance = Activities.objects.create(
                    user = project.assigned_to,
                    message = f"You have been assigned a project: {request.data.get('project_name')}",
                    status ='success',
                ) 
                instance.save()
            
            serializer.save()
            
            instance = Activities.objects.create(
                    user = request.user,
                    message = f"You Updated a Project: {request.data.get('project_name')}",
                    status ='primary',
                ) 
            instance.save()
            

            response_data = {
                "status": True,
                "message":"Project Updated successfully.",
                "data": serializer.data,
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class DeleteProjectView(APIView):
    def delete(self, request, uuid, *args, **kwargs):
        project = get_object_or_404(Project, uuid=uuid)
        
        if project:
            instance = Activities.objects.create(
                    user = request.user,
                    message = f"You Deleted a Project: {project.project_name}",
                    status ='cancelled',
                ) 
            instance = Activities.objects.create(
                    user = project.assigned_to,
                    message = f"A project was Deleted: {project.project_name}",
                    status ='cancelled',
                ) 
            
        project.delete()
        instance.save()
        response_data = {
                "status": True,
                "message": "Project was Deleted successfully.",
                "data": None,
            }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
    
class DashboardData(APIView):
    parser_classes = [JSONParser]
    permission_classes = [CustomAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        role = getattr(user, 'role', 'user')  

        current_date = now()
        start_of_week = current_date - timedelta(days=current_date.weekday() + 1)  
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)

        created_count = [0] * 7
        assigned_count = [0] * 7
        completed_count = [0] * 7

        
        if role == 'admin':
            total_created_projects = Project.objects.filter(created_by=user)
            total_cancelled_or_abandoned_projects = Project.objects.filter(Q(status="abandoned") | Q(status="cancelled"), created_by=user)
            created_projects = total_created_projects.filter(date_created__range=[start_of_week, end_of_week])
            total_completed_projects = Project.objects.filter(created_by=user, status='done')
            completed_projects = total_completed_projects.filter(date_created__range=[start_of_week, end_of_week])
            total_assigned_projects = Project.objects.filter(assigned_to__isnull=False, created_by=user)
            assigned_projects = total_assigned_projects.filter(date_created__range=[start_of_week, end_of_week])
            
            for project in created_projects:
                day_of_week = (project.date_created.weekday() + 1) % 7
                created_count[day_of_week] += 1
            for project in completed_projects:
                day_of_week = (project.date_created.weekday() + 1) % 7
                completed_count[day_of_week] += 1
            for project in assigned_projects:
                day_of_week = (project.date_created.weekday() + 1) % 7
                assigned_count[day_of_week] += 1

        else:
            total_assigned_projects = Project.objects.filter(assigned_to=user)
            assigned_projects = total_assigned_projects.filter(date_created__range=[start_of_week, end_of_week])
            total_completed_projects = Project.objects.filter(assigned_to=user, status='done')
            completed_projects = total_completed_projects.filter(date_created__range=[start_of_week, end_of_week])
            for project in assigned_projects:
                day_of_week = (project.date_created.weekday() + 1) % 7
                assigned_count[day_of_week] += 1
            for project in completed_projects:
                day_of_week = (project.date_created.weekday() + 1) % 7
                completed_count[day_of_week] += 1
                
        start_date_iso = start_of_week.date().isoformat()  
        end_date_iso = end_of_week.date().isoformat()      

        response_data = {
            "status": True,
            "message": "Weekly project stats",
            "data": {
                "total_created_count":total_created_projects.count() if role == 'admin' else None,
                "total_completed_count": total_completed_projects.count(),
                "total_assigned_count": total_assigned_projects.count(),
                "total_cancelled_or_abandoned_count": total_cancelled_or_abandoned_projects.count() if role == 'admin' else None,
                "created_count": created_count if role == 'admin' else None, 
                "assigned_count": assigned_count,  
                "completed_count": completed_count,
                "week_start": start_date_iso,
                "week_end": end_date_iso  
            }
        }
        return Response(response_data)
    

   
class ActivityView(APIView):
    parser_classes = [JSONParser]
    pagination_class = CustomPagination
    permission_classes = [CustomAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_classes = ActivitySerializer   
    
    def get(self, request):
        user = request.user
        activities = Activities.objects.filter(user=user)
        paginator = self.pagination_class()
        paginated_files = paginator.paginate_queryset(activities, request)
        
        serializer = ActivitySerializer(paginated_files, many=True, context={'request': request})
        
        response_data = {
                "status": True,
                "message": "",
                "data": serializer.data,
                "pagination": {
                    "current_page": paginator.page.number,
                    "total_pages": paginator.page.paginator.num_pages,
                    "page_size": paginator.page_size,
                    "total_items": paginator.page.paginator.count,
                }
            }
        return Response(response_data, status=status.HTTP_200_OK)