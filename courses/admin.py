from django.contrib import admin
from .models import Course, Chapter, Note


class NoteInline(admin.TabularInline):
    model = Note
    extra = 1
    fields = ("topic_number", "title", "publish_date")  # keep inline simple
    show_change_link = True  # open full Note edit page


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1
    fields = ("title", "order", "is_visible")
    show_change_link = True


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "is_visible")
    list_editable = ("is_visible",)
    search_fields = ("title", "description")
    inlines = [ChapterInline]


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order", "is_visible")
    list_editable = ("order", "is_visible")
    search_fields = ("title",)
    list_filter = ("course", "is_visible")
    inlines = [NoteInline]
    
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("topic_number", "title", "chapter", "publish_date", "is_visible")  # ✅ show toggle
    list_display_links = ("title",)
    list_editable = ("is_visible",)  # ✅ quick toggle
    search_fields = ("title", "content")
    list_filter = ("publish_date", "chapter", "is_visible")
    ordering = ("-publish_date",)

    fields = ("chapter", "topic_number", "title", "publish_date", "content", "file", "is_visible")
