from django.contrib import admin
from .models import Ticket, TicketComment, Department, Client, UserProfile, Escalation

admin.site.register(UserProfile)
admin.site.register(Client)
admin.site.register(Ticket)
admin.site.register(TicketComment)
admin.site.register(Department)
admin.site.register(Escalation)

