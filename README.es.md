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
  Local-first — your own GPU, with a metered cloud step where it will not fit<br>
  No non-commercial licence anywhere in the chain
</p>

---

El estilo se aplica **al activo**, en el espacio de la textura; no se pinta por vista y luego se une. Si le proporciona a la ruta un concepto de arcilla con formas exageradas, este devolverá una malla texturizada cuyo color provendrá de una referencia estilizada de *esa* malla, y todo aquello que la referencia no pueda ver se rellenará mediante un pincel de retoque enmascarado y una dilatación consciente de la superficie.

Recibe su nombre de las dos partes del problema: los polígonos y la cara que deben mantener.

## Instalar

La ruta en sí es un conjunto de scripts locales que se ejecutan sobre rutas que usted escribe; clone el repositorio y lea [cómo empezar](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Dos servidores se distribuyen como un paquete**: el índice de registros, para que un asistente pueda consultar la secuencia de pruebas en lugar de leerla, y **a partir de la versión 0.4.0, el servidor de medición**, de modo que dos activos medidos con meses de diferencia sigan una única ruta de código.

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` es el servidor MCP stdio sobre el registro (seis herramientas, con la verificación de cuatro puntos como superficie de salud que rechaza) y `facet-index` es el índice en sí (`build` / `verify` / `q` / `claims`). Ejecute cualquiera de ellos desde dentro de una copia; `--db` nombra un índice diferente.

### El servidor de medición: nuevo en la versión 0.4.0

`facet-measure` responde a la **mitad numérica** de una comparación y nunca indica si la salida es buena. Cada carga útil contiene la versión del servidor, el hash del archivo propio del instrumento y un hash de configuración, y `measure_report` **rechaza** comparar cuando hay una discrepancia; esta es la propiedad para la que existe todo esto.

Verificado ejecutando un **verbo** en lugar de `--help`: una malla de control devuelve 786.432 caras con una envolvente de identidad completa en una máquina que no tiene ninguna copia.

**Lo que obtenga depende de una cosa, y es su versión de Python:**

| su Python | `[measure-full]` le proporciona |
|---|---|
| **3.11 / 3.12** | **las ocho herramientas**: `open3d` se instala desde PyPI |
| **3.13** | cuatro herramientas: `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 es la última *versión* y publica paquetes cp38-cp312 sin **ningún paquete fuente (sdist)**, por lo que en 3.13 no hay nada en PyPI para instalar. El paquete adicional lo incluye detrás de `python_version < "3.13"`, por lo que la instalación **tiene éxito** allí y las cuatro herramientas de geometría devuelven **`4` RECHAZADO**, indicando lo que necesitan, en lugar de que falle toda la instalación.

**Para obtener las ocho en Python 3.13**, Open3D publica los paquetes cp313 actuales en su canal de desarrollo continuo. Una URL directa es válida en una línea de comandos; solo está prohibido dentro de los metadatos del paquete publicado:

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **En Windows y macOS, los paquetes de desarrollo tienen el sufijo `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` al momento de escribir) y el nombre cambia a medida que `main` cambia; enumere los activos en [la versión `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) y tome la versión actual. **Esta compilación es con la que se midieron los números dependientes de open3d de esta ruta**, y es una verdadera frontera de comparabilidad: la envolvente de identidad registra el hash del instrumento, no sus dependencias — [E31](docs/experiments/E31-ruling.md).

*Hasta la versión 0.3.1, el paquete contenía dos archivos `.py` y ninguno de los instrumentos de medición, por lo que un servidor de medición instalado no tenía nada que ejecutar. Nadie se dio cuenta durante cuatro versiones porque este repositorio ES la copia: la herramienta funcionaba donde se compiló y nunca había estado en otro lugar.*

⚠ **`pip install facet-mcp` estaba roto en todas las versiones publicadas hasta la versión 0.3.0, y se corrigió en la versión 0.3.1.** El paquete instala `facet_index` como un módulo de nivel superior, por lo que hasta e incluyendo la versión 0.3.0, resolvía la ubicación del registro contra `<venv>/Lib`, que no contiene ni el corpus ni el índice, y `build`, `claims` y `q` sin `--db` fallaban todos.
**En la versión 0.3.0 o anterior, utilice el archivo binario `npx` de arriba.**

A partir de la versión 0.3.1, la raíz se resuelve **probando si existe el registro** en lugar de asumir que existe: ejecute cualquiera de los comandos desde dentro de una copia y lo encontrará; ejecútelo desde cualquier otro lugar y devolverá **`4` RECHAZADO**, indicando ambos directorios que intentó y ambos marcadores que buscó. `$FACET_INDEX_DB` ahora es leído por ambos comandos, y selecciona qué *índice*, nunca qué *corpus*. Medido en un paquete compilado a partir de `main` e instalado en un entorno virtual limpio — [E24](docs/experiments/E24-ruling.md).

*Este bloque se ha corregido dos veces. Primero decía `pipx install facet-mcp # o el paquete Python directamente `, until v0.3.0's read-back ran a **verb** instead of ` --help`.
Luego, indicaba que el paquete "solo funciona para `q` y `claims`"; **`claims` tampoco funcionó**, lo cual E24 descubrió al ejecutarlo. Ambas correcciones se encuentran en [known-defects.md](docs/known-defects.md) con sus mediciones.*

## Estado actual

**Cuatro activos aceptados, de cuatro clases de sujetos, sin costo alguno.** Cada uno fue evaluado por el Director a su propio nivel de zoom: en el archivo GLB o en hojas de tamaño completo; no mediante una métrica que supere un umbral.

| sujeto | clase | aceptado | referencia / pincel / dilatación |
|---|---|---|---|
| **Character (W3)** | humanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | vehículo, rigging delgado | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bestia, membranas de alas | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | accesorio, casi 2D, gris sobre gris | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Las cuotas son de texeles válidos y **no son comparables entre sujetos**: un barco oculta la mayor parte de sí mismo desde el nivel de los ojos y un animal oculta la mitad. Lea cada uno en relación con su propio límite de alcance pre-registrado, en relación con el cual alcanzan el **86–93%**: la diferencia entre las filas es la geometría, no la regresión. [Números completos, con sus denominadores](docs/handbook/subjects.md).

**Es una canalización, no un generador de un solo carácter.** Contradiga la especificación en ocho elementos nombrados y el indicador ganará **8 de 8**: ΔE medio de 46,3 frente a 6,2 en cinco controles mantenidos; mientras que la figura permanece siendo el mismo hombre. La estructura se mantiene mediante la malla y el control; los atributos nombrados se basan en el indicador.

## La ruta

```
  styled 2D concept ╌╌► clay prep ╌╌╮   ← CANDIDATE hop, walked once. Not a route
                                    ╎     stage. Everything below it is the route.
                                    ▼
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

Paso a paso, con la justificación de cada uno: **[el manual](docs/handbook/index.md)**.

**El trazado discontinuo es nuevo y se ha diseñado deliberadamente para que no sea sólido.** La primera sección de la ruta siempre ha mostrado el texto «concepto en arcilla» y, hasta ahora, nada aquí lo hacía realidad: cada pieza de arcilla llegaba a mano y se manipulaba durante el proceso. Ahora existe una herramienta que permite transformar un concepto en arcilla, y su primer prototipo ya se ha probado a tamaño real: la pose, las protecciones para las muñecas, el adorno del cinturón y el dobladillo desgarrado se han incorporado; la masa de la melena no; se midió una ligera pérdida de color en toda la imagen, con un fondo acromático uniforme: **C\* p99.9 = 13.15**. **Lo que este prototipo no puede demostrar es si la malla resultante mejora**, y esa es la única pregunta que justifica su uso, por lo que sigue siendo un candidato con sus resultados registrados: **[preparación del concepto](docs/concept-prep.md)**.

## ¿Qué es lo que hace que funcione?

Seis hallazgos, cada uno de los cuales requirió un experimento y cada uno de los cuales tiene una aplicación más amplia que el objeto de estudio original. [La versión completa, con las mediciones](docs/findings.md).

- **Priorizar la forma sobre el estilo.** Los programas de reconstrucción interpretan el ruido superficial como geometría. Una arcilla limpia, similar a una escultura, con planos deliberadamente exagerados, produce una topología mejor que un sprite estilizado; el modelo estilizado se genera simultáneamente y sirve como referencia de color.
- **Definir el contorno del rostro para obtener un rostro.** Un recorte en forma de busto añade entre un **3,1 y un 4,5 veces más** polígonos a la cabeza, y la diferencia es estructural: párpados separados, una arruga en la frente, fosas nasales modeladas; no se trata simplemente de un desenfoque más marcado.
- **Los modelos gemelos pertenecen a una malla, no a un personaje.** Reutilizar un modelo gemelo en diferentes mallas reduce el uso de recursos en un **62% → 22,7%**, ya que los brazos se proyectan hacia el espacio vacío junto al modelo. Generar modelos gemelos a partir de la malla que se va a texturizar, cada vez.
- **La identidad reside en la instrucción.** Un elemento canónico no mencionado en la instrucción aparece por accidente y desaparecerá de la misma manera; esto se mide cuando unas rodilleras doradas resultan estar presentes en la imagen solo debido al ruido en un ControlNet defectuoso.
- **Consultar la geometría, no un umbral.** Reemplazar una máscara con el contorno exacto obtenido mediante trazado de rayos mejora la cobertura de referencia en un **28,4% → 39,1%** de texeles válidos; se trata de una adición estricta, sin difusión ni uso de la GPU. El método de selección basado en la mediana de las esquinas ha fallado tres veces aquí y se descarta.
- **Eliminar lo que ninguna cámara puede ver, tanto del atlas como de la malla.** El 49% de los texeles del atlas son invisibles desde el exterior; excluir estas caras reduce la interpolación en un 68%. Excluir en lugar de eliminar hace que el fallo sea imposible en lugar de simplemente detectable.

## ¿Qué no se ha resuelto?

Identificados y descritos en la página principal, no en una nota al pie. [Todos ellos se encuentran en el código](docs/known-defects.md).

- La banda de la hoja representa el 0,00 % de la referencia de la etapa 1 en las ocho cámaras: el acero sobre un fondo gris se sitúa exactamente en el umbral del objeto principal. La unión recupera el 55,72 %.
- Las líneas de contorno no están niveladas. Un límite de procedencia presenta una variación de textura que es 5,5 veces mayor que la normal; la región a la que se refiere el director presenta una variación 9,5 veces mayor.
- La dilatación provoca un efecto de sangrado entre las islas del atlas que no están relacionadas: el 74,9 % de los texeles dilatados toman su color de otra isla, con una distancia mediana de 0,177 en una figura de 1,0 de altura.
- Cada reconstrucción en esta ruta es una estructura hueca de doble pared; las paredes tienen un grosor aproximado de dos vóxeles. Ningún predicado volumétrico es válido para ninguna de ellas.

## Cómo se gestiona este repositorio

La disciplina es tan importante como el proceso en sí y existe por una razón: en un ciclo anterior, se llevaron a cabo diez sesiones en las que cada participante evaluó su propio trabajo y redactó unas conclusiones que se leyeron en la sesión siguiente como si fueran hechos establecidos. Nada de lo que ocurría en ese ciclo podía verificarse.

- **Especificación antes del trabajo, informe después, decisión final**: y la sesión que diseña un experimento nunca evalúa sus propios resultados. Hay treinta y un experimentos en [el registro](docs/experiments/).
- **Las correcciones se aplican en su lugar, junto a la medición que las refutó**, nunca como eliminaciones discretas. En la única sesión inicial, se falsificaron seis afirmaciones heredadas, y las seis siguen siendo legibles junto a lo que las reemplazó.
- **Los errores permanecen en el repositorio con su explicación.** [`tools/superseded/`](docs/tools.md) no es un archivo; cualquiera puede ejecutar esas herramientas y observar cómo fallan de la misma manera.
- **Un resultado negativo es un éxito total**, se informa y se cierra, en lugar de ajustarse para obtener un número específico.
- **Las pruebas están vinculadas al commit que modifica el código**: 1047 superaron la prueba con la participación de dos personas, con CI restringida por rutas en las 1002 pruebas herméticas.
- **El registro se puede consultar.** Un índice SQLite + FTS5 sobre todo el historial, verificado en cuatro puntos. Encontró un recuento que el texto había indicado incorrectamente en tres sitios, contando el propio registro.

## Donde está todo

| | |
|---|---|
| **[El manual](docs/handbook/index.md)** | la guía: el recorrido por etapas, los temas que se tratan, el sistema de clasificación. |
| **[Preparación del concepto]** (docs/concept-prep.md) | el candidato Clay Hop: su recorrido en el nivel Gate 0, su ubicación y el objeto especial que desbloquea. |
| **[El registro](docs/experiments/)** | treinta y un experimentos: especificación, informe, decisión y cada una de las predicciones formuladas antes de la medición. |
| **[Lo que se descubrió a lo largo del recorrido]** | los resultados sólidos y las normas que se lograron con tanto esfuerzo, en su totalidad |
| **[Estado de cada herramienta](docs/tools.md)** | qué funciona, qué ha quedado obsoleto y cuáles son las pruebas que respaldan cada afirmación. |
| **[Defectos conocidos](docs/known-defects.md)** | todo aquello que no se haya resuelto, cuantificado y ubicado en el código. |
| **[La evolución del proyecto, tal como ocurrió](docs/arc-history.md)** | la historia cronológica, con las correcciones incluidas. |
| **[CLAUDE.md]** | cómo funciona aquí: los diferentes puestos de trabajo, las normas y el coste de cada uno. |

## Situación de la licencia

En cada etapa se ejecuta de forma local y con una configuración comercial limpia: SDXL (OpenRAIL++), MV-Adapter (código abierto), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Se excluyen deliberadamente los siguientes elementos, con la razón que se indica: **nvdiffrast** (no comercial; aquí se aplica mediante un mecanismo de seguridad estructural, no mediante una certificación), **Hunyuan3D-Paint** (la licencia no es válida en la UE, el Reino Unido y Corea del Sur), **MVPaint** y **TEXGen** (ninguna licencia) y **UltraSharp / SUPIR / StableSR** (escaladores no comerciales).

**El límite de las afirmaciones se establece explícitamente en lugar de dejarse a la interpretación.** Describe la **ruta registrada**, es decir, las etapas del diagrama anterior, desde la conversión de imagen a 3D. Actualmente, el paso inicial de preparación del modelo que precede a esta ruta se ejecuta en una API de nube cerrada cuyos términos este repositorio **no ha verificado**, por lo que ninguna afirmación de licencia aquí cubre un activo creado a partir de uno de sus modelos. Este es un punto pendiente con una vía clara para resolverlo: el modelo local con la licencia correcta es **Qwen-Image-Edit (Apache-2.0)**, y **FLUX.1-Kontext [dev] se excluye por las mismas razones que nvdiffrast**: pesos no comerciales. Ambos se verifican en relación con el catálogo de modelos del estudio, en lugar de recuperarse; la justificación se encuentra en [preparación conceptual](docs/concept-prep.md).

## Modelo de confianza y amenazas

Facet se ejecuta completamente en su propia máquina: cada herramienta es un script que se invoca sobre rutas que usted escribe, por lo que la pregunta útil no es *qué permisos solicita esta aplicación*, sino *qué hacen estos scripts con su máquina*. La respuesta se obtiene mediante mediciones, y cada ejecución se puede repetir; la política completa se encuentra en [SECURITY.md](SECURITY.md):

- **Datos afectados:** mallas, texturas, imágenes y archivos JSON en el disco local, en las rutas que especifique en la línea de comandos. Además, `docs/index/facet.db`, que es *derivado*: no contiene nada que ya no fuera un archivo en este repositorio, y `facet_index.py build` lo regenera desde cero.
- **Datos NO afectados:** nunca se tocan credenciales. Ninguna herramienta lee, almacena ni transmite tokens, claves o contraseñas, y ninguna de ellas está presente en el árbol; se ha realizado una búsqueda para detectar claves con prefijos de proveedor, GitHub PAT, tokens de Slack, ID de clave de AWS, bloques de clave privada, tokens de acceso y asignaciones `api_key`/`password` en línea; **no se encontraron coincidencias**, no hay ningún archivo que parezca contener credenciales.
- **No hay telemetría.** No se recopila ni se envía nada. No hay opción para desactivarla porque no hay nada que desactivar.
- **Salida de red:** dos de las treinta y cuatro herramientas abren un socket: `restylize_views.py` y `texpass_brush.py`, y ambas llaman a una API HTTP de ComfyUI en `--host`, con la configuración **predeterminada `127.0.0.1:8188`**. Ninguna otra herramienta en `tools/` realiza una llamada de red.
- **Permisos:** usuario normal. No se requiere elevación de privilegios, instalación de servicios ni escritura en la configuración del sistema o el registro.

Se revelan tres aspectos importantes en lugar de simplemente afirmarlos, porque una nota de seguridad que solo enumera garantías no es un modelo de amenazas: **las operaciones de archivo no están aisladas** (una herramienta escribe donde sus argumentos lo indican); **muchas herramientas y documentos contienen rutas locales absolutas**, 114 ocurrencias en 26 archivos; no son secretos, sino una revelación del diseño de una máquina, y la razón por la que la mayoría de las herramientas no se ejecutarán sin modificar en otro lugar; y **los fallos inesperados aparecen como rastreos de Python en los 34 scripts de investigación no publicados**, sin ninguna puerta de enlace `--debug`. Las interrupciones deliberadas son mensajes `ANDON:` que contienen la medición que las activó. Este es el contrato del instrumento de investigación, y [SHIP_GATE.md](SHIP_GATE.md) registra exactamente cuándo deja de ser suficiente, lo cual ocurrió para los dos comandos que facet *instala* en la versión 0.2.0: `facet-index` y `facet-mcp` devuelven `0` (correcto) / `1` (error de usuario) / `2` (error de tiempo de ejecución); y, desde [E22](docs/experiments/E22-ruling.md), **`4` RECHAZADO** para una puerta de enlace activada o un paso `verify` fallido, lo que significa que la herramienta funciona y le indica que no continúe en lugar de producir un error de tiempo de ejecución. Todos ellos se niegan con un fallo estructurado que indica el siguiente paso en lugar de un rastreo ([E21](docs/experiments/E21-cli-contract-report.md)).

**Y las puertas de enlace de esos dos comandos ya no son eliminables.** Cada ANDON en lo que instala facet `raise`; una simple `assert` es una declaración `python -O` que se elimina silenciosamente, y 87 de las puertas de enlace de este repositorio podían eliminarse mediante una variable de entorno hasta que E22 las convirtió. Se midió antes y después en la misma puerta de enlace, en cuatro modos de intérprete.
**Y desde [E23](docs/experiments/E23-route-gates-report.md), tampoco lo son las puertas de enlace de la ruta que produjo los cuatro activos aceptados**: sus **57 puntos a través de doce herramientas**, convertidos como un simple movimiento en archivos que ningún test había ejecutado nunca, cada uno de ellos ahora rechazando también bajo `-O` y `PYTHONOPTIMIZE=1`, además de bajo un intérprete normal.
**Y desde [E25](docs/experiments/E25-ruling.md), la clase está cerrada.** Sus **133 puntos a través de 43 archivos**: los instrumentos de medición que produjeron las pruebas para los cuatro activos aceptados anteriores, se convierten de la misma manera, lo que eleva el total que `raise` a **278**.
Exactamente **uno** solo ANDON `assert` permanece en cualquier lugar debajo de `tools/`: `superseded/texpass_thin_mask.py`, que **nunca** se convierte, porque esas herramientas se mantienen para que cualquiera pueda ejecutarlas y ver cómo fallan de la misma manera. Este resto está fijado **por nombre** en la suite de pruebas, por lo que un barrido futuro no puede eliminarlo sin editar el test a propósito.

**Estado del soporte:** este repositorio se desarrolla de forma abierta, con un único equipo y un director, así como sesiones rotativas de asesoramiento y ejecución. `main` es el único estado compatible. No hay canal de lanzamiento, política de retrocompatibilidad ni SLA; en su lugar, existe el registro: cada afirmación está junto al código que la produce, y [docs/experiments](docs/experiments/) contiene las especificaciones, el informe y la resolución para cada una.

## Requisitos

Blender 5.x, Python 3.11+ con `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Solo se necesita una instalación local de ComfyUI para el pincel de retoque. Desarrollado con una RTX 5090; la capacidad de VRAM es más importante que la velocidad bruta.

CI ejecuta el subconjunto hermético de la suite en **ubuntu-latest / Python 3.12** con instalaciones fijas (`.github/workflows/ci.yml`); la capa de artefactos necesita los árboles registrados que se encuentran en `E:\AI\training`, y que no están en Git, por lo que CI los excluye intencionadamente. Localmente, `python -m pytest` ejecuta las **1047** pruebas y `python -m pytest -m "not artifacts"` ejecuta las **1002** pruebas que reproduce CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
