from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from .models import User
from .serializers import UserSerializer
from rest_framework.parsers import JSONParser, MultiPartParser
#from api.models import Activities
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q
from django.contrib.auth.hashers import make_password



class ItemPagination(PageNumberPagination):
    page_size = 25 
    page_size_query_param = 'page_size'
    max_page_size = 100 


class CustomAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.resolver_match.url_name == 'docs' or request.resolver_match.url_name == 'api_schema':
            return True
        return super().has_permission(request, view)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'
    
    

class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [CustomAuthenticated]

    def get_object(self):
        return self.request.user



class UserCreateView(APIView):
    serializer_class = UserSerializer
    parser_classes = [JSONParser, MultiPartParser]
    
    def post(self, request, *args, **kwargs):
        data = request.data

        user_serializer = self.serializer_class(data={
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'email': data.get('email'),
            'role': data.get('role'),
            'is_active': True
        })

        if user_serializer.is_valid():
            user = user_serializer.save(password=make_password(data.get('password')))
            image = request.FILES.get('image')
            if image:
                user.image = image
                user.save()

            return Response({
                "data":None,
                "status":True,
                "message":"User Registered Successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUsers(APIView):
    permission_classes = [CustomAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = ItemPagination
    def get(self, request):
        try:
            searchText = request.query_params.get('search', None)
            
            if searchText is not None:
                users = User.objects.filter(Q(first_name__icontains=searchText) | 
                                         Q(last_name__icontains=searchText) | 
                                         Q(email__icontains=searchText), is_superuser=False
                                         )
            else:
                users = User.objects.exclude(is_superuser=True).order_by('last_name')
            
            paginator = self.pagination_class()
            paginated_files = paginator.paginate_queryset(users, request)
            serializer = UserSerializer(paginated_files, many=True)

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
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
