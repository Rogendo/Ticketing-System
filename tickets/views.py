import random
from .models import Department, Client, UserProfile, Ticket, TicketComment, Escalation
from .serializers import DepartmentSerializer, ClientSerializer, TicketSerializer, TicketCommentSerializer, UserProfileSerializer,EscalationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response

from django.db import models
from rest_framework.permissions import AllowAny


class IsSuperAdmin(permissions.BasePermission):
    permission_classes = [IsAuthenticated]

    def has_permission(self, request, view):
        
        return request.user.profile.role == 'SUPER_ADMIN'


class IsSuperAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Is Authenticated:", request.user.is_authenticated)
        return request.user.profile.role == 'SUPER_AGENT'


class IsClientAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            print("User:", request.user)
            print("Is Authenticated:", request.user.is_authenticated)
            return False
        return request.user.role == 'CLIENT_ADMIN'

# class IsClientAdmin(permissions.BasePermission):
#     permission_classes = [AllowAny]
#     def has_permission(self, request, view):
        
#         return request.user.profile.role == 'CLIENT_ADMIN'


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority', 'client', 'assigned_to']
    search_fields = ['title', 'description']
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        profile = user.profile

        if profile.role == 'SUPER_ADMIN':
            return Ticket.objects.all()
        elif profile.role == 'SUPER_AGENT':
            # Super Agents see escalated tickets + tickets from company clients
            company_clients = Client.objects.filter(name__icontains="Your Company")
            

            return Ticket.objects.filter(
                
                models.Q(escalated_to__in=company_clients) | 
                models.Q(client__in=company_clients))
        
        elif profile.role == 'CLIENT_ADMIN':
            return Ticket.objects.filter(client=profile.client)
        elif profile.role == 'AGENT':
            return Ticket.objects.filter(assigned_to=user)
        else:  # End User
            return Ticket.objects.filter(created_by=user)


class TicketCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TicketCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TicketComment.objects.filter(ticket_id=self.kwargs['ticket_pk'])

    def perform_create(self, serializer):
        ticket = Ticket.objects.get(pk=self.kwargs['ticket_pk'])
        serializer.save(
            author=self.request.user,
            ticket=ticket,
            is_internal=self.request.data.get('is_internal', False)
        )


class EscalationViewSet(viewsets.ModelViewSet):
    serializer_class = EscalationSerializer
    permission_classes = [IsClientAdmin, IsSuperAgent]
    # permission_classes = [IsClientAdmin, IsSuperAgent, IsAuthenticated]

    def perform_create(self, serializer):
        your_company = Client.objects.get(name="Your Software Company")
        ticket = serializer.validated_data['ticket']
        ticket.escalated_to = your_company
        ticket.status = 'ESCALATED'
        ticket.save()
        serializer.save(escalated_by=self.request.user)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer()
    permission_classes = [IsAdminUser]

