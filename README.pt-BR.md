<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.md">English</a>
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

O estilo é aplicado **no ativo**, no espaço da textura — não é pintado para cada visualização e, posteriormente, combinado. Forneça à rota um conceito de argila com formas exageradas e ela retornará uma malha texturizada cuja cor foi obtida a partir de uma referência estilizada *dessa* malha, com tudo o que a referência não podia ver preenchido por um pincel de retoque mascarado e uma dilatação consciente da superfície.

Nomeado para ambas as partes do problema: os polígonos e a face que eles devem manter.

## Instalar

A própria rota é um conjunto de scripts locais que você invoca em caminhos que digita — clone o repositório e leia [introdução](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Dois servidores são enviados como um pacote** — o índice de registro, para que um assistente possa consultar o histórico das evidências em vez de lê-lo e, **a partir da versão 0.4.0, o servidor de medição**, para que dois ativos medidos com meses de diferença passem por um único caminho de código.

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` é o servidor MCP stdio sobre o registro (seis ferramentas, com a verificação de quatro pontos como uma superfície de saúde que rejeita) e `facet-index` é o próprio índice (`build` / `verify` / `q` / `claims`). Execute qualquer um deles dentro de um diretório extraído; `--db` nomeia um índice diferente.

### O servidor de medição — novo na versão 0.4.0

`facet-measure` responde à **metade numérica** de uma comparação e nunca diz se a saída é boa. Cada carga útil contém a versão do servidor, o hash do arquivo do instrumento e um hash de configuração, e `measure_report` **rejeita** comparar em caso de incompatibilidade — que é a propriedade para a qual todo o sistema existe.

Verificado executando um **verbo** em vez de `--help` — uma malha de controle retorna 786.432 faces com um envelope de identidade completo em uma máquina que não tem nenhum diretório extraído.

**O que você obtém depende de uma coisa, e é a sua versão do Python:**

| seu Python | `[measure-full]` oferece |
|---|---|
| **3.11 / 3.12** | **todas as oito ferramentas** — `open3d` instala a partir do PyPI |
| **3.13** | quatro ferramentas; `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 é o *lançamento* mais recente e publica pacotes cp38–cp312 sem **nenhum sdist**, portanto, na versão 3.13 não há nada no PyPI para instalar. O pacote extraído o inclui junto com `python_version < "3.13"`, então a instalação **tem sucesso** ali e as quatro ferramentas de geometria retornam **`4` REJEITADO**, indicando o que precisam — em vez de toda a instalação falhar.

**Para obter todas as oito no Python 3.13**, Open3D publica os pacotes cp313 atuais em seu canal de desenvolvimento contínuo. Uma URL direta é aceitável na linha de comando; ela só é proibida dentro dos metadados do pacote publicado:

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **No Windows e macOS, os pacotes de desenvolvimento são sufixados com `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` no momento da redação) e o nome muda à medida que `main` muda — liste os ativos no [lançamento `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) e pegue o mais recente. **Essa versão é a que foi usada para medir os números dependentes do open3d desta rota**, e ela representa uma verdadeira fronteira de comparabilidade: o envelope de identidade registra o hash do instrumento, não suas dependências — [E31](docs/experiments/E31-ruling.md).

*Até a versão 0.3.1, o pacote continha dois arquivos `.py` e nenhum dos instrumentos de medição, portanto, um servidor de medição instalado não tinha nada para invocar. Ninguém percebeu durante quatro lançamentos porque este repositório É o diretório extraído: a ferramenta funcionava onde era construída e nunca havia estado em outro lugar.*

⚠ **`pip install facet-mcp` estava com defeito em todas as versões lançadas até a versão 0.3.0, e foi corrigido na versão 0.3.1.** O pacote instala `facet_index` como um módulo de nível superior, portanto, até e incluindo a versão 0.3.0, ele resolvia o local do registro em relação a `<venv>/Lib` — que não contém nenhum corpus nem índice — e `build`, `claims` e `q` sem `--db` falhavam.
**Na versão 0.3.0 ou anterior, use o binário `npx` acima.**

A partir da versão 0.3.1, a raiz é resolvida **testando se o registro existe**, em vez de presumir que ele existe: execute qualquer um dos comandos dentro de um diretório extraído e ele o encontrará; execute-o de qualquer outro lugar e ele retornará **`4` REJEITADO**, indicando ambos os diretórios que tentou e ambas as marcas que procurou. `$FACET_INDEX_DB` agora é lido por ambos os comandos, e ele seleciona qual *índice*, nunca qual *corpus*. Medido em um pacote construído a partir de `main` e instalado em um ambiente virtual limpo — [E24](docs/experiments/E24-ruling.md).

*Este bloco foi corrigido duas vezes. Primeiro, dizia `pipx install facet-mcp # ou o pacote Python diretamente `, until v0.3.0's read-back ran a **verb** instead of ` --help`.
Em seguida, afirmava que o pacote "só funciona para `q` e `claims`" — **`claims` também não funcionou**, o que E24 descobriu ao executá-lo. Ambas as correções estão em [known-defects.md](docs/known-defects.md) com suas medições.*

## Situação atual

**Quatro ativos aceitos, de quatro classes de objetos, sem custo.** Cada um foi avaliado pelo Diretor em seu próprio nível de zoom — no arquivo GLB ou em planilhas de tamanho real — e não por uma métrica que atinja um limite.

| objeto | classe | aceito | referência / pincel / dilatação |
|---|---|---|---|
| **Character (W3)** | humanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | veículo, rigging fino | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | animal, membranas das asas | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | adereço, quase 2D, cinza sobre cinza | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

As proporções são de texels válidos e **não são comparáveis entre objetos** — um navio esconde a maior parte de si mesmo do nível dos olhos e um animal esconde metade. Avalie cada um em relação ao seu próprio limite de alcance pré-registrado, em relação ao qual eles atingem **86–93%**: a diferença entre as linhas é geometria, não regressão. [Números completos, com seus denominadores](docs/handbook/subjects.md).

**É um pipeline, não um gerador de um único caractere.** Contradiga a especificação em oito elementos nomeados e o prompt vence **8 de 8** — ΔE mediano de 46,3 contra 6,2 em cinco controles mantidos — enquanto a figura permanece sendo o mesmo homem. A estrutura é mantida pela malha e pelo controle; os atributos nomeados são controlados pelo prompt.

**A questão do projetor foi encerrada em 16 de agosto de 2026** ([E45](docs/experiments/E45-warp-and-aov-kickoff.md)–[E49](docs/experiments/E49-finish-and-cap-kickoff.md)).
As oito placas **compõem**: reconstruídas a partir do conjunto por visualização, sob
pesos de borda × orientação × visibilidade; o atlas renderizado atendeu pela primeira vez ao
critério de aceitação do Diretor nesta rota — duas vezes, em dois arcos —, ao lado de um
atlas enviado cuja rota estava destruindo a pintura das placas. A cadeia que fez isso está em `tools/`
(`emit_view_aovs`, `s3_composite`, `flow_estimate`, `s3_run`, `s3_sheet`,
`atlas_from_aovs`, `twin_mesh_warp`), construída principalmente por meio de um canal de revisão externo
cuja especificação de calibração nomeada tem se mantido **vinte para vinte**, cada uma
verificada aqui executando-a antes que qualquer coisa confie na construção.

**O cânone é dado, e ele define o orçamento (17 de agosto de 2026).** A especificação de identidade
nomeou dezessete elementos; o fluxo de trabalho que gerou os gêmeos nomeou dezesseis; o
perfil padrão, uma nova execução usaria seis. Nada os conectava, então quatro arcos
repararam a composição a jusante da pintura que estava errada na fonte. O cânone é agora um
banco de dados com chave em **superfície** — uma lista de elementos não pode mostrar o que está faltando, e um
espaço ocupável anulável cria um buraco em uma linha —, e `canon_gate` executa **dentro** das ferramentas que
criam uma geração, antes que o diretório de saída exista. Uma geração cujo prompt não cobre o cânone ratificado é rejeitada e nada é escrito.

**É um roteador, e ele falha em estado fechado.** Ele resolve um assunto para seu arquivo de cânone, cobre
um prompt em **ambas** as direções e carrega um escopo. Uma **ferramenta que cria um orçamento e não recebe nenhum cânone não prossegue silenciosamente — ela rejeita.** A saída para um assunto que genuinamente não tem nenhum é baseada em dados do censo e não pode ser usada por um assunto que tem:
`--no-canon --subject GALLEON` prossegue e se anuncia; `--no-canon --subject W3` é
**rejeitado**, porque o W3 tem superfícies. Isso fecha a caixa de seleção por construção, e não por convenção, e isso importa porque a forma anterior — `if args.canon:` — permitiu que o
driver PowerShell enviado passasse pelo portão em silêncio.

**A segunda direção é aquela que detecta um defeito real.** Verificar se o prompt *contém* o cânone encontra um prompt fino. Verificar se tudo no prompt *é* cânone
encontra uma frase que nomeia algo que o personagem não tem — e havia um na configuração ativa: **`gold necklace`**, que este repositório já havia medido como nomeando incorretamente
o medalhão de cinto dourado, *"e o elemento sobrevive por acidente."* Um prompt abrangente com essa frase anexada agora retorna `missing: 0` e ainda assim rejeita, nomeando a cláusula.

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

`prof_hit 5/19` é um **espécime deixado deliberadamente quebrado**: é a configuração ativa que uma execução
realmente usaria, então o primeiro `--profile character.json` deve parar. Reparar
a string excluiria a evidência.

**E há uma planilha, porque os quatro assuntos sem cânone não vão se mover sozinhos.** Ela emite todas as superfícies que o *tipo* de um assunto implica — então um buraco é uma linha antes
de alguém nomeá-lo —, transforma um IDENTITY.md em um inventário, carrega junções como pares para confirmar e reserva espaços de escopo por visualização. É **estruturalmente incapaz de preencher um
espaço ocupável**, e essa é a propriedade que é testada: uma frase venenosa chegando com uma
superfície já atribuída não é escrita. Gerar cânone é um humano percorrendo uma referência;
a planilha apenas torna o percurso mais barato e completo.

**O limite do portão, declarado em vez de deixado para ser descoberto.** Ele verifica as frases de cânone ratificadas em ambas as direções, em um escopo. Ele **não** verifica paráfrases ou
sinônimos — a correspondência semântica colocaria um modelo dentro de um portão, o que este repositório rejeita por princípio —, nem os elementos por visualização até que um escopo de visualização seja declarado, nem se um material nomeado caiu na *superfície* correta. Os espaços de escopo existem e suas listas de superfície estão vazias: preenchê-los é um percurso humano, assim como preencher os espaços ocupáveis. Quatro assuntos têm um IDENTITY.md e nenhum JSON de superfícies — deixados inacabados em vez de gerados sem percorrer a referência.

**Quantos elementos um prompt pode carregar é medido, e não atinge o cânone.** A
literatura precifica cada elemento de prompt adicionado com um custo para se os elementos aparecem ou não, em uma faixa muito abaixo da nossa, então um assento Opus perguntou se as placas já pagas poderiam resolver isso.
**Eles não podem, e a razão é estrutural** — nenhum elemento no corpus mantém sua
frase constante enquanto a contagem ao redor varia *e* é capaz de estar ausente. O que eles
dão é um limite unilateral, de cinco prompts em uma câmera com controle, máscara e semente idênticos: em uma escala de elementos de **10 → 17**, a contagem removeu **nada** do que estava presente em 10, enquanto uma inversão de identidade em *zero* mudança na contagem moveu o intervalo completo de calibração.
**O cânone do W3 pede 19, e o corpus nunca atinge isso**
([E55](docs/experiments/E55-density-vs-identity-report.md)). O estúdio imprime os três
números que são colapsados — 24 superfícies de prompt, 25 verificações necessárias, 19 elementos exclusivos —, então uma contagem de cobertura nunca é citada em relação a uma medição da contagem de elementos.

## A rota

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

Etapa por etapa, com o raciocínio para cada uma: **[o manual](docs/handbook/index.md)**.

**O salto tracejado é novo e é deliberadamente não sólido.** A primeira caixa da rota sempre
leu *conceito de argila*, e até agora nada aqui o fazia — toda argila chegava manualmente e era hashada no caminho. Uma ferramenta conceito→argila agora existe e seu primeiro par foi percorrido em tamanho real: pose, faixas de pulso, medalhão de cinto e bainha rasgada foram todos carregados; a massa da crina não; vazamento de cor medido em toda a imagem **C\* p99.9 = 13.15** com um fundo acromático perfeito.
**O que esse par não pode mostrar é se a malha retorna melhor**, que é a única pergunta que o promove, então ele permanece como um candidato com sua evidência registrada:
**[preparação do conceito](docs/concept-prep.md)**.

## O que faz funcionar

Seis descobertas, cada uma das quais exigiu um experimento e cada uma das quais pode ser generalizada para além do objeto que a gerou. [A versão completa, com as medições](docs/findings.md).

- **Primeiro a forma, depois o estilo.** Os algoritmos de reconstrução interpretam o ruído superficial como geometria. Uma argila limpa, semelhante a uma escultura, com planos deliberadamente exagerados, resulta em uma topologia melhor do que um sprite estilizado; a versão estilizada é gerada simultaneamente e serve como referência de cor.
- **Defina o contorno do rosto, obtenha um rosto.** Um recorte no formato de busto coloca **3,1–4,5 vezes** mais polígonos na cabeça, e a diferença é estrutural — pálpebras separadas, uma ruga na testa, cavidades nasais modeladas —, não apenas um desfoque mais nítido.
- **Os gêmeos pertencem a uma malha, não a um personagem.** Reutilize um gêmeo em diferentes malhas e a cobertura diminui de **62% para 22,7%**, porque os braços se projetam no espaço vazio ao lado do modelo. Gere gêmeos a partir da malha que você está prestes a texturizar, sempre.
- **A identidade pertence à instrução.** Um elemento canônico não nomeado na instrução está aparecendo por acaso e desaparecerá da mesma forma — medido quando as placas douradas no joelho acabaram atingindo a imagem apenas através do ruído em um ControlNet defeituoso.
- **Consulte a geometria, não um limite.** Substituir uma máscara definida pela silhueta exata do raycast moveu a cobertura de referência de **28,4% para 39,1%** de texels válidos — estritamente aditivo, sem difusão, sem GPU. O método de seleção por mediana nos cantos falhou três vezes aqui e foi descontinuado.
- **Elimine o que nenhuma câmera pode ver, do atlas e nunca da malha.** 49% dos texels do atlas são invisíveis de fora; excluir esses elementos reduz a interpolação em **68%**. Excluir, em vez de apagar, torna a falha impossível, em vez de apenas detectável.

## O que ainda não foi resolvido

Identificado e medido, na página principal, em vez de em uma nota de rodapé. [Todos eles, localizados no código](docs/known-defects.md).

- **Algumas áreas visíveis da superfície são mapeadas para o espaço do atlas, mas nenhuma textura é aplicada**, e renderizadas como o preto padrão original da imagem. O mecanismo de texturização do Blender usa amostragem no centro dos texels, portanto, um triângulo que não se sobrepõe ao centro de nenhum texel permanece vazio — seus próprios desenvolvedores
[deram nome ao mecanismo e implementaram uma correção](https://projects.blender.org/blender/blender/pulls/161752)
duas semanas após a compilação, na qual todos os números aqui foram medidos. É uma propriedade da trajetória,
não de um objeto específico: medido em um ativo, **não medido nos outros quatro**.
- **A faixa da lâmina representa 0,00% da referência do estágio 1** em todas as oito câmeras — o aço sobre um fundo cinza se alinha exatamente com o limite da imagem. A união resgata 55,72%.
- **As bordas das pinceladas não estão niveladas.** Um limite de proveniência apresenta uma variação de textura **5,5 vezes** maior; a região que o Diretor nomeou apresenta uma variação **9,5 vezes** maior.
- **A dilatação se espalha entre ilhas do atlas não relacionadas** — 74,9% dos texels dilatados obtêm sua
cor de outra ilha, com uma mediana de 0,177 em uma figura de altura 1,0. ⚠ **Essa proporção é
em relação aos texels do atlas e não representa o que uma câmera vê**: a dilatação representa 26,95% do
atlas renderizado e **4,95% dos pixels da figura renderizada**, uma proporção de 0,18. As cores estão em grandes
mapas, os buracos estão em mapas pequenos, portanto, um texel dilatado é barato no espaço da tela.
- **⚑ O defeito que determina a aceitação é causado pela pintura, e não por nenhum preenchimento** — regiões
que exibem a cor de outro material, o que nenhuma estatística de manchas pode detectar. Medido de três maneiras em
três sessões em três espaços: **91,05% `reference` presente com um enriquecimento de 0,99**, exatamente na
taxa base; a mesma classe em verde de tecido **68,46% `reference`**; e em uma lâmina fina, os próprios texels pintados da
superfície **18,77%** contaminados em relação aos **5,55%** do preenchimento de dilatação.
O preenchimento é obtido corretamente a partir de seu vizinho pintado mais próximo — e esse vizinho já está
incorreto. A mistura em si é uma divisão não documentada em duas faixas
(`M + gaussian_blur_σ16(B − M)`) que mede o **pior dos quatro** cenários nos mesmos
pontos.
- **As vistas nunca são independentes, o que limita todas as correções de mistura.** Para cada conjunto de defeitos,
**100% das faces com duas ou mais câmeras contribuintes têm todas elas dentro de um intervalo de 90°**
(mediana de 45°) e 21% das faces com defeito são vistas por apenas uma câmera. Vistas adjacentes sob
controle quase idêntico falham juntas, portanto, os ganhos multivista publicados da fotogrametria não se
aplicam aqui diretamente.
- **Cada reconstrução nesta trajetória é uma casca oca de parede dupla**, com paredes de aproximadamente dois
voxels. Nenhum predicado volumétrico é válido em um deles.
- **As placas divergem em limites de materiais não nomeados, e a referência é crucial**
(2026-08-16). A deformação interior gêmea para a malha mediu **3,5–11,1 px na mediana** em todas as
oito vistas em comparação com as medianas da silhueta de 1,2–3,0; cada região residual que o Diretor
circulou — corte da manga, mão, parte superior da bota — é uma junção de material que o prompt de geração
nunca nomeou. ⚠ **CORRIGIDO em 2026-08-17, e a correção reforça a descoberta.** Isso dizia "o prompt registrado contém seis elementos" — medido, ele une dois arquivos diferentes. O fluxo de trabalho que gerou os gêmeos nomeia **16 de 17**, faltando apenas
a empunhadura; o *perfil padrão do pincel* nomeia seis. Ambos são verdadeiros, e a frase fez uma afirmação falsa entre eles. O que permanece e é mais importante: a empunhadura, a manopla, a caneleira e a mão
aparecem **zero** vezes no prompt de 16 frases — porque **nenhum elemento para eles existe na referência**. Um prompt completo ainda não pode nomear uma mão que nunca foi especificada.
✅ **ENCERRADO em 2026-08-17** — a lista de superfícies é percorrida, preenchida e **24/24 ratificadas**, e o portão agora rejeita um prompt que não a cobre.
- **4,65–5,57% dos texels válidos são superfícies que nenhuma câmera com anel plano pode ver** — eles falham
no portão de profundidade em todas as vistas, nenhum caminho de projeção pode pintá-los e o pipeline lançado os preencheu com a inundação cega da ilha que criou as marcas escuras. Eles
precisam de uma política (material neutro, pincel ou aceitação), não de uma correção
([relatório E49](docs/experiments/E49-finish-and-cap-report.md)).
- **Polígonos coloridos planos nas folhas de qualidade aceita** — a única classe aberta do Diretor.
⚠ **A hipótese de preenchimento é FALSIFICADA (2026-08-17).** O preenchimento órfão mede *abaixo*
de sua própria taxa base no defeito (0,27x), os patches estão em 90–99% em texels pintados comuns e o mesmo defeito está presente em uma renderização criada a partir de um atlas que
precede a correção pela qual ele é culpado. Em vez disso, rastreado até sua fonte: o gêmeo da vista de renderização está limpo lá, e uma **vista diferente** possui 97 de 115 pixels com defeito em uma face de 0,68 contra 0,60. O patch angular é um **artefato de dispersão** e a cor é uma discordância real entre as vistas em uma superfície que já foi nomeada — portanto, uma regeneração gêmea não é justificada por "o defeito está nos gêmeos".
⚠ **E a correção que esta página propôs também é FALSIFICADA (2026-08-17).** Dizia *"um compositor que prefere a vista de destino é a correção com escopo e não custa nada."* O
compositor já existia e já era o padrão; medido em relação ao classificador plano em imagens estáticas de uma execução registrada, o primeiro alvo **aumenta** a contagem no
alvo nomeado (38 → 40) e aumenta-o acentuadamente em outros dois (23 → 64, 36 → 110), tornando-se *mais* conectado ao fazê-lo. O mecanismo: **a forma é propriedade, a cor não.**
O verde-oliva é a própria pintura da vista 6 de uma superfície que a vista 6 está pintando corretamente, portanto, no alvo 6 — onde o primeiro alvo significa *preferir a vista 6* — a política maximiza exatamente a pintura da qual o defeito é feito. **Uma política de propriedade não pode corrigir uma discordância de cor entre as vistas em uma superfície atribuída corretamente**, o que desativa a família em vez de apenas um braço dela ([E52](docs/experiments/E52-target-first-flats-ruling.md)). O que resta é uma questão de pintura e custa uma geração. *Texto substituído, mantido de acordo com a regra de correções: "ilhas órfãs do tamanho de triângulos únicos, preenchidas em plano a partir de amostras gêmeas adjacentes à borda retiradas com a silhueta não erodida."*

## Como este repositório é executado

A disciplina é tanto um produto quanto o processo, e existe por uma razão: uma fase anterior realizou dez sessões em que cada uma avaliou seu próprio resultado e escreveu conclusões que foram lidas na sessão seguinte como fatos estabelecidos. Nada naquele ciclo era verificável.

- **Especificação antes do trabalho, relatório depois, decisão final** — e a sessão que projeta um experimento nunca avalia seus próprios resultados. Cinquenta e seis experimentos estão em [o registro](docs/experiments/).
- **As correções são aplicadas no local, ao lado da medição que as refutou**, nunca como exclusões discretas. Seis alegações herdadas foram falsificadas apenas na sessão inicial, e todas as seis ainda podem ser lidas ao lado do que as substituiu.
- **Os erros permanecem no repositório com sua razão.** [`tools/superseded/`](docs/tools.md) não é um arquivo — qualquer pessoa pode executar essas ferramentas e observar que elas falham da mesma forma.
- **Um resultado negativo é um sucesso total**, relatado e encerrado, em vez de ajustado para atingir um número.
- **Os testes acompanham o commit que toca o código** — 1339 aprovados por duas pessoas, com CI baseado em caminhos nos 1285 casos herméticos.
- **O registro é pesquisável.** Um índice SQLite + FTS5 sobre todo o histórico, verificado em quatro etapas. Ele encontrou uma contagem de decisões que a redação havia errado em três locais, contando o próprio registro.

## Onde tudo está

| | |
|---|---|
| **[O manual](docs/handbook/index.md)** | o guia — a rota passo a passo, os tópicos, o sistema de perfil |
| **[Preparação do conceito](docs/concept-prep.md)** | a etapa candidata de modelagem: sua execução da Fase 0, seu posicionamento e o item de licença que ela abre |
| **[O registro](docs/experiments/)** | cinquenta e seis experimentos: especificação, relatório, decisão e cada previsão declarada antes da medição |
| **[O que a rota aprendeu](docs/findings.md)** | as descobertas duradouras e as regras conquistadas com dificuldade, na íntegra |
| **[Status de cada ferramenta](docs/tools.md)** | o que funciona, o que está obsoleto e a evidência para cada um |
| **[Defeitos conhecidos](docs/known-defects.md)** | tudo o que não foi resolvido, medido e localizado no código |
| **[A fase, como aconteceu](docs/arc-history.md)** | o histórico cronológico, com as correções intactas |
| **[CLAUDE.md](CLAUDE.md)** | como trabalhar aqui — os papéis, as regras e o custo de cada um |

## Posição da licença

Cada etapa é executada localmente e com total conformidade comercial: SDXL (OpenRAIL++), MV-Adapter (código aberto), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Excluído deliberadamente, com a razão: **nvdiffrast** (não comercial — imposto aqui por um mecanismo estrutural, não por atestado), **Hunyuan3D-Paint** (licença inválida na UE, Reino Unido e Coreia do Sul), **MVPaint** e **TEXGen** (nenhuma licença) e **UltraSharp / SUPIR / StableSR** (ampliadores não comerciais).

**O limite da alegação, declarado em vez de deixado para ser descoberto.** Ele descreve a **rota registrada** — as etapas no diagrama acima, desde imagem para 3D. A etapa candidata de preparação do modelo, anterior a ela, atualmente é executada em uma API de nuvem fechada cujos termos este repositório **não verificou**, portanto, nenhuma alegação de licença aqui cobre um ativo criado a partir de um de seus modelos. Esse é um item aberto com um caminho nomeado para resolvê-lo: o modelo local com licença correta é **Qwen-Image-Edit (Apache-2.0)** e **FLUX.1-Kontext [dev] é excluído pelos mesmos motivos do nvdiffrast** — pesos não comerciais. Ambos verificados em relação ao catálogo de modelos do estúdio, em vez de relembrados; o raciocínio está em [preparação do conceito](docs/concept-prep.md).

## Modelo de confiança e ameaças

a execução ocorre inteiramente na sua própria máquina — cada ferramenta é um script que você invoca em caminhos que digita, portanto, a pergunta útil não é *quais permissões este aplicativo solicita*, mas *o que esses scripts fazem com sua máquina*. Respondido por meio de medição, com cada varredura executada novamente; a política completa está em [SECURITY.md](SECURITY.md):

- **Dados acessados:** malhas, texturas, imagens e JSON no disco local, nos caminhos que você passa na linha de comando. Além disso, `docs/index/facet.db`, que é *derivado* — ele não contém nada que já não fosse um arquivo neste repositório, e `facet_index.py build` o regenera do zero.
- **Dados NÃO acessados:** nenhuma credencial, nunca. Nada aqui lê, armazena ou transmite um token, chave ou senha, e nenhum está presente na árvore — verificado em busca de chaves com prefixo de provedor, GitHub PATs, tokens Slack, IDs de chave AWS, blocos de chave privada, tokens de portador e atribuições `api_key`/`password` inline, **zero correspondências**, nenhum arquivo com formato de credencial rastreado.
- **Sem telemetria.** Nenhuma coletada, nenhuma enviada. Não há opção de desativar porque não há nada para desativar.
- **Egressão de rede:** duas ferramentas abrem um socket — `restylize_views.py` e `texpass_brush.py` — e ambas chamam uma API HTTP ComfyUI em `--host`, **padrão `127.0.0.1:8188`**. Nada mais em `tools/` faz uma chamada de rede.
- **Permissões:** usuário comum. Sem elevação, sem instalação de serviço, sem gravações de configurações do sistema ou registro.

Três arestas afiadas são reveladas em vez de descartadas, porque uma nota de segurança que apenas lista garantias não é um modelo de ameaça: **as operações de arquivo não estão isoladas** (uma ferramenta grava onde seus argumentos indicam); **caminhos locais absolutos estão incorporados em muitas ferramentas e documentações** — 114 ocorrências em 26 arquivos, não segredos, mas a divulgação do layout de uma máquina e o motivo pelo qual a maioria das ferramentas não funcionará sem modificação em outro lugar; e **falhas inesperadas aparecem como rastreamentos Python nos scripts de pesquisa não publicados**, sem nenhum filtro `--debug`. Interrupções deliberadas são mensagens `ANDON:` que carregam a medição que as acionou. Esse é o contrato do instrumento de pesquisa, e [SHIP_GATE.md](SHIP_GATE.md) registra exatamente quando ele deixa de ser bom — o que aconteceu para os dois comandos da faceta *installs* em 0.2.0: `facet-index` e `facet-mcp` retornam `0` ok / `1` erro do usuário / `2` erro de tempo de execução — e, como [E22](docs/experiments/E22-ruling.md), **`4` REJEITADO** para um filtro acionado ou um ramo com falha `verify`, o que significa que a ferramenta está funcionando e dizendo para não prosseguir, em vez de ser um erro de tempo de execução. Todos eles rejeitam com uma falha estruturada que indica o próximo passo, em vez de um rastreamento ([E21](docs/experiments/E21-cli-contract-report.md)).

**E os filtros nesses dois comandos não são mais excluíveis.** Cada ANDON na faceta *installs* `raise`; um `assert` simples é uma declaração que `python -O` remove silenciosamente, e 87 dos filtros deste repositório podiam ser removidos por uma variável de ambiente até que E22 os convertesse. Medido antes e depois no mesmo filtro, em quatro modos de interpretador.
**E como [E23](docs/experiments/E23-route-gates-report.md), nem os filtros na rota que produziu os quatro ativos aceitos** — seus **57 locais em doze ferramentas**, convertidos como uma simples movimentação de arquivos que nenhum teste jamais executou, cada um agora rejeitando sob `-O` e `PYTHONOPTIMIZE=1`, bem como sob um interpretador normal.
**E como [E25](docs/experiments/E25-ruling.md), a classe está fechada.** Seus **133 locais em 43 arquivos** — os instrumentos de medição que produziram as evidências para os quatro ativos aceitos acima — convertem da mesma forma, elevando o total que `raise` para **278**.
Exatamente **um** ANDON simples `assert` permanece em algum lugar sob `tools/`: `superseded/texpass_thin_mask.py`, que **nunca** é convertido, porque essas ferramentas são mantidas de forma que qualquer pessoa possa executá-las e observar sua falha da mesma maneira. Esse restante é fixado **por nome** no conjunto de testes, para que uma varredura futura não possa removê-lo sem editar o teste intencionalmente.

**Status de suporte:** este repositório é desenvolvido de forma aberta, em um único ambiente, por um diretor e um par rotativo de sessões de consultor e executor. `main` é o único estado suportado. Não há canal de lançamento, política de retrocompatibilidade ou SLA — em vez disso, existe o registro: cada afirmação está ao lado do código que a produz, e [docs/experiments](docs/experiments/) contém as especificações, o relatório e a decisão para cada um.

## Requisitos

Blender 5.x, Python 3.11+ com `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Uma instalação local do ComfyUI é necessária apenas para o pincel de preenchimento. Desenvolvido em um RTX 5090; a capacidade da VRAM é mais importante do que a velocidade bruta.

O CI executa o subconjunto hermético do conjunto de testes em **ubuntu-latest / Python 3.12** com instalações fixas (`.github/workflows/ci.yml`); a camada de artefatos precisa das árvores registradas sob `E:\AI\training`, que não estão no git, portanto, o CI as desativa por design. Localmente, `python -m pytest` executa todos os **1339** testes e `python -m pytest -m "not artifacts"` executa os **1285** testes reproduzidos pelo CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
