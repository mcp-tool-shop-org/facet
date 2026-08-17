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

El estilo se aplica **al activo**, en el espacio de la textura; no se pinta por vista y luego se une. Si le proporciona a la ruta un concepto de arcilla con formas exageradas, devolverá una malla texturizada cuyo color proviene de una referencia estilizada de *esa* malla, y todo lo que la referencia no pueda ver se rellenará con un pincel de retoque enmascarado y una dilatación consciente de la superficie.

Recibe su nombre de las dos partes del problema: los polígonos y la cara que deben mantener.

## Instalar

La ruta en sí es un conjunto de scripts locales que se ejecutan sobre rutas que usted escribe; clone el repositorio y lea [cómo empezar](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Dos servidores se distribuyen como un paquete**: el índice de registros, para que un asistente pueda consultar la secuencia de pruebas en lugar de leerla, y **a partir de la versión 0.4.0, el servidor de medición**, de modo que dos activos medidos con meses de diferencia sigan una ruta de código única.

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` es el servidor MCP stdio sobre el registro (seis herramientas, con la verificación de cuatro puntos como superficie de salud que rechaza) y `facet-index` es el índice en sí (`build` / `verify` / `q` / `claims`). Ejecute cualquiera de ellos desde dentro de una copia; `--db` nombra un índice diferente.

### El servidor de medición: nuevo en la versión 0.4.0

`facet-measure` responde a la **mitad numérica** de una comparación y nunca indica si la salida es buena. Cada carga útil contiene la versión del servidor, el hash del archivo del instrumento y un hash de configuración, y `measure_report` **rechaza** comparar cuando hay una discrepancia; esta es la propiedad para la que existe todo esto.

Verificado ejecutando un **verbo** en lugar de `--help`: una malla de control devuelve 786.432 caras con una envolvente de identidad completa en una máquina que no tiene ninguna copia.

**Lo que obtenga depende de una cosa, y es su versión de Python:**

| su Python | `[measure-full]` le proporciona |
|---|---|
| **3.11 / 3.12** | **las ocho herramientas**: `open3d` se instala desde PyPI |
| **3.13** | cuatro herramientas: `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 es la última *versión* y publica paquetes cp38-cp312 sin **ningún sdist**, por lo que en 3.13 no hay nada en PyPI para instalar. El paquete adicional lo incluye detrás de `python_version < "3.13"`, por lo que la instalación **tiene éxito** allí y las cuatro herramientas de geometría devuelven **`4` RECHAZADO**, indicando lo que necesitan, en lugar de que falle toda la instalación.

**Para obtener las ocho en Python 3.13**, Open3D publica los paquetes cp313 actuales en su canal de desarrollo continuo. Una URL directa es válida en una línea de comandos; solo está prohibido dentro de los metadatos del paquete publicado:

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **En Windows y macOS, los paquetes de desarrollo tienen el sufijo `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` al momento de escribir) y el nombre cambia a medida que `main` cambia; enumere los activos en [la versión `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) y tome la versión actual. **Esta compilación es con la que se midieron los números dependientes de open3d de esta ruta**, y es una verdadera frontera de comparabilidad: la envolvente de identidad registra el hash del instrumento, no sus dependencias — [E31](docs/experiments/E31-ruling.md).

*Hasta la versión 0.3.1, el paquete contenía dos archivos `.py` y ninguno de los instrumentos de medición, por lo que un servidor de medición instalado no tenía nada que ejecutar. Nadie se dio cuenta durante cuatro versiones porque este repositorio ES la copia: la herramienta funcionaba donde se compiló y nunca había estado en otro lugar.*

⚠ **`pip install facet-mcp` estaba roto en todas las versiones publicadas hasta la versión 0.3.0, y se corrigió en la versión 0.3.1.** El paquete instala `facet_index` como un módulo de nivel superior, por lo que hasta e incluyendo la versión 0.3.0, resolvía la ubicación del registro contra `<venv>/Lib`, que no contiene ni el corpus ni el índice, y `build`, `claims` y `q` sin `--db` fallaban todos.
**En la versión 0.3.0 o anterior, utilice el binario `npx` de arriba.**

A partir de la versión 0.3.1, la raíz se resuelve **probando si existe el registro** en lugar de asumir que existe: ejecute cualquiera de los comandos desde dentro de una copia y lo encontrará; ejecútelo desde cualquier otro lugar y devolverá **`4` RECHAZADO**, indicando ambos directorios que intentó y ambos marcadores que buscó. `$FACET_INDEX_DB` ahora es leído por ambos comandos, y selecciona qué *índice*, nunca qué *corpus*. Medido en un paquete compilado a partir de `main` e instalado en un entorno virtual limpio — [E24](docs/experiments/E24-ruling.md).

*Este bloque se ha corregido dos veces. Primero decía `pipx install facet-mcp # o el paquete de Python directamente `, until v0.3.0's read-back ran a **verb** instead of ` --help`.
Luego, indicaba que el paquete "solo funciona para `q` y `claims`"; **`claims` tampoco funcionó**, lo que E24 descubrió al ejecutarlo. Ambas correcciones se encuentran en [known-defects.md](docs/known-defects.md) con sus mediciones.*

## Estado actual

**Cuatro activos aceptados, de cuatro clases de sujetos, sin costo alguno.** Cada uno fue evaluado por el Director a su propio nivel de zoom: en el archivo GLB o en hojas de tamaño completo; no mediante una métrica que supere un umbral.

| sujeto | clase | aceptado | referencia / pincel / dilatación |
|---|---|---|---|
| **Character (W3)** | humanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | vehículo, rigging delgado | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bestia, membranas de alas | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | accesorio, casi 2D, gris sobre gris | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Las participaciones son de texeles válidos y **no son comparables entre sujetos**: un barco oculta la mayor parte de sí mismo desde el nivel de los ojos y un animal oculta la mitad. Lea cada uno en relación con su propio límite de alcance pre-registrado, en relación con el cual obtienen **86–93%**: la diferencia entre las filas es la geometría, no la regresión. [Números completos, con sus denominadores](docs/handbook/subjects.md).

**Es una canalización, no un generador de un solo carácter.** Contradiga la especificación en ocho elementos nombrados y el mensaje ganará **8 de 8**: ΔE medio de 46,3 frente a 6,2 en cinco controles mantenidos; mientras que la figura permanece siendo el mismo hombre. La estructura se mantiene mediante la malla y el control; los atributos nombrados se basan en el mensaje.

**La consulta sobre el proyector se cerró el 16 de agosto de 2026** ([E45](docs/experiments/E45-warp-and-aov-kickoff.md)–[E49](docs/experiments/E49-finish-and-cap-kickoff.md)).
Las ocho placas **se componen de**: reconstruidas a partir del conjunto por vista, utilizando
bordes × orientación × pesos de visibilidad; el atlas renderiza lo que el Director consideró *"honesta y
mucho mejor"* y luego *"tiene un aspecto excelente"* — en comparación con un atlas ya implementado cuyo recorrido estaba
destruyendo la pintura. Las placas coinciden en este punto. La cadena que lo hizo está en `tools/`
(`emit_view_aovs`, `s3_composite`, `flow_estimate`, `s3_run`, `s3_sheet`,
`atlas_from_aovs`, `twin_mesh_warp`), cinco de las siete construidas por un canal externo
cuyas calibraciones designadas han demostrado ser **exitosas en todos los casos**, y cada una se ha verificado aquí
antes de confiar en ellas. Lo que queda se indica a continuación, no está oculto: una clase de polígonos de relleno bajo
investigación, una superficie nunca vista que espera una política, y la construcción canónica que el
Director consideró crucial.

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

**El trazado discontinuo es nuevo y está diseñado para que no sea sólido.** La primera caja de la ruta siempre ha mostrado *concepto de arcilla*, y hasta ahora nada aquí lo hacía realidad: cada pieza de arcilla llegaba a mano y se modificaba en el proceso. Ahora existe una herramienta concepto→arcilla, y su primer par ha sido probado a tamaño completo: pose, protectores para las muñecas, medallón para el cinturón y dobladillo rasgado; la masa de la melena no; la fuga de color se midió en toda la imagen con **C\* p99.9 = 13.15** con un fondo acromático uniforme. **Lo que este par no puede mostrar es si la malla mejora**, que es la única pregunta que lo justifica, por lo que sigue siendo un candidato con sus pruebas registradas: **[preparación del concepto](docs/concept-prep.md)**.

## Qué lo hace funcionar

Seis hallazgos, cada uno de los cuales requiere un experimento y cada uno de los cuales se generaliza más allá del sujeto que lo produjo. [La versión completa, con las mediciones](docs/findings.md).

- **Primero la forma, luego el estilo.** Los reconstructores interpretan el ruido superficial como geometría. Una arcilla limpia y de aspecto escultórico, con planos deliberadamente exagerados, produce una mejor topología que un sprite estilizado; el gemelo estilizado se genera al mismo tiempo y se convierte en la referencia de color.
- **Enmarca la cara, obtén una cara.** Un recorte de busto coloca entre **3.1 y 4.5 veces más polígonos** en la cabeza, y la diferencia es estructural: párpados separados, un surco en la frente, cavidades nasales modeladas; no un desenfoque más marcado.
- **Los gemelos pertenecen a una malla, no a un personaje.** Reutiliza un gemelo en diferentes mallas y la cobertura se reduce del **62% al 22.7%**, porque los brazos se proyectan en el espacio vacío junto al modelo. Genera gemelos a partir de la malla que vas a texturizar, cada vez.
- **La identidad pertenece al mensaje.** Un elemento canónico que no se menciona en el mensaje llega por accidente y se irá de la misma manera; se mide cuando las placas doradas para las rodillas resultaron estar llegando a la imagen solo a través del ruido en una ControlNet defectuosa.
- **Pregunta a la geometría, no a un umbral.** Reemplazar una máscara con silueta exacta obtenida mediante trazado de rayos movió la cobertura de referencia del **28.4% al 39.1%** de texeles válidos; estrictamente aditivo, sin difusión, sin GPU. El sombreado de esquina-mediana ha fallado tres veces aquí y se ha retirado.
- **Elimina lo que ninguna cámara puede ver, del atlas y nunca de la malla.** El 49% de los texeles del atlas son invisibles desde el exterior; excluir esas caras reduce la interpolación en un **68%**. Excluir en lugar de eliminar hace que el fallo sea imposible en lugar de simplemente detectable.

## Qué no está resuelto

Nombrado y medido, en la página principal en lugar de en una nota al pie. [Todos ellos, ubicados en el código](docs/known-defects.md).

- **Algunas superficies visibles se asignan al espacio del atlas, pero ninguna textura las incluye**, y se renderizan como
el negro predeterminado sin modificar de la imagen. El "baker" de Blender utiliza un muestreo centrado en texeles, por lo que un triángulo
que no coincide con ningún centro de texel queda vacío; sus propios desarrolladores
[identificaron el mecanismo e implementaron una solución](https://projects.blender.org/blender/blender/pulls/161752)
dos semanas después de la compilación en la que se midieron todos los valores aquí. Es una propiedad del recorrido,
no de un objeto específico: medido en un activo, **sin medir en los otros cuatro**.
- **La banda de borde ocupa el 0,00% de la referencia de la etapa 1** en las ocho cámaras; el acero sobre un
fondo gris se sitúa exactamente en el umbral clave. La unión rescata el 55,72%.
- **Las costuras del trazo no están niveladas.** Un límite de procedencia presenta una diferencia de **5,5 veces** con la variación de textura normal; la región que el Director identificó presenta una diferencia de **9,5 veces**.
- **La dilatación se extiende entre islas del atlas no relacionadas** — el 74,9% de los texeles dilatados toman su
color de otra isla, a una distancia mediana de 0,177 en una figura de altura 1,0. ⚠ **Esta proporción se refiere a los texeles del atlas y no es una afirmación sobre lo que ve una cámara**: la dilatación representa el 26,95% del
atlas renderizado y el **4,95% de los píxeles de la figura renderizada**, una relación de 0,18. La pintura se encuentra en mapas grandes, los agujeros en mapas pequeños, por lo que un texel dilatado es económico en términos de espacio en pantalla.
- **⚑ El defecto que determina la aceptación está determinado por la PINTURA, no por ningún relleno** — regiones
que muestran el color de otro material, algo que ninguna estadística de moteado puede detectar. Medido de tres maneras diferentes por
tres sesiones en tres espacios: **91,05% `reference` con un enriquecimiento de 0,99**, exactamente en la
tasa base; la misma clase en verde tela **68,46% `reference`**; y en una delgada lámina, los texeles pintados de la
superficie **18,77%** contaminados frente al relleno de dilatación del **5,55%**.
El relleno se obtiene correctamente de su vecino pintado más cercano, y ese vecino ya es
incorrecto. La mezcla en sí es una división de dos bandas no documentada
(`M + gaussian_blur_σ16(B − M)`) que mide el **peor de cuatro** valores alternativos en los mismos
puntos.
- **Las vistas nunca son independientes, lo que limita cualquier corrección de la mezcla.** Para cada grupo de defectos,
el **100% de las caras con dos o más cámaras contribuyentes tienen todas dentro de un rango de 90°**
(mediana de 45°), y el 21% de las caras defectuosas son vistas por una sola cámara. Las vistas adyacentes bajo
un control casi idéntico fallan juntas, por lo que las ganancias publicadas en fotogrametría con múltiples vistas no
se transfieren aquí tal cual.
- **Cada reconstrucción en esta ruta es una cáscara hueca de doble pared**, paredes de aproximadamente dos
voxeles. Ningún predicado volumétrico es válido para uno solo.
- **Las placas difieren en límites de materiales no identificados, y la construcción canónica es crucial**
(16 de agosto de 2026). La deformación interior a la malla medida fue de **3,5–11,1 px (mediana)** en las ocho vistas, en comparación con las medianas del contorno de 1,2–3,0; cada región residual que el Director
marcó — corte de manga, mano, parte superior del botín — es una unión de materiales que la indicación generativa
nunca nombró (la indicación registrada contiene seis elementos; agarre, guantelete, greba y
mano aparecen **cero** veces). Su diagnóstico es el registro: *"Nunca construimos correctamente la construcción canónica."* La construcción canónica W3 y la regeneración alimentada por la construcción canónica son
la reparación en etapas ([registro de envío E49](docs/experiments/E49-finish-and-cap-kickoff.md)).
- **El 4,65–5,57% de los texeles válidos son superficies que ninguna cámara con anillo plano puede ver** — fallan
en la compuerta de profundidad en todas las vistas, ninguna ruta de proyección puede pintarlos y el canal ya implementado los cubrió con la inundación ciega a la isla que creó las marcas oscuras. Necesitan una política (material neutro, pincel o aceptación), no una corrección
([informe E49](docs/experiments/E49-finish-and-cap-report.md)).
- **El pase de relleno completo del candidato renderiza polígonos planos y coloreados** — la única clase abierta del Director en las hojas de calidad aceptada (*"tiene un aspecto excelente, pero hay formas poligonales coloreadas"*). Hipótesis bajo prueba, máscaras de procedencia ya etiquetadas: islas huérfanas del tamaño de triángulos individuales, rellenadas de forma plana a partir de muestras gemelas adyacentes al límite tomadas con el contorno no erosionado.

## Cómo se ejecuta este repositorio

La disciplina es tan importante como el producto y la canalización, y existe por una razón: una iteración anterior realizó diez sesiones en las que cada una juzgó su propia salida y escribió conclusiones que la siguiente sesión leyó como un hecho establecido. Nada de eso era verificable.

- **Especificación antes del trabajo, informe después, decisión final**: y la sesión que diseña un experimento nunca evalúa sus propios resultados. Hay cuarenta experimentos en [el registro](docs/experiments/).
- **Las correcciones se aplican en su lugar, junto a la medición que las refutó**, nunca como eliminaciones discretas. Solo en la sesión inicial se falsificaron seis afirmaciones heredadas, y todas siguen siendo legibles junto a lo que las reemplazó.
- **Los fallos permanecen en el repositorio con su motivo.** [`tools/superseded/`](docs/tools.md) no es un archivo; cualquiera puede ejecutar estas herramientas y observar cómo fallan de la misma manera.
- **Un resultado negativo es un éxito total**, se informa y se cierra en lugar de ajustarse a un número.
- **Las pruebas se ejecutan con el commit que modifica el código**: 1233 aprobadas por dos personas, con CI basado en rutas para las 1181 herméticas.
- **El registro es consultable.** Un índice SQLite + FTS5 sobre todo el historial, verificado en cuatro etapas. Encontró un recuento de decisiones que la prosa había indicado incorrectamente en tres sitios, contando el propio registro.

## Donde todo está

| | |
|---|---|
| **[El manual](docs/handbook/index.md)** | la guía: la ruta paso a paso, los temas y el sistema de perfiles |
| **[Preparación del concepto](docs/concept-prep.md)** | el candidato para la etapa de preparación de modelos: su recorrido en la Etapa 0, su ubicación y el elemento de licencia que desbloquea |
| **[El registro](docs/experiments/)** | cuarenta experimentos: especificación, informe, decisión y cada predicción declarada antes de la medición |
| **[Lo que aprendió la ruta](docs/findings.md)** | los hallazgos duraderos y las reglas obtenidas con esfuerzo, en su totalidad |
| **[Estado de cada herramienta](docs/tools.md)** | lo que funciona, lo que está obsoleto y la evidencia para cada uno |
| **[Defectos conocidos](docs/known-defects.md)** | todo lo que no se ha resuelto, medido y ubicado en el código |
| **[La secuencia de eventos, tal como ocurrió](docs/arc-history.md)** | el historial cronológico, con las correcciones intactas |
| **[CLAUDE.md](CLAUDE.md)** | cómo trabajar aquí: los roles, las reglas y el costo de cada uno |

## Posición de la licencia

Cada etapa se ejecuta localmente y es comercialmente limpia: SDXL (OpenRAIL++), MV-Adapter (código abierto), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Excluido deliberadamente, con la razón: **nvdiffrast** (no comercial; se aplica aquí mediante un mecanismo de seguridad estructural, no mediante una certificación), **Hunyuan3D-Paint** (la licencia no es válida en la UE, el Reino Unido y Corea del Sur), **MVPaint** y **TEXGen** (ninguna licencia) y **UltraSharp / SUPIR / StableSR** (ampliadores de escala no comerciales).

**El límite de la afirmación, declarado en lugar de dejarse al descubierto.** Describe la **ruta registrada**: las etapas del diagrama anterior, desde imagen a 3D. La etapa candidata para la preparación de modelos aguas arriba actualmente se ejecuta en una API de nube cerrada cuyos términos este repositorio **no ha verificado**, por lo que ninguna afirmación de licencia aquí cubre un activo creado a partir de uno de sus modelos. Este es un elemento pendiente con una ruta definida para resolverlo: el modelo local con la licencia correcta es **Qwen-Image-Edit (Apache-2.0)**, y **FLUX.1-Kontext [dev] se excluye por las mismas razones que nvdiffrast**: pesos no comerciales. Ambos se verifican en relación con el catálogo de modelos del estudio en lugar de recuperarse; la justificación está en [la preparación del concepto](docs/concept-prep.md).

## Modelo de confianza y amenazas

facet se ejecuta completamente en su propia máquina: cada herramienta es un script que invoca contra rutas que escribe, por lo que la pregunta útil no es *qué permisos solicita esta aplicación*, sino *qué hacen estos scripts con su máquina*. Se responde mediante la medición, y cada ejecución se puede volver a ejecutar; la política completa está en [SECURITY.md](SECURITY.md):

- **Datos afectados:** mallas, texturas, imágenes y JSON en el disco local, en las rutas que proporciona en la línea de comandos. Además, `docs/index/facet.db`, que es *derivado*; no contiene nada que ya no fuera un archivo en este repositorio, y `facet_index.py build` lo regenera desde cero.
- **Datos NO afectados:** nunca se tocan credenciales. Nada aquí lee, almacena ni transmite un token, una clave o una contraseña, y ninguno está presente en el árbol; se ha buscado claves con prefijos de proveedor, GitHub PAT, tokens de Slack, ID de clave de AWS, bloques de clave privada, tokens de portador y asignaciones `api_key`/`password` en línea; **cero coincidencias**, no se rastrea ningún archivo con formato de credencial.
- **No hay telemetría.** Ninguna recopilada, ninguna enviada. No hay opción para desactivarla porque no hay nada que desactivar.
- **Salida de red:** dos de las treinta y seis herramientas abren un socket: `restylize_views.py` y `texpass_brush.py`, y ambas llaman a una API HTTP de ComfyUI en `--host`, **predeterminada `127.0.0.1:8188`**. Nada más en `tools/` realiza una llamada de red.
- **Permisos:** usuario normal. Sin elevación, sin instalación de servicio, sin escrituras en la configuración del sistema o el registro.

Se revelan tres bordes afilados en lugar de eliminarlos, porque una nota de seguridad que solo enumera garantías no es un modelo de amenaza: **las operaciones con archivos no están aisladas** (una herramienta escribe donde sus argumentos indican); **las rutas locales absolutas están integradas en muchas herramientas y documentos**, aparecen 114 veces en 26 archivos, no son secretos, sino una revelación del diseño de una máquina, y la razón por la que la mayoría de las herramientas no se ejecutarán sin modificar en otro lugar; y **los fallos inesperados se manifiestan como rastreos de Python en los 36 scripts de investigación no publicados**, sin ninguna puerta de enlace `--debug`. Las interrupciones deliberadas son mensajes `ANDON:` que contienen la medición que las activó. Ese es el contrato del instrumento de investigación, y [SHIP_GATE.md](SHIP_GATE.md) registra exactamente cuándo deja de ser suficiente, lo cual, para los dos comandos que lo hacen, a partir de la versión 0.2.0: `facet-index` y `facet-mcp` devuelven `0` (correcto) / `1` (error de usuario) / `2` (error en tiempo de ejecución); y, dado que [E22](docs/experiments/E22-ruling.md), se **rechaza `4`** por una puerta de enlace activada o una rama `verify` fallida, lo cual significa que la herramienta está funcionando y le indica que no continúe en lugar de un error en tiempo de ejecución. Todos ellos rechazan con un fallo estructurado que indica el siguiente paso en lugar de un rastreo ([E21](docs/experiments/E21-cli-contract-report.md)).

**Y las puertas de enlace en esos dos comandos ya no se pueden eliminar.** Cada ANDON instala `raise`; un `assert` simple es una declaración que `python -O` elimina silenciosamente, y 87 de las puertas de enlace de este repositorio podían eliminarse mediante una variable de entorno hasta que E22 las convirtió. Se midió antes y después en la misma puerta de enlace, en cuatro modos de intérprete.
**Y dado que [E23](docs/experiments/E23-route-gates-report.md), tampoco lo son las puertas de enlace en la ruta que produjo los cuatro activos aceptados**, sus **57 sitios en doce herramientas**, convertidos como un simple movimiento en archivos que ningún test había ejecutado nunca, cada uno ahora rechazando también bajo `-O` y `PYTHONOPTIMIZE=1`, así como bajo un intérprete normal.
**Y dado que [E25](docs/experiments/E25-ruling.md), la clase está cerrada.** Sus **133 sitios en 43 archivos**, los instrumentos de medición que produjeron las pruebas para los cuatro activos aceptados anteriores, se convierten de la misma manera, lo que eleva el total que `raise` a **278**.
Exactamente **uno** ANDON simple `assert` permanece en cualquier lugar bajo `tools/`: `superseded/texpass_thin_mask.py`, que **nunca** se convierte, porque esas herramientas se mantienen para que cualquiera pueda ejecutarlas y ver cómo fallan de la misma manera. Este resto está fijado **por nombre** en la suite de pruebas, por lo que una revisión futura no puede eliminarlo sin editar el test a propósito.

**Estado del soporte:** este repositorio se desarrolla de forma abierta, en un único entorno, por un director y un par rotatorio de sesiones de asesoramiento y ejecución. `main` es el único estado compatible. No hay canal de lanzamiento, ni política de retrocompatibilidad, ni SLA; lo que sí hay es el registro: cada afirmación está junto al código que la produce, y [docs/experiments](docs/experiments/) contiene las especificaciones, el informe y la resolución para cada una.

## Requisitos

Blender 5.x, Python 3.11+ con `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Solo se necesita una instalación local de ComfyUI para el pincel de retoque. Desarrollado en un RTX 5090; la capacidad de VRAM es más importante que la velocidad bruta.

CI ejecuta el subconjunto hermético de la suite en **ubuntu-latest / Python 3.12** con instalaciones fijas (`.github/workflows/ci.yml`); la capa de artefactos necesita los árboles registrados bajo `E:\AI\training`, que no están en git, por lo que CI los excluye por diseño. Localmente, `python -m pytest` ejecuta las **1233** pruebas y `python -m pytest -m "not artifacts"` ejecuta las **1181** que reproduce CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
