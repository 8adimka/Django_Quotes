from django.contrib import admin

from .models import Quote, Source


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "created_at")
    list_filter = ("type",)
    search_fields = ("title",)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        "short_text",
        "source",
        "base_weight",
        "likes",
        "dislikes",
        "views",
        "created_at",
    )
    list_filter = ("source__type",)
    search_fields = ("text", "source__title")
    autocomplete_fields = ("source",)

    def short_text(self, obj: Quote):
        return (obj.text[:80] + "…") if len(obj.text) > 80 else obj.text

    short_text.short_description = "Цитата"
