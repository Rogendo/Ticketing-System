from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'departments', views.DepartmentViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'tickets', views.TicketViewSet, basename='ticket')
router.register(r'tickets/(?P<ticket_pk>\d+)/comments', views.TicketCommentViewSet, basename='ticket-comment')
router.register(r'escalations', views.EscalationViewSet, basename='escalation')


schema_view = get_schema_view(
    openapi.Info(
        title="Bitz-ITC Ticketing System API",
        default_version='v1',
        description="API for multi-tenant ticketing system",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('api/', include(router.urls)),
    path('auth/', include('djoser.urls.jwt')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]