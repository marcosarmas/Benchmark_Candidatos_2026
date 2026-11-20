# Benchmark de candidatos a alcaldías 2026

Comparación neutral de las propuestas de los candidatos a alcalde en las elecciones seccionales del 29 de noviembre de 2026:

- **Quito** (10 candidatos): `index.html`
- **Latacunga** (9 candidatos): `index.html?ciudad=latacunga`. Los planes de trabajo oficiales del CNE están en `fuentes/latacunga/`.
- **CPCCS** (65 candidatos, se eligen 7): `index.html?ciudad=cpccs`. Tiene los perfiles de los 65 y las propuestas publicadas en la prensa, que cubren a 17 candidatos. Todavía no tiene afinidad, porque los planes oficiales no se han revisado. Este conjunto define sus propios ejes en `ejes_custom` y usa `"tipo": "cpccs"`.
 No hay ranking: cada propuesta lleva su fuente y cuatro indicadores descriptivos (concreta, plazo, costo, competencia municipal).

## Mi afinidad
El usuario responde un cuestionario de contrapesos (método *MaxDiff*): en cada pantalla ve 4 temas de distintos ejes y marca el que **más** y el que **menos** le importa. Una ronda muestra cada tema del catálogo de la ciudad (`data/<ciudad>/intereses.json`) una vez, en unas 20 pantallas. Con "Seguir afinando" se hace otra ronda con grupos distintos.

- **Peso de cada tema:** 3 + 2 × (veces "más" − veces "menos") ÷ veces mostrado, en un rango de 1 a 5.
- **Puntos por candidato:** para cada tema se toma su mejor propuesta etiquetada. Vale 50 puntos base, +20 si es concreta, +10 si tiene plazo, +10 si indica costo y +10 si es competencia municipal (+5 si es compartida).
- **Afinidad:** el promedio ponderado por peso.

Los resultados salen primero en modo ciego, y se pueden compartir por enlace con los pesos en el hash. El avance se guarda solo en el navegador del usuario, en `localStorage`.

## Estructura
- `index.html`: la página (estática, sin dependencias de build).
- `data/<ciudad>/candidatos.json`: los datos fuente de cada ciudad; edítelos aquí.
- `data/<ciudad>/intereses.json`: el catálogo de intereses de esa ciudad; cada propuesta lleva `intereses` en `candidatos.json`.
- `data/<ciudad>.js`: generado; regenerar con `python3 scripts/build_data.py`.
- Para agregar una ciudad: cree `data/<ciudad>/`, genere los datos y añádala a `window.CIUDADES` en `index.html`.

## Publicar en GitHub Pages
Settings → Pages → *Deploy from a branch* → rama `main`, carpeta `/ (root)`.

## Correcciones
Abra un issue con el enlace a la fuente.
