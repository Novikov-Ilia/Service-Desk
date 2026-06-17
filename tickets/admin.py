from django.contrib import admin

from .models import Category, Comment, Ticket, StatusHistory


admin.site.register(Ticket)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(StatusHistory)