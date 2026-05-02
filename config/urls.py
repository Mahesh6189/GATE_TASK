from django.contrib import admin
from django.urls import path
from subjects.views import SubjectListCreateView
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "status": "running",
        "message": "GATE API is working "
    })

urlpatterns = [
    path('', home),  # 
    path('admin/', admin.site.urls),
    path('api/subjects/', SubjectListCreateView.as_view()),
]