from rest_framework import serializers
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):

    subject_name = serializers.CharField(source='subject.name', read_only=True)
    topic_name = serializers.CharField(source='topic.name', read_only=True)

    class Meta:
        model = Question
        exclude = ['correct_option'] 