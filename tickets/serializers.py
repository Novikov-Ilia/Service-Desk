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
    def validate_title(self, value):
        value = value.strip()

        if len(value) < 5:
            raise serializers.ValidationError(
                'Название заявки должно состоять хотя бы 5 символов'
            )
        
        return value
    
    def validate_description(self, value):
        value = value.strip()

        if len(value) < 10:
            raise serializers.ValidationError(
                'Описание заявки должно состоять хотя бы 10 символов'
            )
        
        return value

    class Meta:
        model = Ticket
        fields = [
            'title',
            'description',
            'category',
        ]


class CategorySerializer(serializers.ModelSerializer):
    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                'Название категории не должно быть пустым'
            )
        
        return value

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
    def validate_text(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                'Комментарий не может быть пустым'
            )
        
        return value
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