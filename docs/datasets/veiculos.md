---
dataset:
  id: veiculos
  fonte: infosiga
  titulo: Veículos envolvidos em sinistros de trânsito de São Paulo (Infosiga.SP)
  resumo: Veículos envolvidos nos sinistros de trânsito do estado de São Paulo, uma linha por veículo e sinistro, com tipo, marca e modelo, cor e anos de fabricação e do modelo.
  orgao: Departamento Estadual de Trânsito de São Paulo (Detran-SP), Infosiga.SP
  pagina_oficial: https://infosiga.detran.sp.gov.br/
  licenca: "não informado pela fonte; o portal consultado não traz licença nem termo de uso legíveis (conferido em 2026-11-09)"
  periodicidade: "não informada pela fonte; em 2026-11-09 o painel indicava dados de 2015-01-01 a 2026-09-30 (endpoint minMaxDates) e o dicionário vigente é a versão 1.8 de 15/10/2026"
  cobertura: {inicio: 2014-12, fim: em-curso}
  unidade: um veículo envolvido em um sinistro
  granularidade: {espacial: estado de São Paulo (sem município na tabela; vem de `sinistros` por `id_sinistro`), temporal: dia}
  formato_bruto: "CSV dentro do ZIP dados_infosiga.zip, cp1252, separador ponto e vírgula, um arquivo por faixa de anos (veiculos_2015-2021, veiculos_2022-2024 e veiculos_2025-2026)"
  lake: {estado: convertido, particoes: [ano], chave: [id_veiculo], colunas: 12}
  dados_pessoais: nenhum
  eras:
    - {desde: 2019-01, mudanca: "Até 2018 só constam veículos de sinistros fatais; desde 2019-01 também os de sinistros não fatais e notificações (conferido pelo número de linhas por ano)"}
  revisado_em: 2026-11-09
  versao_fetcher: 0.2.0
---

# Veículos envolvidos em sinistros de trânsito de São Paulo (Infosiga.SP)

## Resumo

Uma linha por veículo envolvido em um sinistro de trânsito no estado de São Paulo, como o Infosiga.SP (sistema do Detran-SP) o publica: tipo de veículo, marca e modelo, cor, anos de fabricação e do modelo e a data do sinistro. Serve para analisar o perfil da frota envolvida em sinistros.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `infosiga/veiculos` |
| Órgão | Departamento Estadual de Trânsito de São Paulo (Detran-SP), Infosiga.SP |
| Página oficial | https://infosiga.detran.sp.gov.br/ |
| Licença | não informado pela fonte; o portal consultado não traz licença nem termo de uso legíveis (conferido em 2026-11-09) |
| Periodicidade | não informada pela fonte; em 2026-11-09 o painel indicava dados de 2015-01-01 a 2026-09-30 (endpoint minMaxDates) e o dicionário vigente é a versão 1.8 de 15/10/2026 |
| Cobertura | 2014-12 a em-curso |
| Unidade (uma linha) | um veículo envolvido em um sinistro |
| Granularidade | espacial: estado de São Paulo (sem município na tabela; vem de `sinistros` por `id_sinistro`); temporal: dia |
| Formato bruto | CSV dentro do ZIP dados_infosiga.zip, cp1252, separador ponto e vírgula, um arquivo por faixa de anos (veiculos_2015-2021, veiculos_2022-2024 e veiculos_2025-2026) |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `id_veiculo` |
| Colunas | 12 |
| Unidades de medida | — |
| Dados pessoais | nenhum |
| Eras | 2019-01: Até 2018 só constam veículos de sinistros fatais; desde 2019-01 também os de sinistros não fatais e notificações (conferido pelo número de linhas por ano) |
| Revisado em | 2026-11-09 |
| Versão do fetcher | 0.2.0 |

## Origem e coleta

- O fetcher baixa `https://infosiga.detran.sp.gov.br/painel/download/file/dados_infosiga.zip`, um único ZIP que traz as três tabelas (sinistros, pessoas e veículos) em nove CSV: um por tabela e faixa de anos (`2015-2021`, `2022-2024` e `2025-2026`). No bruto o arquivo é `dados_infosiga.zip`, com a data da coleta nas cópias de cada versão.
- O dicionário de dados oficial é publicado à parte (`Infosiga_dicionario_dados.zip`, três PDF, um por tabela) e é guardado no bruto, sem conversão.
- O ZIP é o mesmo para as três tabelas; cada dataset do lake converte os arquivos cujo nome traz a tabela (`sinistro`, `pessoa` ou `veiculo`).

## Conteúdo

- Uma linha por veículo envolvido. Conferido no ZIP coletado, versão do fetcher 0.2.0: 1.704.283 linhas de 969.834 sinistros distintos, de 2014-12-21 a 2026-09-30. Por ano: 2015 10.655; 2016 9.762; 2017 9.844; 2018 6.943; 2019 212.290; 2020 199.570; 2021 223.778; 2022 229.139; 2023 245.988; 2024 236.657; 2025 181.664; 2026 137.982 (até 30/09); 2014 (21 a 31/12): 11.
- Tipos (`tipo_veiculo`): `AUTOMOVEL` 717.498; `MOTOCICLETA` 617.007; `NAO DISPONIVEL` 182.607; `CAMINHAO` 65.341; `OUTROS` 47.792; `ONIBUS` 37.058; `BICICLETA` 36.980.
- O dicionário oficial vigente é a versão 1.8, de 15/10/2026.

## Variáveis

As descrições vêm do Dicionário de dados oficial v1.8 (15/10/2026) da tabela `veiculos`. "Fonte do dado" no dicionário: `DETRAN-SP`, `PC, PM e PRF` (siglas do dicionário) ou `IBGE`, por variável. A coluna "Tipo" mostra o tipo que o dicionário declara; no lake todas as colunas são texto.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `id_sinistro` | `id_sinistro` | texto (fonte: int64) | Identificador do sinistro (chave estrangeira para `sinistros`); pode haver mais de um veículo por sinistro | 7 dígitos | todo |
| `id_veiculo` | `id_veiculo` | texto (fonte: int64) | Identificador do veículo envolvido no sinistro, sequencial | 1 a 9999999 | todo |
| `marca_modelo` | `marca_modelo` | texto (fonte: string) | Marca e modelo do veículo envolvido; texto livre; pode ser nulo | livre | todo |
| `ano_fab` | `ano_fab` | texto (fonte: int64) | Ano de fabricação do veículo; pode ser nulo | 1956 até o ano do sinistro | todo |
| `ano_modelo` | `ano_modelo` | texto (fonte: int64) | Ano do modelo do veículo; pode ser nulo | 1956 até o ano do sinistro mais 1 | todo |
| `cor_veiculo` | `cor_veiculo` | texto (fonte: string) | Cor do veículo envolvido; texto livre; pode ser nula | livre | todo |
| `tipo_veiculo` | `tipo_veiculo` | texto (fonte: string) | Tipo de veículo envolvido no sinistro | `AUTOMOVEL`, `BICICLETA`, `CAMINHAO`, `MOTOCICLETA`, `ONIBUS`, `OUTROS`, `NAO DISPONIVEL` | todo |
| `data_sinistro` | `data_sinistro` | texto (fonte: date) | Data do sinistro, `dd/mm/aaaa` (texto no lake) | a partir de 21/12/2014 | todo |
| `ano_sinistro` | `ano_sinistro` | texto (fonte: int64) | Ano do sinistro | a partir de 2014 | todo |
| `mes_sinistro` | `mes_sinistro` | texto (fonte: int64) | Mês do sinistro | 1 a 12 | todo |
| `dia_sinistro` | `dia_sinistro` | texto (fonte: int64) | Dia do sinistro | 1 a 31 | todo |
| `ano_mes_sinistro` | `ano_mes_sinistro` | texto (fonte: string) | Agrupamento de ano e mês do sinistro, `aaaa/mm` | a partir de `2014/12` | todo |
| `ano` | `data_sinistro` (ano) | inteiro | Ano do sinistro, extraído de `data_sinistro` (ou de `ano_sinistro`); é a partição do lake, nunca o ano de fabricação | — | todo |

## No lake

- Dataset `infosiga/veiculos`, particionado por `ano`; um Parquet por arquivo CSV de origem e ano.
- **Todas as colunas são texto.** O conversor lê tudo como texto (convenção do lake), sem converter datas, inteiros nem coordenadas; os tipos da coluna "Tipo" são os que o dicionário oficial declara para a fonte.
- Nomes de coluna normalizados (minúsculas, sem acento, `_` no lugar de símbolos); na amostra conferida eles coincidem com as variáveis do dicionário oficial.
- Codificação cp1252; os poucos bytes que o cp1252 deixa indefinidos viram o caractere de controle de mesmo código, sem perda e sem U+FFFD.
- `ano` é o ano do sinistro, lido de `data_sinistro` (ou, se faltar, de `ano_sinistro`), por linha; nunca de `ano_fab`. Linha sem ano válido (fora de 1900 a 2100) iria para a partição de quarentena `ano=__HIVE_DEFAULT_PARTITION__`; na conversão conferida nenhuma linha foi para lá.
- Como os arquivos de origem são divididos por faixa de anos e `ano` vem da data, a partição `ano=2014` traz as linhas de 21 a 31/12/2014 do primeiro arquivo.

## Cuidados de uso

- **Todas as colunas chegam como texto.** Converta datas (`dd/mm/aaaa`), inteiros e coordenadas antes de calcular. As coordenadas usam vírgula decimal (`-24,013509599`); troque por ponto antes de converter.
- **Valores `NAO DISPONIVEL` e nulos são coisas diferentes** no dicionário: o primeiro é um código de classe da fonte, o segundo é campo sem valor. Trate os dois antes de somar ou agrupar.
- **Dados recentes são atualizáveis.** O dicionário diz que a gravidade da lesão e a contagem de vítimas fatais são atualizadas quando novos boletins de ocorrência chegam, e o óbito vale até 30 dias após o sinistro; os últimos meses mudam entre uma coleta e a seguinte.
- **Cobertura temporal.** Os arquivos trazem sinistros de 2014-12-21 a 2026-09-30 (conferido em 2026-11-09, no ZIP coletado); o painel anuncia o período de 2015-01-01 a 2026-09-30.
- **2015 a 2018 só têm sinistros fatais.** A partir de 2019-01 os arquivos incluem sinistros não fatais e notificações; séries por ano que cruzam 2018/2019 mudam de composição, não de tamanho real do fenômeno (conferido pela contagem por `tipo_registro` e ano, versão do fetcher 0.2.0).
- **Sem município nesta tabela.** Para localizar o veículo, junte com `sinistros` por `id_sinistro` (todo `id_sinistro` desta tabela consta em `sinistros`; conferido).
- **Identificadores.** `id_veiculo` é único em todo o ZIP coletado (1.704.283 linhas e valores distintos), embora o dicionário diga que o identificador é sequencial por veículo no sinistro; não confie nisso em outras coletas sem checar.
- **Anos de fabricação e modelo.** `ano_fab` é nulo em 318.944 linhas e `ano_modelo` em 324.792; na conversão, `ano_fab` vai de 1917 a 2025 e o dicionário diz 1956 como piso do intervalo permitido. `marca_modelo` é nulo em 134.694 linhas e `cor_veiculo` em 290.628.
- **`NAO DISPONIVEL`.** `tipo_veiculo` tem 182.607 linhas `NAO DISPONIVEL`; as colunas `qtd_*` de `sinistros` e esta tabela podem não coincidir por esse motivo (não conferido linha a linha).

## Exemplos

Veículos envolvidos por tipo e idade aproximada da frota (ano do sinistro menos ano de fabricação) em 2024:

```python
import polars as pl

v = pl.scan_parquet("lake/infosiga/veiculos/**/*.parquet", hive_partitioning=True)
idade_frota = (
    v.filter((pl.col("ano") == 2024) & pl.col("ano_fab").is_not_null())
    .with_columns((pl.col("ano_sinistro").cast(pl.Int64) - pl.col("ano_fab").cast(pl.Int64)).alias("idade_veiculo"))
    .filter(pl.col("idade_veiculo") >= 0)
    .group_by("tipo_veiculo")
    .agg(pl.len().alias("veiculos"), pl.col("idade_veiculo").median().alias("mediana_idade"))
    .sort("veiculos", descending=True)
    .collect()
)
```

## Referências

- Painel Infosiga.SP (Detran-SP): https://infosiga.detran.sp.gov.br/
- Dicionários de dados oficiais (PDF, v1.8): https://infosiga.detran.sp.gov.br/painel/download/file/Infosiga_dicionario_dados.zip
- Período disponível no painel (JSON): https://infosiga.detran.sp.gov.br/painel/minMaxDates
