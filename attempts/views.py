from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserAttempt
from .serializers import UserAttemptSerializer

class UserAttemptView(APIView):

    # GET all attempts
    def get(self, request):
        attempts = UserAttempt.objects.all()
        serializer = UserAttemptSerializer(attempts, many=True)
        return Response(serializer.data)

    # POST attempt
    def post(self, request):
        serializer = UserAttemptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)