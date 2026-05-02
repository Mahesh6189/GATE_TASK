from rest_framework import serializers
from .models import UserAttempt

class UserAttemptSerializer(serializers.ModelSerializer):

    question_text = serializers.CharField(source='question.question_text', read_only=True)
    correct_answer = serializers.CharField(source='question.correct_option', read_only=True)

    class Meta:
        model = UserAttempt
        fields = '__all__'
        read_only_fields = ['is_correct']