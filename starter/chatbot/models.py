from django.db import models


class ChatMessage(models.Model):
    session_key = models.CharField(max_length=64, blank=True)
    role = models.CharField(max_length=20)
    content = models.TextField()
    provider = models.CharField(max_length=40, blank=True)
    model = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M:%S} {self.role}"

