from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)

    def save(self, *args, **kwargs):
        self.code = self.code.upper()  # enforce uppercase
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"