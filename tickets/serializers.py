from rest_framework import serializers
from .models import Ticket, TicketComment, Department, Escalation, UserProfile, Client

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email']

class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = '__all__'        
        read_only_fields = ['created_at', 'updated_at', 'created_by']

class TicketCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketComment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'author']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'



class DepartmentSerializer(serializers.ModelSerializer):
    # author = UserProfileSerializer(read_only=True)

    class Meta:
        model = Department
        fields = '__all__'


class EscalationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Escalation
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    # author = UserProfileSerializer(read_only=True)

    class Meta:
        model = Client
        fields = '__all__'
