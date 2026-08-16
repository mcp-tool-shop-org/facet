<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
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

O estilo é aplicado **no ativo**, no espaço da textura — não é pintado para cada visualização e depois combinado. Forneça à rota um conceito de argila com formas exageradas e ela retornará uma malha texturizada cuja cor foi obtida a partir de uma referência estilizada *dessa* malha, com tudo o que a referência não podia ver preenchido por um pincel de retoque mascarado e uma dilatação consciente da superfície.

Nomeado para ambas as partes do problema: os polígonos e a face que eles devem manter.

## Instalar

A própria rota é um conjunto de scripts locais que você invoca em caminhos que digita — clone o repositório e leia [introdução](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**Dois servidores são enviados como um pacote** — o índice de registro, para que um assistente possa consultar o histórico das evidências em vez de lê-lo, e **a partir da versão 0.4.0, o servidor de medição**, para que dois ativos medidos com meses de diferença passem por um único caminho de código.

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

**Para obter todas as oito no Python 3.13**, Open3D publica os pacotes cp313 atuais em seu canal de desenvolvimento contínuo. Uma URL direta é válida na linha de comando; ela só é proibida dentro dos metadados do pacote publicado:

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **No Windows e macOS, os pacotes de desenvolvimento são sufixados com `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` no momento da redação) e o nome muda à medida que `main` muda — liste os ativos no [lançamento `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) e pegue o mais recente. **Essa versão é a que foi usada para medir os números dependentes do open3d desta rota**, e é uma verdadeira barreira de comparabilidade: o envelope de identidade registra o hash do instrumento, não suas dependências — [E31](docs/experiments/E31-ruling.md).

*Até a versão 0.3.1, o pacote continha dois arquivos `.py` e nenhum dos instrumentos de medição, portanto, um servidor de medição instalado não tinha nada para invocar. Ninguém percebeu em quatro lançamentos porque este repositório É o diretório extraído: a ferramenta funcionava onde era construída e nunca havia estado em outro lugar.*

⚠ **`pip install facet-mcp` estava com defeito em todas as versões lançadas até a versão 0.3.0, e foi corrigido na versão 0.3.1.** O pacote instala `facet_index` como um módulo de nível superior, portanto, até e incluindo a versão 0.3.0, ele resolvia o local do registro em relação a `<venv>/Lib` — que não contém nenhum corpus nem índice — e `build`, `claims` e `q` sem `--db` falhavam.
**Na versão 0.3.0 ou anterior, use o binário `npx` acima.**

A partir da versão 0.3.1, a raiz é resolvida **testando se o registro existe**, em vez de presumir que ele existe: execute qualquer um dos comandos dentro de um diretório extraído e ele o encontrará; execute-o de qualquer outro lugar e ele retornará **`4` REJEITADO**, indicando ambos os diretórios que tentou e ambas as marcas que procurou. `$FACET_INDEX_DB` agora é lido por ambos os comandos, e ele seleciona qual *índice*, nunca qual *corpus*. Medido em um pacote construído a partir de `main` e instalado em um ambiente virtual limpo — [E24](docs/experiments/E24-ruling.md).

*Este bloco foi corrigido duas vezes. Primeiro, dizia `pipx install facet-mcp # ou o pacote Python diretamente `, until v0.3.0's read-back ran a **verb** instead of ` --help`.
Depois, dizia que o pacote "só funciona para `q` e `claims`" — **`claims` também não funcionou**, o que E24 descobriu ao executá-lo. Ambas as correções estão em [known-defects.md](docs/known-defects.md) com suas medições.*

## Situação atual

**Quatro ativos aceitos, em quatro classes de assunto, sem custo.** Cada um foi avaliado pelo Diretor em seu próprio nível de zoom — no arquivo GLB ou em planilhas de tamanho normal — não por uma métrica que atinja um limite.

| assunto | classe | aceito | referência / pincel / dilatação |
|---|---|---|---|
| **Character (W3)** | humanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | veículo, rigging fino | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | animal, membranas das asas | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | adereço, quase 2D, cinza sobre cinza | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

As cotas são de texels válidos e **não são comparáveis entre os assuntos** — uma nave esconde a maior parte de si mesma do nível dos olhos e um animal esconde metade. Avalie cada um em relação ao seu próprio limite de alcance pré-registrado, em relação ao qual eles atingem **86–93%**: a diferença entre as linhas é geometria, não regressão. [Números completos, com seus denominadores](docs/handbook/subjects.md).

**É um pipeline, não um gerador de um único caractere.** Contradiga a especificação em oito elementos nomeados e o prompt vence **8 de 8** — ΔE mediano de 46,3 contra 6,2 em cinco controles mantidos — enquanto a figura permanece o mesmo homem. A estrutura é mantida pela malha e pelo controle; os atributos nomeados dependem do prompt.

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

Etapa por etapa, com a justificativa para cada uma: **[o manual](docs/handbook/index.md)**.

**O padrão tracejado é novo e foi criado intencionalmente para não ser sólido.** A primeira caixa da rota sempre continha a inscrição *conceito de argila*, e até agora nada aqui o fazia — toda a argila chegava manualmente e era processada no caminho. Agora existe uma ferramenta conceito→argila, e seu primeiro par foi testado em tamanho real: pose, protetores de pulso, medalhão do cinto e bainha rasgada, tudo presente; a massa da crina não; o vazamento de cor medido em todo o quadro é de **C\* p99.9 = 13.15** com um fundo acromático uniforme. **O que esse par não pode mostrar é se a malha melhora**, que é a única questão que o promove, então ele permanece como um candidato com suas evidências registradas: **[preparação do conceito](docs/concept-prep.md)**.

## O que faz funcionar

Seis descobertas, cada uma das quais exige um experimento e cada uma das quais se generaliza além do objeto que a produziu. [A versão completa, com as
medidas](docs/findings.md).

- **Primeiro a forma, depois o estilo.** Os reconstrutores interpretam o ruído da superfície como geometria. Uma argila limpa, semelhante a uma escultura, com planos deliberadamente exagerados, resulta em uma topologia melhor do que um sprite estilizado; a versão estilizada é gerada simultaneamente e se torna a referência de cor.
- **Enquadre o rosto, obtenha um rosto.** Um recorte de busto coloca **3,1–4,5×** mais polígonos na cabeça, e a diferença é estrutural — pálpebras separadas, uma dobra da testa, cavidades modeladas das narinas — não apenas um desfoque mais nítido.
- **Os gêmeos pertencem a uma malha, não a um personagem.** Reutilize um gêmeo em várias malhas e a cobertura diminui de **62% → 22,7%**, porque os braços se projetam no espaço vazio ao lado do modelo. Gere gêmeos a partir da malha que você está prestes a texturizar, sempre.
- **A identidade pertence ao prompt.** Um elemento canônico não nomeado no prompt está chegando por acaso e sairá da mesma forma — medido quando as placas douradas dos joelhos acabaram alcançando a imagem apenas através do ruído em uma ControlNet quebrada.
- **Peça à geometria, não a um limite.** Substituir uma máscara com contorno pelo exato contorno do raycast moveu a cobertura de referência de **28,4% → 39,1%** de texels válidos — estritamente aditivo, sem difusão, sem GPU. O keying de canto-mediana falhou três vezes aqui e foi descontinuado.
- **Remova o que nenhuma câmera pode ver, do atlas e nunca da malha.** 49% dos texels do atlas são invisíveis de fora; excluir esses elementos reduz a interpolação em **68%**. Excluir em vez de apagar torna a falha impossível, em vez de apenas detectável.

## O que não está resolvido

Nomeado e medido, na página inicial, em vez de em uma nota de rodapé. [Todos eles, localizados no
código](docs/known-defects.md).

- **Alguns mapas de superfície visíveis são mapeados para o espaço do atlas que nenhuma renderização jamais grava**, e aparecem como o preto padrão não alterado da imagem. O "baker" do Blender usa amostragem no centro dos texels, então um triângulo que não se sobrepõe a nenhum centro de texel fica vazio — seus próprios desenvolvedores
[nomearam o mecanismo e incorporaram uma correção](https://projects.blender.org/blender/blender/pulls/161752)
duas semanas após a construção em que todos os números aqui foram medidos. É uma propriedade da rota, não de um objeto específico: medido em um ativo, **não medido nos outros quatro**.
- **A faixa da lâmina representa 0,00% da referência do estágio 1** em todas as oito câmeras — o aço sobre um fundo cinza está exatamente no limite do próprio "key". A união resgata 55,72%.
- **As bordas dos traços não estão niveladas.** Uma fronteira de proveniência apresenta uma variação de textura **5,5×** maior; a região que o Diretor nomeou apresenta uma variação **9,5×** maior.
- **A dilatação vaza entre ilhas do atlas não relacionadas** — 74,9% dos texels dilatados obtêm sua cor de outra ilha, com uma distância mediana de 0,177 em uma figura de altura 1,0. ⚠ **Essa proporção está nos texels do atlas e não é uma afirmação sobre o que uma câmera vê**: a dilatação representa 26,95% do atlas renderizado e **4,95% dos pixels da figura renderizada**, uma razão de 0,18×. A pintura vive em gráficos grandes, os buracos vivem em pequenos, então um texel dilatado é barato no espaço da tela.
- **⚑ O defeito que decide a aceitação é carregado pela PINTURA, não por nenhum preenchimento** — regiões que exibem a cor de outro material, o que nenhuma estatística de manchas consegue detectar. Medido de três maneiras em três sessões em três espaços: **91,05% `reference` carregado com um enriquecimento de 0,99×**, exatamente na taxa base; a mesma classe em verde tecido **68,46% `reference`**; e em uma lâmina fina, os próprios texels pintados da superfície **18,77%** contaminados contra seus **5,55%** de preenchimento de dilatação. O preenchimento obtém corretamente dados do vizinho pintado mais próximo — e esse vizinho já está errado. A própria mistura é uma divisão de duas bandas não documentada
(`M + gaussian_blur_σ16(B − M)`) que mede o **pior dos quatro** alternativos nos mesmos pontos.
- **As visualizações nunca são independentes, o que limita cada correção de mistura.** Para cada "blob" de defeito, **100% das faces com duas ou mais câmeras contribuintes têm todas elas dentro de um intervalo de 90°** (mediana de 45°) e 21% das faces com defeito são vistas por apenas uma câmera. Visualizações adjacentes sob controle quase idêntico falham juntas, portanto, os ganhos multi-visualização publicados da fotogrametria não se transferem aqui em valor nominal.
- **Cada reconstrução nesta rota é uma casca oca de parede dupla**, com paredes de cerca de dois voxels. Nenhum predicado volumétrico é válido em um deles.

## Como este repositório é executado

A disciplina é tão importante quanto o próprio pipeline, e existe por um motivo: uma iteração anterior realizou dez sessões que julgaram seus próprios resultados e escreveram conclusões que a sessão seguinte leu como fato estabelecido. Nada naquele ciclo era verificável.

- **Especificação antes do trabalho, relatório depois, decisão final** — e a sessão que define um experimento nunca avalia seus próprios resultados. Quarenta experimentos estão em [o registro](docs/experiments/).
- **Correções são aplicadas no local, ao lado da medição que as refutou**, nunca como exclusões discretas. Seis alegações herdadas foram consideradas falsas apenas na sessão inicial, e todas as seis ainda podem ser lidas ao lado do que as substituiu.
- **Falhas permanecem no repositório com sua respectiva razão.** [`tools/superseded/`](docs/tools.md) não é um arquivo — qualquer pessoa pode executar essas ferramentas e observar suas falhas da mesma forma.
- **Um resultado negativo é um sucesso completo**, relatado e encerrado, em vez de ajustado para um número específico.
- **Testes acompanham o commit que modifica o código** — 1087 aprovados por duas pessoas, com CI baseado em caminhos nos 1042 testes herméticos.
- **O registro é pesquisável.** Um índice SQLite + FTS5 sobre todo o histórico, verificado em quatro etapas. Ele encontrou uma contagem de decisões que a redação havia indicado incorretamente em três locais, contando o próprio registro.

## Onde tudo está:

| | |
|---|---|
| **[O manual](docs/handbook/index.md)** | o guia — a rota passo a passo, os tópicos e o sistema de perfil |
| **[Preparação do conceito](docs/concept-prep.md)** | a etapa candidata de preparação da argila: sua execução na Etapa 0, seu posicionamento e o item de licença que ela abre |
| **[O registro](docs/experiments/)** | quarenta experimentos: especificação, relatório, decisão e cada previsão declarada antes da medição |
| **[O que a rota aprendeu](docs/findings.md)** | as descobertas duradouras e as regras arduamente conquistadas, em sua totalidade |
| **[Status de cada ferramenta](docs/tools.md)** | o que funciona, o que foi substituído e a evidência para cada um |
| **[Defeitos conhecidos](docs/known-defects.md)** | tudo o que não foi resolvido, medido e localizado no código |
| **[O arco, como aconteceu](docs/arc-history.md)** | o histórico cronológico, com as correções intactas |
| **[CLAUDE.md](CLAUDE.md)** | como trabalhar aqui — os papéis, as regras e o custo de cada um |

## Posição da licença

Cada etapa é executada localmente e está em conformidade com as licenças: SDXL (OpenRAIL++), MV-Adapter (código aberto), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Excluído deliberadamente, com a respectiva razão: **nvdiffrast** (não comercial — imposto aqui por um mecanismo de segurança estrutural, não por atestado), **Hunyuan3D-Paint** (licença inválida na UE, Reino Unido e Coreia do Sul), **MVPaint** e **TEXGen** (nenhuma licença) e **UltraSharp / SUPIR / StableSR** (ampliadores não comerciais).

**O limite da alegação, declarado em vez de deixado para ser descoberto.** Ele descreve a **rota registrada** — as etapas no diagrama acima, desde imagem para 3D. A etapa candidata de preparação da argila, anterior a ela, atualmente é executada em uma API de nuvem fechada cujos termos este repositório **não verificou**, portanto, nenhuma alegação de licença aqui cobre um ativo criado a partir de uma de suas argilas. Este é um item pendente com um caminho nomeado para resolvê-lo: o modelo local com licença correta é **Qwen-Image-Edit (Apache-2.0)**, e **FLUX.1-Kontext [dev] é excluído pelos mesmos motivos de nvdiffrast** — pesos não comerciais. Ambos foram verificados em relação ao catálogo de modelos do estúdio, em vez de relembrados; o raciocínio está em [preparação do conceito](docs/concept-prep.md).

## Modelo de confiança e ameaças

o facet é executado inteiramente na sua própria máquina — cada ferramenta é um script que você executa em caminhos que você digita, portanto, a pergunta útil não é *quais permissões este aplicativo solicita*, mas *o que esses scripts fazem com sua máquina*. Resposta fornecida por meio de medição, com cada execução podendo ser repetida; a política completa está em [SECURITY.md](SECURITY.md):

- **Dados acessados:** malhas, texturas, imagens e JSON no disco local, nos caminhos que você passa na linha de comando. Além disso, `docs/index/facet.db`, que é *derivado* — ele não contém nada que já não fosse um arquivo neste repositório, e `facet_index.py build` o regenera do zero.
- **Dados NÃO acessados:** nenhuma credencial, nunca. Nada aqui lê, armazena ou transmite um token, chave ou senha, e nenhum está presente na árvore — foi verificado para detectar chaves com prefixo de provedor, GitHub PATs, tokens Slack, IDs de chave AWS, blocos de chave privada, tokens de portador e atribuições `api_key`/`password` embutidas, **zero correspondências**, nenhum arquivo com formato de credencial rastreado.
- **Nenhuma telemetria.** Nenhuma coletada, nenhuma enviada. Não há opção de desativar porque não há nada para desativar.
- **Egressos de rede:** duas das trinta e seis ferramentas abrem um socket — `restylize_views.py` e `texpass_brush.py` — e ambas chamam uma API HTTP ComfyUI em `--host`, **padrão `127.0.0.1:8188`**. Nada mais em `tools/` faz uma chamada de rede.
- **Permissões:** usuário comum. Sem elevação, sem instalação de serviço, sem gravações nas configurações do sistema ou no registro.

Três arestas afiadas são reveladas em vez de descartadas, porque uma nota de segurança que apenas lista garantias não é um modelo de ameaça: **as operações de arquivo não estão isoladas** (uma ferramenta grava onde seus argumentos indicam); **caminhos locais absolutos estão incorporados em muitas ferramentas e documentações** — 114 ocorrências em 26 arquivos, não segredos, mas a divulgação do layout de uma máquina e o motivo pelo qual a maioria das ferramentas não funcionará sem modificação em outro lugar; e **falhas inesperadas aparecem como rastreamentos Python nos 36 scripts de pesquisa não publicados**, sem um filtro `--debug`. Interrupções deliberadas são mensagens `ANDON:` que carregam a medição que as acionou. Esse é o contrato do instrumento de pesquisa, e [SHIP_GATE.md](SHIP_GATE.md) registra exatamente quando ele deixa de ser bom — o que aconteceu para os dois comandos no aspecto *instala*, em 0.2.0: `facet-index` e `facet-mcp` retornam `0` ok / `1` erro do usuário / `2` erro de tempo de execução — e, como [E22](docs/experiments/E22-ruling.md), **`4` REJEITADO** para um filtro acionado ou um `verify` com falha, o que significa que a ferramenta está funcionando e dizendo para não prosseguir, em vez de ser um erro de tempo de execução. Todos eles rejeitam com uma falha estruturada que indica o próximo passo, em vez de um rastreamento ([E21](docs/experiments/E21-cli-contract-report.md)).

**E os filtros nesses dois comandos não são mais removíveis.** Cada ANDON no aspecto *instala* `raise`; um `assert` simples é uma declaração que `python -O` remove silenciosamente, e 87 dos filtros deste repositório podiam ser removidos por uma variável de ambiente até que E22 os convertesse. Medido antes e depois no mesmo filtro, em quatro modos de interpretador.
**E, como [E23](docs/experiments/E23-route-gates-report.md), nem os filtros na rota que produziu os quatro ativos aceitos são removíveis** — seus **57 locais em doze ferramentas**, convertidos como uma simples movimentação de arquivos que nenhum teste jamais executou, cada um agora rejeitando também sob `-O` e `PYTHONOPTIMIZE=1`, bem como sob um interpretador normal.
**E, como [E25](docs/experiments/E25-ruling.md), a classe está fechada.** Seus **133 locais em 43 arquivos** — os instrumentos de medição que produziram as evidências para os quatro ativos aceitos acima — convertem da mesma forma, elevando o total que `raise` para **278**.
Exatamente **um** ANDON simples `assert` permanece em qualquer lugar sob `tools/`: `superseded/texpass_thin_mask.py`, que **nunca** é convertido, porque essas ferramentas são mantidas de forma que qualquer pessoa possa executá-las e observar sua falha da mesma maneira. Esse restante é fixado **por nome** na suíte de testes, para que uma varredura futura não possa removê-lo sem editar o teste intencionalmente.

**Status de suporte:** este repositório é desenvolvido em código aberto, em um único ambiente, por um diretor e um par rotativo de sessões de consultor e executor. `main` é o único estado suportado. Não há canal de lançamento, política de retrocompatibilidade ou SLA — em vez disso, existe o registro: cada afirmação está ao lado do código que a produz, e [docs/experiments](docs/experiments/) contém as especificações, o relatório e a decisão para cada uma.

## Requisitos

Blender 5.x, Python 3.11+ com `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Uma instalação local do ComfyUI é necessária apenas para o pincel de preenchimento. Desenvolvido em um RTX 5090; a capacidade da VRAM é mais importante do que a velocidade bruta.

O CI executa o subconjunto hermético da suíte em **ubuntu-latest / Python 3.12** com instalações fixas (`.github/workflows/ci.yml`); a camada de artefatos precisa das árvores registradas sob `E:\AI\training`, que não estão no git, então o CI as desativa por design. Localmente, `python -m pytest` executa todos os **1087** testes e `python -m pytest -m "not artifacts"` executa os **1042** testes reproduzidos pelo CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
