from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Chapter, Note
from datetime import date


def home(request):
    # ✅ Show only visible courses
    courses = Course.objects.filter(is_visible=True)
    return render(request, "courses/home.html", {"courses": courses})


def course_detail(request, course_id):
    # ✅ Prevent access to hidden courses
    course = get_object_or_404(Course, id=course_id, is_visible=True)
    # ✅ Show only visible chapters
    chapters = course.chapters.filter(is_visible=True)
    return render(request, "courses/course_detail.html", {
        "course": course,
        "chapters": chapters
    })


def chapter_detail(request, chapter_id):
    # ✅ Prevent access to hidden chapters
    chapter = get_object_or_404(Chapter, id=chapter_id, is_visible=True)

    today = date.today()

    # ✅ Show only visible notes
    notes = chapter.notes.filter(is_visible=True)

    # ✅ Latest visible note
    latest_note = notes.order_by('-publish_date', '-id').first()

    return render(request, "courses/chapter_detail.html", {
        "chapter": chapter,
        "today": today,
        "latest_note": latest_note,
        "notes": notes,  # ✅ pass notes list
    })


def note_detail(request, note_id):
    # ✅ Prevent access to hidden notes
    note = get_object_or_404(Note, id=note_id, is_visible=True)
    return render(request, "courses/note_detail.html", {"note": note})


# ✅ Toggle visibility of notes
@login_required
def toggle_note_visibility(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.is_visible = not note.is_visible
    note.save()
    return redirect("chapter_detail", chapter_id=note.chapter.id)
