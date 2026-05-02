from rest_framework.generics import ListCreateAPIView
from .models import Subject
from .serializers import SubjectSerializer

class SubjectListCreateView(ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer