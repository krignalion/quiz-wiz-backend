from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedTabularInline

from .models import AnswerOption, Quiz, QuizQuestion, QuizResult


class AnswerOptionInline(NestedTabularInline):
    model = AnswerOption
    extra = 0


class QuizQuestionInline(NestedTabularInline):
    model = QuizQuestion
    inlines = [AnswerOptionInline]
    extra = 0


class QuizAdmin(NestedModelAdmin):
    list_display = ("title", "description", "frequency", "company", "created_by")
    search_fields = ("title", "description")
    list_filter = ("company", "created_by")
    inlines = [QuizQuestionInline]

    class Meta:
        verbose_name_plural = "Quizzes"


class QuizResultAdmin(NestedModelAdmin):
    list_display = ("quiz", "user", "score")
    search_fields = ("quiz__title", "user__user__username")
    list_filter = ("quiz", "user")

    class Meta:
        verbose_name_plural = "Quiz Results"


admin.site.register(Quiz, QuizAdmin)
admin.site.register(AnswerOption)
admin.site.register(QuizResult, QuizResultAdmin)
