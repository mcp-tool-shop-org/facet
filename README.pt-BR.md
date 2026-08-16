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

Verificado executando um **verbo** em vez de `--help` — uma malha de controle retorna 786.432 faces com um envelope de identidade completo em uma máquina sem diretório extraído.

**O que você obtém depende de uma coisa, e é a sua versão do Python:**

| seu Python | `[measure-full]` oferece |
|---|---|
| **3.11 / 3.12** | **todas as oito ferramentas** — `open3d` instala a partir do PyPI |
| **3.13** | quatro ferramentas; `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` |

`open3d` 0.19.0 é o *lançamento* mais recente e publica pacotes cp38–cp312 sem **nenhum sdist**, portanto, na versão 3.13 não há nada no PyPI para instalar. O pacote extra o inclui junto com `python_version < "3.13"`, então a instalação **tem sucesso** ali e as quatro ferramentas de geometria retornam **`4` REJEITADO**, indicando o que precisam — em vez de toda a instalação falhar.

**Para obter todas as oito no Python 3.13**, Open3D publica os pacotes cp313 atuais em seu canal de desenvolvimento contínuo. Uma URL direta é válida na linha de comando; ela só é proibida dentro dos metadados do pacote publicado:

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **No Windows e macOS, os pacotes de desenvolvimento são sufixados com `+<sha>`** (`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl` no momento da redação) e o nome muda à medida que `main` muda — liste os ativos no [lançamento `main-devel`](https://github.com/isl-org/Open3D/releases/tag/main-devel) e pegue o mais recente. **Essa versão é a que os números dependentes de open3d desta rota foram medidos**, e é uma verdadeira barreira de comparabilidade: o envelope de identidade registra o hash do instrumento, não suas dependências — [E31](docs/experiments/E31-ruling.md).

*Até a versão 0.3.1, o pacote continha dois arquivos `.py` e nenhum dos instrumentos de medição, portanto, um servidor de medição instalado não tinha nada para invocar. Ninguém percebeu durante quatro lançamentos porque este repositório É o diretório extraído: a ferramenta funcionava onde era construída e nunca havia estado em outro lugar.*

⚠ **`pip install facet-mcp` estava com defeito em todas as versões lançadas até a versão 0.3.0, e foi corrigido na versão 0.3.1.** O pacote instala `facet_index` como um módulo de nível superior, portanto, até e incluindo a versão 0.3.0, ele resolvia o local do registro em relação a `<venv>/Lib` — que não contém corpus nem índice — e `build`, `claims` e `q` sem `--db` falhavam.
**Na versão 0.3.0 ou anterior, use o binário `npx` acima.**

A partir da versão 0.3.1, a raiz é resolvida **testando se o registro existe**, em vez de presumir que ele existe: execute qualquer um dos comandos dentro de um diretório extraído e ele o encontrará; execute-o de qualquer outro lugar e ele retornará **`4` REJEITADO**, indicando ambos os diretórios que tentou e ambas as marcas que procurou. `$FACET_INDEX_DB` agora é lido por ambos os comandos, e ele seleciona qual *índice*, nunca qual *corpus*. Medido em um pacote construído a partir de `main` e instalado em um ambiente virtual limpo — [E24](docs/experiments/E24-ruling.md).

*Este bloco foi corrigido duas vezes. Primeiro, dizia `pipx install facet-mcp # ou o pacote Python diretamente `, until v0.3.0's read-back ran a **verb** instead of ` --help`.
Depois, dizia que o pacote "só funciona para `q` e `claims`" — **`claims` também não funcionou**, o que E24 descobriu executando-o. Ambas as correções estão em [known-defects.md](docs/known-defects.md) com suas medições.*

## Situação atual

**Quatro ativos aceitos, de quatro classes de objetos, sem custo.** Cada um foi avaliado pelo Diretor em seu próprio nível de zoom — no arquivo GLB ou em planilhas em tamanho real — não por uma métrica que atinja um limite.

| objeto | classe | aceito | referência / pincel / dilatação |
|---|---|---|---|
| **Character (W3)** | humanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | veículo, rigging fino | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | animal, membranas das asas | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | adereço, quase 2D, cinza sobre cinza | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

As proporções são de texels válidos e **não são comparáveis entre objetos** — uma nave esconde a maior parte de si mesma do nível dos olhos e um animal esconde metade. Avalie cada um em relação ao seu próprio limite de alcance pré-registrado, em relação ao qual eles atingem **86–93%**: a diferença entre as linhas é geometria, não regressão. [Números completos, com seus denominadores](docs/handbook/subjects.md).

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

**O "salto tracejado" é novo e foi criado para não ser sólido.** A primeira caixa da rota sempre
exibia *conceito de argila*, e até agora nada aqui o fazia — toda a argila chegava manualmente e
era processada no caminho. Agora existe uma ferramenta conceito→argila, e seu primeiro par foi testado
em tamanho real: pose, faixas para os pulsos, medalhão do cinto e bainha rasgada, tudo presente; a massa da crina não; o vazamento de cor medido em todo o quadro é de **C\* p99.9 = 13.15** com um fundo acromático uniforme. **O que esse par não pode mostrar é se a malha melhora**, que é
a única questão que justifica seu uso, então ele permanece como candidato com suas evidências registradas:
**[preparação do conceito](docs/concept-prep.md)**.

## O que faz funcionar

Seis descobertas, cada uma das quais exigiu um experimento e cada uma das quais se aplica além
do objeto que a gerou. [A versão completa, com as
medidas](docs/findings.md).

- **Primeiro a forma, depois o estilo.** Os softwares de reconstrução interpretam o ruído da superfície como geometria. Uma argila limpa, semelhante a uma escultura, com planos deliberadamente exagerados, resulta em uma topologia melhor do que um sprite estilizado; o gêmeo estilizado é gerado simultaneamente e se torna a
referência de cor.
- **Enquadre o rosto, obtenha um rosto.** Um recorte de busto coloca **3,1–4,5 vezes** mais polígonos na
cabeça, e a diferença é estrutural — pálpebras separadas, uma dobra na testa, cavidades do nariz modeladas — não apenas um desfoque mais nítido.
- **Os gêmeos pertencem a uma malha, não a um personagem.** Reutilize um gêmeo em várias malhas e a cobertura diminui de **62% para 22,7%**, porque os braços se projetam no espaço vazio ao lado do modelo.
Gere gêmeos a partir da malha que você está prestes a texturizar, sempre.
- **A identidade pertence ao prompt.** Um elemento canônico não nomeado no prompt está chegando
por acaso e sairá da mesma forma — medido quando as placas douradas dos joelhos acabaram
atingindo a imagem apenas através do ruído em uma ControlNet quebrada.
- **Peça à geometria, não a um limite.** Substituir uma máscara com contorno pelo exato contorno do raycast moveu a cobertura de referência de **28,4% para 39,1%** de texels válidos — estritamente
aditivo, sem difusão, sem GPU. O keying de canto-mediana falhou três vezes aqui e foi descontinuado.
- **Remova o que nenhuma câmera pode ver, do atlas e nunca da malha.** 49% dos texels do atlas
são invisíveis de fora; excluir esses elementos reduz a interpolação em **68%**. Excluir em vez de apagar torna a falha impossível, em vez de apenas detectável.

## O que não está resolvido

Nomeado e medido, na página inicial, em vez de em uma nota de rodapé. [Todos eles, localizados no
código](docs/known-defects.md).

- **A faixa da lâmina representa 0,00% da referência do estágio 1** em todas as oito câmeras — o aço sobre um fundo cinza se encaixa exatamente no limite do próprio key. A união resgata 55,72%.
- **As costuras dos traços não estão niveladas.** Uma fronteira de proveniência apresenta uma variação de textura **5,5 vezes** maior; a região que o Diretor nomeou apresenta uma variação **9,5 vezes** maior.
- **A dilatação vaza entre ilhas do atlas não relacionadas** — 74,9% dos texels dilatados obtêm sua
cor de outra ilha, com uma mediana de 0,177 de distância em uma figura de altura 1,0.
- **Cada reconstrução nesta rota é uma casca oca de parede dupla**, paredes com cerca de dois
voxels. Nenhum predicado volumétrico é válido em um deles.

## Como este repositório funciona

A disciplina é tão importante quanto o pipeline, e existe por um motivo: uma iteração anterior realizou dez sessões, cada uma das quais avaliou seu próprio resultado e escreveu conclusões que a sessão seguinte leu como fato estabelecido. Nada naquele ciclo era verificável.

- **Especifique antes do trabalho, relate depois, com a decisão final** — e a sessão que projeta um
experimento nunca avalia seus próprios resultados. Trinta e um experimentos estão em
[o registro](docs/experiments/).
- **As correções são aplicadas no local, ao lado da medição que as refutou**, nunca como
exclusões silenciosas. Seis alegações herdadas foram falsificadas na sessão inicial, e todas as seis ainda podem ser lidas ao lado do que as substituiu.
- **As falhas permanecem no repositório com sua razão.** [`tools/superseded/`](docs/tools.md)
não é um arquivo — qualquer pessoa pode executar essas ferramentas e vê-las falhar da mesma forma.
- **Um resultado negativo é um sucesso total**, relatado e encerrado, em vez de ajustado para atingir um
número.
- **Os testes acompanham o commit que toca o código** — 1072 aprovados por duas pessoas, com CI com restrições de caminho nos 1027 herméticos.
- **O registro é pesquisável.** Um índice SQLite + FTS5 em todo o histórico, verificado em quatro etapas. Ele encontrou uma contagem que a prosa havia errado em três locais, contando o próprio registro.

## Onde tudo está

| | |
|---|---|
| **[O manual](docs/handbook/index.md)** | o guia — a rota passo a passo, os objetos, o sistema de perfil |
| **[Preparação do conceito](docs/concept-prep.md)** | o salto candidato de argila: sua caminhada no Gate 0, seu posicionamento e o item de licença que ele abre |
| **[O registro](docs/experiments/)** | trinta e um experimentos: especificação, relatório, decisão e cada previsão declarada antes da medição |
| **[O que a rota aprendeu](docs/findings.md)** | as descobertas duradouras e as regras conquistadas com dificuldade, na íntegra |
| **[Status de cada ferramenta](docs/tools.md)** | o que funciona, o que está obsoleto e a evidência para cada um |
| **[Defeitos conhecidos](docs/known-defects.md)** | tudo o que não foi resolvido, medido e localizado no código |
| **[A iteração, como aconteceu](docs/arc-history.md)** | o histórico cronológico, com as correções intactas |
| **[CLAUDE.md](CLAUDE.md)** | como trabalhar aqui — os papéis, as regras e o custo de cada um |

## Posição da licença

Em cada etapa, o processo é executado localmente e garante a integridade comercial: SDXL (OpenRAIL++), MV-Adapter (código aberto), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Excluído deliberadamente, com a seguinte justificativa: **nvdiffrast** (não comercial — imposto aqui por um mecanismo de segurança estrutural, e não por atestado), **Hunyuan3D-Paint** (licença inválida na UE, Reino Unido e Coreia do Sul), **MVPaint** e **TEXGen** (sem licença) e **UltraSharp / SUPIR / StableSR** (ferramentas de ampliação não comerciais).

**O limite da alegação é definido explicitamente, em vez de deixado para ser descoberto.** Descreve o **percurso registrado** — as etapas no diagrama acima, desde a conversão de imagem para 3D. A etapa candidata de preparação do modelo, anterior a ela, atualmente é executada em uma API de nuvem fechada cujos termos este repositório **não verificou**, portanto, nenhuma alegação de licença aqui cobre um recurso criado a partir de um de seus modelos. Este é um ponto pendente com um caminho definido para sua resolução: o modelo local com a licença correta é **Qwen-Image-Edit (Apache-2.0)**, e **FLUX.1-Kontext [dev] é excluído pelos mesmos motivos do nvdiffrast** — pesos não comerciais. Ambos foram verificados em relação ao catálogo de modelos do estúdio, em vez de serem recuperados; a justificativa está em [preparação do conceito](docs/concept-prep.md).

## Modelo de confiança e ameaças

O facet é executado inteiramente na sua máquina — cada ferramenta é um script que você executa em caminhos que você digita, portanto, a pergunta relevante não é *quais permissões este aplicativo solicita*, mas *o que esses scripts fazem à sua máquina*. A resposta é obtida por meio de medição, com cada execução podendo ser repetida; a política completa está em [SECURITY.md](SECURITY.md):

- **Dados acessados:** meshes, texturas, imagens e arquivos JSON no disco local, nos caminhos que você especifica na linha de comando. Além disso, `docs/index/facet.db`, que é *derivado* — ele não contém nada que já não fosse um arquivo neste repositório, e `facet_index.py build` o regenera do zero.
- **Dados NÃO acessados:** nenhuma credencial, nunca. Nada aqui lê, armazena ou transmite um token, chave ou senha, e nenhum deles está presente na árvore — foi feita uma varredura para detectar chaves com prefixo de provedor, GitHub PATs, tokens Slack, IDs de chave AWS, blocos de chave privada, tokens de portador e atribuições inline `api_key`/`password`, **zero correspondências**, nenhum arquivo que se assemelhe a uma credencial foi encontrado.
- **Nenhuma telemetria.** Nada é coletado ou enviado. Não há opção de desativar porque não há nada para desativar.
- **Saída de rede:** duas das trinta e quatro ferramentas abrem um socket — `restylize_views.py` e `texpass_brush.py` — e ambas chamam uma API HTTP do ComfyUI em `--host`, **padrão `127.0.0.1:8188`**. Nenhuma outra ferramenta em `tools/` faz uma chamada de rede.
- **Permissões:** usuário comum. Sem elevação de privilégios, sem instalação de serviço, sem gravações nas configurações do sistema ou no registro.

Três pontos críticos são revelados em vez de omitidos, porque uma nota de segurança que apenas lista garantias não é um modelo de ameaças: **as operações de arquivo não são executadas em um ambiente isolado** (uma ferramenta grava onde seus argumentos indicam); **caminhos locais absolutos estão incorporados em muitas ferramentas e documentações** — 114 ocorrências em 26 arquivos, não segredos, mas uma divulgação do layout de uma máquina, e a razão pela qual a maioria das ferramentas não será executada sem modificação em outro lugar; e **falhas inesperadas são exibidas como rastreamentos Python nos 34 scripts de pesquisa não publicados**, sem um filtro `--debug`. As interrupções deliberadas são mensagens `ANDON:` que carregam a medição que as acionou. Este é o contrato do instrumento de pesquisa, e [SHIP_GATE.md](SHIP_GATE.md) registra exatamente quando ele deixa de ser bom — o que aconteceu para os dois comandos que o facet *instala*, em 0.2.0: `facet-index` e `facet-mcp` retornam `0` ok / `1` erro do usuário / `2` erro de tempo de execução — e, desde [E22](docs/experiments/E22-ruling.md), **`4` REJEITADO** para um filtro acionado ou uma etapa com falha `verify`, o que significa que a ferramenta está funcionando e informando que você não deve prosseguir, em vez de um erro de tempo de execução. Todos eles se recusam com uma falha estruturada que nomeia a próxima etapa, em vez de um rastreamento ([E21](docs/experiments/E21-cli-contract-report.md)).

**E os filtros nesses dois comandos não são mais excluíveis.** Cada ANDON no que o facet instala é `raise`; um simples `assert` é uma declaração de que `python -O` remove silenciosamente, e 87 dos filtros deste repositório podiam ser removidos por uma variável de ambiente até que E22 os convertesse. Medido antes e depois no mesmo filtro, em quatro modos de interpretador.
**E, desde [E23](docs/experiments/E23-route-gates-report.md), nem os filtros na rota que produziu os quatro recursos aceitos** — seus **57 pontos em doze ferramentas**, convertidos como uma simples movimentação de arquivos que nenhum teste jamais executou, cada um agora se recusando sob `-O` e `PYTHONOPTIMIZE=1`, bem como sob um interpretador normal.
**E, desde [E25](docs/experiments/E25-ruling.md), a classe está fechada.** Seus **133 pontos em 43 arquivos** — os instrumentos de medição que produziram as evidências para os quatro recursos aceitos acima — convertem da mesma forma, elevando o total que `raise` para **278**.
Exatamente **um** ANDON simples `assert` permanece em qualquer lugar sob `tools/`: `superseded/texpass_thin_mask.py`, que **nunca** é convertido, porque essas ferramentas são mantidas de forma que qualquer pessoa possa executá-las e observar sua falha da mesma maneira. Esse restante é fixado **por nome** no conjunto de testes, para que uma execução futura não possa removê-lo sem editar o teste intencionalmente.

**Status de suporte:** este repositório é desenvolvido em código aberto, em um único ambiente, por um diretor e um par rotativo de sessões de consultor e executor. `main` é o único estado suportado. Não há canal de lançamento, política de retrocompatibilidade ou SLA — em vez disso, existe o registro: cada alegação está ao lado do código que a produz, e [docs/experiments](docs/experiments/) contém as especificações, o relatório e a decisão para cada uma delas.

## Requisitos

Blender 5.x, Python 3.11+ com `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Uma instalação local do ComfyUI é necessária apenas para o pincel de retoque. Desenvolvido em uma RTX 5090; a capacidade da VRAM é mais importante do que a velocidade bruta.

O CI executa o subconjunto hermético da suíte no ambiente **ubuntu-latest / Python 3.12**, com instalações fixas (`.github/workflows/ci.yml`); a camada de artefatos necessita das árvores registradas em `E:\AI\training`, que não estão no Git, portanto, o CI as exclui intencionalmente. Localmente, `python -m pytest` executa todos os **1072** testes e `python -m pytest -m "not artifacts"` executa os **1027** testes reproduzidos pelo CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
