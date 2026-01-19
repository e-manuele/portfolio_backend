from django.contrib import admin
from .models import Project, BlogPost, ContactMessage


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "featured",
        "created_at",
    )
    list_filter = (
        "category",
        "featured",
        "created_at",
    )
    search_fields = (
        "title",
        "description",
        "technologies",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "published",
        "published_at",
        "created_at",
    )
    list_filter = (
        "published",
        "published_at",
        "created_at",
    )
    search_fields = (
        "title",
        "content",
        "excerpt",
    )
    prepopulated_fields = {
        "slug": ("title",),
    }
    ordering = ("-published_at", "-created_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "subject",
        "read",
        "created_at",
    )
    list_filter = (
        "read",
        "created_at",
    )
    search_fields = (
        "name",
        "email",
        "subject",
        "message",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
