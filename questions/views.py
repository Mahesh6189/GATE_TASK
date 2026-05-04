from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import Question
from .serializers import QuestionSerializer

class QuestionListCreateView(APIView):

    def get_permissions(self):
        """
        GET: AllowAny (public read)
        POST: IsAdminUser (only admins can create)
        """
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request):
        questions = Question.objects.all()

        # Filter by subject, topic, difficulty
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailView(APIView):

    def get_permissions(self):
        """
        GET: AllowAny (public read)
        PUT/PATCH: IsAdminUser (only admins can update)
        DELETE: IsAdminUser (only admins can delete)
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return None

    def get(self, request, pk):
        """Retrieve a single question"""
        question = self.get_object(pk)
        if not question:
            return Response(
                {"error": "Question not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, pk):
        """Update a question (admin only)"""
        question = self.get_object(pk)
        if not question:
            return Response(
                {"error": "Question not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """Partial update of a question (admin only)"""
        question = self.get_object(pk)
        if not question:
            return Response(
                {"error": "Question not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a question (admin only)"""
        question = self.get_object(pk)
        if not question:
            return Response(
                {"error": "Question not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        question.delete()
        return Response(
            {"message": "Question deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )