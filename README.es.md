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

El estilo se aplica **al activo**, en el espacio de la textura, y no se pinta por vista ni se une posteriormente. Si se introduce una forma exagerada en arcilla como entrada, obtendrá una malla texturizada cuyo color proviene de una referencia estilizada de *esa* malla, y todo aquello que la referencia no pueda ver se rellena con un pincel de retoque con máscara y una dilatación consciente de la superficie.

Recibe su nombre de las dos partes del problema: los polígonos y la cara que deben mantener.

## Instalar

La propia ruta es un conjunto de scripts locales que se ejecutan en rutas que se escriben; clone el repositorio y lea [cómo empezar](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Dos servidores se distribuyen como un paquete**: el índice de registros, para que un asistente pueda consultar la secuencia de pruebas en lugar de leerla, y **a partir de la versión 0.4.0, el servidor de medición**, de modo que dos activos medidos con meses de diferencia sigan una única ruta de código.

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` es el servidor MCP stdio sobre el registro (seis herramientas, con la verificación de cuatro puntos como superficie de salud que rechaza) y `facet-index` es el propio índice (`build` / `verify` / `q` / `claims`). Ejecute cualquiera de ellos desde dentro de una copia; `--db` nombra un índice diferente.

### El servidor de medición: nuevo en la versión 0.4.0

`facet-measure` responde a la **mitad numérica** de una comparación y nunca indica si la salida es buena. Cada carga útil contiene la versión del servidor, el hash del archivo propio del instrumento y un hash de configuración, y `measure_report` **rechaza** comparar cuando hay una discrepancia, que es la propiedad para la que existe todo esto.

Verificado ejecutando un **verbo** en lugar de `--help`: una malla de control devuelve 786.432 caras con un envoltorio de identidad completo en una máquina que no tiene ninguna copia.

**Lo que obtenga depende de una cosa, y es su versión de Python:**

| su Python | `[measure-full]` le proporciona |
|---|---|
| **3.11 / 3.12** | **las ocho herramientas**: `open3d` se instala desde PyPI |
| **3.13** | cuatro herramientas: `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 es la última *versión* y publica ruedas cp38-cp312 sin **ningún sdist**, por lo que en 3.13 no hay nada en PyPI para instalar. El paquete adicional lo incluye detrás de `python_version < "3.13"`, por lo que la instalación **tiene éxito** allí y las cuatro herramientas de geometría devuelven **`4` RECHAZADO**, indicando lo que necesitan, en lugar de que falle toda la instalación.

**Para obtener las ocho en Python 3.13**, Open3D publica ruedas cp313 actuales en su canal de desarrollo continuo. Una URL directa es válida en una línea de comandos; solo está prohibida dentro de los metadatos del paquete publicado:

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **En Windows y macOS, las ruedas de desarrollo tienen el sufijo `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` al momento de escribir) y el nombre cambia a medida que `main` cambia; enumere los activos en [la versión `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) y tome la actual. **Esta compilación es con la que se midieron los números dependientes de open3d de esta ruta**, y es una verdadera frontera de comparabilidad: el envoltorio de identidad registra el hash del instrumento, no sus dependencias — [E31](docs/experiments/E31-ruling.md).

*Hasta la versión 0.3.1, la rueda contenía dos archivos `.py` y ninguno de los instrumentos de medición, por lo que un servidor de medición instalado no tenía nada que ejecutar. Nadie se dio cuenta durante cuatro versiones porque este repositorio ES la copia: la herramienta funcionaba donde se compiló y nunca había estado en otro lugar.*

⚠ **`pip install facet-mcp` estaba roto en todas las versiones publicadas hasta la versión 0.3.0, y se corrigió en la versión 0.3.1.** La rueda instala `facet_index` como un módulo de nivel superior, por lo que hasta e incluyendo la versión 0.3.0, resolvía la ubicación del registro contra `<venv>/Lib`, que no contiene ni corpus ni índice, y `build`, `claims` y `q` sin `--db` fallaban todos.
**En la versión 0.3.0 o anterior, utilice el binario `npx` anterior.**

A partir de la versión 0.3.1, la raíz se resuelve **probando el registro** en lugar de asumir que existe: ejecute cualquiera de los comandos desde dentro de una copia y lo encontrará; ejecútelo desde cualquier otro lugar y devolverá **`4` RECHAZADO**, indicando ambos directorios que intentó y ambos marcadores que buscó. `$FACET_INDEX_DB` ahora es leído por ambos comandos, y selecciona qué *índice*, nunca qué *corpus*. Medido en una rueda compilada a partir de `main` e instalada en un entorno virtual limpio — [E24](docs/experiments/E24-ruling.md).

*Este bloque se ha corregido dos veces. Primero decía `pipx install facet-mcp # o el paquete de Python directamente `, until v0.3.0's read-back ran a **verb** instead of ` --help`.
Luego, indicaba que la rueda "solo funciona para `q` y `claims`", pero **`claims` tampoco funcionó**, lo que E24 descubrió al ejecutarlo. Ambas correcciones se encuentran en [known-defects.md](docs/known-defects.md) con sus mediciones.*

## Estado actual

**Cuatro activos aceptados, de cuatro clases de sujetos, sin costo alguno.** Cada uno fue evaluado por el Director a su propio zoom: en el archivo GLB o en hojas de tamaño completo, y no mediante una métrica que supere un umbral.

| sujeto | clase | aceptado | referencia / pincel / dilatación |
|---|---|---|---|
| **Character (W3)** | humanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | vehículo, rigging delgado | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | bestia, membranas de alas | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | accesorio, casi 2D, gris sobre gris | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Las cuotas son de texeles válidos y **no son comparables entre sujetos**: un barco oculta la mayor parte de sí mismo desde el nivel de los ojos y un animal oculta la mitad. Lea cada uno en relación con su propio límite de alcance pre-registrado, en relación con el cual obtienen **86–93%**: la diferencia entre las filas es la geometría, no la regresión. [Números completos, con sus denominadores](docs/handbook/subjects.md).

**Es una canalización, no un generador de un solo carácter.** Contradiga la especificación en ocho elementos nombrados y la instrucción ganará **8 de 8**: ΔE mediano de 46,3 frente a 6,2 en cinco controles mantenidos, mientras que la figura permanece siendo el mismo hombre. La estructura se mantiene mediante la malla y el control; los atributos nombrados se basan en la instrucción.

**La pregunta sobre el proyector se cerró el 16 de agosto de 2026** ([E45](docs/experiments/E45-warp-and-aov-kickoff.md)–[E49](docs/experiments/E49-finish-and-cap-kickoff.md)).
Las ocho placas **se componen de**: reconstruidas a partir del conjunto por vista, utilizando
pesos de borde × orientación × visibilidad; el atlas renderizado superó la
barrera de aceptación del director por primera vez en esta ruta, dos veces, a lo largo de dos arcos, junto a un
atlas enviado cuya ruta había estado deteriorando la pintura; las placas están de acuerdo. La cadena que lo hizo está en `tools/`
(`emit_view_aovs`, `s3_composite`, `flow_estimate`, `s3_run`, `s3_sheet`,
`atlas_from_aovs`, `twin_mesh_warp`), construida en gran medida a través de un canal de revisión externo
cuyas reclamaciones de calibración designadas han sido **veinte sobre veinte**, cada una
verificada aquí al ejecutarla antes de que algo confiara en la compilación.

**El canon son datos y establece los límites del gasto (17 de agosto de 2026).** La especificación de identidad
nombró diecisiete elementos; el flujo de trabajo que generó las copias nombró dieciséis; la
configuración predeterminada del perfil, una ejecución nueva, nombró seis. Nada los conectaba, por lo que cuatro arcos
repararon la composición aguas abajo de la pintura que era incorrecta en la fuente. El canon es ahora una
base de datos con clave en **superficie**: una lista de elementos no puede mostrarle qué falta y un
ocupante anulable crea un agujero en una fila, y `canon_gate` se ejecuta **dentro** de las herramientas que
crean una generación, antes de que exista el directorio de salida. Una generación cuyo mensaje
no cubre el canon ratificado es rechazada y no se escribe nada.

**Es un enrutador y está configurado para fallar de forma segura.** Resuelve un sujeto a su archivo de canon, cubre
un mensaje en **ambas** direcciones y lleva consigo un alcance. Una **herramienta que crea un gasto y no recibe ningún canon no procede silenciosamente; lo rechaza**. La solución para un sujeto que genuinamente no tiene ninguno es respaldada por datos censales y no puede ser utilizada por un sujeto que sí lo tiene:
`--no-canon --subject GALLEON` procede y se anuncia a sí mismo; `--no-canon --subject W3` es
**rechazado**, porque W3 tiene superficies. Eso cierra la casilla de verificación por construcción en lugar de
por convención, y eso importa porque la forma anterior (`if args.canon:`) permitió que el
controlador de PowerShell enviado pasara silenciosamente por la puerta.

**La segunda dirección es la que detecta un defecto real.** Verificar que el mensaje *contiene* el canon encuentra un mensaje escaso. Verificar que todo en el mensaje *es* canon
encuentra una frase que nombra algo que el personaje no tiene, y había uno presente en
la configuración predeterminada activa: **`gold necklace`**, que este repositorio ya había medido como un error al
nombrar el medallón del cinturón dorado, *"y el elemento sobrevive por accidente"*. Un mensaje de cobertura con
esa frase añadida ahora devuelve `missing: 0` y sigue siendo rechazado, nombrando la cláusula.

```
canon_gate 1.0.0  census  (occupancy is not ratification)
subject      named   occupancy   ratified   prof_hit surfaces
W3              19       24/24      24/24       5/19 canon/w3.surfaces.json
GALLEON         13           -          -      11/13 NONE
DRAGON          11           -          -      10/11 NONE
LONGSWORD        5         5/5        5/5        4/5 canon/longsword.surfaces.json
E10-LAYER        1           -          -          - NONE
LOGO             0           -          -          - NONE
```

`prof_hit 5/19` es un **ejemplar dejado deliberadamente roto**: es la configuración predeterminada activa que una ejecución
realmente utilizaría, por lo que se supone que el primer `--profile character.json` debe detenerse. Reparar
la cadena eliminaría la evidencia.

**Y hay una hoja de cálculo, porque los cuatro sujetos sin canon no van a moverse solos.** Emite cada superficie que el *tipo* de un sujeto implica; por lo tanto, un agujero es una fila antes de que alguien le haya puesto nombre; convierte un archivo IDENTITY.md en un inventario, lleva las articulaciones como pares para confirmar y reserva espacios de alcance por vista. Es **estructuralmente incapaz de llenar un
ocupante**, y esa es la propiedad que se prueba: una frase tóxica que llega con una
superficie ya asignada no se escribe. Generar canon es un humano caminando por una referencia;
la hoja de cálculo simplemente hace que el recorrido sea más económico y completo.

**El límite de la puerta, declarado en lugar de dejado a la deriva.** Verifica las frases del canon ratificado en ambas direcciones, dentro de un alcance. **No** verifica paráfrasis o
sinónimos; el emparejamiento semántico colocaría un modelo dentro de una puerta, lo que este repositorio rechaza por principio; ni los troncos por vista hasta que se declare un alcance de vista, ni si un material nombrado aterrizó en la *superficie* correcta. Los espacios de alcance existen y sus listas de superficies están vacías: llenarlos es un recorrido humano, igual que llenar los ocupantes. Cuatro sujetos tienen un archivo IDENTITY.md y ningún archivo JSON de superficies; se dejaron sin terminar en lugar de generarse sin realizar el recorrido por la referencia.

**Se mide cuántos elementos puede contener un mensaje, y no alcanza el canon.** La
literatura establece el precio de cada elemento de mensaje adicional a costa de si los elementos aparecen o no, dentro de un rango muy inferior al nuestro, por lo que un asiento Opus preguntó si las placas ya pagadas podrían resolverlo. **No pueden, y la razón es estructural**: ningún elemento del corpus mantiene su
frase constante mientras el recuento a su alrededor varía *y* puede estar ausente. Lo que sí dan es un límite unilateral, desde cinco mensajes en una cámara con control, máscara y semilla idénticos: sobre una escala de elementos de **10 → 17**, se eliminó **nada** de lo que estaba presente en 10, mientras que un cambio de identidad en *cero* recuento movió todo el intervalo de calibración. **El canon de W3 pide 19, y el corpus nunca lo alcanza**
([E55](docs/experiments/E55-density-vs-identity-report.md)). El estudio imprime los tres
números que se combinan: 24 superficies de mensaje, 25 comprobaciones requeridas, 19 elementos únicos; por lo tanto, nunca se cita un recuento de cobertura en relación con una medición del recuento de elementos.

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

Paso a paso, con el razonamiento para cada uno: **[el manual](docs/handbook/index.md)**.

**El salto discontinuo es nuevo y está deliberadamente diseñado para no ser sólido.** La primera casilla de la ruta siempre ha
mostrado *concepto de arcilla*, y hasta ahora nada aquí lo había creado; cada arcilla llegaba a mano y se procesaba en el camino. Ahora existe una herramienta de concepto→arcilla y su primer par ha sido recorrido
a tamaño completo: pose, muñequeras, medallón del cinturón y dobladillo rasgado, todo incluido; la masa de la melena no; se midió la fuga de color en toda la imagen con **C\* p99.9 = 13.15** con un fondo acromático impecable. **Lo que este par no puede mostrar es si la malla vuelve mejor**, que es
la única pregunta que lo promueve, por lo que sigue siendo un candidato con su evidencia registrada:
**[preparación del concepto](docs/concept-prep.md)**.

## Qué lo hace funcionar

Seis hallazgos, cada uno de los cuales requiere un experimento y cada uno de los cuales se aplica más allá del sujeto que lo generó. [La versión completa, con las mediciones](docs/findings.md).

- **Primero la forma, luego el estilo.** Los reconstructores interpretan el ruido superficial como geometría. Una arcilla limpia y de aspecto escultórico, con planos deliberadamente exagerados, produce una topología mejor que un sprite estilizado; el modelo estilizado se genera al mismo tiempo y sirve como referencia de color.
- **Define el rostro, obtén un rostro.** Un recorte del busto coloca entre un **3,1 y 4,5 veces** más polígonos en la cabeza, y la diferencia es estructural: párpados separados, una arruga en la frente, cavidades nasales modeladas; no se trata simplemente de un desenfoque más marcado.
- **Los gemelos pertenecen a una malla, no a un personaje.** Reutiliza un gemelo en diferentes mallas y la cobertura disminuye del **62% al 22,7%**, porque los brazos se proyectan hacia el espacio vacío junto al modelo. Genera gemelos a partir de la malla que vas a texturizar, cada vez.
- **La identidad pertenece a la instrucción.** Un elemento canónico que no se menciona en la instrucción aparece por accidente y desaparecerá de la misma manera; esto se mide cuando las rodilleras doradas resultaron estar presentes en la imagen solo debido al ruido en un ControlNet defectuoso.
- **Consulta la geometría, no un umbral.** Reemplazar una máscara clave con la silueta exacta del trazado de rayos movió la cobertura de referencia del **28,4% al 39,1%** de texeles válidos; es estrictamente aditivo, sin difusión, sin GPU. El método de selección basado en el punto medio de las esquinas ha fallado tres veces aquí y se ha descartado.
- **Elimina lo que ninguna cámara puede ver, del atlas y nunca de la malla.** El 49% de los texeles del atlas son invisibles desde el exterior; excluir esas caras reduce la interpolación en un 68%. Excluir en lugar de eliminar hace que el fallo sea imposible en lugar de simplemente detectable.

## Lo que aún no se ha resuelto

Identificado y medido, en la página principal en lugar de en una nota al pie. [Todos ellos, ubicados en el código](docs/known-defects.md).

- **Algunos mapas de superficie visibles se corresponden con el espacio del atlas que nunca se guarda**, y se representan como el negro predeterminado sin modificar de la imagen. El motor de renderizado de Blender utiliza un muestreo centrado en texeles, por lo que un triángulo que no coincida con ningún centro de texel queda vacío; sus propios desarrolladores
[denominaron el mecanismo e implementaron una solución](https://projects.blender.org/blender/blender/pulls/161752)
dos semanas después de la compilación en la que se midieron todos los valores aquí. Es una propiedad de la ruta,
no de un objeto específico: medido en un activo, **sin medir en los otros cuatro**.
- **La banda del contorno representa el 0,00 % de la referencia de la etapa 1** en las ocho cámaras; el acero sobre un fondo gris se sitúa exactamente en el umbral clave. La unión recupera el 55,72 %.
- **Las costuras no están niveladas.** Un límite de procedencia presenta una variación de textura **5,5 veces** mayor que la normal; la región que identificó el Director presenta una variación **9,5 veces** mayor.
- **La dilatación se extiende entre islas del atlas no relacionadas**, y el 74,9 % de los texeles dilatados obtienen su
color de otra isla, con una mediana de 0,177 en una figura de 1,0 de altura. ⚠ **Esta proporción corresponde a los texeles del atlas y no es una afirmación sobre lo que ve una cámara**: la dilatación representa el 26,95 % del
atlas renderizado y el **4,95 % de los píxeles de la figura renderizada**, una relación de 0,18. La pintura se encuentra en mapas grandes, los agujeros en mapas pequeños, por lo que un texel dilatado es económico en términos de espacio de pantalla.
- **⚑ El defecto que determina la aceptación está determinado por la PINTURA, no por ningún relleno** — regiones
que muestran el color de otro material, algo que ninguna estadística de motas puede detectar. Medido de tres maneras en tres sesiones y en tres espacios: **91,05 % `reference`, con un enriquecimiento de 0,99**, exactamente en la
tasa base; la misma clase en verde tela **68,46 % `reference`**; y en una fina lámina, los texeles pintados propios de la superficie **18,77 %** contaminan el relleno de dilatación del **5,55 %**.
El relleno se obtiene correctamente de su vecino pintado más cercano, y ese vecino ya es incorrecto. El propio proceso de mezcla es una división de dos bandas no documentada
(`M + gaussian_blur_σ16(B − M)`) que mide **el peor de cuatro** valores alternativos en los mismos
puntos.
- **Las vistas nunca son independientes, lo que limita cualquier solución de mezcla.** Para cada grupo de defectos,
**el 100 % de las caras con dos o más cámaras contribuyentes tienen todas ellas dentro de un rango de 90°**
(mediana de 45°) y el 21 % de las caras con defectos son vistas por una sola cámara. Las vistas adyacentes bajo un control casi idéntico fallan juntas, por lo que las ganancias publicadas en fotogrametría de múltiples vistas no se transfieren aquí tal cual.
- **Cada reconstrucción en esta ruta es una carcasa hueca de doble pared**, con paredes de aproximadamente dos
voxeles. Ningún predicado volumétrico es válido para uno solo.
- **Las placas difieren en los límites de materiales sin nombre, y el canon es la clave**
(2026-08-16). La deformación interior gemela a la malla medida fue de **3,5–11,1 px (mediana)** en las ocho vistas, frente a las medianas de silueta de 1,2–3,0; cada región que el Director marcó — corte de manga, mano, parte superior del botín — es una unión de materiales que la indicación de generación nunca nombró. ⚠ **CORREGIDO el 2026-08-17 y la corrección agudiza el hallazgo.** Esto decía: "la indicación registrada contiene seis elementos", pero se midió y resultó que une dos archivos diferentes. El flujo de trabajo que generó los gemelos nombra **16 de 17**, faltando solo
el agarre; el *perfil predeterminado del pincel* nombra seis. Ambos son ciertos, y la oración hizo una afirmación falsa entre ellos. Lo que se mantiene y es más importante: el agarre, el guantelete, la espinillera y la mano aparecen **cero** veces en la indicación de 16 frases, porque **no existe ningún elemento para ellos en el canon**. Una indicación completa aún no puede nombrar una mano que nunca se especificó.
✅ **CERRADO el 2026-08-17**: se recorre la lista de superficies, se rellena y se **ratifica 24/24**, y ahora la puerta rechaza una indicación que no la cubre.
- **Entre el 4,65 % y el 5,57 % de los texeles válidos son superficie que ninguna cámara plana puede ver**; fallan
en la compuerta de profundidad en todas las vistas, ninguna ruta de proyección puede pintarlos y el pipeline enviado los cubrió con la inundación ciega a la isla que creó las marcas oscuras. Necesitan una política (material neutro, pincel o aceptación), no una solución
([informe E49](docs/experiments/E49-finish-and-cap-report.md)).
- **Polígonos de color plano en las hojas de grado aceptado**: la única clase abierta del Director.
⚠ **La hipótesis del pase de relleno está FALSIFICADA (2026-08-17).** El relleno huérfano mide *por debajo*
de su propia tasa base en el defecto (0,27x), los parches se sitúan entre el 90 y el 99 % sobre texeles pintados normales y el mismo defecto está presente en un renderizado creado a partir de un atlas que es anterior a la reparación por la que se le culpó. En cambio, se rastrea hasta su origen: el gemelo propio de la vista de renderizado está limpio allí, y una **vista diferente** posee 97 de los 115 píxeles con defectos en una orientación de 0,68 frente a 0,60. El parche angular es un **artefacto de dispersión** y el color es una verdadera discrepancia entre vistas en una superficie que ya está nombrada; por lo tanto, no se justifica una regeneración del gemelo con la afirmación de que "el defecto está en los gemelos".
⚠ **Y la reparación que esta página propuso también está FALSIFICADA (2026-08-17).** Decía: *"un compositor que prefiera la vista objetivo es la solución y no cuesta nada"*. El compositor ya existía y ya era el predeterminado; medido en comparación con el clasificador plano de imágenes fijas de una ejecución registrada, la preferencia por la vista objetivo **aumenta** el recuento en la vista objetivo (38 → 40) y lo aumenta considerablemente en otras dos (23 → 64, 36 → 110), volviéndose *más* conectado al hacerlo. El mecanismo: **la forma es propiedad, el color no.**
El aceitunado es la pintura propia de la vista 6 de una superficie que la vista 6 está pintando correctamente, por lo que en la vista objetivo 6 —donde la preferencia por la vista objetivo significa *preferir la vista 6*— la política maximiza exactamente la pintura de la que está hecho el defecto. **Una política de propiedad no puede reparar una discrepancia de color entre vistas en una superficie atribuida correctamente**, lo que elimina toda la familia en lugar de solo un brazo ([E52](docs/experiments/E52-target-first-flats-ruling.md)). Lo que queda es una cuestión de pintura y cuesta una generación. *Texto obsoleto, conservado según la regla de las correcciones: "islas huérfanas del tamaño de triángulos individuales, rellenadas en plano a partir de muestras gemelas adyacentes al límite tomadas con la silueta no erosionada".*

## ¿Cómo se ejecuta este repositorio?

La disciplina es tanto el producto como el proceso, y existe por una razón: en una fase anterior se realizaron diez sesiones en las que cada una evaluó su propio resultado y escribió conclusiones que, en la sesión siguiente, se consideraron hechos establecidos. Nada de lo que ocurría en ese ciclo era verificable.

- **Especificación antes del trabajo, informe después, decisión final**; y la sesión que diseña un experimento nunca evalúa sus propios resultados. Hay cincuenta y seis experimentos en [el registro](docs/experiments/).
- **Las correcciones se aplican en su lugar, junto a la medición que las refutó**, no como eliminaciones discretas. En la sesión inicial, se falsificaron seis afirmaciones heredadas, y todas siguen siendo legibles junto a lo que las reemplazó.
- **Los fallos permanecen en el repositorio con su motivo.** [`tools/superseded/`](docs/tools.md) no es un archivo; cualquiera puede ejecutar esas herramientas y observar cómo fallan de la misma manera.
- **Un resultado negativo es un éxito total**, se informa y se cierra, en lugar de ajustarse a un número.
- **Las pruebas se ejecutan con el commit que modifica el código**; 1338 superadas por dos personas, con CI basado en rutas para las 1284 versiones herméticas.
- **El registro es consultable.** Un índice SQLite + FTS5 sobre todo el historial, verificado en cuatro puntos. Encontró un recuento de decisiones que la prosa había indicado incorrectamente en tres sitios, contando el propio registro.

## Donde todo está

| | |
|---|---|
| **[El manual](docs/handbook/index.md)** | la guía: la ruta paso a paso, los temas y el sistema de perfiles |
| **[Preparación del concepto](docs/concept-prep.md)** | el candidato para la fase de modelado: su recorrido en la Fase 0, su ubicación y el elemento de licencia que desbloquea |
| **[El registro](docs/experiments/)** | cincuenta y seis experimentos: especificación, informe, decisión y cada predicción establecida antes de la medición |
| **[Lo que aprendió la ruta](docs/findings.md)** | los resultados duraderos y las reglas obtenidas con esfuerzo, en su totalidad |
| **[Estado de cada herramienta](docs/tools.md)** | lo que funciona, lo que está obsoleto y la evidencia para cada uno |
| **[Defectos conocidos](docs/known-defects.md)** | todo lo que no se ha resuelto, medido y ubicado en el código |
| **[La fase, tal como ocurrió](docs/arc-history.md)** | el historial cronológico, con las correcciones intactas |
| **[CLAUDE.md](CLAUDE.md)** | cómo trabajar aquí: los roles, las reglas y el coste de cada uno |

## Posición de la licencia

Cada fase se ejecuta localmente y es comercialmente limpia: SDXL (OpenRAIL++), MV-Adapter (código abierto), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Excluido deliberadamente, con la razón: **nvdiffrast** (no comercial; se aplica aquí mediante un mecanismo de seguridad estructural, no mediante una certificación), **Hunyuan3D-Paint** (la licencia no es válida en la UE, el Reino Unido y Corea del Sur), **MVPaint** y **TEXGen** (ninguna licencia) y **UltraSharp / SUPIR / StableSR** (ampliadores de escala no comerciales).

**El límite de la afirmación, indicado en lugar de dejarse al descubierto.** Describe la **ruta registrada**: las fases del diagrama anterior, desde imagen a 3D. La fase candidata de preparación del modelo aguas arriba actualmente se ejecuta en una API de nube cerrada cuyos términos este repositorio **no ha verificado**, por lo que ninguna afirmación de licencia aquí cubre un activo creado a partir de uno de sus modelos. Este es un elemento abierto con una ruta definida para cerrarlo: el modelo local con la licencia correcta es **Qwen-Image-Edit (Apache-2.0)**, y **FLUX.1-Kontext [dev] se excluye por las mismas razones que nvdiffrast**: pesos no comerciales. Ambos se verifican en relación con el catálogo de modelos del estudio, en lugar de recuperarse; la justificación está en [la preparación del concepto](docs/concept-prep.md).

## Modelo de confianza y amenazas

facet se ejecuta completamente en tu propia máquina: cada herramienta es un script que ejecutas sobre rutas que escribes, por lo que la pregunta útil no es *qué permisos solicita esta aplicación*, sino *qué hacen estos scripts con tu máquina*. La respuesta se obtiene mediante la medición, y cada ejecución se puede repetir; la política completa está en [SECURITY.md](SECURITY.md):

- **Datos afectados:** mallas, texturas, imágenes y JSON en el disco local, en las rutas que indicas en la línea de comandos. Además, `docs/index/facet.db`, que es *derivado*; no contiene nada que ya no fuera un archivo en este repositorio, y `facet_index.py build` lo regenera desde cero.
- **Datos NO afectados:** nunca se tocan credenciales. Nada aquí lee, almacena ni transmite un token, una clave o una contraseña, y ninguno está presente en el árbol; se ha buscado claves con prefijos de proveedor, GitHub PATs, tokens de Slack, ID de clave de AWS, bloques de clave privada, tokens de portador y asignaciones `api_key`/`password` en línea; **cero coincidencias**, no se rastrea ningún archivo con formato de credencial.
- **No hay telemetría.** Ninguna se recopila ni se envía. No hay opción para desactivarla porque no hay nada que desactivar.
- **Salida de red:** dos herramientas abren un socket: `restylize_views.py` y `texpass_brush.py`, y ambas llaman a una API HTTP de ComfyUI en `--host`, **predeterminada `127.0.0.1:8188`**. Nada más en `tools/` realiza una llamada de red.
- **Permisos:** usuario normal. Sin elevación, sin instalación de servicio, sin escritura en la configuración del sistema o el registro.

Se revelan tres bordes afilados en lugar de eliminarlos, porque una nota de seguridad que solo enumera garantías no es un modelo de amenaza: **las operaciones con archivos no están aisladas** (una herramienta escribe donde sus argumentos indican); **las rutas locales absolutas están integradas en muchas herramientas y documentos**, aparecen 114 veces en 26 archivos, no son secretos, sino una revelación del diseño de una máquina, y la razón por la que la mayoría de las herramientas no se ejecutarán sin modificar en otro lugar; y **los fallos inesperados aparecen como rastreos de Python en los scripts de investigación no publicados**, sin ninguna barrera `--debug`. Las interrupciones deliberadas son mensajes `ANDON:` que contienen la medición que las activó. Ese es el contrato del instrumento de investigación, y [SHIP_GATE.md](SHIP_GATE.md) registra exactamente cuándo deja de ser suficiente, lo cual, para los dos comandos en la faceta *instala*, fue a partir de la versión 0.2.0: `facet-index` y `facet-mcp` devuelven `0` (correcto) / `1` (error de usuario) / `2` (error en tiempo de ejecución); y, dado que [E22](docs/experiments/E22-ruling.md), se indica **`4` RECHAZADO** para una barrera activada o una rama fallida `verify`, lo cual significa que la herramienta está funcionando y le indica que no continúe en lugar de un error en tiempo de ejecución. Todos ellos rechazan con un fallo estructurado que indica el siguiente paso en lugar de un rastreo ([E21](docs/experiments/E21-cli-contract-report.md)).

**Y las barreras en esos dos comandos ya no se pueden eliminar.** Cada ANDON en la faceta *instala* `raise`; una simple instrucción `assert` es una declaración que `python -O` elimina silenciosamente, y 87 de las barreras de este repositorio podían eliminarse mediante una variable de entorno hasta que E22 las convirtió. Se midió antes y después en la misma barrera, en cuatro modos de intérprete.
**Y dado que [E23](docs/experiments/E23-route-gates-report.md), tampoco lo son las barreras en la ruta que produjo los cuatro activos aceptados**, sus **57 sitios en doce herramientas**, convertidos como un simple movimiento en archivos que ningún test había ejecutado nunca, cada uno de ellos ahora rechazando también bajo `-O` y `PYTHONOPTIMIZE=1`, así como bajo un intérprete normal.
**Y dado que [E25](docs/experiments/E25-ruling.md), la clase está cerrada.** Sus **133 sitios en 43 archivos**, los instrumentos de medición que produjeron las pruebas para los cuatro activos aceptados anteriores, se convierten de la misma manera, lo que eleva el total que `raise` a **278**.
Exactamente **uno** solo ANDON simple `assert` permanece en cualquier lugar bajo `tools/`: `superseded/texpass_thin_mask.py`, que **nunca** se convierte, porque esas herramientas se mantienen para que cualquiera pueda ejecutarlas y ver cómo fallan de la misma manera. Este resto está fijado **por nombre** en el conjunto de pruebas, por lo que una revisión futura no puede eliminarlo sin editar la prueba a propósito.

**Estado del soporte:** este repositorio se desarrolla de forma abierta, en un único entorno, por un director y un par rotatorio de sesiones de asesoramiento y ejecución. `main` es el único estado compatible. No hay canal de lanzamiento, ni política de retrocompatibilidad, ni SLA; lo que sí hay es el registro: cada afirmación está junto al código que la produce, y [docs/experiments](docs/experiments/) contiene las especificaciones, el informe y la resolución para cada una.

## Requisitos

Blender 5.x, Python 3.11+ con `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Solo se necesita una instalación local de ComfyUI para el pincel de retoque. Desarrollado en un RTX 5090; la capacidad de VRAM es más importante que la velocidad bruta.

CI ejecuta el subconjunto hermético del conjunto de pruebas en **ubuntu-latest / Python 3.12** con instalaciones fijas (`.github/workflows/ci.yml`); la capa de artefactos necesita los árboles registrados bajo `E:\AI\training`, que no están en git, por lo que CI los excluye por diseño. Localmente, `python -m pytest` ejecuta las **1338** pruebas y `python -m pytest -m "not artifacts"` ejecuta las **1284** que reproduce CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
