from rest_framework import serializers
from .models import UserAttempt

class UserAttemptSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    question_text = serializers.CharField(source='question.text', read_only=True)
    correct_answer = serializers.CharField(source='question.correct_option', read_only=True)

    class Meta:
        model = UserAttempt
        fields = '__all__'
        read_only_fields = ['is_correct']

    def validate(self, attrs):
        user = attrs.get('user')
        question = attrs.get('question')

        if UserAttempt.objects.filter(user=user, question=question).exists():
            raise serializers.ValidationError(
                "You have already attempted this question."
            )
        return attrs