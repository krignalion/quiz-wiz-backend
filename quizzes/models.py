from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models

from company.models import Company
from users.models import UserProfile


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    frequency = models.PositiveIntegerField(default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def clean(self):
        question_count = self.quizquestion_set.count()

        if question_count < 2:
            raise ValidationError(
                {"__all__": ["The quiz must contain a minimum of 2 questions."]}
            )

        super().clean()


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    correct_answer = ArrayField(models.CharField(max_length=255), default=list)
    is_multiple_answers = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = "Quizzes"

    def clean(self):
        if self.answer_options.count() < 2:
            raise ValidationError(
                {
                    "__all__": [
                        'Each question must have a minimum of 2 answer choices. \
                         You have a question right now "{}" only {} option(s)'.format(
                            self.text, self.answer_options.count()
                        )
                    ]
                }
            )

        super().clean()


class AnswerOption(models.Model):
    question = models.ForeignKey(
        QuizQuestion, on_delete=models.CASCADE, related_name="answer_options"
    )
    text = models.TextField()

    def __str__(self):
        return self.text


class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    answers = ArrayField(models.TextField(), default=list)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.quiz.title

    class Meta:
        verbose_name_plural = "Quiz Results"
