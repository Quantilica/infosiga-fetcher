---
dataset:
  id: pessoas
  fonte: infosiga
  titulo: Pessoas envolvidas em sinistros de trânsito de São Paulo (Infosiga.SP)
  resumo: Pessoas (vítimas, condutores e passageiros) envolvidas nos sinistros de trânsito do estado de São Paulo, uma linha por pessoa e sinistro, com sexo, idade, gravidade da lesão e dados de óbito.
  orgao: Departamento Estadual de Trânsito de São Paulo (Detran-SP), Infosiga.SP
  pagina_oficial: https://infosiga.detran.sp.gov.br/
  licenca: "não informado pela fonte; o portal consultado não traz licença nem termo de uso legíveis (conferido em 2026-11-09)"
  periodicidade: "não informada pela fonte; em 2026-11-09 o painel indicava dados de 2015-01-01 a 2026-09-30 (endpoint minMaxDates) e o dicionário vigente é a versão 1.8 de 15/10/2026"
  cobertura: {inicio: 2014-12, fim: em-curso}
  unidade: uma pessoa envolvida em um sinistro
  granularidade: {espacial: município, temporal: dia}
  formato_bruto: "CSV dentro do ZIP dados_infosiga.zip, cp1252, separador ponto e vírgula, um arquivo por faixa de anos (pessoas_2015-2021, pessoas_2022-2024 e pessoas_2025-2026)"
  lake: {estado: convertido, particoes: [ano], chave: [id_pessoa], colunas: 31}
  dados_pessoais: 
    - {coluna: sexo, categoria: "sexo da vítima (dado sensível quando combinado com os demais)"}
    - {coluna: idade, categoria: "idade da vítima"}
    - {coluna: profissao, categoria: "profissão da vítima, texto livre"}
    - {coluna: grau_de_instrucao, categoria: "grau de instrução"}
    - {coluna: nacionalidade, categoria: "nacionalidade, texto livre"}
    - {coluna: data_obito, categoria: "data do óbito"}
  eras:
    - {desde: 2019-01, mudanca: "Até 2018 só constam pessoas de sinistros fatais; desde 2019-01 também as de sinistros não fatais e notificações (conferido pelo número de linhas por ano)"}
  revisado_em: 2026-11-09
  versao_fetcher: 0.2.0
---

# Pessoas envolvidas em sinistros de trânsito de São Paulo (Infosiga.SP)

## Resumo

Uma linha por pessoa envolvida em um sinistro de trânsito no estado de São Paulo, como o Infosiga.SP (sistema do Detran-SP) a publica: posição da vítima (condutor, passageiro, pedestre), modo de transporte, sexo, idade e faixas etárias, gravidade da lesão, escolaridade, profissão, nacionalidade e dados do óbito quando houve. Serve para estudos de mortalidade e lesões no trânsito.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `infosiga/pessoas` |
| Órgão | Departamento Estadual de Trânsito de São Paulo (Detran-SP), Infosiga.SP |
| Página oficial | https://infosiga.detran.sp.gov.br/ |
| Licença | não informado pela fonte; o portal consultado não traz licença nem termo de uso legíveis (conferido em 2026-11-09) |
| Periodicidade | não informada pela fonte; em 2026-11-09 o painel indicava dados de 2015-01-01 a 2026-09-30 (endpoint minMaxDates) e o dicionário vigente é a versão 1.8 de 15/10/2026 |
| Cobertura | 2014-12 a em-curso |
| Unidade (uma linha) | uma pessoa envolvida em um sinistro |
| Granularidade | espacial: município; temporal: dia |
| Formato bruto | CSV dentro do ZIP dados_infosiga.zip, cp1252, separador ponto e vírgula, um arquivo por faixa de anos (pessoas_2015-2021, pessoas_2022-2024 e pessoas_2025-2026) |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `id_pessoa` |
| Colunas | 31 |
| Unidades de medida | — |
| Dados pessoais | `sexo` (sexo da vítima (dado sensível quando combinado com os demais)); `idade` (idade da vítima); `profissao` (profissão da vítima, texto livre); `grau_de_instrucao` (grau de instrução); `nacionalidade` (nacionalidade, texto livre); `data_obito` (data do óbito) |
| Eras | 2019-01: Até 2018 só constam pessoas de sinistros fatais; desde 2019-01 também as de sinistros não fatais e notificações (conferido pelo número de linhas por ano) |
| Revisado em | 2026-11-09 |
| Versão do fetcher | 0.2.0 |

## Origem e coleta

- O fetcher baixa `https://infosiga.detran.sp.gov.br/painel/download/file/dados_infosiga.zip`, um único ZIP que traz as três tabelas (sinistros, pessoas e veículos) em nove CSV: um por tabela e faixa de anos (`2015-2021`, `2022-2024` e `2025-2026`). No bruto o arquivo é `dados_infosiga.zip`, com a data da coleta nas cópias de cada versão.
- O dicionário de dados oficial é publicado à parte (`Infosiga_dicionario_dados.zip`, três PDF, um por tabela) e é guardado no bruto, sem conversão.
- O ZIP é o mesmo para as três tabelas; cada dataset do lake converte os arquivos cujo nome traz a tabela (`sinistro`, `pessoa` ou `veiculo`).

## Conteúdo

- Uma linha por pessoa envolvida. Conferido no ZIP coletado, versão do fetcher 0.2.0: 1.956.089 linhas de 981.184 sinistros distintos, de 2014-12-21 a 2026-09-30. Por ano: 2015 7.589; 2016 7.027; 2017 6.591; 2018 6.426; 2019 245.107; 2020 230.557; 2021 260.886; 2022 266.128; 2023 279.963; 2024 273.875; 2025 211.908; 2026 160.019 (até 30/09); 2014 (21 a 31/12): 13.
- Gravidade (`gravidade_lesao`): `LEVE` 871.721; `ILESO` 771.006; `NAO DISPONIVEL` 146.808; `GRAVE` 101.325; `FATAL` 65.229.
- Sexo: `MASCULINO` 1.410.911; `FEMININO` 532.988; `NAO DISPONIVEL` 12.190.
- O dicionário oficial vigente é a versão 1.8, de 15/10/2026.

## Variáveis

As descrições vêm do Dicionário de dados oficial v1.8 (15/10/2026) da tabela `pessoas`. "Fonte do dado" no dicionário: `DETRAN-SP`, `PC, PM e PRF` (siglas do dicionário) ou `IBGE`, por variável. A coluna "Tipo" mostra o tipo que o dicionário declara; no lake todas as colunas são texto.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `id_sinistro` | `id_sinistro` | texto (fonte: int64) | Identificador do sinistro (chave estrangeira para `sinistros`); pode haver mais de uma pessoa por sinistro | 7 dígitos | todo |
| `id_pessoa` | `id_pessoa` | texto (fonte: int64) | Identificador da pessoa no sinistro, sequencial gerado para cada pessoa envolvida | 1 a 9999999 | todo |
| `id_veiculo` | `id_veiculo` | texto (fonte: int64) | Identificador do veículo (chave estrangeira para `veiculos`); pode ser nulo; pode haver mais de uma pessoa por veículo | 1 a 9999999 | todo |
| `cod_ibge` | `cod_ibge` | texto (fonte: int64) | Código do município no IBGE | 7 dígitos | todo |
| `municipio` | `municipio` | texto (fonte: string) | Município onde ocorreu o sinistro | 645 municípios do estado, em caixa alta e sem acento | todo |
| `regiao_administrativa` | `regiao_administrativa` | texto (fonte: string) | Região administrativa onde ocorreu o sinistro | 16 valores | todo |
| `tipo_via` | `tipo_via` | texto (fonte: string) | Tipo da via onde ocorreu o sinistro | `ESTRADAS E RODOVIAS`, `VIAS URBANAS`, `NAO DISPONIVEL` | todo |
| `tipo_veiculo_vitima` | `tipo_veiculo_vitima` | texto (fonte: string) | Veículo de locomoção da vítima; pode ser nulo | `AUTOMOVEL`, `BICICLETA`, `CAMINHAO`, `MOTOCICLETA`, `ONIBUS`, `OUTROS`, `NAO DISPONIVEL` | todo |
| `tipo_de_vitima` | `tipo_de_vitima` | texto (fonte: string) | Posição da vítima no sinistro | `CONDUTOR`, `PASSAGEIRO`, `PEDESTRE`, `NAO DISPONIVEL` | todo |
| `modo_transporte_vitima` | `modo_transporte_vitima` | texto (fonte: string) | Modo de transporte da vítima; criada para agrupar `tipo_de_vitima = PEDESTRE` aos demais modos vindos de `tipo_veiculo_vitima`; pode ser nulo | `PEDESTRE`, `BICICLETA`, `MOTOCICLETA`, `AUTOMOVEL`, `ONIBUS`, `CAMINHAO`, `OUTROS`, `NAO DISPONIVEL` | todo |
| `sexo` | `sexo` | texto (fonte: string) | Sexo da vítima | `FEMININO`, `MASCULINO`, `NAO DISPONIVEL` | todo |
| `idade` | `idade` | texto (fonte: int64) | Idade da vítima na data do sinistro; pode ser nula | anos, maior ou igual a 0 | todo |
| `gravidade_lesao` | `gravidade_lesao` | texto (fonte: string) | Gravidade da lesão classificada pelo agente que registrou a ocorrência; pode ser atualizada com boletins de ocorrência registrados depois | `FATAL`, `GRAVE`, `LEVE`, `ILESO`, `NAO DISPONIVEL` | todo |
| `faixa_etaria_demografica` | `faixa_etaria_demografica` | texto (fonte: string) | Classificação etária da vítima para análise populacional, nas classes do IBGE | `00 a 04`, `05 a 09`, ... `85 a 89`, `90 e +`, `NAO DISPONIVEL` | todo |
| `faixa_etaria_legal` | `faixa_etaria_legal` | texto (fonte: string) | Classificação etária pela legislação: 0-17 anos para menores, acima de 60 anos para idosos | `0-17`, `18-24`, ... `75-79`, `80 ou mais`, `NAO DISPONIVEL` | todo |
| `profissao` | `profissao` | texto (fonte: string) | Profissão da vítima; texto livre; pode ser nula | livre | todo |
| `grau_de_instrucao` | `grau_de_instrucao` | texto (fonte: string) | Grau de instrução da vítima; pode ser nulo | `BÁSICO`, `MÉDIO`, `SUPERIOR` | todo |
| `nacionalidade` | `nacionalidade` | texto (fonte: string) | Nacionalidade da vítima; texto livre; pode ser nula | livre | todo |
| `data_sinistro` | `data_sinistro` | texto (fonte: date) | Data do sinistro, `dd/mm/aaaa` (texto no lake) | a partir de 21/12/2014 | todo |
| `ano_sinistro` | `ano_sinistro` | texto (fonte: int64) | Ano do sinistro | a partir de 2014 | todo |
| `mes_sinistro` | `mes_sinistro` | texto (fonte: int64) | Mês do sinistro | 1 a 12 | todo |
| `dia_sinistro` | `dia_sinistro` | texto (fonte: int64) | Dia do sinistro | 1 a 31 | todo |
| `ano_mes_sinistro` | `ano_mes_sinistro` | texto (fonte: string) | Agrupamento de ano e mês do sinistro; o dicionário diz `mm/aaaa`, mas os arquivos trazem `aaaa/mm` | a partir de `2014/12` | todo |
| `data_obito` | `data_obito` | texto (fonte: date) | Data do óbito, se aplicável; `dd/mm/aaaa` (texto no lake); nula quando não há óbito registrado | a partir de 01/01/2015 | todo |
| `ano_obito` | `ano_obito` | texto (fonte: int64) | Ano do óbito, se aplicável | a partir de 2015 | todo |
| `mes_obito` | `mes_obito` | texto (fonte: int64) | Mês do óbito, se aplicável | 1 a 12 | todo |
| `dia_obito` | `dia_obito` | texto (fonte: int64) | Dia do óbito, se aplicável | 1 a 31 | todo |
| `ano_mes_obito` | `ano_mes_obito` | texto (fonte: string) | Agrupamento de ano e mês do óbito, se aplicável | a partir de 2015/01 | todo |
| `local_obito` | `local_obito` | texto (fonte: string) | Tipo de local onde ocorreu o óbito; pode ser nulo | `VIA`, `ESTABELECIMENTO SAUDE` (nos arquivos, `ESTABELECIMENTO DE SAUDE`), `OUTROS`, `NAO DISPONIVEL` | todo |
| `local_via` | `local_via` | texto (fonte: string) | Tipo de jurisdição onde ocorreu o óbito (o dicionário usa este nome com o título "Tipo de local"); pode ser nulo | `PUBLICO`, `PRIVADO`, `NAO DISPONIVEL` | todo |
| `tempo_sinistro_obito` | `tempo_sinistro_obito` | texto (fonte: int64) | Tempo em dias entre o sinistro e o óbito; pode ser nulo | dias, 0 a 30 | todo |
| `ano` | `data_sinistro` (ano) | inteiro | Ano do sinistro, extraído de `data_sinistro` (ou de `ano_sinistro`); é a partição do lake | — | todo |

## No lake

- Dataset `infosiga/pessoas`, particionado por `ano`; um Parquet por arquivo CSV de origem e ano.
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
- **Quem aparece.** Há uma linha por pessoa envolvida, inclusive ilesos (771.006 linhas `ILESO`) e `NAO DISPONIVEL` (146.808). Para vítimas fatais use `gravidade_lesao = FATAL` (65.229 linhas na conversão); todas elas têm `data_obito`, e só elas.
- **Identificadores.** `id_pessoa` é único em todo o ZIP coletado (1.956.089 linhas e valores distintos). `id_veiculo` é nulo em 384.389 linhas (pessoas sem veículo associado, por exemplo pedestres).
- **Campos pouco preenchidos.** `grau_de_instrucao` é nulo em 1.542.749 de 1.956.089 linhas; `modo_transporte_vitima` em 370.030; `profissao` em 196.082; `idade` em 17.881; as colunas de óbito (`data_obito`, `ano_obito`, `mes_obito`, `dia_obito`, `ano_mes_obito`, `local_obito`, `tempo_sinistro_obito`) em 1.890.860, o que equivale às pessoas sem óbito registrado.
- **Mês do óbito pode ser posterior ao do sinistro.** `data_obito` pode cair em outro mês ou ano que `data_sinistro` (até 30 dias, pelo dicionário); a partição `ano` é a do sinistro.
- **Idade.** Na conversão, `idade` varia de 0 a 102 anos.
- **Sinistros sem pessoas.** Só 981.184 dos 1.450.961 sinistros de `sinistros` têm pessoas nesta tabela; todo `id_sinistro` daqui consta em `sinistros` (conferido).

## Exemplos

Vítimas fatais por modo de transporte e faixa etária legal em 2024:

```python
import polars as pl

p = pl.scan_parquet("lake/infosiga/pessoas/**/*.parquet", hive_partitioning=True)
mortes = (
    p.filter((pl.col("ano") == 2024) & (pl.col("gravidade_lesao") == "FATAL"))
    .group_by("modo_transporte_vitima", "faixa_etaria_legal")
    .len()
    .sort("len", descending=True)
    .collect()
)
```

## Referências

- Painel Infosiga.SP (Detran-SP): https://infosiga.detran.sp.gov.br/
- Dicionários de dados oficiais (PDF, v1.8): https://infosiga.detran.sp.gov.br/painel/download/file/Infosiga_dicionario_dados.zip
- Período disponível no painel (JSON): https://infosiga.detran.sp.gov.br/painel/minMaxDates
