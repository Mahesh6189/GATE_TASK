from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from .models import UserAttempt
from .serializers import UserAttemptSerializer

class UserAttemptView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        attempts = UserAttempt.objects.filter(user=request.user)
        serializer = UserAttemptSerializer(attempts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserAttemptSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttemptStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        attempts = UserAttempt.objects.filter(user=user)
        total_attempts = attempts.count()
        correct_attempts = attempts.filter(is_correct=True).count()
        incorrect_attempts = total_attempts - correct_attempts

        subject_stats = attempts.values(
            'question__subject__name'
        ).annotate(
            total=Count('id'),
            correct=Count('id', filter=Q(is_correct=True)),
        ).order_by('question__subject__name')

        difficulty_stats = attempts.values(
            'question__difficulty'
        ).annotate(
            total=Count('id'),
            correct=Count('id', filter=Q(is_correct=True)),
        ).order_by('question__difficulty')

        return Response({
            'user': user.username,
            'total_attempts': total_attempts,
            'correct_attempts': correct_attempts,
            'incorrect_attempts': incorrect_attempts,
            'subject_stats': list(subject_stats),
            'difficulty_stats': list(difficulty_stats),
        })