from django.contrib import admin

from .models import Comment, Post, PostMedia, Category


class PostMediaInline(admin.TabularInline):
    model = PostMedia
    extra = 1
    fields = ("file", "caption", "order")


class CommentInline(admin.TabularInline):
    """Permite ver y borrar los comentarios desde la propia entrada."""

    model = Comment
    extra = 0
    can_delete = True
    fields = ("name", "body", "created_at")
    readonly_fields = ("name", "body", "created_at")

    def has_add_permission(self, request, obj=None):
        return False  # los comentarios los escriben los visitantes, no el admin


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "published_at", "comment_count")
    list_filter = ("published", "published_at")
    search_fields = ("title", "summary", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    inlines = [PostMediaInline, CommentInline]

    @admin.display(description="comentarios")
    def comment_count(self, obj):
        return obj.comments.count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Moderación: listado de todos los comentarios con borrado individual o masivo."""

    list_display = ("name", "post", "short_body", "created_at")
    list_filter = ("post", "created_at")
    search_fields = ("name", "body")
    readonly_fields = ("post", "name", "body", "created_at")

    @admin.display(description="comentario")
    def short_body(self, obj):
        return obj.body if len(obj.body) <= 60 else obj.body[:57] + "…"

    def has_add_permission(self, request):
        return False

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}