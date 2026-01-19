from rest_framework import serializers
from .models import Project, BlogPost, ContactMessage
from django.contrib.auth.models import User

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'category', 'technologies', 
                  'image_url', 'project_url', 'github_url', 'featured', 
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'content', 'excerpt', 'cover_image',
                  'published', 'published_at', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'published_at']


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message', 'read', 'created_at']
        read_only_fields = ['created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']
