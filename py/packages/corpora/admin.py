from django.contrib import admin
from .models import Corpus, File, Split


@admin.register(Corpus)
class CorpusAdmin(admin.ModelAdmin):
    list_display = ("name", "uuid", "url", "created_at", "updated_at")
    search_fields = ("name", "uuid", "url")
    list_filter = ("created_at", "updated_at")
    ordering = ("-updated_at",)
    readonly_fields = ("uuid", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("name", "uuid", "url")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("path", "corpus", "checksum", "created_at", "updated_at")
    search_fields = ("path", "checksum", "corpus__name")
    list_filter = ("corpus", "created_at", "updated_at")
    ordering = ("corpus", "path")
    readonly_fields = ("checksum", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("corpus", "path", "content")}),
        ("AI Summary", {"fields": ("ai_summary", "vector_of_summary")}),
        ("Metadata", {"fields": ("checksum", "created_at", "updated_at")}),
    )


@admin.register(Split)
class SplitAdmin(admin.ModelAdmin):
    list_display = ("file", "order", "content_preview", "metadata")
    search_fields = ("file__path", "content")
    list_filter = ("file__corpus", "file")
    ordering = ("file", "order")
    readonly_fields = ("vector",)
    fieldsets = (
        (None, {"fields": ("file", "order", "content")}),
        ("Vector Data", {"fields": ("vector", "metadata")}),
    )

    def content_preview(self, obj):
        return obj.content[:50] + "..." if obj.content else "No content"

    content_preview.short_description = "Content Preview"
