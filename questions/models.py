from django.db import models
from django.core.exceptions import ValidationError
from subjects.models import Subject
from topics.models import Topic


class Question(models.Model):

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    OPTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]

    # ---------------------
    # MAIN FIELDS
    # ---------------------
    text = models.TextField()

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        db_index=True
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True
    )

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        db_index=True
    )

    year = models.IntegerField(
        db_index=True
    )

    # ---------------------
    # OPTIONS
    # ---------------------
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()

    correct_option = models.CharField(
        max_length=1,
        choices=OPTION_CHOICES
    )

    explanation = models.TextField(blank=True, null=True)

    # ---------------------
    # VALIDATION LOGIC
    # ---------------------
    def clean(self):
        super().clean()

        # Year validation (SAFE for Django admin empty input)
        if self.year is None or self.year == '':
            raise ValidationError("Year is required")

        try:
            year = int(self.year)
        except (TypeError, ValueError):
            raise ValidationError("Year must be a valid number")

        if year < 1991 or year > 2026:
            raise ValidationError("Year must be between 1991 and 2026")

        # Topic-Subject consistency check
        if self.topic and self.topic.subject != self.subject:
            raise ValidationError("Selected topic does not belong to this subject")


    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

    # ---------------------
    # STRING OUTPUT
    # ---------------------
    def __str__(self):
        return f"{self.subject.name} - {self.text[:40]}"