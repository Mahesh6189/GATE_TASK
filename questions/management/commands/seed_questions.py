import json
from pathlib import Path

from django.core.management.base import BaseCommand

from subjects.models import Subject
from topics.models import Topic
from questions.models import Question


class Command(BaseCommand):
    help = 'Load questions from seed_data/questions.json into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            default='seed_data/questions.json',
            help='Path to the questions JSON file'
        )

    def handle(self, *args, **options):
        file_path = Path(options['path'])

        if not file_path.exists():
            self.stderr.write(self.style.ERROR(f'Path not found: {file_path}'))
            return

        with file_path.open('r', encoding='utf-8') as f:
            questions = json.load(f)

        inserted = 0
        skipped = 0

        for item in questions:
            subject_code = item.get('subject_code')
            subject_name = item.get('subject_name')
            topic_name = item.get('topic_name')
            text = item.get('text')
            difficulty = item.get('difficulty')
            year = item.get('year')
            option_a = item.get('option_a')
            option_b = item.get('option_b')
            option_c = item.get('option_c')
            option_d = item.get('option_d')
            correct_option = item.get('correct_option')
            explanation = item.get('explanation', '')

            if not (subject_code and subject_name and text and difficulty and year and option_a and option_b and option_c and option_d and correct_option):
                self.stderr.write(self.style.WARNING(f'Skipping invalid record: {item}'))
                skipped += 1
                continue

            subject, _ = Subject.objects.get_or_create(
                code=subject_code.upper(),
                defaults={'name': subject_name}
            )
            if subject.name != subject_name:
                subject.name = subject_name
                subject.save()

            topic = None
            if topic_name:
                topic, _ = Topic.objects.get_or_create(
                    name=topic_name,
                    subject=subject
                )

            if Question.objects.filter(text=text, subject=subject, year=year).exists():
                skipped += 1
                continue

            Question.objects.create(
                text=text,
                subject=subject,
                topic=topic,
                difficulty=difficulty,
                year=year,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_option=correct_option,
                explanation=explanation,
            )
            inserted += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seed completed: inserted={inserted}, skipped={skipped}'
        ))
