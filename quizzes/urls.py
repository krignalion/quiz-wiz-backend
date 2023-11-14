from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CompanyQuizList, CreateQuizView, QuizDetailView, QuizViewSet

router = DefaultRouter()
router.register(r"", QuizViewSet, basename="quiz")

urlpatterns = [
    path("create_quiz/", CreateQuizView.as_view(), name="create_quiz"),
    path(
        "companies/<int:company_id>/",
        CompanyQuizList.as_view(),
        name="company-quiz-list",
    ),
    path("quiz/<int:pk>/", QuizDetailView.as_view(), name="quiz_detail"),
    path("", include(router.urls)),
]
