
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('accounts/', include('accounts.urls')),
    path('api/v1/', include('api_v1.urls')),
    path('api_schema/', get_schema_view(title="API Schema", description="API DOCS GUIDE"), name='api_schema'),
    path('docs/', TemplateView.as_view(
        template_name='docs.html',
        extra_context={'schema_url':'api_schema'}
        ), name='swagger-ui'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


schema_url_patterns = [
    path('api/v1/', include('api_v1.urls')),
]