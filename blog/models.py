import os

from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class PostQuerySet(models.QuerySet):
    def published(self):
        """Entradas visibles para el público (publicadas y con fecha ya cumplida)."""
        return self.filter(published=True, published_at__lte=timezone.now())

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    """Una entrada del blog. Solo el administrador puede crearlas (desde /admin)."""

    title = models.CharField("título", max_length=200)
    slug = models.SlugField(
        "slug",
        max_length=220,
        unique=True,
        blank=True,
        help_text="Parte de la URL. Se completa sola a partir del título.",
    )
    summary = models.CharField(
        "resumen",
        max_length=300,
        help_text="Se muestra en el listado del blog y en la home.",
    )
    content = models.TextField(
        "contenido",
        help_text="Texto de la entrada. Los saltos de línea se respetan; una línea en blanco separa párrafos.",
    )
    cover = models.ImageField(
        "portada",
        upload_to="posts/covers/",
        blank=True,
        help_text="Imagen principal (opcional).",
    )
    categories = models.ManyToManyField(
        Category,
        related_name="posts",
        blank=True
    )
    published = models.BooleanField(
        "publicada",
        default=True,
        help_text="Destildala para guardar la entrada como borrador.",
    )
    published_at = models.DateTimeField("fecha de publicación", default=timezone.now)
    updated_at = models.DateTimeField("última edición", auto_now=True)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ["-published_at"]  # cronológico: la más nueva primero
        verbose_name = "entrada"
        verbose_name_plural = "entradas"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "entrada"
            slug, n = base, 2
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})


IMAGE_EXTENSIONS = ("jpg", "jpeg", "png", "gif", "webp")
VIDEO_EXTENSIONS = ("mp4", "webm", "ogg")
OTHER_EXTENSIONS = ("pdf",)


class PostMedia(models.Model):
    """Archivo multimedia (imagen, video o PDF) adjunto a una entrada."""

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="media", verbose_name="entrada"
    )
    file = models.FileField(
        "archivo",
        upload_to="posts/media/",
        validators=[
            FileExtensionValidator(
                IMAGE_EXTENSIONS + VIDEO_EXTENSIONS + OTHER_EXTENSIONS
            )
        ],
    )
    caption = models.CharField("epígrafe", max_length=200, blank=True)
    order = models.PositiveSmallIntegerField("orden", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "archivo multimedia"
        verbose_name_plural = "archivos multimedia"

    def __str__(self):
        return self.caption or os.path.basename(self.file.name)

    @property
    def extension(self):
        return os.path.splitext(self.file.name)[1].lower().lstrip(".")

    @property
    def is_image(self):
        return self.extension in IMAGE_EXTENSIONS

    @property
    def is_video(self):
        return self.extension in VIDEO_EXTENSIONS


class Comment(models.Model):
    """Comentario anónimo (nombre + texto). Solo el administrador puede borrarlos."""

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", verbose_name="entrada"
    )
    name = models.CharField("nombre", max_length=60)
    body = models.TextField("comentario", max_length=1000)
    created_at = models.DateTimeField("fecha", auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "comentario"
        verbose_name_plural = "comentarios"

    def __str__(self):
        return f"{self.name} en «{self.post.title}»"
