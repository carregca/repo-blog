from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .forms import CommentForm
from .models import Comment, Post


class PostListView(ListView):
    """Listado cronológico (más nuevas primero) con paginación."""

    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.published()

class CategoryPostListView(ListView):
    """Listado de entradas pertenecientes a una categoría."""

    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.published().filter(
            categories__slug=self.kwargs["slug"]
        )

def post_detail(request, slug):
    """Detalle de una entrada + formulario y listado de comentarios."""
    # El staff puede previsualizar borradores; el público solo ve las publicadas.
    queryset = Post.objects.all() if request.user.is_staff else Post.objects.published()
    post = get_object_or_404(queryset, slug=slug)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "¡Gracias! Tu comentario fue publicado.")
            return redirect(f"{post.get_absolute_url()}#comentarios")
    else:
        form = CommentForm()

    published = Post.objects.published()
    context = {
        "post": post,
        "media_items": post.media.all(),
        "comments": post.comments.all(),
        "form": form,
        "newer_post": published.filter(published_at__gt=post.published_at)
        .order_by("published_at")
        .first(),
        "older_post": published.filter(published_at__lt=post.published_at).first(),
    }
    return render(request, "blog/post_detail.html", context)


@require_POST
def comment_delete(request, pk):
    """Borra un comentario. Solo quien tenga el permiso (el administrador)."""
    if not request.user.has_perm("blog.delete_comment"):
        raise PermissionDenied
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    comment.delete()
    messages.success(request, "Comentario eliminado.")
    return redirect(f"{post.get_absolute_url()}#comentarios")
