from rest_framework import serializers

from .models import AnswerOption, Quiz, QuizQuestion, QuizResult


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ("id", "text")


class QuizQuestionSerializer(serializers.ModelSerializer):
    answer_options = serializers.SerializerMethodField()

    class Meta:
        model = QuizQuestion
        fields = (
            "id",
            "text",
            "correct_answer",
            "is_multiple_answers",
            "answer_options",
        )

    def get_answer_options(self, obj):
        answer_options = AnswerOption.objects.filter(question=obj)
        answer_option_serializers = AnswerOptionSerializer(answer_options, many=True)
        return answer_option_serializers.data


class QuizSerializer(serializers.ModelSerializer):
    quiz_questions = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = (
            "id",
            "title",
            "description",
            "frequency",
            "company",
            "created_by",
            "quiz_questions",
        )

    def get_quiz_questions(self, obj):
        questions = QuizQuestion.objects.filter(quiz=obj)
        serializer = QuizQuestionSerializer(questions, many=True)
        return serializer.data


class QuizCreateQuestionSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionSerializer(many=True)

    class Meta:
        model = QuizQuestion
        fields = (
            "id",
            "text",
            "correct_answer",
            "is_multiple_answers",
            "answer_options",
        )


class QuizCreateSerializer(serializers.ModelSerializer):
    quiz_questions = QuizCreateQuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = (
            "id",
            "title",
            "description",
            "frequency",
            "company",
            "created_by",
            "quiz_questions",
        )

    def validate(self, data):
        quiz_questions_data = data.get("quiz_questions", [])

        if len(quiz_questions_data) < 2:
            raise serializers.ValidationError(
                {"__all__": ["The quiz must contain a minimum of 2 questions."]}
            )

        for question_data in quiz_questions_data:
            options_data = question_data.get("answer_options", [])

            if len(options_data) < 2:
                raise serializers.ValidationError(
                    {
                        "__all__": [
                            "Each question must have a minimum of 2 answer choices."
                        ]
                    }
                )

        return data

    def create(self, validated_data):
        quiz_questions_data = validated_data.pop("quiz_questions", [])
        quiz = Quiz.objects.create(**validated_data)

        for question_data in quiz_questions_data:
            answer_options_data = question_data.pop("answer_options", [])
            question = QuizQuestion.objects.create(quiz=quiz, **question_data)

            for option_data in answer_options_data:
                AnswerOption.objects.create(question=question, **option_data)

        return quiz


class QuizResultSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)

    class Meta:
        model = QuizResult
        fields = ("id", "quiz", "username", "answers", "score")
