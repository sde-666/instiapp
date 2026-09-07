from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("course/<int:course_id>/", views.course_detail, name="course_detail"),
    path("chapter/<int:chapter_id>/", views.chapter_detail, name="chapter_detail"),
    path("note/<int:note_id>/", views.note_detail, name="note_detail"),

    # ✅ New toggle route
    path("note/<int:note_id>/toggle/", views.toggle_note_visibility, name="toggle_note_visibility"),
]
