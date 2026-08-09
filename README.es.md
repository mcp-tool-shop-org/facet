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

El estilo se aplica **al activo**, en el espacio de la textura; no se pinta por vista y luego se une. Si le proporciona a la ruta un concepto de arcilla con formas exageradas, devolverá una malla texturizada cuyo color proviene de una referencia estilizada de *esa* malla, y todo lo que la referencia no pueda ver se rellenará con un pincel de retoque enmascarado y una dilatación consciente de la superficie.

Recibe su nombre por las dos partes del problema: los polígonos y la cara que deben mantener.

## Instalar

La ruta en sí es un conjunto de scripts locales que se ejecutan en rutas que usted escribe; clone el repositorio y lea [cómo empezar](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**El índice de registro se distribuye como un paquete**, por lo que un asistente puede consultar la evidencia en lugar de leerla:

```bash
npx @mcptoolshop/facet          # zero-prerequisite; verified binary, no Python needed
pipx install facet-mcp          # or the Python package directly
```

Vienen con él dos comandos: `facet-mcp`, el servidor MCP stdio (seis herramientas, con la verificación de cuatro puntos como una superficie de salud que rechaza) y `facet-index` (`build` / `verify` / `q` / `claims`). Apunte cualquiera a un índice con `--db` o `$FACET_INDEX_DB`.

## Dónde se encuentra

**Cuatro activos aceptados, de cuatro clases de sujetos, sin costo.** Cada uno fue evaluado por el Director en su propio nivel de zoom: en el GLB o en hojas de tamaño completo; no mediante una métrica que supere un umbral.

| sujeto | clase | aceptado | referencia / pincel / dilatación |
|---|---|---|---|
| **Character (W3)** | humanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | vehículo, rigging delgado | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bestia, membranas de alas | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | accesorio, casi 2D, gris sobre gris | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Las acciones son de texeles válidos y **no son comparables entre sujetos**: un barco oculta la mayor parte de sí mismo desde el nivel de los ojos y un animal oculta la mitad. Analice cada uno en relación con su propio límite de alcance predefinido, en relación con el cual alcanzan el **86–93 %**: la diferencia entre las filas es la geometría, no la regresión. [Números completos, con sus
denominadores](docs/handbook/subjects.md).

**Es una canalización, no un generador de un solo carácter.** Contradiga la especificación en ocho elementos nombrados y el mensaje ganará **8 de 8**: ΔE mediano de 46,3 frente a 6,2 en cinco controles mantenidos; mientras que la figura permanece siendo el mismo hombre. La estructura se mantiene mediante la malla y el control; los atributos nombrados se basan en el mensaje.

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

## Lo que lo hace funcionar

Seis hallazgos, cada uno de los cuales requiere un experimento y cada uno de los cuales se generaliza más allá del sujeto que lo produjo. [La versión completa, con las
mediciones](docs/findings.md).

- **Primero la forma, luego el estilo.** Los reconstructores leen el ruido de la superficie como geometría. Una arcilla limpia y similar a una escultura, con planos deliberadamente exagerados, devuelve una mejor topología que un sprite estilizado; el gemelo estilizado se genera junto con él y se convierte en la referencia de color.
- **Enmarque la cara, obtenga una cara.** Un recorte de busto coloca **de 3,1 a 4,5 veces más** polígonos en la cabeza, y la diferencia es estructural: párpados separados, un surco en la frente, cavidades nasales modeladas; no un desenfoque más marcado.
- **Los gemelos pertenecen a una malla, no a un personaje.** Reutilice un gemelo en varias mallas y la cobertura se reduce del **62 % al 22,7 %**, porque los brazos se proyectan hacia el espacio vacío junto al modelo. Genere gemelos a partir de la malla que va a texturizar, cada vez.
- **La identidad pertenece al mensaje.** Un elemento canónico no nombrado en el mensaje está llegando por accidente y se irá de la misma manera; se mide cuando las placas doradas para las rodillas resultaron estar llegando a la imagen solo a través del ruido en un ControlNet defectuoso.
- **Pregunte por la geometría, no por un umbral.** Reemplazar una máscara clave con el contorno exacto del raycast movió la cobertura de referencia del **28,4 % al 39,1 %** de texeles válidos; estrictamente aditivo, sin difusión, sin GPU. El sombreado de esquinas-mediana ha fallado tres veces aquí y se retira.
- **Elimine lo que ninguna cámara pueda ver, del atlas y nunca de la malla.** El 49 % de los texeles del atlas son invisibles desde el exterior; excluir esas caras reduce la interpolación en un **68 %**. Excluir en lugar de eliminar hace que el fallo sea imposible en lugar de simplemente detectable.

## Lo que no está resuelto

Nombrado y medido, en la página principal en lugar de en una nota al pie. [Todos ellos, ubicados en
el código](docs/known-defects.md).

- **La banda de la hoja toma el 0,00 % de la referencia de la etapa 1** en las ocho cámaras; el acero sobre un fondo gris se sitúa exactamente en el umbral de la clave. La unión rescata el 55,72 %.
- **Las costuras del trazo no están niveladas.** Un límite de procedencia presenta una variación de textura **5,5 veces mayor**; la región que nombró el Director presenta una variación **9,5 veces mayor**.
- **La dilatación se extiende entre islas de atlas no relacionadas**: el 74,9 % de los texeles dilatados toman su color de otra isla, desde una mediana de 0,177 en una figura de 1,0 de altura.
- **Cada reconstrucción en esta ruta es una doble pared hueca**, con paredes de aproximadamente dos vóxeles. Ningún predicado volumétrico es válido sobre uno.

## Cómo se ejecuta este repositorio

La disciplina es tan importante como el producto que la canalización, y existe por una razón: una iteración anterior realizó diez sesiones en las que cada una evaluó su propia salida y escribió conclusiones que la sesión siguiente leyó como un hecho establecido. Nada de eso era verificable.

- **Especificación antes del trabajo, informe después, decisión final**: y la sesión que diseña un experimento nunca evalúa sus propios resultados. Hay veintitrés experimentos en [el registro](docs/experiments/).
- **Las correcciones se aplican en su lugar, junto a la medición que las refutó**, nunca como eliminaciones discretas. En la sesión inicial, se falsificaron seis afirmaciones heredadas y todas siguen siendo legibles junto a lo que las reemplazó.
- **Los fallos permanecen en el repositorio con su motivo.** [`tools/superseded/`](docs/tools.md) no es un archivo; cualquiera puede ejecutar estas herramientas y observar cómo fallan de la misma manera.
- **Un resultado negativo es un éxito total**, se informa y se cierra en lugar de ajustarse a un número.
- **Las pruebas se ejecutan con el commit que modifica el código**: 370 aprobadas por dos personas, con CI basado en rutas para las 362 herméticas.
- **El registro se puede consultar.** Un índice SQLite + FTS5 sobre todo el historial, verificado en cuatro etapas. Encontró un recuento de decisiones que la prosa había indicado incorrectamente en tres sitios, contando el propio registro.

## Donde todo está

| | |
|---|---|
| **[El manual](docs/handbook/index.md)** | la guía: la ruta paso a paso, los temas, el sistema de perfiles |
| **[El registro](docs/experiments/)** | veintitrés experimentos: especificación, informe, decisión y cada predicción declarada antes de la medición |
| **[Lo que aprendió la ruta](docs/findings.md)** | los hallazgos duraderos y las reglas obtenidas con esfuerzo, en su totalidad |
| **[Estado de cada herramienta](docs/tools.md)** | lo que funciona, lo que está obsoleto y la evidencia para cada uno |
| **[Defectos conocidos](docs/known-defects.md)** | todo lo que no se ha resuelto, medido y ubicado en el código |
| **[La trayectoria, tal como ocurrió](docs/arc-history.md)** | el historial cronológico, con las correcciones intactas |
| **[CLAUDE.md](CLAUDE.md)** | cómo trabajar aquí: los roles, las reglas y el costo de cada uno |

## Posición de la licencia

Cada etapa se ejecuta localmente y es comercialmente limpia: SDXL (OpenRAIL++), MV-Adapter (código abierto), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Excluido deliberadamente, con la razón: **nvdiffrast** (no comercial; se aplica aquí mediante un mecanismo de seguridad estructural, no mediante una certificación), **Hunyuan3D-Paint** (la licencia es nula en la UE, el Reino Unido y Corea del Sur), **MVPaint** y **TEXGen** (ninguna licencia) y **UltraSharp / SUPIR / StableSR** (ampliadores de escala no comerciales).

## Modelo de confianza y amenazas

facet se ejecuta completamente en su propia máquina: cada herramienta es un script que invoca contra las rutas que escribe, por lo que la pregunta útil no es *qué permisos solicita esta aplicación*, sino *qué hacen estos scripts con su máquina*. La respuesta se obtiene mediante la medición, y cada iteración se puede volver a ejecutar; la política completa está en [SECURITY.md](SECURITY.md):

- **Datos afectados:** mallas, texturas, imágenes y JSON en el disco local, en las rutas que proporciona en la línea de comandos. Además, `docs/index/facet.db`, que es *derivado*; no contiene nada que ya no fuera un archivo en este repositorio, y `facet_index.py build` lo regenera desde cero.
- **Datos NO afectados:** nunca se tocan credenciales. Nada aquí lee, almacena ni transmite un token, una clave o una contraseña, y ninguno está presente en el árbol; se ha buscado claves con prefijos de proveedor, GitHub PAT, tokens de Slack, ID de clave de AWS, bloques de clave privada, tokens de portador y asignaciones `api_key`/`password` en línea; **cero coincidencias**, no hay archivos con formato de credencial.
- **No hay telemetría.** Ninguna se recopila ni se envía. No hay opción para desactivarla porque no hay nada que desactivar.
- **Salida de red:** dos de las treinta y cuatro herramientas abren un socket: `restylize_views.py` y `texpass_brush.py`, y ambas llaman a una API HTTP de ComfyUI en `--host`, **predeterminado `127.0.0.1:8188`**. Nada más en `tools/` realiza una llamada de red.
- **Permisos:** usuario normal. Sin elevación, sin instalación de servicio, sin escrituras en la configuración del sistema o el registro.

Se revelan tres puntos críticos en lugar de ocultarlos, porque una nota de seguridad que solo enumera garantías no es un modelo de amenazas: **las operaciones de archivo no están aisladas** (una herramienta escribe donde sus argumentos indican); **las rutas locales absolutas están integradas en muchas herramientas y documentos**: 114 ocurrencias en 26 archivos, no son secretos, sino una divulgación del diseño de una máquina, y la razón por la que la mayoría de las herramientas no se ejecutarán sin modificar en otro lugar; y **los fallos inesperados aparecen como rastreos de Python en los 34 scripts de investigación no publicados**, sin puerta de enlace `--debug`. Las detenciones deliberadas son mensajes `ANDON:` que contienen la medición que las activó. Ese es el contrato del instrumento de investigación, y [SHIP_GATE.md](SHIP_GATE.md) registra exactamente cuándo deja de ser lo suficientemente bueno; para los dos comandos que facet *instala*, a partir de la versión 0.2.0: `facet-index` y `facet-mcp` devuelven `0` correcto / `1` error de usuario / `2` error en tiempo de ejecución, y, desde [E22](docs/experiments/E22-ruling.md), **`4` RECHAZADO** por una puerta de enlace activada o un fallo `verify`, que es la herramienta funcionando y diciéndole que no continúe, en lugar de un error en tiempo de ejecución. Todos se niegan con un fallo estructurado que indica el siguiente paso en lugar de un rastreo ([E21](docs/experiments/E21-cli-contract-report.md)).

**Y las puertas en esos dos comandos ya no se pueden eliminar.** Cada ANDON en la faceta instala `raise`; un simple `assert` es una instrucción que `python -O` elimina silenciosamente, y 87 de las puertas de este repositorio podían eliminarse mediante una variable de entorno hasta que E22 las convirtió. Se midió antes y después en la misma puerta, en cuatro modos de intérprete.
**Y dado que [E23](docs/experiments/E23-route-gates-report.md), tampoco lo son las puertas de la ruta que produjo los cuatro activos aceptados**; sus **57 sitios distribuidos en doce herramientas**, se convirtieron como un simple movimiento de archivos sin que ninguna prueba los hubiera ejecutado jamás, y ahora cada uno falla bajo `-O` y `PYTHONOPTIMIZE=1`, así como bajo un intérprete normal.
**134 puertas en las herramientas de investigación restantes siguen siendo aserciones**, nombradas aquí en lugar de omitidas, con ámbito definido por [E22 Ruling 4](docs/experiments/E22-ruling.md), y ninguna de ellas se encuentra en una faceta de comando que instala: 132 son instrumentos de medición bajo `diagnostics/`, una es una comprobación de renderizado y la de `superseded/` **nunca** se convierte, porque estas herramientas se mantienen para que cualquiera pueda ejecutarlas y observar cómo fallan de la misma manera.

**Estado del soporte:** este repositorio se desarrolla de forma abierta, en un único entorno, por un director y una pareja rotativa de sesiones de asesoramiento y ejecución. `main` es el único estado compatible. No hay canal de lanzamiento, ni política de retrocompatibilidad, ni SLA; en cambio, existe un registro: cada afirmación está junto al código que la produce, y [docs/experiments](docs/experiments/) contiene las especificaciones, el informe y la resolución para cada una.

## Requisitos

Blender 5.x, Python 3.11+ con `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Se necesita una instalación local de ComfyUI solo para el pincel de retoque. Desarrollado con una RTX 5090; la capacidad de VRAM es más importante que la velocidad bruta.

CI ejecuta el subconjunto hermético de la suite en **ubuntu-latest / Python 3.12** con instalaciones fijas (`.github/workflows/ci.yml`); la capa de artefactos necesita los árboles registrados bajo `E:\AI\training`, que no están en git, por lo que CI los excluye por diseño. Localmente, `python -m pytest` ejecuta las **370** pruebas y `python -m pytest -m "not artifacts"` ejecuta las **362** que reproduce CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
