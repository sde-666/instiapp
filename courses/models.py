from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import date


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    is_visible = models.BooleanField(default=True)  # ✅ Toggle visibility

    def __str__(self):
        return self.title


class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="chapters")
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)  # ✅ For custom ordering
    is_visible = models.BooleanField(default=True)  # ✅ Toggle visibility

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Note(models.Model):
    chapter = models.ForeignKey("Chapter", on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=200)
    topic_number = models.PositiveIntegerField(default=1)
    content = RichTextUploadingField(blank=True, null=True)
    file = models.FileField(upload_to="notes/", blank=True, null=True)
    publish_date = models.DateField(default=date.today)
    is_visible = models.BooleanField(default=True)  # ✅ Toggle visibility

    class Meta:
        ordering = ["-publish_date", "topic_number"]

    def __str__(self):
        return f"Topic {self.topic_number}: {self.title}"


    def save(self, *args, **kwargs):
        if self._state.adding and not self.topic_number:  # Only assign if not set
            last_note = Note.objects.filter(chapter=self.chapter).order_by("-topic_number").first()
            if last_note:
                self.topic_number = last_note.topic_number + 1
            else:
                self.topic_number = 1
        super().save(*args, **kwargs)
