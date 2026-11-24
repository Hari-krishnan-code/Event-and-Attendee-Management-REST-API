from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EventDb(models.Model):
    title = models.CharField(max_length=100)
    event_date = models.DateField()
    venue = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_events")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class EventAttendeeDb(models.Model):
    event = models.ForeignKey(EventDb, on_delete=models.CASCADE, related_name="event_details")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="event_attendees")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event', 'user'], name='unique_event_attendee')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"