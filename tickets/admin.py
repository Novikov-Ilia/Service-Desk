from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Category, Comment, Ticket, StatusHistory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
    )
    list_display_links = (
        'id',
        'title',
    )
    search_fields = (
        'title',
    )
    ordering = (
        'title',
    )


class AdminChangeLinkMixin:
    def _admin_change_link(self, model, related_id, label):
        url = reverse(
            f'admin:{model._meta.app_label}_{model._meta.model_name}_change', 
            args=(related_id,),
        )
        return format_html('<a href="{}">{}</a>', url, label)
    
    @admin.display(description='Author', ordering='author__username')
    def link_to_author(self, obj):
        if related_id := obj.author_id:
            User = get_user_model()
            return self._admin_change_link(
                User,
                related_id,
                obj.author,
            )
        else:
            return '-'
    
    @admin.display(description='Assigned to', ordering='assigned_to__username')
    def link_to_assigned(self, obj):
        if related_id := obj.assigned_to_id:
            User = get_user_model()
            return self._admin_change_link(
                User,
                related_id,
                obj.assigned_to,
            )
        else:
            return '-'
        
    @admin.display(description='Category', ordering='category__title')
    def link_to_category(self, obj):
        if related_id := obj.category_id:
            return self._admin_change_link(
                Category,
                related_id,
                obj.category,
            )
        else:
            return '-'

    @admin.display(description='Ticket', ordering='ticket__title')
    def link_to_ticket(self, obj):
        if related_id := obj.ticket_id:
            return self._admin_change_link(
                Ticket,
                related_id,
                obj.ticket,
            )
        else:
            return '-'
        
    @admin.display(description='Changed by', ordering='changed_by__username')
    def link_to_changed_by(self, obj):
        if related_id := obj.changed_by_id:
            User = get_user_model()
            return self._admin_change_link(
                User,
                related_id,
                obj.changed_by,
            )
        else:
            return '-'
        

class StatusHistoryInline(admin.TabularInline):
    model = StatusHistory
    extra = 0
    can_delete = False

    readonly_fields = (
        'old_status',
        'new_status',
        'comment',
        'changed_at',
        'changed_by',
    )

    def has_add_permission(self, request, obj=None):
        return False
    
    
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('created_at', 'updated_at')    


@admin.register(Ticket)
class TicketAdmin(AdminChangeLinkMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'link_to_category',
        'status',
        'link_to_author',
        'link_to_assigned',
        'created_at',
        'updated_at',
    )
    list_display_links = (
        'title',
        'id',
    )
    list_select_related = (
        'category',
        'author',
        'assigned_to',
    )
    list_filter = (
        'category',
        'status',
        'author',
        'assigned_to',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'title',
        'description',
        'author__username',
        'assigned_to__username',
    )
    date_hierarchy = 'created_at'
    ordering = ('status', '-created_at')
    inlines = (CommentInline, StatusHistoryInline)

@admin.register(Comment)
class CommentAdmin(AdminChangeLinkMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'text_preview',
        'link_to_ticket',
        'link_to_author',
        'created_at',
        'updated_at',
    )
    list_display_links = (
        'id',
        'text_preview',
    )
    list_select_related = (
        'author',
        'ticket',
    )
    list_filter = (
        'ticket',
        'author',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'text',
        'author__username',
        'ticket__title',
        'ticket__description',
    )
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    @admin.display(description='text')
    def text_preview(self, obj):
        return obj.text[:60]
    

@admin.register(StatusHistory)
class StatusHistoryAdmin(AdminChangeLinkMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'link_to_ticket',
        'old_status',
        'new_status',
        'link_to_changed_by',
        'changed_at',
    )
    list_display_links = (
        'id',
    )
    list_select_related = (
        'ticket',
        'changed_by',
    )
    list_filter = (
        'old_status',
        'new_status',
        'changed_at',
        'changed_by',
    )
    search_fields = (
        'ticket__title',
        'comment',
        'changed_by__username',
    )
    readonly_fields = (
        'ticket',
        'old_status',
        'new_status',
        'comment',
        'changed_at',
        'changed_by',
    )
    
    date_hierarchy = 'changed_at'
    ordering = ('-changed_at',)
    
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False