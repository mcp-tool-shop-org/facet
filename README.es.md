<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.md">English</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/facet/readme.png" alt="facet" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/facet/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/facet/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="docs/experiments/"><img src="https://img.shields.io/badge/record-spec%20%E2%86%92%20report%20%E2%86%92%20ruling-8a6f3f" alt="The record"></a>
  <a href="https://mcp-tool-shop-org.github.io/facet/"><img src="https://img.shields.io/badge/landing%20page-live-2ea043" alt="Landing page"></a>
</p>

<p align="center">
  <strong>A styled 2D concept goes in. A textured 3D asset comes out.</strong><br>
  Local hardware end to end · no non-commercial licence anywhere in the chain
</p>

---

El estilo se aplica **al objeto**, en el espacio de la textura; no se pinta por cada vista y luego se unen las partes. Si se introduce un modelo conceptual de arcilla con formas exageradas, el programa genera una malla texturizada cuyo color proviene de una referencia estilizada de *esa* misma malla, y todo aquello que la referencia no podía mostrar se rellena mediante un pincel de retoque con máscara y una herramienta de expansión que tiene en cuenta la superficie.

Recibe su nombre de los dos elementos que componen el problema: los polígonos y la superficie que deben cubrir.

## En qué punto se encuentra

**Cuatro elementos aceptados, pertenecientes a cuatro categorías diferentes, sin asignarles créditos.** Cada uno fue evaluado por el director en su propio formato (ya sea en la plataforma GLB o en hojas de tamaño completo), y no según un criterio que estableciera un umbral.

| asunto | clase | aceptado/a | referencia / pincel / dilatación |
|---|---|---|---|
| **Character (W3)** | humanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | vehículo, aparejo ligero | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bestia, membranas alares | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | objeto de atrezzo, casi bidimensional, en tonos grises. | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Las muestras corresponden a texeles válidos y **no son comparables entre diferentes sujetos**; por ejemplo, un barco oculta la mayor parte de sí mismo desde el nivel de los ojos y un animal se esconde a medias. Analice cada uno en relación con su propio límite máximo preestablecido, que es el valor al que alcanzan el **86–93 %**: la diferencia entre las filas radica en la geometría, no en la regresión. [Datos completos, con sus denominadores](docs/handbook/subjects.md).

**Se trata de un proceso, no de un generador que produce una sola imagen.** Al contradecir la especificación en ocho elementos concretos, el modelo obtiene **8 de 8** —la mediana de ΔE es de 46,3 frente a los 6,2 obtenidos con cinco imágenes de referencia—, mientras que la figura resultante sigue siendo la misma. La estructura se mantiene gracias a la malla y al control; los atributos definidos influyen en el resultado final.

## La ruta

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

Paso a paso, con la justificación de cada uno: **[el manual](docs/handbook/index.md)**.

## ¿Qué es lo que hace que funcione?

Seis hallazgos, cada uno de los cuales requirió un experimento y cada uno de los cuales tiene una aplicación más amplia que el objeto de estudio original. [La versión completa, con las mediciones](docs/findings.md).

- **Priorizar la forma sobre el estilo.** Los programas de reconstrucción interpretan el ruido superficial como geometría. Una arcilla limpia, similar a una escultura, con planos deliberadamente exagerados, produce una topología mejor que un sprite estilizado; el modelo gemelo estilizado se genera simultáneamente y sirve como referencia de color.
- **Definir el contorno del rostro para obtener un rostro.** Un recorte en forma de busto añade entre un **3,1 y un 4,5 veces** más polígonos a la cabeza, y la diferencia es estructural: párpados separados, una arruga en la frente, cavidades nasales modeladas; no se trata simplemente de un desenfoque más marcado.
- **Los gemelos pertenecen a una malla, no a un personaje.** Reutilizar un gemelo en diferentes mallas reduce el número de polígonos necesarios en un **62% → 22,7%**, ya que los brazos se proyectan hacia el espacio vacío junto al modelo. Generar gemelos a partir de la malla que se va a texturizar, cada vez.
- **La identidad reside en la instrucción.** Un elemento canónico no mencionado en la instrucción aparece por accidente y desaparecerá de la misma manera; esto se mide cuando unas rodilleras doradas resultan estar presentes en la imagen solo debido al ruido en un ControlNet defectuoso.
- **Consultar la geometría, no un umbral.** Reemplazar una máscara con el contorno exacto obtenido mediante trazado de rayos mejora la cobertura de referencia en un **28,4% → 39,1%** de texeles válidos; se trata de una adición estricta, sin difusión ni uso de la GPU. El método de selección basado en la mediana de los bordes ha fallado tres veces aquí y se descarta.
- **Eliminar lo que ninguna cámara puede ver, tanto del atlas como de la malla.** El 49% de los texeles del atlas son invisibles desde el exterior; excluir estas caras reduce la interpolación en un 68%. Excluir en lugar de eliminar hace que el fallo sea imposible, en lugar de simplemente detectable.

## ¿Qué no se ha resuelto?

Identificados y descritos en la página principal, no en una nota al pie. [Todos ellos se encuentran en el código](docs/known-defects.md).

- La banda de la hoja representa el 0,00 % de la referencia de la etapa 1 en las ocho cámaras; el acero sobre un fondo gris se sitúa exactamente en el umbral del objeto principal. La unión recupera el 55,72 %.
- Las líneas de contorno no están niveladas. Un límite de procedencia presenta una variación **5,5 veces** mayor que la textura ordinaria; la región a la que se refiere el director presenta una variación **9,5 veces** mayor.
- La dilatación provoca un efecto de sangrado entre las islas del atlas que no están relacionadas: el 74,9 % de los texeles dilatados toman su color de otra isla, con una distancia mediana de 0,177 en una figura de 1,0 de altura.
- Cada reconstrucción en esta ruta es una estructura hueca de doble pared; las paredes tienen un grosor aproximado de dos vóxeles. Ningún predicado volumétrico es válido para ninguna de ellas.

## Cómo se gestiona este repositorio

La disciplina es tan importante como el proceso en sí y existe por una razón: en un ciclo anterior, se llevaron a cabo diez sesiones en las que cada participante evaluó su propio trabajo y redactó unas conclusiones que se leyeron en la sesión siguiente como si fueran hechos establecidos. Nada de lo que ocurría en ese ciclo podía verificarse.

- **Especificación antes del trabajo, informe después, decisión final**: y la sesión que diseña un experimento nunca evalúa sus propios resultados. Hay veinte experimentos en [el registro](docs/experiments/).
- **Las correcciones se aplican en su lugar, junto a la medición que las refutó**, nunca como eliminaciones discretas. En la sesión inicial, se falsificaron seis afirmaciones heredadas y las seis siguen siendo legibles junto a lo que las reemplazó.
- **Los errores permanecen en el repositorio con su explicación.** [`tools/superseded/`](docs/tools.md) no es un archivo; cualquiera puede ejecutar esas herramientas y observar cómo fallan de la misma manera.
- **Un resultado negativo es un éxito total**, se informa y se cierra en lugar de ajustarse para obtener un número específico.
- **Las pruebas están vinculadas al commit que modifica el código**: 213 superaron la prueba con dos desarrolladores, con CI restringida por rutas en las 205 versiones herméticas.
- **El registro es consultable.** Un índice SQLite + FTS5 sobre todo el historial, verificado en cuatro puntos. Encontró un recuento de decisiones que el texto había indicado incorrectamente en tres sitios, contando el propio registro.

## Donde está todo

| | |
|---|---|
| **[El manual](docs/handbook/index.md)** | la guía: el recorrido por etapas, los temas que se tratan, el sistema de clasificación. |
| **[El registro](docs/experiments/)** | veinte experimentos: especificación, informe, veredicto y cada predicción realizada antes de la medición. |
| **[Lo que aprendió la ruta](docs/findings.md)** | los resultados duraderos y las reglas obtenidas con esfuerzo, en su totalidad. |
| **[Estado de cada herramienta](docs/tools.md)** | lo que funciona, lo que está obsoleto y la evidencia para cada uno. |
| **[Defectos conocidos](docs/known-defects.md)** | todo aquello que no se ha resuelto, medido y localizado en el código. |
| **[La secuencia de eventos](docs/arc-history.md)** | el historial cronológico, con las correcciones intactas. |
| **[CLAUDE.md](CLAUDE.md)** | cómo trabajar aquí: los roles, las reglas y el costo de cada uno. |

## Situación de la licencia

Cada etapa se ejecuta localmente y cumple con los requisitos comerciales: SDXL (OpenRAIL++), MV-Adapter (código abierto), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Excluido deliberadamente, con la razón: **nvdiffrast** (no comercial; se aplica aquí mediante un mecanismo de seguridad estructural, no mediante una certificación), **Hunyuan3D-Paint** (la licencia no es válida en la UE, el Reino Unido y Corea del Sur), **MVPaint** y **TEXGen** (ninguna licencia) y **UltraSharp / SUPIR / StableSR** (ampliadores de escala no comerciales).

## Modelo de confianza y amenazas

Facet se ejecuta completamente en su propia máquina; cada herramienta es un script que invoca sobre rutas que usted escribe, por lo que la pregunta útil no es *qué permisos solicita esta aplicación*, sino *qué hacen estos scripts con su máquina*. La respuesta se obtiene mediante la medición, y cada iteración puede volver a ejecutarse; la política completa está en [SECURITY.md](SECURITY.md):

- **Datos accedidos:** mallas, texturas, imágenes y archivos JSON en el disco local, en las rutas que usted proporciona en la línea de comandos. Además, `docs/index/facet.db`, que es *derivado*; no contiene nada que ya no fuera un archivo en este repositorio, y `facet_index.py build` lo regenera desde cero.
- **Datos NO accedidos:** nunca se accede a ninguna credencial. Nada aquí lee, almacena ni transmite un token, una clave o una contraseña, y ninguno está presente en el árbol; se ha realizado una búsqueda de claves con prefijos de proveedor, GitHub PAT, tokens de Slack, ID de clave de AWS, bloques de clave privada, tokens de portador y asignaciones `api_key`/`password` en línea; **cero coincidencias**, no se rastrea ningún archivo con formato de credencial.
- **No hay telemetría.** Ninguna se recopila ni se envía. No hay opción para desactivarla porque no hay nada que desactivar.
- **Salida de red:** dos de las treinta y cuatro herramientas abren un socket: `restylize_views.py` y `texpass_brush.py`, y ambas llaman a una API HTTP de ComfyUI en `--host`, **predeterminado `127.0.0.1:8188`**. Nada más en `tools/` realiza una llamada de red.
- **Permisos:** usuario normal. Sin elevación de privilegios, sin instalación de servicios, sin escrituras en la configuración del sistema o el registro.

Se revelan tres aspectos críticos en lugar de ocultarlos, porque una nota de seguridad que solo enumera garantías no es un modelo de amenazas: **las operaciones de archivo no están aisladas** (una herramienta escribe donde sus argumentos indican); **las rutas locales absolutas están integradas en muchas herramientas y documentos**: 114 ocurrencias en 26 archivos, no son secretos, sino una divulgación del diseño de una máquina, y la razón por la que la mayoría de las herramientas no se ejecutarán sin modificar en otro lugar; y **los fallos inesperados aparecen como rastreos de pila de Python**, sin una puerta de enlace `--debug` ni un formato de error estructurado. Las detenciones deliberadas son mensajes `ANDON:` que contienen la medición que las activó. Ese es el contrato del instrumento de investigación, y [SHIP_GATE.md](SHIP_GATE.md) registra exactamente cuándo deja de ser lo suficientemente bueno.

**Estado del soporte:** este repositorio se desarrolla a cielo abierto, en una sola máquina, por un solo director y un par rotatorio de sesiones de asesoramiento y ejecución. `main` es el único estado compatible. No hay canal de lanzamiento, ni política de retrocompatibilidad, ni SLA; en cambio, existe el registro: cada afirmación está junto al código que la produce, y [docs/experiments](docs/experiments/) contiene las especificaciones, el informe y el veredicto para cada una.

## Requisitos

Blender 5.x, Python 3.11+ con `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Se necesita una instalación local de ComfyUI solo para el pincel de retoque. Desarrollado en una RTX 5090; la capacidad de VRAM es más importante que la velocidad bruta.

CI ejecuta el subconjunto hermético del conjunto en **ubuntu-latest / Python 3.12** con instalaciones fijas (`.github/workflows/ci.yml`); la capa de artefactos necesita los árboles registrados bajo `E:\AI\training`, que no están en git, por lo que CI los excluye por diseño. Localmente, `python -m pytest` ejecuta las **213** pruebas y `python -m pytest -m "not artifacts"` ejecuta las **205** pruebas que reproduce CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
