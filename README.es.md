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

El estilo se aplica **al activo**, en el espacio de la textura, y no se pinta por vista ni se une posteriormente. Si se proporciona una ruta con un concepto de arcilla con formas exageradas, se obtiene una malla texturizada cuyo color proviene de una referencia estilizada de *esa* malla, y todo lo que la referencia no puede ver se rellena con un pincel de retoque con máscara y una dilatación que tiene en cuenta la superficie.

Recibe su nombre de las dos partes del problema: los polígonos y la superficie que deben representar.

## Instalar

La ruta en sí es un conjunto de scripts locales que se ejecutan en las rutas que se escriben; clone el repositorio y lea [cómo empezar](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Dos servidores se distribuyen como un paquete**: el índice de registros, para que un asistente pueda consultar el historial de pruebas en lugar de leerlo, y, **a partir de la versión 0.4.0, el servidor de medición**, de modo que dos activos medidos con meses de diferencia sigan el mismo flujo de código.

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` es el servidor MCP de stdio que opera sobre el registro (seis herramientas, con la verificación de cuatro puntos como una superficie de salud que rechaza) y `facet-index` es el índice en sí (`build` / `verify` / `q` / `claims`). Ejecute cualquiera de ellos desde dentro de un directorio de trabajo; `--db` identifica un índice diferente.

### El servidor de medición: nuevo en la versión 0.4.0

`facet-measure` responde a la **mitad numérica** de una comparación y nunca indica si la salida es correcta. Cada carga útil contiene la versión del servidor, el hash del archivo del instrumento y un hash de configuración, y `measure_report` **rechaza** la comparación si hay una discrepancia, que es la propiedad por la que existe todo esto.

Verificado ejecutando un **verbo** en lugar de `--help`: una malla de control devuelve 786.432 caras con un envoltorio de identidad completo en una máquina que no tiene un directorio de trabajo.

**Lo que obtenga depende de una cosa, y es su versión de Python:**

| Su Python | `[measure-full]` le proporciona |
|---|---|
| **3.11 / 3.12** | **las ocho herramientas**: `open3d` se instala desde PyPI |
| **3.13** | cuatro herramientas: `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 es la última *versión* y publica paquetes cp38-cp312 sin **ningún paquete fuente (sdist)**, por lo que en la versión 3.13 no hay nada en PyPI que se pueda instalar. El paquete adicional lo incluye junto con `python_version < "3.13"`, por lo que la instalación **tiene éxito** y las cuatro herramientas de geometría devuelven **`4` RECHAZADO**, indicando lo que necesitan, en lugar de que falle toda la instalación.

**Para obtener las ocho herramientas en Python 3.13**, Open3D publica los paquetes cp313 actuales en su canal de desarrollo continuo. Una URL directa es válida en la línea de comandos; solo está prohibido dentro de los metadatos del paquete publicado:

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **En Windows y macOS, los paquetes de desarrollo tienen el sufijo `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` en el momento de escribir esto) y el nombre cambia a medida que `main` cambia; enumere los activos en [la versión `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) y tome el paquete actual. **Esta versión es la que se utilizó para medir los números dependientes de open3d de esta ruta**, y es una verdadera frontera de comparabilidad: el envoltorio de identidad registra el hash del instrumento, no sus dependencias: [E31](docs/experiments/E31-ruling.md).

*Hasta la versión 0.3.1, el paquete contenía dos archivos `.py` y ninguno de los instrumentos de medición, por lo que un servidor de medición instalado no tenía nada que ejecutar. Nadie se dio cuenta durante cuatro versiones porque este repositorio ES el directorio de trabajo: la herramienta funcionaba donde se compilaba y nunca había estado en otro lugar.*

⚠ **`pip install facet-mcp` estaba dañado en todas las versiones publicadas hasta la versión 0.3.0 y se corrigió en la versión 0.3.1.** El paquete instala `facet_index` como un módulo de nivel superior, por lo que hasta e incluyendo la versión 0.3.0, resolvía la ubicación del registro en relación con `<venv>/Lib`, que no contiene ni el corpus ni el índice, y `build`, `claims` y `q` fallaban sin `--db`.
**En la versión 0.3.0 o anterior, utilice el archivo binario `npx` anterior.**

A partir de la versión 0.3.1, la raíz se resuelve **probando el registro** en lugar de asumir que existe: ejecute cualquiera de los comandos desde dentro de un directorio de trabajo y lo encontrará; ejecútelo desde cualquier otro lugar y devolverá **`4` RECHAZADO**, indicando los dos directorios que intentó y los dos marcadores que buscó. `$FACET_INDEX_DB` ahora lo leen ambos comandos y selecciona qué *índice*, nunca qué *corpus*. Medido en un paquete compilado a partir de `main` e instalado en un entorno virtual limpio: [E24](docs/experiments/E24-ruling.md).

*Este bloque se ha corregido dos veces. Primero decía `pipx install facet-mcp # o el paquete de Python directamente `, until v0.3.0's read-back ran a **verb** instead of ` --help`.
Luego decía que el paquete "solo funciona para `q` y `claims`"; **`claims` tampoco funcionaba**, lo que E24 descubrió al ejecutarlo. Ambas correcciones se encuentran en [known-defects.md](docs/known-defects.md) con sus mediciones.*

## Estado actual

**Cuatro activos aceptados, de cuatro clases de objetos, sin coste alguno.** Cada uno fue evaluado por el Director a su propio nivel de zoom, ya sea en el archivo GLB o en hojas de tamaño completo, y no por una métrica que supere un umbral.

| objeto | clase | aceptado | referencia / pincel / dilatación |
|---|---|---|---|
| **Character (W3)** | humanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | vehículo, rigging delgado | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bestia, membranas de alas | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | accesorio, casi 2D, gris sobre gris | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Las proporciones son de texeles válidos y **no son comparables entre objetos**: un barco oculta la mayor parte de sí mismo desde el nivel de los ojos y un animal oculta la mitad. Evalúe cada uno en relación con su propio límite de alcance predefinido, en relación con el cual obtienen **86-93%**: la diferencia entre las filas es la geometría, no la regresión. [Números completos, con sus denominadores](docs/handbook/subjects.md).

**Un quinto sujeto está a mitad del proceso, y es la primera referencia construida
(2026-08-17 → 2026-08-19).** A1, "el archivista", comenzó a partir de una referencia que contenía
su propia receta integrada, en lugar de partir de un concepto en arcilla, y cada etapa desde entonces
se ha basado en eso: el canon se ratificó en **16/16 superficies** antes de que existiera una malla,
una malla aprobada por el criterio del Director, un entorno que reprodujo la referencia
**pixel por pixel tres veces**, un conjunto de ocho vistas con un manifiesto sha256, y dos
fallos de contaminación identificados, cada uno medido en un mecanismo antes de que se
cambiara algo. El proceso de renderizado fue aprobado [2026-08-19](docs/experiments/E70-baked-look-report.md) — **en cuanto a la identidad y el conjunto de prendas, y ese es el alcance total de esa aprobación.**

**Luego, el pincel se abrió y solo escribe en los huecos.** El primer trazo se realizó con un ángulo de 90 grados el 2026-08-19: la invariancia ANDON indicó **0,014 lv con el componente caliente más grande de 0 px** fuera de la figura en 472.318 px probados, y `commit` escribió **3.585 texeles**, ocupando los huecos **2.044.423 → 2.040.838** con el atlas de origen, cuya identidad se volvió a verificar posteriormente. En el zoom del Director, el triángulo pálido en el cuello del chaleco se volvió de color ciruela y la costura se ve como una sola prenda. No inventó una cara, no giró la cabeza ni pintó un segundo chaleco.

**El resultado metodológico es más importante que el activo.** A lo largo de todo ese proceso, la
intensidad de ControlNet nunca se modificó; cada corrección **eliminó una causa** en lugar de
aplicar fuerza contra ella. Dos de los fallos fueron defectos en las especificaciones del asesor,
detectados por los sistemas de ejecución y por un canal de revisión externo antes de que se
utilizara un crédito, y ambos están identificados en el registro con la medición que los invalidó.

**Es una cadena de procesamiento, no un generador de un solo personaje.** Contradiga la
especificación en ocho elementos identificados y el mensaje tendrá éxito **en 8 de 8**; la
desviación media ΔE es de 46,3 frente a 6,2 en cinco controles mantenidos, mientras que la
figura sigue siendo el mismo hombre. La estructura se mantiene mediante la malla y el control; los
atributos identificados se aplican al mensaje.

**La cuestión del proyector se cerró el 2026-08-16** ([E45](docs/experiments/E45-warp-and-aov-kickoff.md)–[E49](docs/experiments/E49-finish-and-cap-kickoff.md)).
Las ocho imágenes **se componen**: reconstruidas a partir del conjunto por vista, utilizando
pesos de borde × orientación × visibilidad; el atlas renderizado superó la barra de aceptación
del Director por primera vez en esta ruta, dos veces, en dos procesos, junto a un atlas
publicado cuya ruta había estado destruyendo la pintura; las imágenes coinciden. La cadena que lo
logró está en `tools/` (`emit_view_aovs`, `s3_composite`, `flow_estimate`, `s3_run`, `s3_sheet`, `atlas_from_aovs`, `twin_mesh_warp`), construida en gran medida a través de un
canal de revisión externo cuyos criterios de calibración nominados han sido válidos **en veinte de
veinte casos**, cada uno verificado aquí al ejecutarlo antes de que se confiara en la compilación.

**El canon son datos, y establece los límites del proceso (2026-08-17).** La especificación de
identidad nombró diecisiete elementos; el flujo de trabajo que generó los gemelos nombró
dieciséis; la configuración predeterminada, una ejecución nueva, nombró seis. Nada los conectaba,
por lo que cuatro procesos repararon la composición aguas abajo de la pintura que era incorrecta
en la fuente. El canon es ahora una base de datos con clave en **superficie**: una lista de
elementos no puede mostrarle lo que falta, y un ocupante anulable convierte un hueco en una fila,
y `canon_gate` se ejecuta **dentro** de las herramientas que crean una generación, antes de que exista el
directorio de salida. Se rechaza una generación cuyo mensaje no cubra el canon ratificado y no se
escribe nada.

**Es un enrutador y está configurado para fallar de forma segura.** Resuelve un sujeto a su archivo
de canon, cubre un mensaje en **ambas** direcciones y lleva un alcance. **Una herramienta que
crea un proceso y a la que no se le proporciona un canon no procede de forma silenciosa; lo
rechaza.** La vía de escape para un sujeto que genuinamente no tiene ninguno está respaldada por
un censo y no puede ser utilizada por un sujeto que sí lo tiene: `--no-canon --subject GALLEON` procede y se anuncia; `--no-canon --subject W3`
se **rechaza**, porque W3 tiene superficies. Esto cierra la casilla de verificación por construcción,
no por convención, y es importante porque la forma anterior (`if args.canon:`) permitió que el controlador
PowerShell publicado pasara silenciosamente por la puerta.

**La segunda dirección es la que detecta un defecto real.** Comprobar que el mensaje *contiene* el
canon encuentra un mensaje escaso. Comprobar que todo en el mensaje *es* canon encuentra una
frase que nombra algo que el personaje no tiene, y había una en la configuración predeterminada
activa: **`gold necklace`**, que este repositorio ya había medido como un error al nombrar el medallón del
cinturón dorado, *"y el elemento sobrevive por accidente."* Un mensaje que cubra esa frase ahora
devuelve `missing: 0` y se rechaza de todos modos, nombrando la cláusula.

```
canon_gate 1.0.0  census  (occupancy is not ratification)
subject      named   occupancy   ratified   prof_hit surfaces
W3              19       24/24      24/24       5/19 canon/w3.surfaces.json
GALLEON         13           -          -      11/13 NONE
DRAGON          11           -          -      10/11 NONE
LONGSWORD        5         5/5        5/5        4/5 canon/longsword.surfaces.json
E10-LAYER        1           -          -          - NONE
LOGO             0           -          -          - NONE
A1              10       16/16      16/16      10/10 canon/a1.surfaces.json
```

`prof_hit 5/19` es un **ejemplar deliberadamente roto**: es la configuración predeterminada activa que
utilizaría una ejecución, por lo que se supone que el primer `--profile character.json` debe detenerse. Reparar la cadena
eliminaría la evidencia.

**Y hay una hoja de cálculo, porque los cuatro sujetos sin canon no van a seguir el proceso por sí
solos.** Emite cada superficie que implica el *tipo* de un sujeto, por lo que un hueco es una fila
antes de que alguien lo haya nombrado, convierte un archivo IDENTITY.md en un inventario, lleva
las uniones como pares para confirmar y reserva espacios de alcance por vista. Es **estructuralmente
incapaz de llenar un ocupante**, y esa es la propiedad que se prueba: una frase tóxica que llega
con una superficie ya asignada no se escribe. Generar un canon es un humano que sigue una
referencia; la hoja de cálculo solo hace que el proceso sea más económico y completo.

**El límite de la puerta se establece explícitamente, en lugar de dejarse a la interpretación.** Comprueba las frases canónicas validadas en ambas direcciones, dentro de un alcance. No comprueba paráfrasis ni sinónimos; la correspondencia semántica colocaría un modelo dentro de una puerta, lo cual este repositorio rechaza por principio, ni tampoco comprueba los elementos por vista hasta que se declare un alcance de vista, ni si un material específico se ha colocado en la superficie *correcta*. Existen espacios de alcance y sus listas de superficies están vacías: rellenarlos es una tarea manual, igual que rellenar los elementos. Cuatro sujetos tienen un archivo IDENTITY.md y no tienen archivos JSON de superficies; se dejaron sin completar en lugar de generarse sin realizar el proceso manual.

**Se mide cuántos elementos puede contener una instrucción, y no alcanza el canon.** La documentación establece el precio de cada elemento adicional de la instrucción, lo que afecta a si los elementos aparecen o no, dentro de un rango mucho menor al nuestro, por lo que se preguntó a un usuario de Opus si las imágenes ya pagadas podrían resolverlo. **No pueden, y la razón es estructural:** ningún elemento del corpus mantiene su frase constante mientras que el recuento a su alrededor varía *y* puede estar ausente. Lo que sí proporcionan es un límite unilateral, de cinco instrucciones en una cámara con control, máscara y semilla idénticos; en una escala de elementos de **10 → 17**, se elimina el recuento y no se elimina **nada** de lo que estaba presente en 10, mientras que un cambio de identidad en el recuento *cero* movió todo el intervalo de calibración. **El canon de W3 solicita 19, y el corpus nunca lo alcanza** ([E55](docs/experiments/E55-density-vs-identity-report.md)). El estudio imprime los tres números que se combinan: 24 superficies de instrucción, 25 comprobaciones requeridas, 19 elementos únicos; por lo tanto, nunca se cita un recuento de cobertura en relación con una medición del recuento de elementos.

**Un sexto sujeto participó para responder a una pregunta diferente y obtuvo un resultado negativo (2026-09-22).** Se reconstruyó un guardián del puerto para `ai-rpg-stage` para probar qué sucede *después* de la pintura (poses y accesorios), y se reconstruye correctamente y luego **falla en el auto-rigging**. Se eliminaron cuatro posibles causas mediante la medición, en lugar de mediante la argumentación: entrada sin texturas, recuento de componentes, topología de la malla y la pose. **El discriminador no está identificado**, y [`canon/BASE-FIGURE.md`](canon/BASE-FIGURE.md) contiene la tabla de lo que se probó, sin indicar una causa, porque la única causa que este repositorio identificó, la separación del brazo del torso, se refutó en la misma hora mediante una pose A real que falló en una separación *mayor* que una pose que tuvo éxito.

**El resultado es un contrato de tamaño y dos puertas.** Cada reconstrucción que realiza esta ruta se normaliza a **1.002 en su eje más largo**, medido en cuatro activos no relacionados, con tres decimales; por lo tanto, una malla de accesorio no tiene una escala real y un escudo de calefacción cargado tal cual es una puerta de 1.8 m. El tamaño real de un accesorio ahora se declara una vez en milímetros, se almacena junto al archivo y se comprueba en lugar de confiar en él (`tools/prop_scale.py`, unidad de escena **1.0 = 1.8 m**). Un accesorio que *toca* una figura en un vértice no se mantiene, por lo que la puerta de contacto informa de una distancia mínima **y un área de contacto** (`tools/verify/prop_contact.py`); el activo que lo provocó tocó en 0.00072 en 97 puntos de 624.510 y claramente no estaba sujeto. Y el resultado de un auto-rig ahora se lee en lugar de asumirse: `tools/verify/rig_report.py` indica las articulaciones, compara la malla como un *conjunto* en lugar de un recuento y dice si hay o no skinning.

**Una mano con seis dedos alcanzó una hoja aceptable después de pasar por cuatro puertas que no podían ver las manos.** El director lo encontró simplemente observando. La cláusula 7 del canon (cinco dedos por mano) existe porque la cláusula 2 la causó, y ahora las manos son un elemento de aceptación en su zoom, en lugar de algo sobre lo que las métricas guardaban silencio.

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

**El salto discontinuo es nuevo y se ha diseñado deliberadamente para que no sea sólido.** La primera casilla de la ruta siempre ha mostrado *concepto de arcilla*, y hasta ahora nada aquí lo había generado: cada arcilla llegaba a mano y se procesaba en el camino. Ahora existe una herramienta de concepto→arcilla y su primer par se ha probado a tamaño completo: pose, muñequeras, medallón del cinturón y dobladillo rasgado; la masa de la melena no; se midió la fuga de color en toda la imagen con **C\* p99.9 = 13.15** con un fondo acromático uniforme. **Lo que este par no puede mostrar es si la malla vuelve mejor**, que es la única pregunta que lo promueve, por lo que sigue siendo un candidato con su evidencia registrada: **[preparación del concepto](docs/concept-prep.md)**.

## Lo que lo hace funcionar

Seis hallazgos, cada uno de los cuales requirió un experimento y cada uno de los cuales se generaliza más allá del sujeto que lo produjo. [La versión completa, con las mediciones](docs/findings.md).

- **Primero la forma, luego el estilo.** Los reconstructores interpretan el ruido superficial como geometría. Una arcilla limpia, similar a una escultura, con planos deliberadamente exagerados, produce una mejor topología que un sprite estilizado; el gemelo estilizado se genera simultáneamente y se convierte en la referencia de color.
- **Define el rostro, obtén un rostro.** Un recorte de busto coloca entre un **3,1 y un 4,5 veces** más polígonos en la cabeza, y la diferencia es estructural: párpados separados, un pliegue en la frente, cavidades nasales modeladas, no un desenfoque más marcado.
- **Los gemelos pertenecen a una malla, no a un personaje.** Reutiliza un gemelo en diferentes mallas y la cobertura se reduce del **62% al 22,7%**, porque los brazos se proyectan en el espacio vacío junto al modelo. Genera gemelos a partir de la malla que vas a texturizar, cada vez.
- **La identidad pertenece a la instrucción.** Un elemento canónico que no se menciona en la instrucción aparece por accidente y desaparecerá de la misma manera; se mide cuando las rodilleras doradas resultaron estar presentes en la imagen solo a través del ruido en un ControlNet defectuoso.
- **Consulta la geometría, no un umbral.** Reemplazar una máscara clave con la silueta exacta del trazado de rayos movió la cobertura de referencia del **28,4% al 39,1%** de texeles válidos: estrictamente aditivo, sin difusión, sin GPU. El ajuste de clave de mediana de esquina ha fallado **cuatro** veces aquí y se ha retirado: un degradado pintado, un renderizado de arcilla en tonos grises, el fondo de estudio iluminado de un modelo de difusión y una referencia de difusión cuyos propios bordes abarcan L\* 48,1–81,1. ⚠ La forma aún se incluye en un producto, `tools/verify/gate_mesh.py`, que muestrea una sola esquina: se menciona aquí en lugar de aplicarse silenciosamente.
- **Elimina lo que ninguna cámara puede ver, del atlas y nunca de la malla.** El 49% de los texeles del atlas son invisibles desde el exterior; excluir esas caras reduce la interpolación en un **68%**. Excluir en lugar de eliminar hace que el fallo sea imposible en lugar de simplemente detectable.

## Qué no está resuelto

Mencionado y medido, en la página principal en lugar de en una nota al pie. [Todos ellos, ubicados en el código](docs/known-defects.md).

- **Algunas superficies visibles se asignan a un espacio de atlas que nunca se guarda**, y se representan como el negro predeterminado sin modificar de la imagen. El motor de renderizado de Blender utiliza un muestreo centrado en texeles, por lo que un triángulo que no se superpone a ningún centro de texel queda vacío; sus propios desarrolladores
[denominaron el mecanismo e implementaron una solución](https://projects.blender.org/blender/blender/pulls/161752)
dos semanas después de la compilación en la que se midieron todos los valores aquí. Es una propiedad de la ruta,
no de un objeto específico: medido en un activo, **no medido en los otros cuatro**.
- **La banda de la hoja representa el 0.00% de la referencia de la etapa 1** en las ocho cámaras; el acero sobre un fondo gris se sitúa exactamente en el umbral de la clave. La unión rescata el 55.72%.
- **Las uniones de los trazos no están niveladas.** Un límite de procedencia presenta una variación de textura **5.5 veces** mayor; la región que el Director nombró presenta una variación **9.5 veces** mayor.
- **La dilatación se extiende entre islas de atlas no relacionadas**; el 74.9% de los texeles dilatados toman su
color de otra isla, con una mediana de 0.177 de distancia en una figura de 1.0 de altura. ⚠ **Esta proporción se
refiere a los texeles del atlas y no es una afirmación sobre lo que ve una cámara**: la dilatación representa el 26.95% del
atlas renderizado y el **4.95% de los píxeles de la figura renderizada**, una proporción de 0.18. La pintura se encuentra en mapas grandes,
los agujeros en mapas pequeños, por lo que un texel dilatado es económico en el espacio de la pantalla.
- **⚑ El defecto que determina la aceptación es generado por la PINTURA, no por ningún relleno**; regiones
que muestran el color de otro material, lo cual ninguna estadística de motas puede detectar. Medido de tres maneras por
tres sesiones en tres espacios: **91.05% `reference`, con un enriquecimiento de 0.99**, exactamente
en la tasa base; la misma clase en verde de tela **68.46% `reference`**; y en una delgada hoja, los
propios texeles pintados de la superficie **18.77%** contaminados frente al **5.55%** del relleno de dilatación.
El relleno se obtiene correctamente de su vecino pintado más cercano, y ese vecino ya es
incorrecto. La mezcla en sí es una división de dos bandas no documentada
(`M + gaussian_blur_σ16(B − M)`) que mide **el peor de cuatro** valores alternativos en los mismos
puntos.
- **⚑ Una superficie pintada resulta con bandas, y es el hallazgo de propiedad anterior que llega a
un activo aceptado.** La superficie gemela de A1 es un lavado continuo; el renderizado se divide en franjas
verticales de diferentes tonos de melocotón. `project_twins` es **el que gana todo**: una cámara gana cada
texel de forma definitiva por el peso de la cara, la propiedad en lugar de la media, y la superficie se ve por
la vista frontal y los dos cuadrantes de 45°, que **no coinciden en el valor del color en R 13.0 / G 13.9
/ B 18.3** en todo el anillo aceptado. Donde dos mapas UV en la superficie son propiedad de
diferentes cámaras, la diferencia se manifiesta como un paso marcado, por lo que **las bandas son límites de isla, no suciedad**
y tampoco la clase de agujero gris. **El pincel no puede corregirlo estructuralmente**: `commit` escribe solo en texeles de agujero y los texeles con estilo están congelados. Se nombran dos soluciones y ninguna se aplica: dejar que la vista frontal sea propietaria de toda la banda de la cabeza, o una mezcla de uniones
**que permita reescribir el color de la superficie**, lo cual ninguna etapa de esta ruta puede hacer actualmente.
La media ponderada ya se acumula en la herramienta y el atlas mezclado ya existe
en el disco; nadie lo ha puesto delante del Director. **Esto estaba presente en la hoja de la que se aprobó el renderizado**, y la aprobación cubría la identidad y el conjunto de prendas: un defecto abierto en un artefacto aceptado no es una contradicción, pero el registro no debe indicar que la aprobación cubre una propiedad que nadie evaluó.
- **Las vistas nunca son independientes, lo que limita cada solución de mezcla.** Para cada grupo de defectos,
**el 100% de las superficies con dos o más cámaras contribuyentes tienen todas dentro de un rango de 90°**
(mediana de 45°), y el 21% de las superficies con defectos son vistas por una sola cámara. Las vistas adyacentes bajo
un control casi idéntico fallan juntas, por lo que las ganancias publicadas de fotogrametría de múltiples vistas no
se transfieren aquí tal cual.
- **Cada reconstrucción en esta ruta es una carcasa hueca de doble pared**, con paredes de aproximadamente dos
voxeles. Ningún predicado volumétrico es válido en una de ellas.
- **Las placas no coinciden en los límites de materiales no nombrados, y el canon es el punto clave**
(2026-08-16). La deformación interior de la superficie a la malla medida fue de **3.5–11.1 px de mediana** en todas
las ocho vistas, en comparación con las medianas de la silueta de 1.2–3.0; cada región residual que el Director
circuló (corte de la manga, mano, parte superior del zapato) es una unión de materiales que el mensaje de generación
nunca nombró. ⚠ **CORREGIDO el 2026-08-17, y la corrección agudiza el hallazgo.** Esto decía "el mensaje registrado contiene seis elementos", medido, que suelda dos archivos diferentes. El flujo de trabajo que generó los gemelos nombra **16 de 17**, faltando solo
el agarre; el *perfil predeterminado del pincel* nombra seis. Ambos son ciertos, y la oración hizo una
afirmación falsa de ellos. Lo que se mantiene y es más importante: el agarre, el brazalete, la espinillera y la mano
aparecen **cero** veces en el mensaje de 16 frases, porque **no existe ningún elemento para ellos en
el canon**. Un mensaje completo aún no puede nombrar una mano que nunca se especificó.
✅ **CERRADO el 2026-08-17**: se recorre la lista de superficies, se completa y se **ratifica 24/24**, y
la puerta ahora rechaza un mensaje que no lo cubre.
- **El 4.65–5.57% de los texeles válidos son superficies que ninguna cámara de anillo plano puede ver**; fallan
en la puerta de profundidad en todas las vistas, ninguna ruta de proyección puede pintarlos, y la canalización enviada los cubrió con la inundación ciega a la isla que creó las marcas oscuras. Necesitan una política (material neutro, pincel o aceptación), no una solución
([informe E49](docs/experiments/E49-finish-and-cap-report.md)).
- **Polígonos de color plano en las hojas de grado aceptado**: la única clase abierta del Director.
⚠ **La hipótesis del pase de relleno es FALSA (2026-08-17).** El relleno huérfano mide *por debajo*
de su propia tasa base en el defecto (0.27x), los parches se sitúan en un 90–99% en texeles pintados normales, y el mismo defecto está presente en un renderizado construido a partir de un atlas que
predata la reparación que se le atribuyó. En cambio, se rastrea hasta su origen: el gemelo de la vista de renderizado está limpio allí, y una **vista diferente** es propietaria de 97 de 115 píxeles de defecto con una cara de 0.68 frente a 0.60. El parche angular es un **artefacto de dispersión** y el color es una diferencia real entre vistas en una superficie que ya está nombrada, por lo que una regeneración del gemelo no está justificada por "el defecto está en los gemelos".
⚠ **Y la reparación que esta página propuso también es FALSA (2026-08-17).** Decía *"un
compositor que prefiera la vista de destino es la solución y no cuesta nada".* El
compositor ya existía y ya era el predeterminado; medido en comparación con el clasificador plano en las imágenes fijas de una ejecución registrada, el primer destino **aumenta** el recuento en el
destino nombrado (38 → 40) y lo aumenta bruscamente en otros dos (23 → 64, 36 → 110), volviéndose
*más* conectado al hacerlo. El mecanismo: **la forma es la propiedad, el color no lo es.**
El color oliva es la pintura de la vista 6 de una superficie que la vista 6 está pintando correctamente, por lo que en el destino 6, donde el primer destino significa *preferir la vista 6*, la política maximiza exactamente la pintura de la que está hecho el defecto. **Una política de propiedad no puede corregir una diferencia de color entre vistas en una superficie correctamente atribuida**, lo que descarta la familia en lugar de solo un brazo de ella ([E52](docs/experiments/E52-target-first-flats-ruling.md)). Lo que queda es una cuestión de pintura y cuesta una generación. *Texto obsoleto, conservado según la regla de correcciones: "islas huérfanas del tamaño de triángulos individuales, rellenas de forma plana a partir de muestras gemelas adyacentes a los límites tomadas con la silueta no erosionada".*

- **Una reconstrucción que no aplicará el rigging automático, sin ningún discriminador conocido.** Uno de los seis sujetos se reconstruye correctamente y falla en el rigging automático. Entrada sin texturas, recuento de componentes, topología de la malla y la pose se eliminan cada uno mediante mediciones, y la causa por la que este repositorio *sí* nombró algo se falsificó en la misma hora, por lo que la tabla permanece sin ella. Asignar un rigging que sí existe tiene un límite medido en lugar de una solución: aproximadamente 20 grados de rotación del brazo se mantienen correctamente, aproximadamente 110 grados distorsionan los hombros y la unión rígida de la placa [no lo repara](docs/tools.md); las tres reparaciones intentadas se midieron y las tres fallaron.
- **Ningún accesorio ha sido montado y aceptado.** El contrato de tamaño y la puerta de contacto existen y se prueban con mallas sintéticas a una separación conocida. Aún no se ha colocado nada en una mano y se ha evaluado en el zoom del Director, y hasta que eso suceda, la puerta es un instrumento sin soporte en un activo real.

## Cómo se ejecuta este repositorio

La disciplina es tan importante como el producto y el flujo de trabajo, y existe por una razón: una iteración anterior realizó diez sesiones en las que cada una evaluó su propio resultado y escribió conclusiones que la sesión siguiente leyó como un hecho establecido. Nada de ese proceso era verificable.

- **Especificación antes del trabajo, informe después, decisión final**, y la sesión que diseña un experimento nunca califica sus propios resultados. Setenta y tres experimentos están en [el registro](docs/experiments/).
- **Las correcciones se aplican en su lugar, junto a la medición que las refutó**, nunca como eliminaciones discretas. Seis afirmaciones heredadas se falsificaron en la sesión fundacional, y las seis aún son legibles junto a lo que las reemplazó.
- **Los fallos permanecen en el repositorio con su razón.** [`tools/superseded/`](docs/tools.md) no es un archivo; cualquiera puede ejecutar esas herramientas y observar cómo fallan de la misma manera.
- **Un resultado negativo es un éxito total**, que se informa y se cierra en lugar de ajustarse a un número.
- **Las pruebas se ejecutan con el commit que modifica el código**, 1376 aprobadas en dos entornos, con CI con restricciones de ruta en las 1319 herméticas.
- **El registro se puede consultar.** Un índice SQLite + FTS5 sobre todo el historial, verificado en cuatro puntos. Encontró un recuento de decisiones que el texto tenía incorrecto en tres sitios, contando el propio registro.

## Dónde está todo

| | |
|---|---|
| **[El manual](docs/handbook/index.md)** | la guía: la ruta paso a paso, los sujetos, el sistema de perfiles |
| **[Accesorios y riggings](docs/handbook/props-and-rigs.md)** | la etapa posterior al pintado: el sujeto que no aplicará el rigging automático y los dos contratos que convierten un accesorio en un accesorio |
| **[Preparación del concepto](docs/concept-prep.md)** | el salto de arcilla candidato: su recorrido de la Puerta 0, su colocación y el elemento de licencia que abre |
| **[El registro](docs/experiments/)** | setenta y tres experimentos: especificación, informe, decisión y cada predicción establecida antes de la medición |
| **[Lo que aprendió la ruta](docs/findings.md)** | los hallazgos duraderos y las reglas obtenidas con esfuerzo, en su totalidad |
| **[Estado de cada herramienta](docs/tools.md)** | lo que funciona, lo que está obsoleto y la evidencia para cada uno |
| **[Defectos conocidos](docs/known-defects.md)** | todo lo que no se ha resuelto, medido y localizado en el código |
| **[La iteración, tal como ocurrió](docs/arc-history.md)** | el historial cronológico, con las correcciones intactas |
| **[CLAUDE.md](CLAUDE.md)** | cómo trabajar aquí: los roles, las reglas y el costo de cada uno |

## Posición de la licencia

Cada etapa se ejecuta localmente y es comercialmente limpia: SDXL (OpenRAIL++), MV-Adapter (abierto), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Excluido deliberadamente, con la razón: **nvdiffrast** (no comercial, aplicado aquí mediante un mecanismo de seguridad estructural, no mediante una certificación), **Hunyuan3D-Paint** (licencia inválida en la UE, el Reino Unido y Corea del Sur), **MVPaint** y **TEXGen** (sin licencia) y **UltraSharp / SUPIR / StableSR** (ampliadores no comerciales).

**El límite de la afirmación, declarado en lugar de dejado a la deriva.** Describe la **ruta registrada**: las etapas del diagrama anterior, desde la imagen a 3D. El salto de preparación de arcilla candidato aguas arriba actualmente se ejecuta en una API de nube cerrada cuyos términos este repositorio **no ha verificado**, por lo que ninguna afirmación de licencia aquí cubre un activo creado a partir de una de sus arcillas. Ese es un elemento abierto con una ruta definida para cerrarlo: el modelo local con licencia correcta es **Qwen-Image-Edit (Apache-2.0)**, y **FLUX.1-Kontext [dev] se excluye por las mismas razones que nvdiffrast**: pesos no comerciales. Ambos se verificaron con el catálogo de modelos del estudio en lugar de recordarlos; el razonamiento está en [la preparación del concepto](docs/concept-prep.md).

## Modelo de confianza y amenazas

facet se ejecuta completamente en su propia máquina: cada herramienta es un script que invoca contra rutas que escribe, por lo que la pregunta útil no es *qué permisos solicita esta aplicación*, sino *qué hacen estos scripts en su máquina*. Respondiendo mediante la medición, con cada iteración que se puede volver a ejecutar; la política completa está en [SECURITY.md](SECURITY.md):

- **Datos afectados:** mallas, texturas, imágenes y archivos JSON en el disco local, en las rutas que
se especifiquen en la línea de comandos. Además, `docs/index/facet.db`, que se *deriva* — no contiene
nada que no fuera ya un archivo en este repositorio, y `facet_index.py build`
lo regenera desde cero.
- **Datos NO afectados:** nunca se tocan las credenciales. Nada aquí lee, almacena ni transmite
un token, clave o contraseña, y ninguno está presente en el árbol — se ha revisado para
eliminar las claves con prefijo de proveedor, los tokens PAT de GitHub, los tokens de Slack, los ID de clave de AWS, los bloques de clave privada,
los tokens de acceso y las asignaciones en línea `api_key`/`password`, **cero coincidencias**, no se rastrea ningún archivo con formato de credencial.
- **No hay telemetría.** No se recopila ni se envía nada. No hay opción de exclusión porque no hay
nada de lo que excluirse.
- **Salida de red:** dos herramientas abren un socket — `restylize_views.py`
y `texpass_brush.py` — y ambas llaman a una API HTTP de ComfyUI en `--host`, **valor
predeterminado `127.0.0.1:8188`**. Nada más en `tools/` realiza una llamada de red.
- **Permisos:** usuario normal. Sin elevación de privilegios, sin instalación de servicios, sin escrituras en la configuración del sistema
o en el registro.

Se revelan tres aspectos importantes en lugar de simplemente afirmarlos, porque una nota de seguridad que
solo enumera garantías no es un modelo de amenazas: **las operaciones de archivos no están aisladas**
(una herramienta escribe donde sus argumentos lo indican); **las rutas locales absolutas están integradas en muchas
herramientas y documentos** — 114 ocurrencias en 26 archivos, no son secretos, sino una divulgación de la estructura de una
máquina, y la razón por la que la mayoría de las herramientas no se ejecutarán sin modificar en otro lugar; y
**los fallos inesperados aparecen como rastreos de Python en los scripts de investigación no publicados**, sin ninguna puerta de enlace `--debug`. Las interrupciones deliberadas son mensajes `ANDON:` que contienen la
medida que las activó. Ese es el contrato del instrumento de investigación, y
[SHIP_GATE.md](SHIP_GATE.md) registra exactamente cuándo deja de ser suficiente — lo que, para las dos facetas de comandos *instala*, fue a la versión 0.2.0: `facet-index` y `facet-mcp` devuelven
`0` correcto / `1` error de usuario / `2` error en tiempo de ejecución — y, dado que
[E22](docs/experiments/E22-ruling.md), **`4` RECHAZADO** para una puerta de enlace activada o una rama `verify` fallida, que es la herramienta funcionando y diciéndole que no continúe en lugar de un
error en tiempo de ejecución. Todos ellos se niegan con un fallo estructurado que indica el siguiente paso en lugar de un rastreo ([E21](docs/experiments/E21-cli-contract-report.md)).

**Y las puertas de enlace en esos dos comandos ya no se pueden eliminar.** Cada ANDON en la faceta de instalación `raise`; un `assert` simple es una declaración `python -O` que se elimina silenciosamente,
y 87 de las puertas de enlace de este repositorio se podían eliminar mediante una variable de entorno hasta que E22 las convirtió. Se midió antes y después en la misma puerta de enlace, en cuatro modos de intérprete.
**Y, dado que [E23](docs/experiments/E23-route-gates-report.md), tampoco lo son las puertas de enlace en
la ruta que produjo los cuatro activos aceptados** — sus **57 sitios en doce
herramientas**, convertidos como un simple movimiento de archivos que ningún test había ejecutado nunca, cada uno de ellos ahora se niega bajo `-O` y `PYTHONOPTIMIZE=1`, así como bajo un intérprete normal.
**Y, dado que [E25](docs/experiments/E25-ruling.md), la clase está cerrada.** Sus **133 sitios
en 43 archivos** — los instrumentos de medición que produjeron la evidencia para los cuatro
activos aceptados anteriores — se convierten de la misma manera, lo que eleva el total que `raise` a **278**.
Exactamente **uno** ANDON simple `assert` permanece en cualquier lugar debajo de `tools/`:
`superseded/texpass_thin_mask.py`, que **nunca** se convierte, porque se mantiene para que cualquiera pueda ejecutarlas y verlas fallar de la misma manera. Ese resto se fija
**por nombre** en la suite de pruebas, por lo que un barrido futuro no puede eliminarlo sin editar la
prueba a propósito.

**Estado de soporte:** este repositorio se desarrolla de forma abierta, en un único entorno, por un único director
y un par de sesiones de asesor y ejecutor que van rotando. `main` es el único estado compatible. No hay canal de lanzamiento, ni política de retrocompatibilidad, ni SLA; en su lugar, existe el registro: cada afirmación está junto al código que la produce, y
[docs/experiments](docs/experiments/) contiene las especificaciones, el informe y la resolución para
cada una.

## Requisitos

Blender 5.x, Python 3.11+ con `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`,
`spandrel`, `torch`. Solo se necesita una instalación local de ComfyUI para el pincel de retoque.
Desarrollado con una RTX 5090; la capacidad de VRAM es más importante que la velocidad bruta.

**Dos intérpretes, y la división es deliberada.** La suite, las herramientas MCP servidas y
cada ejecución de medición se ejecutan con el entorno que contiene los pines de CI (3.12). La
etapa de reconstrucción se ejecuta con un segundo intérprete con la versión **3.10**, porque las ruedas TRELLIS que necesita están compiladas para él. Una herramienta que no se importa suele estar solicitándose desde el otro intérprete.

CI ejecuta el subconjunto hermético de la suite en **ubuntu-latest / Python 3.12** con
instalaciones fijas (`.github/workflows/ci.yml`); la capa de artefactos necesita los árboles registrados bajo `E:\AI\training`, que no están en git, por lo que CI los deselecciona por diseño.
Localmente, `python -m pytest` ejecuta las **1376** pruebas y `python -m pytest -m "not artifacts"`
ejecuta las **1319** que reproduce CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
