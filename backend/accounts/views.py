from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from .models import User
from .serializers import UserSerializer, ChangePasswordSerializer
#from api.models import Activities
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q


class ItemPagination(PageNumberPagination):
    page_size = 25 
    page_size_query_param = 'page_size'
    max_page_size = 100 



class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'
    
    

class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



class GetUsers(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    authentication_classes = [JWTAuthentication]
    pagination_class = ItemPagination
    def get(self, request):
        try:
            searchText = request.query_params.get('searchText', None)
            
            if searchText is not None:
                users = User.objects.filter(Q(first_name=searchText) | 
                                         Q(last_name=searchText) | 
                                         Q(email=searchText), is_superuser=False
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
        
    
class ChangePassword(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # Set the new password
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            
            if request.user.role != 'security_officer':
                instance = Activities.objects.create(
                    user = request.user,
                    icon_tag = 'lock',
                    message = "You changed your password",
                    status ='success',
                ) 
                instance.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
             
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
