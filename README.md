# Benchmark de candidatos a la Alcaldía de Quito 2026

Comparación neutral de las propuestas de los 10 candidatos a la Alcaldía del Distrito Metropolitano de Quito (elecciones seccionales del 29 de noviembre de 2026). No hay ranking: cada propuesta lleva su fuente y cuatro indicadores descriptivos (concreta, plazo, costo, competencia municipal).

## Mi afinidad
Cada ítem del catálogo (`data/intereses.json`) se califica del 1 al 5 según su importancia; los ítems sin calificar no cuentan. Para cada interés se toma la mejor propuesta etiquetada de cada candidato: 50 puntos base, +20 si es concreta, +10 si tiene plazo, +10 si indica costo y +10 si es competencia municipal (+5 si es compartida). La afinidad es el promedio ponderado por la calificación de cada ítem. Los resultados salen primero en modo ciego, se pueden compartir por enlace y se calculan en el navegador, sin guardar nada.

## Estructura
- `index.html`: la página (estática, sin dependencias de build).
- `data/candidatos.json`: los datos fuente; edítelos aquí.
- `data/intereses.json`: catálogo de intereses; cada propuesta lleva `intereses` en `candidatos.json`.
- `data.js`: generado; regenerar con `python3 scripts/build_data.py`.

## Publicar en GitHub Pages
Settings → Pages → *Deploy from a branch* → rama `main`, carpeta `/ (root)`.

## Correcciones
Abra un issue con el enlace a la fuente.
