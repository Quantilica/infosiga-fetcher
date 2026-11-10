# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não lançado]

### Adicionado
- O fetcher declara os fatos da fonte (`FetcherInfo`: id canônico, apelidos, órgão, licença, página e cadência) para o registro de fetchers da Quantilica.

### Alterado
- Requer `quantilica-core>=0.19.0` (e `quantilica-cli>=0.17.0` como host).

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

