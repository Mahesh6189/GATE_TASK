from django.db import models
from django.contrib.auth.models import User
from questions.models import Question


class UserAttempt(models.Model):

    OPTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    selected_option = models.CharField(
        max_length=1,
        choices=OPTION_CHOICES
    )

    is_correct = models.BooleanField(editable=False)

    attempted_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # auto-calculate correctness
        self.is_correct = (
            self.selected_option == self.question.correct_option
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - Q{self.question.id}"