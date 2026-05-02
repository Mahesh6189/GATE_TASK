from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Question
from .serializers import QuestionSerializer

class QuestionListCreateView(APIView):

    # GET all questions
    def get(self, request):
        subject_id = request.query_params.get('subject')
        topic_id = request.query_params.get('topic')

        questions = Question.objects.all()

        if subject_id:
            questions = questions.filter(subject_id=subject_id)

        if topic_id:
            questions = questions.filter(topic_id=topic_id)

        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    # POST new question
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)