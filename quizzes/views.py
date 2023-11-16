from django.http import JsonResponse

from rest_framework import generics, serializers, status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Quiz
from .permissions import IsOwnerOrAdmin
from .serializers import (
    AnswerOptionSerializer,
    QuizCreateSerializer,
    QuizQuestionSerializer,
    QuizSerializer,
)


class QuizPagination(PageNumberPagination):
    page_size = 10


class CompanyQuizList(ListAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        company_id = self.kwargs["company_id"]
        return Quiz.objects.filter(company_id=company_id)


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    pagination_class = QuizPagination

    def create(self, request, *args, **kwargs):
        try:
            quiz_data = request.data
            serializer = self.get_serializer(data=quiz_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return JsonResponse(serializer.data, status=201, headers=headers)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def perform_create(self, serializer):
        try:
            quiz = serializer.save()

            quiz_questions_data = self.request.data.get("quiz_questions", [])
            for question_data in quiz_questions_data:
                question_serializer = QuizQuestionSerializer(data=question_data)
                question_serializer.is_valid(raise_exception=True)
                question = question_serializer.save(quiz=quiz)

                options_data = question_data.get("question_options", [])
                for option_data in options_data:
                    option_serializer = AnswerOptionSerializer(data=option_data)
                    option_serializer.is_valid(raise_exception=True)
                    option_serializer.save(question=question)

            return JsonResponse(serializer.data, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class CreateQuizView(generics.CreateAPIView):
    serializer_class = QuizCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def create(self, request, *args, **kwargs):
        try:
            quiz_data = request.data
            serializer = self.get_serializer(data=quiz_data)
            serializer.is_valid(raise_exception=True)
            quiz = self.perform_create(serializer)
            return Response(
                {
                    "message": "Quiz successfully created.",
                    "quiz": QuizCreateSerializer(quiz).data,
                },
                status=status.HTTP_201_CREATED,
            )
        except serializers.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "message": "Quiz successfully updated.",
                "quiz": QuizCreateSerializer(instance).data,
            }
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Quiz successfully deleted."}, status=status.HTTP_204_NO_CONTENT
        )
