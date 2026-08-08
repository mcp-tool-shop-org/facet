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

O estilo é aplicado **no ativo**, no espaço da textura — não é pintado para cada visualização e, posteriormente, combinado. Forneça à sequência um conceito de argila com formas exageradas e ela retornará uma malha texturizada cuja cor foi obtida a partir de uma referência estilizada *dessa* malha, com tudo o que a referência não podia ver preenchido por um pincel de retoque mascarado e uma dilatação consciente da superfície.

Nomeado para ambas as partes do problema: os polígonos e a face que eles devem representar.

## Instalar

A própria sequência é um conjunto de scripts locais que você invoca em caminhos que digita — clone o repositório e leia [o guia de início](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/).

**O índice de registro é fornecido como um pacote**, para que um assistente possa consultar o histórico das evidências em vez de lê-lo:

```bash
npx @mcptoolshop/facet          # zero-prerequisite; verified binary, no Python needed
pipx install facet-mcp          # or the Python package directly
```

Dois comandos são incluídos — `facet-mcp`, o servidor MCP stdio (seis ferramentas, com a verificação de quatro pontos como uma superfície de saúde que rejeita) e `facet-index` (`build` / `verify` / `q` / `claims`). Aponte qualquer um para um índice com `--db` ou `$FACET_INDEX_DB`.

## Onde ele se encontra

**Quatro ativos aceitos, em quatro classes de objetos, sem custo.** Cada um foi avaliado pelo Diretor em seu próprio nível de zoom — no GLB ou em folhas de tamanho normal — não por uma métrica que atinja um limite.

| objeto | classe | aceito | referência / pincel / dilatação |
|---|---|---|---|
| **Character (W3)** | humanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | veículo, rigging fino | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | animal, membranas das asas | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | adereço, quase 2D, cinza sobre cinza | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

As partes são de texels válidos e **não são comparáveis entre os objetos** — um navio esconde a maior parte de si mesmo do nível dos olhos e um animal esconde metade. Avalie cada um em relação ao seu próprio limite de alcance pré-registrado, no qual eles atingem **86–93%**: a diferença entre as linhas é geometria, não regressão. [Números completos, com seus
denominadores](docs/handbook/subjects.md).

**É uma sequência de processamento, não um gerador de um único caractere.** Contradiga a especificação em oito elementos nomeados e o prompt vence **8 de 8** — ΔE mediano de 46,3 contra 6,2 em cinco controles mantidos — enquanto a figura permanece a mesma. A estrutura é mantida pela malha e pelo controle; os atributos nomeados acompanham o prompt.

## A sequência

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

Etapa por etapa, com a justificativa para cada uma: **[o guia](docs/handbook/index.md)**.

## O que faz funcionar

Seis descobertas, cada uma das quais custou um experimento e cada uma das quais se generaliza além do objeto que a produziu. [A versão completa, com as
medidas](docs/findings.md).

- **Forma primeiro, estilo depois.** Os reconstrutores interpretam o ruído da superfície como geometria. Uma argila limpa, semelhante a uma escultura, com planos deliberadamente exagerados, resulta em uma topologia melhor do que um sprite estilizado; o gêmeo estilizado é gerado simultaneamente e se torna a referência de cor.
- **Enquadre o rosto, obtenha um rosto.** Um recorte de busto coloca **3,1–4,5 vezes** mais polígonos na cabeça, e a diferença é estrutural — pálpebras separadas, uma ruga na testa, cavidades das narinas modeladas — não um desfoque mais nítido.
- **Os gêmeos pertencem a uma malha, não a um personagem.** Reutilize um gêmeo em várias malhas e a cobertura entra em colapso de **62% para 22,7%**, porque os braços se projetam no espaço vazio ao lado do modelo. Gere gêmeos a partir da malha que você está prestes a texturizar, sempre.
- **A identidade pertence ao prompt.** Um elemento canônico não nomeado no prompt está chegando por acidente e sairá da mesma forma — medido quando as placas de joelho douradas acabaram atingindo a imagem apenas através do ruído em um ControlNet quebrado.
- **Pergunte à geometria, não a um limite.** Substituir uma máscara com chave pela silhueta exata do raycast moveu a cobertura da referência de **28,4% para 39,1%** de texels válidos — estritamente aditivo, sem difusão, sem GPU. O keying de canto-mediana falhou três vezes aqui e foi descontinuado.
- **Remova o que nenhuma câmera pode ver, do atlas e nunca da malha.** 49% dos texels do atlas são invisíveis do lado de fora; excluir esses faces reduz a interpolação em **68%**. Excluir em vez de apagar torna a falha impossível, em vez de apenas detectável.

## O que não está resolvido

Nomeado e medido, na página inicial, em vez de em uma nota de rodapé. [Todos eles, localizados no
código](docs/known-defects.md).

- **A faixa da lâmina ocupa 0,00% da referência da etapa 1** em todas as oito câmeras — o aço sobre um fundo cinza está exatamente no próprio limite da chave. A união resgata 55,72%.
- **As costuras do traço não são niveladas.** Um limite de proveniência apresenta uma variação de textura **5,5 vezes** maior; a região que o Diretor nomeou apresenta uma variação **9,5 vezes** maior.
- **A dilatação vaza entre ilhas de atlas não relacionadas** — 74,9% dos texels dilatados obtêm sua cor de outra ilha, de uma mediana de 0,177 de distância em uma figura com altura 1,0.
- **Cada reconstrução nesta sequência é uma casca oca de parede dupla**, paredes com cerca de dois voxels. Nenhum predicado volumétrico é válido em um deles.

## Como este repositório é executado

A disciplina é tão importante quanto a própria sequência de processamento, e ela existe por um motivo: uma sequência anterior realizou dez sessões que avaliaram seu próprio resultado e escreveram conclusões que a sessão seguinte leu como fato estabelecido. Nada naquele ciclo era verificável.

- **Definir antes do trabalho, relatar depois, decisão final** — e a sessão que projeta um experimento nunca avalia seus próprios resultados. Vinte experimentos estão em [o registro](docs/experiments/).
- **Correções são aplicadas no local, ao lado da medição que as refutou**, nunca como exclusões silenciosas. Seis alegações herdadas foram consideradas falsas apenas na sessão inicial, e todas as seis ainda podem ser lidas ao lado do que as substituiu.
- **Falhas permanecem no repositório com sua razão.** [`tools/superseded/`](docs/tools.md) não é um arquivo — qualquer pessoa pode executar essas ferramentas e observar suas falhas da mesma forma.
- **Um resultado negativo é um sucesso total**, relatado e encerrado, em vez de ajustado para um número específico.
- **Testes acompanham o commit que afeta o código** — 218 aprovados por duas pessoas, com CI baseado em caminhos nos 210 testes herméticos.
- **O registro pode ser consultado.** Um índice SQLite + FTS5 sobre todo o histórico, verificado em quatro etapas. Ele encontrou uma contagem de decisão que a prosa havia apresentado incorretamente em três locais, contando o próprio registro.

## Onde tudo está

| | |
|---|---|
| **[O manual](docs/handbook/index.md)** | o guia — o roteiro passo a passo, os tópicos, o sistema de perfil |
| **[O registro](docs/experiments/)** | vinte experimentos: especificação, relatório, decisão e cada previsão declarada antes da medição |
| **[O que o roteiro aprendeu](docs/findings.md)** | as descobertas duradouras e as regras conquistadas com dificuldade, na íntegra |
| **[Status de cada ferramenta](docs/tools.md)** | o que funciona, o que está obsoleto e a evidência para cada um |
| **[Defeitos conhecidos](docs/known-defects.md)** | tudo o que não foi resolvido, medido e localizado no código |
| **[O arco, como aconteceu](docs/arc-history.md)** | o histórico cronológico, com as correções intactas |
| **[CLAUDE.md](CLAUDE.md)** | como trabalhar aqui — os papéis, as regras e o custo de cada um |

## Posição da licença

Cada etapa é executada localmente e está em conformidade com as licenças: SDXL (OpenRAIL++), MV-Adapter (aberto), open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Excluído deliberadamente, com a razão: **nvdiffrast** (não comercial — imposto aqui por um gatilho estrutural, não por atestado), **Hunyuan3D-Paint** (licença inválida na UE, Reino Unido e Coreia do Sul), **MVPaint** e **TEXGen** (nenhuma licença) e **UltraSharp / SUPIR / StableSR** (ampliadores não comerciais).

## Modelo de confiança e ameaças

o facet é executado inteiramente em sua própria máquina — cada ferramenta é um script que você invoca em caminhos que digita, portanto, a pergunta útil não é *quais permissões este aplicativo solicita*, mas *o que esses scripts fazem com sua máquina*. Respondido por meio de medição, com cada execução podendo ser repetida; a política completa está em [SECURITY.md](SECURITY.md):

- **Dados acessados:** malhas, texturas, imagens e JSON no disco local, nos caminhos que você passa na linha de comando. Além disso, `docs/index/facet.db`, que é *derivado* — ele não contém nada que já não fosse um arquivo neste repositório, e `facet_index.py build` o regenera do zero.
- **Dados NÃO acessados:** nenhum dado de credencial, nunca. Nada aqui lê, armazena ou transmite um token, chave ou senha, e nenhum está presente na árvore — verificado em busca de chaves com prefixo de provedor, GitHub PATs, tokens Slack, IDs de chave AWS, blocos de chave privada, tokens de portador e atribuições `api_key`/`password` inline, **zero correspondências**, nenhum arquivo com formato de credencial rastreado.
- **Nenhuma telemetria.** Nenhuma coletada, nenhuma enviada. Não há opção de desativar porque não há nada para desativar.
- **Egressos de rede:** duas das trinta e quatro ferramentas abrem um socket — `restylize_views.py` e `texpass_brush.py` — e ambas chamam uma API HTTP do ComfyUI em `--host`, **padrão `127.0.0.1:8188`**. Nada mais em `tools/` faz uma chamada de rede.
- **Permissões:** usuário comum. Sem elevação, sem instalação de serviço, sem gravações nas configurações do sistema ou no registro.

Três pontos críticos são divulgados em vez de omitidos, porque uma nota de segurança que lista apenas garantias não é um modelo de ameaças: **as operações de arquivo não são executadas em sandbox** (uma ferramenta grava onde seus argumentos indicam); **caminhos locais absolutos estão incorporados em muitas ferramentas e documentos** — 114 ocorrências em 26 arquivos, não segredos, mas uma divulgação do layout de uma máquina e a razão pela qual a maioria das ferramentas não será executada sem modificações em outro lugar; e **falhas inesperadas aparecem como rastreamentos do Python**, sem um filtro `--debug` e sem um formato de erro estruturado. As interrupções deliberadas são mensagens `ANDON:` que carregam a medição que as acionou. Esse é o contrato do instrumento de pesquisa, e [SHIP_GATE.md](SHIP_GATE.md) registra exatamente quando ele deixa de ser bom o suficiente.

**Status de suporte:** este repositório é desenvolvido em código aberto, em uma única configuração, por um diretor e um par rotativo de sessões de consultor e executor. `main` é o único estado suportado. Não há canal de lançamento, nenhuma política de retrocompatibilidade e nenhum SLA — em vez disso, existe o registro: cada alegação está ao lado do código que a produz, e [docs/experiments](docs/experiments/) contém a especificação, o relatório e a decisão para cada uma.

## Requisitos

Blender 5.x, Python 3.11+ com `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch`. Uma instalação local do ComfyUI é necessária apenas para o pincel de retoque. Desenvolvido em uma RTX 5090; a capacidade da VRAM é mais importante do que a velocidade bruta.

O CI executa o subconjunto hermético do conjunto no **ubuntu-latest / Python 3.12** com instalações fixas (`.github/workflows/ci.yml`); a camada de artefatos precisa das árvores registradas em `E:\AI\training`, que não estão no git, portanto, o CI as desativa por design. Localmente, `python -m pytest` executa todos os **218** testes e `python -m pytest -m "not artifacts"` executa os **210** testes reproduzidos pelo CI.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
