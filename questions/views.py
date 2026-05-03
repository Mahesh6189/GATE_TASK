from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Question
from .serializers import QuestionSerializer

class QuestionListCreateView(APIView):

    permission_classes = [IsAuthenticated]  

    def get(self, request):
        questions = Question.objects.all()

        
        subject_id = request.query_params.get('subject')
        topic_id = request.query_params.get('topic')
        difficulty = request.query_params.get('difficulty')

        if subject_id:
            questions = questions.filter(subject_id=subject_id)

        if topic_id:
            questions = questions.filter(topic_id=topic_id)

        if difficulty:
            questions = questions.filter(difficulty=difficulty)

        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)