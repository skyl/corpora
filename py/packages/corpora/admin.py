from django.contrib import admin
from .models import Corpus, CorpusTextFile, Split


@admin.register(Corpus)
class CorpusAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "url", "created_at", "updated_at")
    search_fields = ("name", "id", "url")
    ordering = ("-updated_at",)
    readonly_fields = ("id", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("name", "id", "url")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(CorpusTextFile)
class CorpusTextFileAdmin(admin.ModelAdmin):
    autocomplete_fields = ("corpus",)
    list_display = ("path", "corpus", "checksum", "created_at", "updated_at")
    search_fields = ("path", "checksum", "corpus__name")
    ordering = ("corpus", "path")
    readonly_fields = ("checksum", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("corpus", "path", "content")}),
        ("AI Summary", {"fields": ("ai_summary",)}),
        (
            "Metadata",
            {"fields": ("checksum", "created_at", "updated_at")},
        ),
    )


@admin.register(Split)
class SplitAdmin(admin.ModelAdmin):
    autocomplete_fields = ("file",)
    list_display = ("file", "order", "content_preview", "metadata")
    search_fields = ("file__path", "content")
    ordering = ("file", "order")
    fieldsets = (
        (None, {"fields": ("file", "order", "content")}),
        ("Meta", {"fields": ("metadata",)}),
    )

    def content_preview(self, obj):
        return obj.content[:50] + "..." if obj.content else "No content"

    content_preview.short_description = "Content Preview"
