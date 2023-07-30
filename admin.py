from typing import Any
from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from general.models import (
    Post,
    User,
    Comment,
    Reaction,
)
from general.filters import AuthorFilter, PostFilter
from django_admin_listfilter_dropdown.filters import ChoiceDropdownFilter


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "username",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    )
    readonly_fields = (
        "date_joined",
        "last_login",
    )
    search_fields = (
        "id",
        "username",
        "email",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    )
    fieldsets = (
        (
            "Личные данные", {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                )
            }
        ),
        (
            "Учетные данные", {
                "fields": (
                    "username",
                    "password",
                )
            }
        ),
        (
            "Статусы", {
                "classes": (
                    "collapse",
                ),
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                )
            }
        ),
        (
            None, {
                "fields": (
                    "friends",
                )
            }
        ),
        (
            "Даты", {
                "fields": (
                    "date_joined",
                    "last_login",
                )
            }
        )
    )


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "get_body",
        "get_comment_count",
        "created_at",
    )
    fields = (
        "id",
        "author",
        "title",
        "body",
        "created_at",
        "get_body",
        "get_comment_count",
    )

    readonly_fields = (
        "id",
        "created_at",
        "get_body",
        "get_comment_count"
    )

    list_filter = (
        AuthorFilter,
        "author", "created_at"
    )
    search_fields = (
        "id",
        "title",
    )

    def get_body(self, obj):
        max_length = 64
        if len(obj.body) > max_length:
            return obj.body[:61] + "..."
        return obj.body
    get_body.short_description = "body"

    def get_comment_count(self, obj):
        return obj.comments.count()
    get_comment_count.short_description = "count comment"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("comments")


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "post",
        "body",
        "created_at",
    )
    list_display_links = (
        "id",
        "body",
    )
    search_fields = (
        "id",
    )
    list_filter = (
        PostFilter,
        AuthorFilter,
    )
    raw_id_fields = (
        "author",
    )


@admin.register(Reaction)
class ReactionModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "value",
        "post",
    )
    search_fields = (
        "id",
        "author__username",
        "post",
    )
    list_filter = (
        PostFilter,
        AuthorFilter,
        ("value", ChoiceDropdownFilter),
    )
    raw_id_fields = (
        "author",
        "post",
    )


admin.site.unregister(Group)
