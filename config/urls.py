from django.contrib import admin
from django.urls import path, include
from subjects.views import SubjectListCreateView
from topics.views import TopicListCreateView
from questions.views import QuestionListCreateView
from attempts.views import UserAttemptView
from django.http import JsonResponse
from accounts.views import RegisterView, LoginView

def home(request):
    return JsonResponse({
        "status": "running",
        "message": "GATE API is working"
    })

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),

    # Subject API
    path('api/subjects/', SubjectListCreateView.as_view()),

    # Topic API
    path('api/topics/', TopicListCreateView.as_view()),

    # Question API
    path('api/questions/', QuestionListCreateView.as_view()),
    # user attempt

      path('api/attempts/', UserAttemptView.as_view()),

      
       path('api/register/', include('register.urls')),
path('api/login/', LoginView.as_view()),
]