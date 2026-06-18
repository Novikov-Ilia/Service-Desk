from django.db import models
from django.conf import settings

class Ticket(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новая"
        IN_PROGRESS = "in_progress", "В работе"
        RESOLVED = "resolved", "Решена"
        CLOSED = "closed", "Закрыта"

        
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='created_tickets',
        null=True,
        )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='assigned_tickets',
        null=True,
        blank=True,
        )
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        null=True,
        related_name='tickets',
        blank=True,
    )
    
    def __str__(self):
        return f"ticket #{self.id} - {self.title}"


class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='comments',
        null=True,
        )
    
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    
    def __str__(self):
        return f'comment #{self.id} to {self.ticket}'
    

class Category(models.Model):
    title = models.CharField(max_length=64, unique=True)
    
    def __str__(self):
        return self.title
    
    
class StatusHistory(models.Model):
    old_status=models.CharField(max_length=20, choices=Ticket.Status.choices)
    new_status=models.CharField(max_length=20, choices=Ticket.Status.choices)
    comment = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    
    ticket = models.ForeignKey(
        Ticket,
        related_name="status_changes",
        on_delete=models.CASCADE,
    )
    changed_by=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='status_changes',
        on_delete=models.SET_NULL,
        null=True,
    )
    
    
    def __str__(self):
        return f'Ticket #{self.ticket_id}: {self.old_status} → {self.new_status}'