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

O estilo é aplicado **no objeto**, no espaço da textura — não é pintado para cada perspectiva e depois combinado. Forneça ao programa um modelo conceitual em argila com formas exageradas e ele retornará uma malha texturizada cuja cor foi obtida a partir de uma referência estilizada *dessa* malha, com tudo o que a referência não conseguia visualizar preenchido por um pincel de retoque mascarado e uma dilatação que considera a superfície.

O nome faz referência a ambos os aspetos do problema: os polígonos e a superfície que eles devem preencher.

## Qual é a situação atual?

**Quatro trabalhos aprovados, abrangendo quatro áreas de estudo diferentes, sem qualquer requisito de créditos.** Cada um foi avaliado pelo diretor, individualmente – seja no formato digital (GLB) ou em folhas impressas em tamanho real –, e não com base em critérios quantitativos que estabelecessem um limite mínimo.

| assunto; tema; matéria | classe | aceito(a) / aprovado(a) | referência / pincel / dilatação |
|---|---|---|---|
| **Character (W3)** | humanoide | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | veículo, cabo fino | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | fera, membranas das asas | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | objeto de cena, quase bidimensional, tons de cinza sobre cinza | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

As amostras são de texels válidos e **não podem ser comparadas entre diferentes objetos** — um navio esconde a maior parte de si mesmo a partir do nível dos olhos e um animal esconde metade do corpo. Analise cada um em relação ao seu limite máximo pré-definido, no qual atingem uma percentagem de **86–93%**: a diferença entre as linhas é geométrica, não estatística. [Números completos, com os seus denominadores](docs/handbook/subjects.md).

**É um processo, não um gerador de imagens com apenas um único elemento.** Ao contradizer as especificações em oito elementos nomeados, o modelo obtém **8 de 8** pontos – a diferença média ΔE é de 46,3, contra 6,2 nos cinco exemplos de referência –, enquanto a imagem mantém a mesma pessoa. A estrutura é mantida pela malha e pelo controle; os atributos nomeados são determinados pelo comando (prompt).

## O percurso/a rota

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

Passo a passo, com a explicação de cada um: **[o manual](docs/handbook/index.md)**.

## O que faz com que funcione?

Seis descobertas, cada uma das quais exigiu a realização de um experimento e cada uma das quais tem implicações que vão além do objeto de estudo que as gerou. [A versão completa, com as medições](docs/findings.md).

- **Priorize a forma, depois o estilo.** Os programas de reconstrução interpretam o ruído da superfície como geometria. Uma argila limpa, com aparência escultórica e planos deliberadamente exagerados, resulta numa topologia melhor do que um sprite estilizado; o modelo estilizado é gerado em paralelo e serve como referência de cor.
- **Defina o contorno do rosto, crie um rosto.** Um recorte no formato de busto coloca **3,1–4,5 vezes** mais polígonos na cabeça, e a diferença é estrutural – pálpebras separadas, uma ruga na testa, cavidades nasais modeladas –, não apenas um desfoque mais nítido.
- **Os modelos gêmeos pertencem a uma malha, não a um personagem.** Reutilize um modelo gêmeo em várias malhas e a cobertura diminui de **62% para 22,7%**, porque os braços se projetam no espaço vazio ao lado do modelo. Gere modelos gêmeos a partir da malha que você está prestes a texturizar, sempre.
- **A identidade pertence à instrução.** Um elemento canônico não mencionado na instrução aparece por acidente e desaparecerá da mesma forma – medido quando as placas douradas nos joelhos acabaram aparecendo na imagem apenas através do ruído numa versão corrompida do ControlNet.
- **Consulte a geometria, não um limite.** Substituir uma máscara com o contorno exato obtido por traçado de raio moveu a cobertura de referência de **28,4% para 39,1%** de texels válidos – estritamente aditivo, sem difusão, sem uso da GPU. O método de seleção baseado no canto-mediana falhou três vezes aqui e foi descontinuado.
- **Elimine o que nenhuma câmera pode ver, do atlas e nunca da malha.** 49% dos texels do atlas são invisíveis a partir do exterior; excluir essas faces reduz a interpolação em **68%**. Excluir, em vez de apagar, torna a falha impossível, em vez de apenas detectável.

## O que ainda não foi resolvido?

Identificados e descritos, na página principal em vez de numa nota de rodapé. [Todos eles estão localizados no código](docs/known-defects.md).

- **A faixa da lâmina representa 0,00% da referência do estágio 1** em todas as oito câmaras — o aço sobre um fundo cinzento está exatamente no limite definido. A união recupera 55,72%.
- **As bordas dos traços não estão niveladas.** Um limite de proveniência apresenta uma variação **5,5 vezes** maior do que a textura normal; a região designada pelo diretor apresenta uma variação **9,5 vezes** maior.
- **A dilatação causa sobreposição entre ilhas do atlas não relacionadas** — 74,9% dos texels dilatados obtêm sua cor de outra ilha, com uma distância mediana de 0,177 em uma figura com altura de 1,0.
- **Cada reconstrução nesta rota é uma estrutura oca de parede dupla**, com paredes de aproximadamente dois voxels. Nenhum predicado volumétrico é válido para ela.

## Como este repositório é gerenciado

A disciplina é tão importante quanto o processo em si e existe por uma razão: numa fase anterior, foram realizadas dez sessões nas quais cada participante avaliou o seu próprio trabalho e redigiu conclusões que foram lidas na sessão seguinte como se fossem factos estabelecidos. Nada nesse ciclo podia ser verificado.

- **Definir antes do trabalho, relatar depois, decidir por último** — e a sessão que planeja um experimento nunca avalia os seus próprios resultados. Vinte experimentos estão em [o registro](docs/experiments/).
- **As correções são aplicadas no local, ao lado da medição que as refutou**, nunca como exclusões discretas. Seis alegações herdadas foram consideradas falsas apenas na sessão inicial, e todas as seis ainda podem ser consultadas ao lado do que as substituiu.
- **Os resultados negativos permanecem no repositório com a sua justificativa.** [`tools/superseded/`](docs/tools.md) não é um arquivo — qualquer pessoa pode executar essas ferramentas e observar o seu fracasso da mesma forma.
- **Um resultado negativo é um sucesso completo**, relatado e encerrado, em vez de ajustado para atingir um valor específico.
- **Os testes acompanham o commit que modifica o código** — 213 aprovados por duas pessoas, com CI restrito a caminhos nas 205 versões herméticas.
- **O registro pode ser consultado.** Um índice SQLite + FTS5 sobre todo o histórico, verificado em quatro pontos. Ele encontrou uma contagem de resultados que o texto havia indicado incorretamente em três locais, contando o próprio registro.

## Onde tudo acontece

| | |
|---|---|
| **[O manual](docs/handbook/index.md)** | o guia – o percurso dividido em etapas, os temas abordados, o sistema de classificação. |
| **[O registro](docs/experiments/)** | vinte experimentos: especificação, relatório, avaliação e cada previsão declarada antes da medição |
| **[O que a rota aprendeu](docs/findings.md)** | as descobertas duradouras e as regras arduamente conquistadas, na íntegra |
| **[Status de cada ferramenta](docs/tools.md)** | o que funciona, o que está obsoleto e a evidência para cada um |
| **[Defeitos conhecidos](docs/known-defects.md)** | tudo o que não foi resolvido, medido e localizado no código |
| **[O ciclo, como aconteceu](docs/arc-history.md)** | o histórico cronológico, com as correções preservadas |
| **[CLAUDE.md](CLAUDE.md)** | como trabalhar aqui — os papéis, as regras e o custo de cada um |

## Posição da licença

Cada etapa é executada localmente e está em conformidade com os requisitos comerciais: SDXL (OpenRAIL++), MV-Adapter (código aberto),
open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy,
trimesh.

Excluído deliberadamente, com a justificativa: **nvdiffrast** (não comercial — imposto aqui
por um mecanismo de segurança estrutural, não por atestado), **Hunyuan3D-Paint** (licença inválida na
UE, Reino Unido e Coreia do Sul), **MVPaint** e **TEXGen** (nenhuma licença) e
**UltraSharp / SUPIR / StableSR** (ampliadores não comerciais).

## Modelo de confiança e ameaças

o facet é executado inteiramente na sua própria máquina — cada ferramenta é um script que você executa em relação a
caminhos que você digita, portanto, a pergunta útil não é *quais permissões este aplicativo solicita*, mas
*o que esses scripts fazem com sua máquina*. Resposta fornecida por meio de medição, com cada
execução repetível; a política completa está em [SECURITY.md](SECURITY.md):

- **Dados acessados:** malhas, texturas, imagens e JSON no disco local, nos caminhos que você
fornece na linha de comando. Além disso, `docs/index/facet.db`, que é *derivado* — ele contém
nada que já não fosse um arquivo neste repositório, e `facet_index.py build`
o regenera do zero.
- **Dados NÃO acessados:** nenhum dado de credencial, nunca. Nada aqui lê, armazena ou transmite
um token, chave ou senha, e nenhum está presente na árvore — verificado para
chaves com prefixo de provedor, GitHub PATs, tokens Slack, IDs de chaves AWS, blocos de chave privada,
tokens de portador e atribuições inline `api_key`/`password`, **zero correspondências**, nenhum
arquivo semelhante a credencial rastreado.
- **Nenhuma telemetria.** Nenhuma coletada, nenhuma enviada. Não há opção de desativar porque não há
nada para desativar.
- **Saída de rede:** duas das trinta e quatro ferramentas abrem um socket — `restylize_views.py`
e `texpass_brush.py` — e ambas chamam uma API HTTP do ComfyUI em `--host`, **padrão
`127.0.0.1:8188`**. Nada mais em `tools/` faz uma chamada de rede.
- **Permissões:** usuário comum. Sem elevação, sem instalação de serviço, sem gravações nas configurações do sistema
ou no registro.

Três pontos críticos são divulgados em vez de serem omitidos, porque uma nota de segurança que
apenas lista garantias não é um modelo de ameaças: **as operações de arquivo não estão isoladas**
(uma ferramenta grava onde seus argumentos indicam); **caminhos locais absolutos estão incorporados em muitas
ferramentas e documentos** — 114 ocorrências em 26 arquivos, não segredos, mas uma divulgação do layout de uma
máquina, e a razão pela qual a maioria das ferramentas não será executada sem modificações em outro lugar; e
**falhas inesperadas aparecem como rastreamentos do Python**, sem um filtro `--debug` e sem um
formato de erro estruturado. As interrupções deliberadas são mensagens `ANDON:` que carregam a medição
que as acionou. Esse é o contrato do instrumento de pesquisa, e
[SHIP_GATE.md](SHIP_GATE.md) registra exatamente quando ele deixa de ser bom o suficiente.

**Status de suporte:** este repositório é desenvolvido em código aberto, em uma única máquina, por um único diretor
e um par rotativo de sessões de consultor e executor. `main` é o único estado suportado. Não há canal de lançamento, nenhuma política de retrocompatibilidade e nenhum SLA — em vez disso, existe
o registro: cada afirmação está ao lado do código que a produz, e
[docs/experiments](docs/experiments/) contém a especificação, o relatório e a avaliação para
cada um.

## Requisitos

Blender 5.x, Python 3.11+ com `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`,
`spandrel`, `torch`. Uma instalação local do ComfyUI é necessária apenas para o pincel de retoque.
Desenvolvido em uma RTX 5090; a capacidade da VRAM é mais importante do que a velocidade bruta.

O CI executa o subconjunto hermético do conjunto no **ubuntu-latest / Python 3.12** com
instalações fixas (`.github/workflows/ci.yml`); a camada de artefatos precisa das árvores registradas em `E:\AI\training`, que não estão no git, portanto, o CI as exclui por design.
Localmente, `python -m pytest` executa todos os **213** testes e `python -m pytest -m "not artifacts"`
executa os **205** que o CI reproduz.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
