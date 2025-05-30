from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=200)
    support_email = models.EmailField()
    support_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    ROLES = [
        ('SUPER_ADMIN', 'Super Admin'),
        ('SUPER_AGENT', 'Super Agent'),  # New role
        ('CLIENT_ADMIN', 'Client Admin'),
        ('AGENT', 'Agent'),
        ('END_USER', 'End User')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True, related_name='client')
    role = models.CharField(max_length=20, choices=ROLES)


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
        ('ESCALATED', 'Escalated'),
        ('IN_PROGRESS', 'In Progress')
    ]
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical')
    ]
    CHANNEL_CHOICES = [
        ('Whatsapp','Whatsapp'),
        ('Email', 'Email'),
        ('Web form', 'Web form')
    ]


    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client') 
    escalated_to = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)  # Escalated to Bitz-ITC company
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES, default='Web form', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.status}"


class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_internal = models.BooleanField(default=False)  # For internal notes (agents/super agents)

    def __str__(self):
        return f"{self.ticket} - {self.message}"


class Escalation(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    reason = models.TextField()
    escalated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    escalated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket} - {self.reason}"

