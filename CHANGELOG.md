# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não lançado]

### Corrigido

- `lake`: diretório de entrada ausente passa a ser erro do `ConvertResult` (antes devolvia resultado vazio sem erro e o `convert` saía 0).
- `lake`: ZIP sem nenhum membro reconhecido (o conversor só aceita CSVs com "sinistro", "pessoa" ou "veiculo" no nome) passa a ser erro do arquivo, com a lista dos membros CSV na mensagem. Antes, se o Detran renomeasse os CSVs, nada era convertido e nada era reportado. Membro reconhecido de um dataset não pedido (`--dataset`) continua não sendo erro.

### Removido

- `InfosigaClient.get_min_max_dates`: devolvia `{}` tanto para erro quanto para resposta vazia e nenhum código a chamava (a consulta ao endpoint `minMaxDates` segue documentada em `docs/`, só como referência manual). A constante `INFOSIGA_MIN_MAX_DATES_URL` permanece.

## [0.3.2] - 2026-11-24

### Corrigido

- `lake`: o conversor passa a ter `inventory()`, e a auditoria do lake deixa de acusar `sem_parquet` no `dicionario/dicionario_dados@AAAAMMDD.zip` vigente. O grupo `dicionario` (dicionário de dados em PDF) nunca vai ao lake no conversor, mas sem inventário a auditoria o contava como arquivo de fonte com conversor e cobrava um Parquet que não existe. Agora o inventário o declara `nao_tabular`, junto com qualquer arquivo que não seja ZIP ou CSV; a versão antiga de um bruto que tem outra mais nova é `superado`; o ZIP de dados e o CSV solto de uma das três tabelas seguem esperando Parquet, e o CSV de tabela desconhecida também (a auditoria o acusa). O `convert` não muda.

## [0.3.1] - 2026-11-19

### Adicionado

- Testes: identidade do registro conferida.

### Alterado

- CI e infraestrutura alinhados ao template (fetcher-template v0.2.1).

### Corrigido

- `lake`: o build sem mudança não lê mais o bruto. Antes de abrir o ZIP ou transcodificar o CSV, confere pelos rodapés do lake (`LakeWriter.origin_complete`, que usa o sha256 do sidecar) se o bruto já está em dia e com todas as saídas, e, estando, só conta `skipped` pelas saídas declaradas (`origin_outputs`), sem varrer o membro nem calcular o hash. Cada Parquet declara as saídas do bruto no dataset (a união dos anos de todos os membros do ZIP): uma conversão interrompida num ano ou membro deixa de virar pulo permanente, e o bruto é reaberto até completar; lake gravado antes da declaração reconverte uma vez. Membro com erro determinístico continua aparecendo a cada build. O CSV solto de outra tabela, os sidecars e o grupo `dicionario` deixam de ser abertos. Mesma contagem de `converted`/`skipped`/`errors`; `force` e bruto novo seguem convertendo. Com mais de um membro por dataset no ZIP, a conversão faz uma passada a mais para listar os anos antes de gravar. Exige `quantilica-analytics>=0.15.0`.
- CI: o pyproject declara o PyPI antes do índice Quantilica (`[[tool.uv.index]]`), e o workflow perde `--index` e `--index-strategy`. Com a estratégia padrão `first-index`, o `uv sync` só consulta o índice para o que não está no PyPI (`quantilica-analytics`) e deixa de receber o 503 intermitente que o GitHub Pages devolve a caminhos inexistentes.

## [0.3.0] - 2026-11-14

### Adicionado
- O fetcher declara os fatos da fonte (`FetcherInfo`: id canônico, apelidos, órgão, licença, página e cadência) para o registro de fetchers da Quantilica.

### Alterado
- Requer `quantilica-core>=0.19.0` (e `quantilica-cli>=0.17.0` como host).
- `FetcherInfo.licenca` passa a declarar a licença da fonte: Sem licença declarada; dados públicos pela Lei 12.527/2011 (LAI) e Decreto 8.777/2016.

## [0.2.1] - 2026-11-09

### Adicionado
- Documentação dos dados em `docs/`: página da fonte, páginas dos datasets `sinistros`, `pessoas` e `veiculos` com dicionário de todas as variáveis (a partir do dicionário oficial v1.8) e esquemas de referência do lake, verificados por `tests/test_docs.py`.

## [0.2.0] - 2026-11-04

### Corrigido
- Lake: cada membro de um ZIP vira um arquivo de origem próprio (chave composta
  `zip__membro`). Antes, `veiculos_2015-2021` e `veiculos_2022-2024` do mesmo ZIP
  compartilhavam sha256 e partição, e o `LakeWriter` descartava o segundo.
- Lake: `veiculos` (e `pessoas`) deixam de ser particionados por `ano_fab` (ano de
  fabricação). A partição `ano` vem de `data_sinistro`/`ano_sinistro` por linha; sem
  essas colunas, do ano inicial da faixa do arquivo (coluna `periodo_arquivo`). Linha
  sem ano válido vai para `ano=__HIVE_DEFAULT_PARTITION__` (quarentena), não mais para
  2015 (`fill_null(2015)` removido).
- Lake: leitura membro a membro em streaming, decodificação cp1252 estrita (sem
  `errors="replace"`), colunas lidas como texto (sem inferência com 5000 linhas) e
  `skipped` contado à parte.
- Sem o extra `analysis`, o comando `convert` termina com código 1 e a instrução de instalação (`quantilica install infosiga --extra analysis`), sem traceback.

## [0.1.0] - 2026-11-01

### Adicionado
- Versão inicial do pacote `infosiga-fetcher` (`quantilica infosiga`).
- Suporte a `list`, `check`, `sync` e verificação de frescor via SDK `FetcherApp`.

- Conversor Universal Hive Parquet Lake com `DatasetSpec` em `lake.py`.

