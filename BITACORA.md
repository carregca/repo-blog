# Bitácora — TP Django: sitio personal con blog

## Plan

1. Crear el proyecto Django (`config`) y dos apps: `portfolio` y `blog`.
2. Convertir el HTML en templates con herencia (`base.html`) y `{% static %}`.
3. Modelos del blog: `Post`, `PostMedia`, `Comment`.
4. Admin para crear entradas y moderar comentarios.
5. Vistas: listado paginado, detalle con formulario de comentarios.
6. Estilos del blog coherentes con el portfolio.
7. Tests, README y entrega.

## Dificultades y cómo las resolví

**1. Un selector global rompió el encabezado de la entrada.** `styles.css` define estilos directamente sobre la etiqueta `header` (posición fija, fondo, blur). Al usar `<header>` dentro de la entrada para el título, se comportaba como una segunda barra fija. Lo cambié por un `<div class="post-header">`. Lección: los selectores de etiqueta desnuda condicionan todo el sitio.

**2. Especificidad del CSS heredado.** Reglas como `.section > p` pisaban estilos nuevos (por ejemplo el aviso de borrador). Resolví subiendo la especificidad del selector nuevo en lugar de tocar `styles.css`.

**3. El tema oscuro/claro no se recordaba.** En una sola página no importaba, pero con un blog el visitante cambia de página y el tema volvía a oscuro. Moví el script a `theme.js` y guardo la elección en `localStorage`. También corregí un detalle del modo claro: el subrayado del menú era blanco sobre fondo claro.

**4. Slugs únicos.** Dos entradas con el mismo título generarían la misma URL. `Post.save()` genera el slug desde el título y agrega `-2`, `-3`… si ya existe.

**5. "Solo el admin borra comentarios".** Además del admin de Django, agregué un botón *Eliminar* en la entrada que solo se muestra con el permiso `blog.delete_comment`. La vista lo vuelve a verificar del lado del servidor (403 si no lo tiene) y solo acepta POST, porque ocultar el botón no alcanza como seguridad.

**6. Spam en comentarios sin login.** Sin registro, cualquiera puede publicar. Sumé un campo honeypot y validación de largo; la moderación queda a cargo del admin.

**7. Archivos multimedia.** `ImageField` necesita Pillow. Para videos y PDFs usé un modelo aparte (`PostMedia`) con un validador de extensiones, y en el template decido cómo mostrar cada archivo (`<img>`, `<video>` o enlace). En desarrollo hay que servir `MEDIA_ROOT` desde `urls.py`.
