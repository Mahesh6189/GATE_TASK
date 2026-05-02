from django.contrib import admin
from django.urls import path
from subjects.views import SubjectListCreateView
from topics.views import TopicListCreateView
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "status": "running",
        "message": "GATE API is working "
    })

urlpatterns = [
    path('', home),  
    path('admin/', admin.site.urls),

    # Subject API
    path('api/subjects/', SubjectListCreateView.as_view()),

    #topic api
    path('api/topics/', TopicListCreateView.as_view()),
]