from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Booking, SupportTicket, Statistics

admin.site.register(User, UserAdmin)
admin.site.register(Booking)
admin.site.register(SupportTicket)
admin.site.register(Statistics)