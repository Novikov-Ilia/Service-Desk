from rest_framework import serializers
from .models import Ticket, Comment, Category, StatusHistory


class TicketReadSerializer(serializers.ModelSerializer):
    author_username = serializers.StringRelatedField(
        source='author',
        read_only=True
    )
    author_id = serializers.IntegerField(
        read_only=True
    )
    assigned_to_username = serializers.StringRelatedField(
        source='assigned_to',
        read_only=True
    )
    assigned_to_id = serializers.IntegerField(
        read_only=True
    )
    category_id = serializers.IntegerField(read_only=True)
    category_title = serializers.CharField(
        source='category.title',
        read_only=True
    )

    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'description',
            'created_at', 
            'updated_at',
            'status',
            'author_username',
            'author_id',
            'assigned_to_username',
            'assigned_to_id',
            'category_id',
            'category_title',
        ]
        read_only_fields = fields


class TicketWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            'title',
            'description',
            'category',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'title',
        ]
        read_only_fields = [
            'id',
        ]


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'text',
        ]



class CommentReadSerializer(serializers.ModelSerializer):
    author_username = serializers.StringRelatedField(
        source='author',
        read_only=True
    )
    author_id = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
            'author_username',
            'author_id',
            'ticket',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields

class StatusHistorySerializer(serializers.ModelSerializer):
    changed_by_username = serializers.StringRelatedField(
        source='changed_by',
        read_only=True
    )

    class Meta:
        model = StatusHistory
        fields = [
            'id',
            'old_status',
            'new_status',
            'comment',
            'changed_at',
            'ticket',
            'changed_by',
            'changed_by_username',
        ]
        read_only_fields = fields