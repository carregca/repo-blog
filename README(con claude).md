# Sitio web personal — Facundo Garcia (Django)

Portfolio personal con blog, desarrollado con **Django** para el Laboratorio de Algoritmos y Estructuras de Datos.
Toma el portfolio HTML/CSS original y le suma un blog con entradas cronológicas, archivos multimedia y comentarios, manteniendo la misma estética (tema oscuro/claro, Space Mono + Inter, bordes finos, imágenes en escala de grises).

## Qué hace

- **Home / portfolio** (`/`): mismas secciones que el sitio original (inicio, sobre mí, habilidades, proyectos, contacto) más una sección con las 3 últimas entradas del blog.
- **Blog** (`/blog/`): listado ordenado cronológicamente (más nueva primero) y paginado.
- **Entrada** (`/blog/<slug>/`): texto, portada, galería multimedia (imágenes, videos MP4/WebM/OGG y PDF), navegación a la entrada anterior/siguiente y comentarios.
- **Comentarios**: cualquier visitante puede comentar con nombre + texto (sin registro). Solo el administrador puede eliminarlos, desde `/admin/` o con el botón *Eliminar* que le aparece en la propia entrada cuando está logueado.
- **Solo el administrador crea entradas**: no existe ninguna vista pública de creación; se cargan desde `/admin/`. También puede guardar borradores y programar fechas de publicación.
- Tema claro/oscuro que se recuerda entre páginas (localStorage).
- Anti-spam básico: campo *honeypot* en el formulario de comentarios.

## Estructura

```
portfolio_django/
├── manage.py
├── requirements.txt
├── config/            # settings, urls raíz, wsgi/asgi
├── portfolio/         # app de la home (view + urls)
├── blog/              # app del blog
│   ├── models.py      # Post, PostMedia, Comment
│   ├── admin.py       # alta de entradas y moderación de comentarios
│   ├── forms.py       # CommentForm (+ honeypot)
│   ├── views.py       # listado, detalle (+ comentar), eliminar comentario
│   ├── urls.py
│   ├── tests.py
│   └── management/commands/seed_blog.py   # datos de ejemplo
├── templates/
│   ├── base.html      # header, footer y tema compartidos
│   ├── portfolio/index.html
│   └── blog/          # post_list, post_detail, _post_card
├── static/
│   ├── css/styles.css # CSS original del portfolio (sin modificar)
│   ├── css/blog.css   # estilos nuevos del blog, mismo lenguaje visual
│   ├── js/theme.js
│   ├── images/, cv/, favicon.svg
└── media/             # archivos subidos desde el admin (no se versiona)
```

## Puesta en marcha

Requiere Python 3.10+.

```bash
# 1. Entorno virtual
python -m venv .venv
source .venv/bin/activate          # Windows (cmd):  .venv\Scripts\activate
                                   # Windows (PowerShell): .venv\Scripts\Activate.ps1

# 2. Dependencias
pip install -r requirements.txt

# 3. Base de datos (SQLite) — la migración inicial ya viene incluida
python manage.py migrate

# 4. Usuario administrador (es quien crea entradas y borra comentarios)
python manage.py createsuperuser

# 5. (Opcional) cargar 3 entradas de ejemplo con un comentario
python manage.py seed_blog

# 6. Levantar el servidor
python manage.py runserver
```

- Sitio: <http://127.0.0.1:8000/>
- Admin: <http://127.0.0.1:8000/admin/>

### Cómo publicar una entrada

1. Entrar a `/admin/` → **Entradas** → **Añadir entrada**.
2. Completar título, resumen y contenido (una línea en blanco separa párrafos). La portada es opcional.
3. En **Archivos multimedia** subir imágenes, videos o PDF, con epígrafe y orden.
4. Guardar. Si se destilda *Publicada* queda como borrador (solo el admin logueado lo ve).

### Tests

```bash
python manage.py test
```

Cubren: slugs únicos, orden cronológico, borradores ocultos, comentar sin login, honeypot, y que solo el admin pueda borrar comentarios.

## Decisiones de diseño

- **Comentarios sin registro**: el enunciado deja a elección un sistema de usuarios. Elegí no implementarlo (nombre + texto) para mantener el foco en el blog; el costo es que no hay forma de validar identidades, por eso el honeypot y la moderación por el admin.
- **Contenido en texto plano** con `linebreaks`: Django escapa el HTML, así que ningún visitante ni entrada puede inyectar código. Se evitó Markdown para no sumar dependencias.
- **`styles.css` se dejó tal cual** y todo lo nuevo vive en `blog.css`, cargado después, reutilizando las variables `--color-*` y las mismas convenciones (esquinas, líneas, mono para metadatos, modo claro con `body.light-mode`).
- **Sin CMS externo**: se resolvió con el admin de Django para entender bien modelos, vistas y templates.

## Documentación del proceso

Ver [`BITACORA.md`](BITACORA.md).
