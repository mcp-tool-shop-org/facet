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

O estilo é aplicado **no ativo**, no espaço da textura — não é aplicado em cada visualização e, posteriormente, combinado. Forneça à rota um conceito de argila com formas exageradas e ela retornará uma malha texturizada cuja cor foi obtida de uma referência estilizada *dessa* malha, com tudo o que a referência não podia ver preenchido por um pincel de preenchimento com máscara e uma dilatação que considera a superfície.

Nomeado para representar as duas partes do problema: os polígonos e a face que eles devem representar.

## Instalar

A própria rota é um conjunto de scripts locais que você executa em caminhos que você digita — clone o repositório e leia [introdução](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Dois servidores são fornecidos como um pacote** — o índice de registro, para que um assistente possa consultar o histórico de evidências em vez de lê-lo, e, **a partir da versão 0.4.0, o servidor de medição**, para que dois ativos medidos com meses de diferença passem por um único caminho de código.

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` é o servidor MCP stdio sobre o registro (seis ferramentas, com a verificação de quatro pontos como uma superfície de saúde que rejeita) e `facet-index` é o próprio índice (`build` / `verify` / `q` / `claims`). Execute qualquer um deles dentro de um diretório de checkout; `--db` nomeia um índice diferente.

### O servidor de medição — novo na versão 0.4.0

`facet-measure` responde à **metade numérica** de uma comparação e nunca diz se a saída é boa. Cada carga útil contém a versão do servidor, o hash do arquivo do instrumento e um hash de configuração, e `measure_report` **rejeita** comparar em caso de incompatibilidade — que é a propriedade para a qual todo o sistema existe.

Verificado executando um **verbo** em vez de `--help` — uma malha de controle retorna 786.432 faces com um envelope de identidade completo em uma máquina que não tem nenhum diretório de checkout.

**O que você obtém depende de uma coisa, e é a sua versão do Python:**

| seu Python | `[measure-full]` oferece |
|---|---|
| **3.11 / 3.12** | **todas as oito ferramentas** — `open3d` instala a partir do PyPI |
| **3.13** | quatro ferramentas; `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 é a última *versão* e publica pacotes cp38–cp312 com **nenhum sdist**, portanto, na versão 3.13, não há nada no PyPI para instalar. O pacote extra o inclui junto com `python_version < "3.13"`, para que a instalação **tenha sucesso** e as quatro ferramentas de geometria retornem **`4` REJEITADO**, indicando o que precisam — em vez de a instalação inteira falhar.

**Para obter todas as oito ferramentas no Python 3.13**, o Open3D publica os pacotes cp313 atuais em seu canal de desenvolvimento contínuo. Uma URL direta é válida na linha de comando; ela só é proibida dentro dos metadados do pacote publicado:

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **No Windows e macOS, os pacotes de desenvolvimento são sufixados com `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` no momento da redação) e o nome muda à medida que `main` muda — liste os ativos no [lançamento `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) e pegue o mais recente. **Essa versão é a que os números dependentes do open3d desta rota foram medidos**, e é uma verdadeira barreira de comparabilidade: o envelope de identidade registra o hash do instrumento, não suas dependências — [E31](docs/experiments/E31-ruling.md).

*Até a versão 0.3.1, o pacote continha dois arquivos `.py` e nenhum dos instrumentos de medição, portanto, um servidor de medição instalado não tinha nada para executar. Ninguém percebeu por quatro versões porque este repositório É o diretório de checkout: a ferramenta funcionava onde era construída e nunca esteve em outro lugar.*

⚠ **`pip install facet-mcp` estava com defeito em todas as versões lançadas até a versão 0.3.0 e foi corrigido na versão 0.3.1.** O pacote instala `facet_index` como um módulo de nível superior, portanto, até e incluindo a versão 0.3.0, ele resolvia o local do registro em relação a `<venv>/Lib` — que não contém nenhum corpus nem índice — e `build`, `claims` e `q`, todos falhavam sem `--db`.
**Na versão 0.3.0 ou anterior, use o binário `npx` acima.**

A partir da versão 0.3.1, a raiz é resolvida **testando o registro** em vez de presumir que ele existe: execute qualquer um dos comandos dentro de um diretório de checkout e ele o encontrará; execute-o de qualquer outro lugar e ele retornará **`4` REJEITADO**, indicando os dois diretórios que tentou e os dois marcadores que procurou. `$FACET_INDEX_DB` agora é lido por ambos os comandos e ele seleciona qual *índice*, nunca qual *corpus*. Medido em um pacote construído a partir de `main` e instalado em um ambiente virtual limpo — [E24](docs/experiments/E24-ruling.md).

*Este bloco foi corrigido duas vezes. Primeiro, dizia `pipx install facet-mcp # ou o pacote Python diretamente `, until v0.3.0's read-back ran a **verb** instead of ` --help`.
Em seguida, dizia que o pacote "só funciona para `q` e `claims`" — **`claims` também não funcionou**, o que E24 descobriu ao executá-lo. Ambas as correções estão em [known-defects.md](docs/known-defects.md) com suas medições.*

## Situação atual

**Quatro ativos aceitos, em quatro classes de assunto, com custo zero.** Cada um foi avaliado pelo Diretor em seu próprio zoom — no arquivo GLB ou em planilhas em tamanho real — e não por uma métrica que atinja um limite.

| assunto | classe | aceito | referência / pincel / dilatação |
|---|---|---|---|
| **Character (W3)** | humanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | veículo, rigging fino | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | animal, membranas das asas | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | adereço, quase 2D, cinza sobre cinza | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

As ações são de texels válidos e **não são comparáveis entre os assuntos** — uma nave esconde a maior parte de si mesma do nível dos olhos e um animal esconde metade. Avalie cada um em relação ao seu próprio limite de alcance pré-registrado, em relação ao qual eles atingem **86–93%**: a diferença entre as linhas é a geometria, não a regressão. [Números completos, com seus denominadores](docs/handbook/subjects.md).

**Um quinto objeto está no meio do processo e é a primeira referência construída
(2026-08-17 → 2026-08-19).** A1, "o arquivista", foi iniciado a partir de uma referência que continha
sua própria receita embutida, em vez de um conceito em argila, e cada etapa desde então foi
baseada nisso: o cânone foi ratificado em **16/16 superfícies** antes que uma malha existisse,
uma malha aprovada pelo Diretor, um local que reproduziu a referência **pixel a pixel, três vezes**,
um conjunto de oito vistas com um manifesto sha256 e duas falhas de contaminação nomeadas,
cada uma medida em um mecanismo antes que qualquer coisa fosse alterada. O processo foi aprovado
[2026-08-19](docs/experiments/E70-baked-look-report.md) — **com base na identidade e no conjunto de
roupas, e esse é todo o escopo dessa aprovação.**

**Em seguida, o pincel se abriu e começou a preencher apenas os espaços vazios.** O primeiro traço
atingiu um ângulo de 90 graus em 2026-08-19: a invariância ANDON registrou **0,014 lv com o
maior componente quente de 0 px** fora da figura, em 472.318 px testados, e `commit` escreveu
**3.585 texels**, preenchendo os espaços **2.044.423 → 2.040.838**, com o atlas de origem
reverificado, byte a byte, posteriormente. No zoom do Diretor, o triângulo pálido na gola do colete
tornou-se cor de ameixa e a costura parece ser uma única peça de roupa. Não criou um rosto, não
virou a cabeça nem pintou um segundo colete.

**O resultado metodológico é mais importante do que o ativo.** Ao longo de todo esse processo, a
força do ControlNet nunca foi alterada — cada correção **removeu uma causa** em vez de aplicar
força contra ela. Duas das falhas foram defeitos nas especificações do consultor, detectados pelos
executores e por um canal de revisão externo antes que um crédito fosse gasto, e ambos estão
nomeados no registro com a medição que os invalidou.

**É um pipeline, não um gerador de um único caractere.** Contradiga a especificação em oito
elementos nomeados e o prompt vence **8 de 8** — a mediana ΔE é de 46,3, em comparação com 6,2
em cinco controles mantidos — enquanto a figura permanece a mesma. A estrutura é mantida pela
malha e pelo controle; os atributos nomeados são aplicados ao prompt.

**A questão do projetor foi encerrada em 2026-08-16** ([E45](docs/experiments/E45-warp-and-aov-kickoff.md)–[E49](docs/experiments/E49-finish-and-cap-kickoff.md)).
As oito placas **compõem**: reconstruídas a partir do conjunto por vista, sob os pesos de borda ×
orientação × visibilidade, as renderizações do atlas superaram a barra de aceitação do Diretor pela
primeira vez nesta rota — duas vezes, em duas etapas — ao lado de um atlas enviado cuja rota
estava destruindo a pintura, mas as placas concordam. A cadeia que fez isso está em `tools/`
(`emit_view_aovs`, `s3_composite`, `flow_estimate`, `s3_run`, `s3_sheet`,
`atlas_from_aovs`, `twin_mesh_warp`), construída em grande parte por meio de um canal de revisão externo, cujas alegações de
calibração nomeadas foram mantidas **vinte para vinte**, cada uma verificada aqui, executando-a
antes que qualquer coisa confiasse na construção.

**O cânone é um dado e ele controla o gasto (2026-08-17).** A especificação de identidade nomeou
dezessete elementos; o fluxo de trabalho que gerou os gêmeos nomeou dezesseis; o perfil padrão,
uma nova execução usaria seis. Nada os conectava, então quatro etapas corrigiram a composição
posteriormente, em relação à pintura que estava errada na fonte. O cânone agora é um banco de
dados, com chave em **superfície** — uma lista de elementos não pode mostrar o que está faltando,
e um ocupante anulável torna um espaço vazio uma linha — e `canon_gate` é executado **dentro** das
ferramentas que criam uma geração, antes que o diretório de saída exista. Uma geração cujo prompt
não cobre o cânone ratificado é rejeitada e nada é escrito.

**É um roteador e ele é configurado para falhar com segurança.** Ele resolve um objeto para seu
arquivo de cânone, cobre um prompt em **ambas** as direções e carrega um escopo. **Uma ferramenta
que cria um gasto e não recebe um cânone não prossegue silenciosamente — ela se recusa.** A
solução para um objeto que genuinamente não tem nenhum é baseada em dados e não pode ser usada
por um objeto que tem: `--no-canon --subject GALLEON` prossegue e se anuncia; `--no-canon --subject W3` é
**rejeitado**, porque W3 tem superfícies. Isso fecha a caixa de seleção por construção, e não por
convenção, e isso é importante porque a forma anterior — `if args.canon:` — permitiu que o driver PowerShell
enviado passasse pelo portão em silêncio.

**A segunda direção é aquela que detecta um defeito real.** Verificar se o prompt *contém* o cânone
encontra um prompt fraco. Verificar se tudo no prompt *é* cânone encontra uma frase que nomeia
algo que o personagem não tem — e havia uma no padrão ativo: **`gold necklace`**, que este repositório já havia
medido como nomeando incorretamente o medalhão de cinto dourado, *"e o elemento sobrevive por
acaso."* Um prompt abrangente com essa frase anexada agora retorna `missing: 0` e se recusa de qualquer
forma, nomeando a cláusula.

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

`prof_hit 5/19` é um **espécime deixado deliberadamente quebrado**: é o padrão ativo que uma execução realmente
usaria, então o primeiro `--profile character.json` deve parar. Reparar a string excluiria a evidência.

**E há uma planilha, porque os quatro objetos sem cânone não vão se mover sozinhos.** Ela emite
cada superfície que o *tipo* de um objeto implica — então um espaço vazio é uma linha antes que
alguém o nomeie — transforma um arquivo IDENTITY.md em um inventário, carrega junções como pares
para confirmar e reserva espaços de escopo por vista. É **estruturalmente incapaz de preencher um
ocupante**, e essa é a propriedade que é testada: uma frase venenosa que chega com uma superfície
já atribuída não é escrita. Gerar um cânone é um humano seguindo uma referência; a planilha apenas
torna o processo mais barato e completo.

**O limite da cena, definido em vez de deixado para ser descoberto.** Ele verifica as frases do cânone aprovado em ambas as direções, dentro de um determinado escopo. Ele **não** verifica paráfrases ou sinônimos — a correspondência semântica colocaria um modelo dentro de um limite, o que este repositório rejeita por princípio — nem elementos por cena até que um escopo de cena seja declarado, nem se um material nomeado foi aplicado na superfície *correta*. Os espaços de escopo existem e suas listas de superfície estão vazias: preenchê-los é uma tarefa manual, assim como preencher os ocupantes. Quatro objetos têm um arquivo IDENTITY.md e nenhum arquivo JSON de superfície — deixado inacabado em vez de gerado sem percorrer a referência.

**É medido quantos elementos um prompt pode conter, e não atinge o cânone.** A literatura define o preço de cada elemento de prompt adicionado, com um custo para a possibilidade de os elementos aparecerem, em uma faixa muito abaixo da nossa, então um pedido do Opus perguntou se as imagens já pagas poderiam resolver isso. **Não podem, e a razão é estrutural** — nenhum elemento no corpus mantém sua frase constante enquanto a contagem ao seu redor varia *e* pode estar ausente. O que eles fornecem é um limite unilateral, de cinco prompts em uma câmera com controle, máscara e semente idênticos: em uma escala de elementos de **10 → 17**, a contagem removida **não** inclui nada que estivesse presente em 10, enquanto uma mudança de identidade em *zero* alterou o intervalo total de calibração. **O cânone do W3 pede 19, e o corpus nunca atinge esse valor** ([E55](docs/experiments/E55-density-vs-identity-report.md)). O estúdio imprime os três números que são combinados — 24 superfícies de prompt, 25 verificações necessárias, 19 elementos exclusivos — então, uma contagem de cobertura nunca é citada em relação a uma medição da contagem de elementos.

**Um sexto objeto foi usado para responder a uma pergunta diferente e retornou um resultado negativo (2026-09-22).** Um protetor de cena para `ai-rpg-stage` foi reconstruído para testar o que acontece *após* a aplicação da textura — poses e adereços — e ele é reconstruído corretamente e, em seguida, **falha no auto-rigging.** Quatro causas potenciais foram eliminadas por meio de medição, em vez de argumentação: entrada sem textura, contagem de componentes, topologia da malha e a pose. **O discriminador não foi identificado**, e [`canon/BASE-FIGURE.md`](canon/BASE-FIGURE.md) contém a tabela do que foi testado, embora se recuse a nomear uma causa — porque a única causa que este repositório nomeou, a separação do braço do torso, foi refutada dentro da mesma hora por uma pose A verdadeira que falhou em uma separação *maior* do que uma pose que foi aprovada.

**O resultado é um contrato de tamanho e duas cenas.** Cada reconstrução que este processo realiza retorna normalizada para **1,002 em seu eixo mais longo** — medido em quatro ativos não relacionados, com três casas decimais — então, uma malha de adereço não tem uma escala real e um escudo de aquecedor carregado como está é uma porta de 1,8 m. O tamanho real de um adereço agora é declarado uma vez em milímetros, armazenado ao lado do arquivo e verificado em vez de confiado (`tools/prop_scale.py`, unidade da cena **1,0 = 1,8 m**). Um adereço que *toca* uma figura em um vértice não é mantido, então a cena de contato relata uma distância mínima **e uma área de contato** (`tools/verify/prop_contact.py`) — o ativo que o provocou tocou em 0,00072 em 97 pontos de 624.510 e claramente não estava sendo segurado. E o resultado de um auto-rig agora é lido em vez de presumido: `tools/verify/rig_report.py` lista as articulações, compara a malha como um *conjunto* em vez de uma contagem e diz se o skinning está presente.

**Uma mão com seis dedos alcançou uma imagem aceita após passar por quatro cenas que não conseguiam ver mãos.** O Diretor a encontrou olhando. A cláusula 7 do cânone — cinco dedos por mão — existe porque a cláusula 2 a causou, e as mãos agora são um item de aceitação em seu zoom, em vez de algo sobre o qual as métricas ficavam em silêncio.

## O processo

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

Etapa por etapa, com a justificativa para cada uma: **[o manual](docs/handbook/index.md)**.

**O salto tracejado é novo e é deliberadamente não sólido.** A primeira caixa do processo sempre leu *conceito de argila*, e até agora nada aqui o produzia — cada argila chegava manualmente e era processada no caminho. Agora existe uma ferramenta de conceito→argila e seu primeiro par foi testado em tamanho real: pose, braceletes de pulso, medalhão de cinto e bainha rasgada foram incluídos; a massa da crina não; o vazamento de cor medido em todo o quadro **C\* p99,9 = 13,15** com um fundo acromático perfeito. **O que esse par não pode mostrar é se a malha retorna melhor**, que é a única questão que o promove, então ele permanece como um candidato com sua evidência registrada: **[preparação do conceito](docs/concept-prep.md)**.

## O que faz funcionar

Seis descobertas, cada uma das quais exigiu um experimento e cada uma das quais se generaliza além do objeto que a produziu. [A versão completa, com as
medições](docs/findings.md).

- **Primeiro a forma, depois o estilo.** Os algoritmos de reconstrução interpretam o ruído da superfície como geometria. Uma argila limpa, semelhante a uma escultura, com planos deliberadamente exagerados, resulta numa topologia melhor do que um sprite estilizado; o modelo estilizado é gerado em paralelo e serve como referência de cor.
- **Defina o contorno do rosto, obtenha um rosto.** Um recorte em forma de busto coloca **3,1–4,5 vezes** mais polígonos na cabeça, e a diferença é estrutural — pálpebras separadas, uma ruga na testa, cavidades nasais modeladas — e não apenas um desfoque mais acentuado.
- **Os modelos gêmeos pertencem a uma malha, não a um personagem.** Reutilize um modelo gêmeo em várias malhas e a cobertura diminui de **62% para 22,7%**, porque os braços se projetam no espaço vazio ao lado do modelo. Gere modelos gêmeos a partir da malha que você está prestes a texturizar, sempre.
- **A identidade pertence ao prompt.** Um elemento canônico não nomeado no prompt está surgindo por acidente e desaparecerá da mesma forma — medido quando as placas douradas dos joelhos acabaram aparecendo na imagem apenas através do ruído em um ControlNet defeituoso.
- **Consulte a geometria, não um limite.** Substituir uma máscara com o contorno exato do raycast moveu a cobertura de referência de **28,4% para 39,1%** de texels válidos — estritamente aditivo, sem difusão, sem GPU. O método de seleção de contorno por mediana falhou **quatro** vezes aqui e foi descontinuado — um gradiente pintado, uma renderização de argila em tons de cinza, o fundo de estúdio iluminado de um modelo de difusão e uma referência de difusão cujos próprios cantos abrangem L\* 48,1–81,1. ⚠ A forma ainda está presente em um dos produtos, `tools/verify/gate_mesh.py`, que amostra um único canto: nomeado aqui em vez de usado silenciosamente.
- **Elimine o que nenhuma câmera pode ver, do atlas e nunca da malha.** 49% dos texels do atlas são invisíveis de fora; excluir esses elementos reduz a interpolação em **68%**. Excluir em vez de apagar torna a falha impossível, em vez de apenas detectável.

## O que não foi resolvido

Nomeado e medido, na página principal em vez de em uma nota de rodapé. [Todos eles, localizados no código](docs/known-defects.md).

- **Algumas áreas visíveis da superfície são mapeadas para o espaço do atlas, mas nenhuma delas é escrita durante o processo de "bake"**, e são renderizadas como o preto padrão original da imagem. O "baker" do Blender usa amostragem do centro do texel, portanto, um triângulo que não se sobrepõe ao centro de nenhum texel permanece vazio — seus próprios desenvolvedores
[deram um nome ao mecanismo e implementaram uma correção](https://projects.blender.org/blender/blender/pulls/161752)
duas semanas após a versão em que todos os números aqui foram medidos. É uma propriedade da trajetória,
não de um objeto específico: medido em um ativo, **não medido nos outros quatro**.
- **A faixa da lâmina representa 0,00% da referência do estágio 1** em todas as oito câmeras — o aço em um fundo cinza está exatamente no limite do objeto. A união resgata 55,72%.
- **As bordas dos traços não estão niveladas.** Um limite de proveniência apresenta uma variação de textura **5,5 vezes** maior; a região que o Diretor nomeou apresenta uma variação **9,5 vezes** maior.
- **A dilatação se espalha entre ilhas do atlas não relacionadas** — 74,9% dos texels dilatados obtêm sua
cor de outra ilha, com uma mediana de 0,177 de distância em uma figura com altura de 1,0. ⚠ **Essa proporção está
nos texels do atlas e não é uma afirmação sobre o que uma câmera vê**: a dilatação representa 26,95% do
atlas renderizado e **4,95% dos pixels da figura renderizada**, uma proporção de 0,18. A pintura existe em grandes
gráficos, os buracos existem em pequenos, portanto, um texel dilatado é barato no espaço da tela.
- **⚑ O defeito que determina a aceitação é causado pela pintura, e não por nenhum preenchimento** — regiões
que exibem a cor de outro material, o que nenhuma estatística de manchas pode detectar. Medido de três maneiras por
três sessões em três espaços: **91,05% `reference`, com um enriquecimento de 0,99**, exatamente na
taxa base; a mesma classe em verde de tecido **68,46% `reference`**; e em uma fina lâmina, os próprios texels pintados da
superfície **18,77%** contaminados em relação aos **5,55%** do preenchimento de dilatação.
O preenchimento é obtido corretamente de seu vizinho pintado mais próximo — e esse vizinho já
está incorreto. A própria mistura é uma divisão de duas faixas não documentada
(`M + gaussian_blur_σ16(B − M)`) que mede **o pior de quatro** alternativas nos mesmos
pontos.
- **⚑ Uma face pintada apresenta faixas, e é a descoberta de propriedade acima que leva à
aceitação de um ativo.** A face gêmea de A1 é uma única camada contínua; o "bake" é dividido em faixas
verticais de diferentes tons de pêssego. `project_twins` é **o vencedor leva tudo** — uma câmera vence cada
texel de forma definitiva, com base no peso da face, na propriedade em vez da média — e a face é vista pela
vista frontal e pelas duas vistas de 45°, que **discordam em relação ao valor da pele em R 13,0 / G 13,9
/ B 18,3** ao longo do anel aceito. Onde dois gráficos UV na face pertencem
a câmeras diferentes, a discordância se manifesta como uma etapa acentuada, portanto, **as faixas são limites de ilha, não sujeira** — e também não são a classe do buraco cinza. **O pincel estruturalmente
não pode corrigi-lo**: `commit` escreve apenas nos texels de buraco e os texels estilizados estão congelados. Duas
soluções são nomeadas e nenhuma é adotada — deixe a vista frontal possuir toda a faixa da cabeça ou uma mistura de bordas
**permitida para reescrever a pele estilizada**, o que nenhuma etapa nesta trajetória pode fazer atualmente.
A média ponderada já está acumulada na ferramenta e o atlas misturado já existe
no disco; ninguém o colocou à frente do Diretor. **Isso estava presente na folha da qual o "bake"
foi aprovado**, e a aprovação cobriu a identidade e o conjunto de roupas — um defeito aberto em um artefato aceito não é uma contradição, mas o registro não deve indicar que uma aprovação cobre uma propriedade que ninguém avaliou.
- **As vistas nunca são independentes, o que limita todas as correções de mistura.** Para cada conjunto de defeitos,
**100% das faces com duas ou mais câmeras contribuintes têm todas elas dentro de um intervalo de 90°**
(mediana de 45°), e 21% das faces com defeitos são vistas por apenas uma câmera. Vistas adjacentes sob
controle quase idêntico falham juntas, portanto, os ganhos de várias vistas publicados da fotogrametria não
se transferem aqui em valor nominal.
- **Cada reconstrução nesta trajetória é uma casca oca de parede dupla**, com paredes de cerca de
dois voxels. Nenhum predicado volumétrico é válido em um deles.
- **As placas discordam em limites de materiais não nomeados, e o cânone é o ponto crucial**
(2026-08-16). A deformação interior para a malha medida apresentou uma **mediana de 3,5 a 11,1 px** em todas
as oito vistas em relação às medianas de silhueta de 1,2 a 3,0; cada região de resíduo que o Diretor circulou — corte da manga, mão, parte superior da bota — é uma junção de material que o prompt de geração
nunca nomeou. ⚠ **CORRIGIDO em 2026-08-17, e a correção aprimora a descoberta.** Isso
dizia "o prompt registrado contém seis elementos" — medido, ele une dois arquivos diferentes. O fluxo de trabalho que gerou os gêmeos nomeia **16 de 17**, faltando apenas
a empunhadura; o *perfil padrão do pincel* nomeia seis. Ambos são verdadeiros, e a frase fez uma
afirmação falsa entre eles. O que permanece e é mais importante: a empunhadura, a manopla, a caneleira e a mão
aparecem **zero** vezes no prompt de 16 frases — porque **nenhum elemento para eles existe
no cânone**. Um prompt completo ainda não pode nomear uma mão que nunca foi especificada.
✅ **FECHADO em 2026-08-17** — a lista de superfícies é percorrida, preenchida e **24/24 ratificadas**, e
o portão agora rejeita um prompt que não a cobre.
- **4,65–5,57% dos texels válidos são superfícies que nenhuma câmera de anel plano pode ver** — eles falham
no portão de profundidade em todas as vistas, nenhuma rota de projeção pode pintá-los e o pipeline lançado os preencheu com a inundação cega da ilha que criou as marcas escuras. Eles
precisam de uma política (material neutro, pincel ou aceitação), não de uma correção
([relatório E49](docs/experiments/E49-finish-and-cap-report.md)).
- **Polígonos coloridos planos nas folhas de grau aceito** — a única classe aberta do Diretor.
⚠ **A hipótese de preenchimento é FALSIFICADA (2026-08-17).** O preenchimento órfão mede *abaixo*
de sua própria taxa base no defeito (0,27x), os patches estão localizados em 90–99% dos texels pintados comuns e o defeito idêntico está presente em uma renderização construída a partir de um atlas que
precede a correção pela qual ele é culpado. Em vez disso, rastreado até sua fonte: o gêmeo da vista de renderização está limpo lá, e uma **vista diferente** possui 97 de 115 pixels de defeito em uma face de 0,68 em relação a 0,60. O patch angular é um **artefato de dispersão** e a cor é uma discordância real entre as vistas em uma superfície que já foi nomeada — portanto, uma regeneração do gêmeo não é justificada por "o defeito está nos gêmeos".
⚠ **E a correção que esta página propôs também é FALSIFICADA (2026-08-17).** Dizia *"um
compositor que prefere a vista de destino é a correção de escopo e não custa nada."* O
compositor já existia e já era o padrão; medido em relação ao classificador plano em imagens estáticas de uma execução registrada, o primeiro destino **aumenta** a contagem no
destino nomeado (38 → 40) e a aumenta acentuadamente em outros dois (23 → 64, 36 → 110), tornando-se
*mais* conectado ao fazê-lo. O mecanismo: **a forma é propriedade, a cor não é.**
O azeitona é a própria pintura da vista 6 de uma superfície que a vista 6 está pintando corretamente, portanto, no destino 6 — onde o primeiro destino significa *preferir a vista 6* — a política maximiza exatamente a pintura da qual o
defeito é feito. **Uma política de propriedade não pode corrigir uma discordância de cor entre as vistas em uma superfície atribuída corretamente**, o que desativa a família em vez de apenas um braço dela
([E52](docs/experiments/E52-target-first-flats-ruling.md)). O que resta é uma questão de pintura e custa uma geração. *Texto substituído, mantido de acordo com a regra de correções:
"ilhas órfãs do tamanho de triângulos únicos, preenchidas de forma plana a partir de amostras gêmeas adjacentes à borda, obtidas com a silhueta não erodida."*

- **Uma reconstrução que não aplicará o "auto-rig", sem nenhum discriminador conhecido.** Um dos seis
objetos é reconstruído corretamente e falha na aplicação do "auto-rig". Entrada sem textura, contagem de componentes,
topologia da malha e a pose são eliminados individualmente por meio de medição — e a causa pela qual este repositório
*afirmou* ter sido falsificada na mesma hora, portanto, a tabela permanece sem uma. Posicionar um "rig"
que realmente existe tem um limite medido em vez de uma correção: aproximadamente 20 graus de rotação do braço
permanecem estáveis, aproximadamente 110 graus danificam os ombros e a ligação rígida da placa
[não a corrige](docs/tools.md) — todas as três tentativas de correção foram medidas e todas
as três falharam.
- **Nenhum acessório foi montado e aceito.** O contrato de tamanho e o "gate" de contato existem
e são testados em relação a malhas sintéticas em uma separação conhecida. Nada foi colocado
em uma mão e avaliado no "zoom" do Diretor, e até que isso aconteça, o "gate" é um
instrumento sem "scalp" em um ativo real.

## Como este repositório é executado

A disciplina é tão importante quanto o produto e o fluxo de trabalho, e existe por um motivo: um
ciclo anterior executou dez sessões, cada uma das quais avaliou seu próprio resultado e escreveu conclusões que
a sessão seguinte leu como um fato estabelecido. Nada naquele ciclo era verificável.

- **Especificação antes do trabalho, relatório depois, decisão final** — e a sessão que projeta um
experimento nunca avalia seus próprios resultados. Setenta e três experimentos estão em
[registro](docs/experiments/).
- **As correções são aplicadas no local, ao lado da medição que as refutou**, nunca como
exclusões silenciosas. Seis alegações herdadas foram falsificadas na sessão inicial, e
todas as seis ainda podem ser lidas ao lado do que as substituiu.
- **As falhas permanecem no repositório com sua razão.** [`tools/superseded/`](docs/tools.md)
não é um arquivo — qualquer pessoa pode executar essas ferramentas e observar que elas falham da mesma maneira.
- **Um resultado negativo é um sucesso total**, relatado e encerrado, em vez de ajustado para um
número.
- **Os testes acompanham o "commit" que toca o código** — 1376 aprovados em duas etapas, com
CI com restrições de caminho nos 1319 casos herméticos.
- **O registro é pesquisável.** Um índice SQLite + FTS5 em todo o histórico, verificado em
quatro etapas. Ele encontrou uma contagem de decisões que o texto havia errado em três locais, contando
o próprio registro.

## Onde tudo está

| | |
|---|---|
| **[O manual](docs/handbook/index.md)** | o guia — a rota passo a passo, os objetos, o sistema de perfil |
| **[Acessórios e "rigs"](docs/handbook/props-and-rigs.md)** | a etapa após a pintura: o objeto que não aplicará o "auto-rig" e os dois contratos que tornam um acessório um acessório |
| **[Preparação do conceito](docs/concept-prep.md)** | o "hop" de argila candidato: sua caminhada no "Gate 0", seu posicionamento e o item de licença que ele abre |
| **[O registro](docs/experiments/)** | setenta e três experimentos: especificação, relatório, decisão e cada previsão declarada antes da medição |
| **[O que a rota aprendeu](docs/findings.md)** | as descobertas duradouras e as regras conquistadas com dificuldade, na íntegra |
| **[Status de cada ferramenta](docs/tools.md)** | o que funciona, o que está obsoleto e as evidências para cada um |
| **[Defeitos conhecidos](docs/known-defects.md)** | tudo o que não foi resolvido, medido e localizado no código |
| **[O ciclo, como aconteceu](docs/arc-history.md)** | o histórico cronológico, com as correções intactas |
| **[CLAUDE.md](CLAUDE.md)** | como trabalhar aqui — os papéis, as regras e o custo de cada um |

## Posição da licença

Cada etapa é executada localmente e é comercialmente limpa: SDXL (OpenRAIL++), MV-Adapter (aberto),
open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy,
trimesh.

Deliberadamente excluído, com a razão: **nvdiffrast** (não comercial — imposto aqui
por um gatilho estrutural, não por atestado), **Hunyuan3D-Paint** (licença inválida na
UE, Reino Unido e Coreia do Sul), **MVPaint** e **TEXGen** (nenhuma licença) e
**UltraSharp / SUPIR / StableSR** (ampliadores não comerciais).

**O limite da alegação, declarado em vez de deixado para ser descoberto.** Ele descreve o
**ciclo registrado** — as etapas no diagrama acima, desde a imagem para 3D. O
"hop" de preparação de argila candidato, a montante, atualmente é executado em uma API de nuvem fechada cujos termos
este repositório **não verificou**, portanto, nenhuma alegação de licença aqui cobre um ativo feito de uma de
suas argilas. Esse é um item aberto com um caminho nomeado para fechá-lo: o modelo local com licença correta é
**Qwen-Image-Edit (Apache-2.0)**, e **FLUX.1-Kontext [dev] é excluído pelos mesmos motivos de nvdiffrast** — pesos não comerciais. Ambos verificados em relação ao catálogo de modelos do estúdio, em vez de recuperados; o raciocínio está em
[preparação do conceito](docs/concept-prep.md).

## Modelo de confiança e ameaças

o facet é executado inteiramente em sua própria máquina — cada ferramenta é um script que você invoca em relação a
caminhos que você digita, portanto, a pergunta útil não é *quais permissões este aplicativo solicita*, mas
*o que esses scripts fazem com sua máquina*. Respondido por meio de medição, com cada varredura executável novamente; a política completa está em [SECURITY.md](SECURITY.md):

- **Dados afetados:** malhas, texturas, imagens e arquivos JSON no disco local, nos caminhos que você
especifica na linha de comando. Além disso, `docs/index/facet.db`, que é *derivado* — não contém nada que já não fosse um arquivo neste repositório, e `facet_index.py build`
o regenera do zero.
- **Dados NÃO afetados:** nenhum dado de credencial, em momento algum. Nada aqui lê, armazena ou transmite
um token, chave ou senha, e nenhum está presente na árvore — foi feita uma varredura para
detectar chaves com prefixo de provedor, GitHub PATs, tokens do Slack, IDs de chave AWS, blocos de chave privada,
tokens de portador e atribuições `api_key`/`password` embutidas, **zero correspondências**, nenhum arquivo com formato de credencial rastreado.
- **Sem telemetria.** Nenhum dado coletado, nenhum dado enviado. Não há opção de desativar, porque não há nada para desativar.
- **Tráfego de rede:** duas ferramentas abrem um socket — `restylize_views.py`
e `texpass_brush.py` — e ambas chamam uma API HTTP do ComfyUI em `--host`, **padrão
`127.0.0.1:8188`**. Nada mais em `tools/` faz uma chamada de rede.
- **Permissões:** usuário comum. Sem elevação de privilégios, sem instalação de serviço, sem alterações nas configurações do sistema
ou no registro.

Três pontos críticos são revelados em vez de serem omitidos, porque uma nota de segurança que
apenas lista garantias não é um modelo de ameaças: **as operações de arquivo não são executadas em um ambiente isolado**
(uma ferramenta grava onde seus argumentos indicam); **caminhos locais absolutos estão embutidos em muitas
ferramentas e documentações** — 114 ocorrências em 26 arquivos, não são segredos, mas uma divulgação do layout de uma
máquina, e a razão pela qual a maioria das ferramentas não será executada sem modificações em outro lugar; e
**falhas inesperadas aparecem como rastreamentos do Python nos scripts de pesquisa não publicados**, sem nenhuma proteção `--debug`. As interrupções deliberadas são mensagens `ANDON:` que carregam a
medição que as acionou. Esse é o contrato do instrumento de pesquisa, e
[SHIP_GATE.md](SHIP_GATE.md) registra exatamente quando ele deixa de ser bom o suficiente — o que, para as duas facetas de comando *instala*, ocorreu em 0.2.0: `facet-index` e `facet-mcp` retornam
`0` ok / `1` erro de usuário / `2` erro de tempo de execução — e, desde
[E22](docs/experiments/E22-ruling.md), **`4` REJEITADO** para uma proteção acionada ou um `verify` com falha, o que significa que a ferramenta está funcionando e informando que você não deve prosseguir, em vez de um
erro de tempo de execução. Todas elas rejeitam com uma falha estruturada que nomeia o próximo passo em vez de um rastreamento ([E21](docs/experiments/E21-cli-contract-report.md)).

**E as proteções nesses dois comandos não são mais exclusíveis.** Cada ANDON no que instala `raise`; um `assert` simples é uma declaração de que `python -O` remove silenciosamente,
e 87 das proteções deste repositório podiam ser removidas por uma variável de ambiente até que E22 as convertesse. Medido antes e depois na mesma proteção, em quatro modos de interpretador.
**E, desde [E23](docs/experiments/E23-route-gates-report.md), nem as proteções na rota que produziu os quatro ativos aceitos** — seus **57 pontos em doze
ferramentas**, convertidos como uma simples movimentação de arquivos que nenhum teste jamais executou, cada um agora rejeitando sob `-O` e `PYTHONOPTIMIZE=1`, bem como sob um interpretador normal.
**E, desde [E25](docs/experiments/E25-ruling.md), a classe está fechada.** Seus **133 pontos em 43 arquivos** — os instrumentos de medição que produziram as evidências para os quatro
ativos aceitos acima — convertem da mesma forma, elevando o total que `raise` para **278**.
Exatamente **um** ANDON simples `assert` permanece em qualquer lugar sob `tools/`:
`superseded/texpass_thin_mask.py`, que **nunca** é convertido, porque essas ferramentas são
mantidas para que qualquer pessoa possa executá-las e observá-las falhar da mesma forma. Esse restante é fixado
**por nome** no conjunto de testes, para que uma varredura futura não possa removê-lo sem editar o
teste intencionalmente.

**Status de suporte:** este repositório é desenvolvido de forma aberta, em um único ambiente, por um único diretor
e um par rotativo de sessões de consultor e executor. `main` é o único estado suportado. Não há canal de lançamento, nenhuma política de retrocompatibilidade e nenhum SLA — em vez disso, há
o registro: cada afirmação está ao lado do código que a produz, e
[docs/experiments](docs/experiments/) contém as especificações, o relatório e a decisão para
cada um.

## Requisitos

Blender 5.x, Python 3.11+ com `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`,
`spandrel`, `torch`. Uma instalação local do ComfyUI é necessária apenas para o pincel de preenchimento.
Desenvolvido em um RTX 5090; a capacidade da VRAM é mais importante do que a velocidade bruta.

**Dois interpretadores, e a divisão é intencional.** O conjunto, as ferramentas MCP servidas e
cada medição são executadas no ambiente que contém os pinos do CI (3.12). O estágio de reconstrução é executado em um segundo interpretador, fixado em **3.10**, porque as rodas TRELLIS de que ele precisa são construídas para ele. Uma ferramenta que falha ao importar geralmente está sendo solicitada do outro interpretador.

O CI executa o subconjunto hermético do conjunto em **ubuntu-latest / Python 3.12** com instalações fixas (`.github/workflows/ci.yml`); a camada de artefatos precisa das árvores registradas em `E:\AI\training`, que não estão no git, portanto, o CI as desativa por design.
Localmente, `python -m pytest` executa todos os **1376** testes e `python -m pytest -m "not artifacts"`
executa os **1319** que o CI reproduz.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
