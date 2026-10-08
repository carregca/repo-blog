from django.urls import path
from .views import CategoryPostListView
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("comentario/<int:pk>/eliminar/", views.comment_delete, name="comment_delete"),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
    path("categoria/<slug:slug>/", CategoryPostListView.as_view(), name="category_posts"),
]
