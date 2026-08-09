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
  Local hardware end to end · no non-commercial licence anywhere in the chain
</p>

---

O estilo é aplicado **no ativo**, no espaço da textura — não é pintado para cada visualização e depois combinado. Forneça à rota um conceito de argila com formas exageradas e ela retornará uma malha texturizada cuja cor foi obtida a partir de uma referência estilizada *dessa* malha, com tudo o que a referência não podia ver preenchido por um pincel de retoque mascarado e uma dilatação consciente da superfície.

Nomeado para ambas as partes do problema: os polígonos e a face que eles devem representar.

## Instalar

A própria rota é um conjunto de scripts locais que você invoca em caminhos que digita — clone o repositório e leia [introdução](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**O índice do registro é fornecido como um pacote**, para que um assistente possa consultar o histórico de evidências em vez de lê-lo:

```bash
npx @mcptoolshop/facet          # zero-prerequisite; verified binary, no Python needed
```

Dois comandos são incluídos — `facet-mcp`, o servidor MCP stdio (seis ferramentas, com a verificação de quatro pontos como uma superfície de saúde que recusa), e `facet-index` (`build` / `verify` / `q` / `claims`). Execute-o dentro de um diretório extraído; `--db` nomeia um índice diferente.

⚠ **`pip install facet-mcp` estava com defeito em todas as versões lançadas até a v0.3.0, e foi corrigido na v0.3.1.** O pacote instala `facet_index` como um módulo de nível superior, portanto, até e incluindo a v0.3.0, ele resolvia o local do registro em relação a `<venv>/Lib` — que não contém corpus nem índice — e `build`, `claims` e `q` sem `--db` falhavam.
**Na v0.3.0 ou anterior, use o binário `npx` acima.**

A partir da v0.3.1, a raiz é resolvida **testando o registro** em vez de presumir que ele existe: execute qualquer um dos comandos dentro de um diretório extraído e ele o encontrará; execute-o de qualquer outro lugar e ele será encerrado com **`4` RECUSADO**, nomeando ambos os diretórios que tentou e ambas as marcas que procurou.
`$FACET_INDEX_DB` agora é lido por ambos os comandos, e ele seleciona qual *índice*, nunca qual *corpus*. Medido em um pacote construído a partir de `main` e instalado em um ambiente virtual limpo — [E24](docs/experiments/E24-ruling.md).

*Este bloco foi corrigido duas vezes. Primeiro, dizia `pipx install facet-mcp # ou o pacote Python diretamente`, until v0.3.0's read-back ran a **verb** instead of `--help`.
Em seguida, afirmou que o pacote "funciona apenas para `q` e `claims`" — **`claims` também não funcionou**, o que E24 descobriu ao executá-lo. Ambas as correções estão em [known-defects.md](docs/known-defects.md) com suas medições.*

## Onde está

**Quatro ativos aceitos, de quatro classes de objetos, sem custo.** Cada um foi avaliado pelo Diretor em seu próprio nível de zoom — no GLB ou em folhas de tamanho real — não por uma métrica que atinge um limite.

| objeto | classe | aceito | referência / pincel / dilatação |
|---|---|---|---|
| **Character (W3)** | humanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | veículo, rigging fino | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | animal, membranas das asas | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | adereço, quase 2D, cinza sobre cinza | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

As proporções são de texels válidos e **não são comparáveis entre os objetos** — um navio esconde a maior parte de si mesmo do nível dos olhos e um animal esconde metade. Avalie cada um em relação ao seu próprio limite de alcance pré-registrado, em relação ao qual eles atingem **86–93%**: a diferença entre as linhas é geometria, não regressão. [Números completos, com seus denominadores](docs/handbook/subjects.md).

**É um pipeline, não um gerador de um único caractere.** Contradiga a especificação em oito elementos nomeados e o prompt vence **8 de 8** — ΔE mediano de 46,3 contra 6,2 em cinco controles mantidos — enquanto a figura permanece o mesmo homem. A estrutura é mantida pela malha e pelo controle; os atributos nomeados acompanham o prompt.

## A rota

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

Etapa por etapa, com a justificativa para cada uma: **[o manual](docs/handbook/index.md)**.

## O que faz funcionar

Seis descobertas, cada uma das quais custou um experimento e cada uma das quais se generaliza além do objeto que a produziu. [A versão completa, com as medições](docs/findings.md).

- **Forma primeiro, estilo depois.** Os reconstrutores leem o ruído da superfície como geometria. Uma argila limpa, semelhante a uma escultura, com planos deliberadamente exagerados, retorna com uma topologia melhor do que um sprite estilizado; o gêmeo estilizado é gerado em conjunto e se torna a referência de cor.
- **Enquadre o rosto, obtenha um rosto.** Um recorte de busto coloca **3,1–4,5 vezes** mais polígonos na cabeça, e a diferença é estrutural — pálpebras separadas, uma ruga na testa, cavidades modeladas das narinas — não um desfoque mais nítido.
- **Os gêmeos pertencem a uma malha, não a um personagem.** Reutilize um gêmeo em várias malhas e a cobertura entra em colapso de **62% para 22,7%**, porque os braços se projetam no espaço vazio ao lado do modelo. Gere gêmeos a partir da malha que você está prestes a texturizar, sempre.
- **A identidade pertence ao prompt.** Um elemento canônico não nomeado no prompt está chegando por acidente e sairá da mesma forma — medido quando as placas de joelho douradas acabaram atingindo a imagem apenas através do ruído em um ControlNet com defeito.
- **Pergunte à geometria, não a um limite.** Substituir uma máscara chaveada pela silhueta exata do raycast moveu a cobertura da referência de **28,4% para 39,1%** de texels válidos — estritamente aditivo, sem difusão, sem GPU. O keying de canto-mediana falhou três vezes aqui e foi descontinuado.
- **Remova o que nenhuma câmera pode ver, da textura e nunca da malha.** 49% dos texels da textura são invisíveis do lado de fora; excluir esses rostos reduz a interpolação em **68%**. Excluir em vez de excluir torna a falha impossível em vez de apenas detectável.

## O que não está resolvido

Nomeado e medido, na página inicial em vez de em uma nota de rodapé. [Todos eles, localizados no código](docs/known-defects.md).

- A faixa da lâmina representa 0,00% da referência do estágio 1 em todas as oito câmeras — o aço sobre um fundo cinza está exatamente no limite definido. A combinação resulta em 55,72%.
- As costuras dos traços não estão niveladas. Um limite de origem apresenta uma variação de textura **5,5×** maior; a região que o Diretor nomeou apresenta uma variação **9,5×** maior.
- A dilatação causa sangramento entre ilhas do atlas não relacionadas — 74,9% dos texels dilatados obtêm sua cor de outra ilha, com uma distância mediana de 0,177 em uma figura com altura de 1,0.
- Cada reconstrução nesta rota é uma casca oca de parede dupla, com paredes de aproximadamente dois voxels. Nenhum predicado volumétrico é válido em uma delas.

## Como este repositório funciona

A disciplina é tão importante quanto o processo, e existe por um motivo: uma iteração anterior realizou dez sessões, nas quais cada uma avaliou seu próprio resultado e escreveu conclusões que foram lidas na sessão seguinte como fatos estabelecidos. Nada naquele ciclo era verificável.

- Especifique antes do trabalho, faça o relatório depois e tome a decisão final — e a sessão que projeta um experimento nunca avalia seus próprios resultados. Vinte e seis experimentos estão em [o registro](docs/experiments/).
- As correções são aplicadas no local, ao lado da medição que as refutou, e não como exclusões silenciosas. Seis alegações herdadas foram consideradas falsas na sessão inicial, e todas as seis ainda podem ser lidas ao lado do que as substituiu.
- Os erros permanecem no repositório com sua respectiva razão. [`tools/superseded/`](docs/tools.md) não é um arquivo — qualquer pessoa pode executar essas ferramentas e observar que elas falham da mesma forma.
- Um resultado negativo é um sucesso total, relatado e encerrado em vez de ajustado para atingir um número.
- Os testes são executados no commit que modifica o código — 790 aprovados por duas pessoas, com CI baseado em caminhos nos 761 herméticos.
- O registro pode ser consultado. Um índice SQLite + FTS5 sobre todo o histórico, verificado em quatro etapas. Ele encontrou uma contagem de decisões que a redação havia apresentado incorretamente em três locais, contando o próprio registro.

## Onde tudo está

| | |
|---|---|
| **[O manual](docs/handbook/index.md)** | o guia — a rota passo a passo, os sujeitos, o sistema de perfil |
| **[O registro](docs/experiments/)** | vinte e seis experimentos: especificação, relatório, decisão e cada previsão declarada antes da medição |
| **[O que a rota aprendeu](docs/findings.md)** | as descobertas duradouras e as regras conquistadas com dificuldade, na íntegra |
| **[Status de cada ferramenta](docs/tools.md)** | o que funciona, o que foi substituído e a evidência para cada um |
| **[Defeitos conhecidos](docs/known-defects.md)** | tudo o que não foi resolvido, medido e localizado no código |
| **[A iteração, como aconteceu](docs/arc-history.md)** | o histórico cronológico, com as correções intactas |
| **[CLAUDE.md](CLAUDE.md)** | como trabalhar aqui — os papéis, as regras e o custo de cada um |

## Posição da licença

Cada etapa é executada localmente e está em conformidade com as políticas comerciais: SDXL (OpenRAIL++), MV-Adapter (código aberto), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Deliberadamente excluído, com a respectiva razão: **nvdiffrast** (não comercial — imposto aqui por um mecanismo estrutural, e não por atestado), **Hunyuan3D-Paint** (licença inválida na UE, Reino Unido e Coreia do Sul), **MVPaint** e **TEXGen** (nenhuma licença) e **UltraSharp / SUPIR / StableSR** (ampliadores não comerciais).

## Modelo de confiança e ameaças

o facet é executado inteiramente em sua própria máquina — cada ferramenta é um script que você invoca contra caminhos que você digita, portanto, a pergunta útil não é *quais permissões este aplicativo solicita*, mas *o que esses scripts fazem com sua máquina*. A resposta é fornecida pela medição, com cada execução podendo ser repetida; a política completa está em [SECURITY.md](SECURITY.md):

- **Dados acessados:** malhas, texturas, imagens e JSON no disco local, nos caminhos que você passa na linha de comando. Além disso, `docs/index/facet.db`, que é *derivado* — ele não contém nada que já não fosse um arquivo neste repositório, e `facet_index.py build` o regenera do zero.
- **Dados NÃO acessados:** nenhuma credencial, nunca. Nada aqui lê, armazena ou transmite um token, chave ou senha, e nenhum está presente na árvore — foi verificado para detectar chaves com prefixo de provedor, GitHub PATs, tokens Slack, IDs de chave AWS, blocos de chave privada, tokens de portador e atribuições `api_key`/`password` embutidas, **zero correspondências**, nenhum arquivo com formato de credencial rastreado.
- **Nenhuma telemetria.** Nenhuma coletada, nenhuma enviada. Não há opção de desativar porque não há nada para desativar.
- **Egressos de rede:** duas das trinta e quatro ferramentas abrem um socket — `restylize_views.py` e `texpass_brush.py` — e ambas chamam uma API HTTP do ComfyUI em `--host`, **padrão `127.0.0.1:8188`**. Nada mais em `tools/` faz uma chamada de rede.
- **Permissões:** usuário comum. Sem elevação, sem instalação de serviço, sem gravações nas configurações do sistema ou no registro.

Três arestas afiadas são reveladas em vez de descartadas, porque uma nota de segurança que apenas lista garantias não é um modelo de ameaça: **as operações de arquivo não estão isoladas** (uma ferramenta grava onde seus argumentos indicam); **caminhos locais absolutos estão incorporados em muitas ferramentas e documentações** — 114 ocorrências em 26 arquivos, não segredos, mas a divulgação do layout de uma máquina e o motivo pelo qual a maioria das ferramentas não funcionará sem modificação em outro lugar; e **falhas inesperadas aparecem como rastreamentos Python nos 34 scripts de pesquisa não publicados**, sem um filtro `--debug`. Interrupções deliberadas são mensagens `ANDON:` que carregam a medição que as acionou. Esse é o contrato do instrumento de pesquisa, e [SHIP_GATE.md](SHIP_GATE.md) registra exatamente quando ele deixa de ser bom — o que aconteceu para os dois comandos da faceta *instala*, em 0.2.0: `facet-index` e `facet-mcp` retornam `0` ok / `1` erro do usuário / `2` erro de tempo de execução — e, como [E22](docs/experiments/E22-ruling.md), **`4` REJEITADO** para um filtro acionado ou um `verify` com falha, o que significa que a ferramenta está funcionando e dizendo para não prosseguir, em vez de ser um erro de tempo de execução. Todos eles rejeitam com uma falha estruturada que indica o próximo passo, em vez de um rastreamento ([E21](docs/experiments/E21-cli-contract-report.md)).

**E os filtros nesses dois comandos não são mais removíveis.** Cada ANDON na faceta de instalação `raise`; um `assert` simples é uma declaração que `python -O` remove silenciosamente, e 87 dos filtros deste repositório podiam ser removidos por uma variável de ambiente até que E22 os convertesse. Medido antes e depois no mesmo filtro, em quatro modos de interpretador.
**E, como [E23](docs/experiments/E23-route-gates-report.md), nem os filtros na rota que produziu os quatro ativos aceitos** — seus **57 locais em doze ferramentas**, convertidos como uma simples movimentação de arquivos que nenhum teste jamais executou, cada um agora rejeitando também sob `-O` e `PYTHONOPTIMIZE=1`, bem como sob um interpretador normal.
**E, como [E25](docs/experiments/E25-ruling.md), a classe está fechada.** Seus **133 locais em 43 arquivos** — os instrumentos de medição que produziram as evidências para os quatro ativos aceitos acima — convertem da mesma forma, elevando o total que `raise` para **278**.
Exatamente **um** ANDON simples `assert` permanece em qualquer lugar sob `tools/`: `superseded/texpass_thin_mask.py`, que **nunca** é convertido, porque essas ferramentas são mantidas de modo que qualquer pessoa possa executá-las e observar sua falha da mesma forma. Esse restante é fixado **por nome** na suíte de testes, para que uma varredura futura não possa removê-lo sem editar o teste intencionalmente.

**Status de suporte:** este repositório é desenvolvido de forma aberta, em um único ambiente, por um diretor e um par rotativo de sessões de consultor e executor. `main` é o único estado suportado. Não há canal de lançamento, política de retrocompatibilidade ou SLA — em vez disso, existe o registro: cada afirmação está ao lado do código que a produz, e [docs/experiments](docs/experiments/) contém as especificações, o relatório e a decisão para cada um.

## Requisitos

Blender 5.x, Python 3.11+ com `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Uma instalação local do ComfyUI é necessária apenas para o pincel de preenchimento. Desenvolvido em um RTX 5090; a capacidade da VRAM é mais importante do que a velocidade bruta.

O CI executa o subconjunto hermético da suíte em **ubuntu-latest / Python 3.12** com instalações fixas (`.github/workflows/ci.yml`); a camada de artefatos precisa das árvores registradas sob `E:\AI\training`, que não estão no git, então o CI as desativa por design. Localmente, `python -m pytest` executa todos os **790** testes e `python -m pytest -m "not artifacts"` executa os **761** que o CI reproduz.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
