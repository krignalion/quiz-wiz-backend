from django.db import transaction

from rest_framework import serializers

from .models import Answer, AnswerOption, Quiz, QuizQuestion, QuizResult


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ("id", "text")


class QuizQuestionSerializer(serializers.ModelSerializer):
    answer_options = serializers.SerializerMethodField()
    correct_answer = serializers.SerializerMethodField()

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

    def get_correct_answer(self, obj):
        correct_answer = obj.correct_answer.all()
        correct_answer_serializers = AnswerOptionSerializer(correct_answer, many=True)
        return correct_answer_serializers.data


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
    correct_answer = AnswerOptionSerializer(many=True)

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

            is_multiple_answers = question_data.get("is_multiple_answers", False)
            correct_answer_data = question_data.get("correct_answer", [])

            if not correct_answer_data:
                raise serializers.ValidationError(
                    {
                        "__all__": [
                            "Each question must have at least one correct answer."
                        ]
                    }
                )

            if is_multiple_answers and len(correct_answer_data) < 2:
                raise serializers.ValidationError(
                    {
                        "__all__": [
                            "If is_multiple_answers is True, there must be at least 2 correct answers."
                        ]
                    }
                )

            if len(options_data) < len(correct_answer_data):
                raise serializers.ValidationError(
                    {
                        "__all__": [
                            "The number of answer options must be greater than or equal to, the correct answers."
                        ]
                    }
                )

        return data

    def create(self, validated_data):
        quiz_questions_data = validated_data.pop("quiz_questions", [])
        quiz = Quiz.objects.create(**validated_data)

        quiz_questions = []
        answer_options = []
        correct_answers = []

        for question_data in quiz_questions_data:
            answer_options_data = question_data.pop("answer_options", [])
            correct_answer_data = question_data.pop("correct_answer", [])

            question = QuizQuestion(quiz=quiz, **question_data)
            quiz_questions.append(question)

            for option_data in answer_options_data:
                answer_options.append(AnswerOption(question=question, **option_data))

            for correct_answer_entry in correct_answer_data:
                correct_answers.append(
                    Answer(question=question, **correct_answer_entry)
                )

        with transaction.atomic():
            QuizQuestion.objects.bulk_create(quiz_questions)
            AnswerOption.objects.bulk_create(answer_options)
            Answer.objects.bulk_create(correct_answers)

        return quiz


class QuizResultSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)

    class Meta:
        model = QuizResult
        fields = ("id", "quiz", "username", "answers", "score")
