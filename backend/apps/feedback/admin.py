from django.contrib import admin

from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    """Админка обратной связи."""

    list_display = [
        'id',
        'title',
        'status',
        'email',
        'created_at',
        'updated_at',
    ]
    search_fields = [
        'title',
        'email',
    ]
    list_filter = [
        'status',
        'created_at',
        'updated_at',
    ]


admin.site.register(Feedback, FeedbackAdmin)
