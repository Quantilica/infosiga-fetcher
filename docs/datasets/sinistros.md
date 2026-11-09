---
dataset:
  id: sinistros
  fonte: infosiga
  titulo: Sinistros de trânsito de São Paulo (Infosiga.SP)
  resumo: Registros de sinistros de trânsito no estado de São Paulo (fatais, não fatais e notificações), um por ocorrência, com local, data, tipo e quantidade de veículos e vítimas.
  orgao: Departamento Estadual de Trânsito de São Paulo (Detran-SP), Infosiga.SP
  pagina_oficial: https://infosiga.detran.sp.gov.br/
  licenca: "não informado pela fonte; o portal consultado não traz licença nem termo de uso legíveis (conferido em 2026-11-09)"
  periodicidade: "não informada pela fonte; em 2026-11-09 o painel indicava dados de 2015-01-01 a 2026-09-30 (endpoint minMaxDates) e o dicionário vigente é a versão 1.8 de 15/10/2026"
  cobertura: {inicio: 2014-12, fim: em-curso}
  unidade: um sinistro de trânsito (ocorrência)
  granularidade: {espacial: município (com latitude e longitude do local), temporal: dia}
  formato_bruto: "CSV dentro do ZIP dados_infosiga.zip, cp1252, separador ponto e vírgula, um arquivo por faixa de anos (sinistros_2015-2021, sinistros_2022-2024 e sinistros_2025-2026)"
  lake: {estado: convertido, particoes: [ano], chave: [id_sinistro], colunas: 50}
  dados_pessoais: nenhum
  eras:
    - {desde: 2019-01, mudanca: "Até 2018 os arquivos trazem só sinistros fatais; desde 2019-01 também constam sinistros não fatais e notificações (conferido nos arquivos)"}
  revisado_em: 2026-11-09
  versao_fetcher: 0.2.0
---

# Sinistros de trânsito de São Paulo (Infosiga.SP)

## Resumo

Um registro por sinistro de trânsito no estado de São Paulo, como o Infosiga.SP (sistema do Detran-SP) o publica: natureza do registro (fatal, não fatal ou notificação), data, hora, local (logradouro, município, coordenadas), características da via, tipo principal e subtipos do sinistro e contagens de veículos e de pessoas por gravidade. Serve para estudar a distribuição espacial e temporal dos sinistros e de suas vítimas.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `infosiga/sinistros` |
| Órgão | Departamento Estadual de Trânsito de São Paulo (Detran-SP), Infosiga.SP |
| Página oficial | https://infosiga.detran.sp.gov.br/ |
| Licença | não informado pela fonte; o portal consultado não traz licença nem termo de uso legíveis (conferido em 2026-11-09) |
| Periodicidade | não informada pela fonte; em 2026-11-09 o painel indicava dados de 2015-01-01 a 2026-09-30 (endpoint minMaxDates) e o dicionário vigente é a versão 1.8 de 15/10/2026 |
| Cobertura | 2014-12 a em-curso |
| Unidade (uma linha) | um sinistro de trânsito (ocorrência) |
| Granularidade | espacial: município (com latitude e longitude do local); temporal: dia |
| Formato bruto | CSV dentro do ZIP dados_infosiga.zip, cp1252, separador ponto e vírgula, um arquivo por faixa de anos (sinistros_2015-2021, sinistros_2022-2024 e sinistros_2025-2026) |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `id_sinistro` |
| Colunas | 50 |
| Unidades de medida | — |
| Dados pessoais | nenhum |
| Eras | 2019-01: Até 2018 os arquivos trazem só sinistros fatais; desde 2019-01 também constam sinistros não fatais e notificações (conferido nos arquivos) |
| Revisado em | 2026-11-09 |
| Versão do fetcher | 0.2.0 |

## Origem e coleta

- O fetcher baixa `https://infosiga.detran.sp.gov.br/painel/download/file/dados_infosiga.zip`, um único ZIP que traz as três tabelas (sinistros, pessoas e veículos) em nove CSV: um por tabela e faixa de anos (`2015-2021`, `2022-2024` e `2025-2026`). No bruto o arquivo é `dados_infosiga.zip`, com a data da coleta nas cópias de cada versão.
- O dicionário de dados oficial é publicado à parte (`Infosiga_dicionario_dados.zip`, três PDF, um por tabela) e é guardado no bruto, sem conversão.
- O ZIP é o mesmo para as três tabelas; cada dataset do lake converte os arquivos cujo nome traz a tabela (`sinistro`, `pessoa` ou `veiculo`).

## Conteúdo

- Uma linha por sinistro. Conferido no ZIP coletado, versão do fetcher 0.2.0: 1.450.961 sinistros, de 2014-12-21 a 2026-09-30, mais 11 linhas na partição `ano=2014` (21 a 31/12/2014). Por ano: 2015 5.951; 2016 5.314; 2017 5.071; 2018 4.870; 2019 174.589; 2020 157.889; 2021 181.876; 2022 192.157; 2023 208.034; 2024 198.688; 2025 190.239; 2026 126.272 (até 30/09).
- Por `tipo_registro` desde 2019: `SINISTRO NAO FATAL`, `NOTIFICACAO` e `SINISTRO FATAL` (por exemplo, em 2024: 129.747, 63.105 e 5.836). Entre 2015 e 2018 só há `SINISTRO FATAL`.
- A cobertura espacial é o estado de São Paulo: 645 municípios e 16 regiões administrativas na conversão.
- O dicionário oficial vigente é a versão 1.8, de 15/10/2026.

## Variáveis

As descrições vêm do Dicionário de dados oficial v1.8 (15/10/2026) da tabela `sinistros`. "Fonte do dado" no dicionário: `DETRAN-SP`, `PC, PM e PRF` (siglas do dicionário) ou `IBGE`, por variável. A coluna "Tipo" mostra o tipo que o dicionário declara; no lake todas as colunas são texto.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `id_sinistro` | `id_sinistro` | texto (fonte: int64) | Identificador único do sinistro (chave primária) | número sequencial de 7 dígitos gerado pelo Infosiga | todo |
| `tipo_registro` | `tipo_registro` | texto (fonte: string) | Classificação do registro de ocorrência conforme a natureza | `SINISTRO FATAL` (pelo menos um óbito em até 30 dias), `SINISTRO NAO FATAL` (pelo menos uma vítima ferida e nenhum óbito em até 30 dias), `NOTIFICACAO` (registro na central sem boletim de ocorrência formal) | todo |
| `data_sinistro` | `data_sinistro` | texto (fonte: date) | Data em que ocorreu o sinistro, no formato `dd/mm/aaaa` (texto no lake) | a partir de 21/12/2014 | todo |
| `ano_sinistro` | `ano_sinistro` | texto (fonte: int64) | Ano do sinistro | a partir de 2014 | todo |
| `mes_sinistro` | `mes_sinistro` | texto (fonte: int64) | Mês do sinistro | 1 a 12 | todo |
| `dia_sinistro` | `dia_sinistro` | texto (fonte: int64) | Dia do sinistro | 1 a 31 | todo |
| `hora_sinistro` | `hora_sinistro` | texto (fonte: time) | Hora do sinistro, `HH:MM`; pode ser nula | 00:00 a 23:59 | todo |
| `ano_mes_sinistro` | `ano_mes_sinistro` | texto (fonte: string) | Agrupamento de ano e mês; nos arquivos aparece como `aaaa/mm` | a partir de `2014/12` | todo |
| `dia_da_semana` | `dia_da_semana` | texto (fonte: string) | Dia da semana do sinistro | `Domingo`, `Segunda-feira`, `Terça-feira`, `Quarta-feira`, `Quinta-feira`, `Sexta-feira`, `Sábado` | todo |
| `turno` | `turno` | texto (fonte: string) | Turno do dia | `MADRUGADA` (00:00 a 05:59), `MANHA` (06:00 a 11:59), `TARDE` (12:00 a 17:59), `NOITE` (18:00 a 23:59), `NAO DISPONIVEL` | todo |
| `logradouro` | `logradouro` | texto (fonte: string) | Logradouro onde ocorreu o sinistro; texto livre, pode ser nulo | livre | todo |
| `numero_logradouro` | `numero_logradouro` | texto (fonte: float64) | Numeral da via onde ocorreu o sinistro; o formato varia conforme o tipo de via e o órgão de origem; pode ser nulo | livre | todo |
| `tipo_via` | `tipo_via` | texto (fonte: string) | Tipo da via onde ocorreu o sinistro | `ESTRADAS E RODOVIAS`, `VIAS URBANAS`, `NAO DISPONIVEL` | todo |
| `tipo_local` | `tipo_local` | texto (fonte: string) | Tipo de local onde ocorreu o sinistro; pode ser nulo | `PUBLICO`, `PRIVADO`, `NAO DISPONIVEL` | todo |
| `latitude` | `latitude` | texto (fonte: float64) | Latitude (y) do local, em WGS84 (EPSG:4326); pode ser nula | graus decimais; no arquivo, com vírgula decimal | todo |
| `longitude` | `longitude` | texto (fonte: float64) | Longitude (x) do local, em WGS84 (EPSG:4326); pode ser nula | graus decimais; no arquivo, com vírgula decimal | todo |
| `cod_ibge` | `cod_ibge` | texto (fonte: int64) | Código do município no IBGE | 7 dígitos | todo |
| `municipio` | `municipio` | texto (fonte: string) | Município onde ocorreu o sinistro | 645 municípios do estado, em caixa alta e sem acento | todo |
| `regiao_administrativa` | `regiao_administrativa` | texto (fonte: string) | Região administrativa onde ocorreu o sinistro, conforme a divisão territorial da legislação estadual | 16 valores (ex.: `METROPOLITANA DE SÃO PAULO`, `CAMPINAS`, `SOROCABA`) | todo |
| `administracao` | `administracao` | texto (fonte: string) | Órgão responsável pela administração da via; em rodovias vem da base viária do DER por comparação do logradouro com o código da rodovia; em vias municipais é a prefeitura; pode ser nulo | `PREFEITURA`, `CONCESSIONÁRIA`, `DER`, `ARTESP`, `DNIT`, `NAO DISPONIVEL` | todo |
| `conservacao` | `conservacao` | texto (fonte: string) | Órgão responsável pela conservação da via, com a mesma regra de `administracao`; pode ser nulo | ex.: `Regional DER (Rodovia Estadual)`, `DNIT (Rodovia Federal)`, `Prefeitura (Municipal)`, `NAO DISPONIVEL` | todo |
| `circunscricao` | `circunscricao` | texto (fonte: string) | Órgão que possui a circunscrição da via, com a mesma regra de `administracao`; em vias municipais é municipal; pode ser nulo | `MUNICIPAL`, `ESTADUAL`, `FEDERAL`, `NAO DISPONIVEL` | todo |
| `tp_sinistro_primario` | `tp_sinistro_primario` | texto (fonte: string) | Classificação principal do tipo de sinistro, pela priorização (1 a 14) dos tipos: ATROPELAMENTO (1 pedestre, 2 vítima fora do veículo), COLISAO (3 frontal, 4 traseira, 5 lateral, 6 transversal, 7 outros), CHOQUE (8), OUTROS (9 capotamento, 10 engavetamento, 11 tombamento, 12 atropelamento de animal, 13 outros) e NAO DISPONIVEL (14) | `ATROPELAMENTO`, `COLISAO`, `CHOQUE`, `OUTROS`, `NAO DISPONIVEL` | todo |
| `qtd_pedestre` | `qtd_pedestre` | texto (fonte: int64) | Quantidade de pedestres envolvidos no sinistro; nula quando não há | inteiros maiores ou iguais a 0 | todo |
| `qtd_bicicleta` | `qtd_bicicleta` | texto (fonte: int64) | Quantidade de bicicletas envolvidas | inteiros maiores ou iguais a 0 | todo |
| `qtd_motocicleta` | `qtd_motocicleta` | texto (fonte: int64) | Quantidade de motocicletas envolvidas | inteiros maiores ou iguais a 0 | todo |
| `qtd_automovel` | `qtd_automovel` | texto (fonte: int64) | Quantidade de automóveis envolvidos | inteiros maiores ou iguais a 0 | todo |
| `qtd_onibus` | `qtd_onibus` | texto (fonte: int64) | Quantidade de ônibus envolvidos | inteiros maiores ou iguais a 0 | todo |
| `qtd_caminhao` | `qtd_caminhao` | texto (fonte: int64) | Quantidade de caminhões envolvidos | inteiros maiores ou iguais a 0 | todo |
| `qtd_veic_outros` | `qtd_veic_outros` | texto (fonte: int64) | Quantidade de veículos de outros tipos não especificados envolvidos | inteiros maiores ou iguais a 0 | todo |
| `qtd_veic_nao_disponivel` | `qtd_veic_nao_disponivel` | texto (fonte: int64) | Quantidade de veículos não classificados ou com tipo não informado | inteiros maiores ou iguais a 0 | todo |
| `qtd_gravidade_fatal` | `qtd_gravidade_fatal` | texto (fonte: int64) | Pessoas envolvidas com lesão fatal (morte no local ou até 30 dias após a ocorrência; o campo é atualizado com o boletim de ocorrência da Polícia Civil quando a vítima falece depois) | inteiros maiores ou iguais a 0 | todo |
| `qtd_gravidade_grave` | `qtd_gravidade_grave` | texto (fonte: int64) | Pessoas envolvidas com lesão classificada como grave | inteiros maiores ou iguais a 0 | todo |
| `qtd_gravidade_leve` | `qtd_gravidade_leve` | texto (fonte: int64) | Pessoas envolvidas com lesão classificada como leve | inteiros maiores ou iguais a 0 | todo |
| `qtd_gravidade_ileso` | `qtd_gravidade_ileso` | texto (fonte: int64) | Pessoas ilesas; passam a ser considerados condutores não lesionados envolvidos em sinistros fatais e não fatais | inteiros maiores ou iguais a 0 | todo |
| `qtd_gravidade_nao_disponivel` | `qtd_gravidade_nao_disponivel` | texto (fonte: int64) | Pessoas com tipo de lesão não informado | inteiros maiores ou iguais a 0 | todo |
| `tp_sinistro_atrop_pedestre` | `tp_sinistro_atrop_pedestre` | texto (fonte: string) | Indica se ocorreu atropelamento de pedestre (`S` = sim, nulo = não). Substitui `tp_sinistro_atropelamento` quando a pessoa atropelada é pedestre; pode estar ligado a uma vítima pedestre e a uma vítima ocupante do veículo que atropelou | `S` ou nulo | todo |
| `tp_sinistro_atrop_vitima_fora_veic` | `tp_sinistro_atrop_vitima_fora_veic` | texto (fonte: string) | Indica se ocorreu atropelamento de vítima fora do veículo (`S` = sim, nulo = não). Substitui `tp_sinistro_atropelamento` quando a pessoa atropelada é ocupante de veículo que estava fora dele quando foi atropelada | `S` ou nulo | todo |
| `tp_sinistro_colisao_frontal` | `tp_sinistro_colisao_frontal` | texto (fonte: string) | Indica se ocorreu colisão frontal (`S` = sim, nulo = não) | `S` ou nulo | todo |
| `tp_sinistro_colisao_traseira` | `tp_sinistro_colisao_traseira` | texto (fonte: string) | Indica se ocorreu colisão traseira (`S` = sim, nulo = não) | `S` ou nulo | todo |
| `tp_sinistro_colisao_lateral` | `tp_sinistro_colisao_lateral` | texto (fonte: string) | Indica se ocorreu colisão lateral (`S` = sim, nulo = não) | `S` ou nulo | todo |
| `tp_sinistro_colisao_transversal` | `tp_sinistro_colisao_transversal` | texto (fonte: string) | Indica se ocorreu colisão transversal (`S` = sim, nulo = não) | `S` ou nulo | todo |
| `tp_sinistro_colisao_outros` | `tp_sinistro_colisao_outros` | texto (fonte: string) | Indica se ocorreu outro tipo de colisão (`S` = sim, nulo = não) | `S` ou nulo | todo |
| `tp_sinistro_choque` | `tp_sinistro_choque` | texto (fonte: string) | Indica se ocorreu choque (`S` = sim, nulo = não) | `S` ou nulo | todo |
| `tp_sinistro_atrop_animal` | `tp_sinistro_atrop_animal` | texto (fonte: string) | Indica se ocorreu atropelamento de animal (`S` = sim, nulo = não). Criada para os casos em que a vítima é ocupante de veículo; por ter dinâmica distinta dos demais atropelamentos, entra no agrupamento `OUTROS` | `S` ou nulo | todo |
| `tp_sinistro_capotamento` | `tp_sinistro_capotamento` | texto (fonte: string) | Indica se ocorreu capotamento (`S` = sim, nulo = não) | `S` ou nulo | todo |
| `tp_sinistro_engavetamento` | `tp_sinistro_engavetamento` | texto (fonte: string) | Indica se ocorreu engavetamento (`S` = sim, nulo = não) | `S` ou nulo | todo |
| `tp_sinistro_tombamento` | `tp_sinistro_tombamento` | texto (fonte: string) | Indica se ocorreu tombamento (`S` = sim, nulo = não) | `S` ou nulo | todo |
| `tp_sinistro_outros` | `tp_sinistro_outros` | texto (fonte: string) | Indica se ocorreu outro tipo de sinistro (`S` = sim, nulo = não) | `S` ou nulo | todo |
| `tp_sinistro_nao_disponivel` | `tp_sinistro_nao_disponivel` | texto (fonte: string) | Indica que a classificação do tipo de sinistro não está disponível (`S` = sim, nulo = não) | `S` ou nulo | todo |
| `ano` | `data_sinistro` (ano) | inteiro | Ano do sinistro, extraído de `data_sinistro` (ou de `ano_sinistro`); é a partição do lake | — | todo |

## No lake

- Dataset `infosiga/sinistros`, particionado por `ano`; um Parquet por arquivo CSV de origem e ano.
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
- **Quantidades e sinalizadores nulos.** As colunas `qtd_*` e `tp_sinistro_*` (exceto `tp_sinistro_primario`) só vêm preenchidas quando a contagem é maior que zero ou o tipo ocorre (`S`). Na conversão nenhuma linha traz o texto `0` nas colunas `qtd_*` conferidas (`qtd_pedestre`, `qtd_gravidade_fatal`, `qtd_automovel`, `qtd_gravidade_ileso`), e as 61.251 linhas `SINISTRO FATAL` têm todas `qtd_gravidade_fatal` preenchida; por isso nulo equivale a zero, uma leitura inferida desses fatos (o dicionário só diz que o campo pode ser nulo). Substitua nulo por 0 antes de somar. `qtd_gravidade_fatal` é nula em 1.389.710 de 1.450.961 linhas.
- **Identificador.** `id_sinistro` é único no ZIP coletado (1.450.961 linhas e 1.450.961 valores distintos).
- **Coordenadas.** `latitude` é nula em 124.547 linhas; das 1.326.414 com valor, 168 ficam fora de um retângulo aproximado em torno do estado (latitude de −25,4 a −19,7, longitude de −53,2 a −44,1), com mínimos de −87,5 (latitude) e máximo 0,0 (longitude), e 136 têm latitude 0. A fonte não declara essas coordenadas como inválidas; confira antes de mapear.
- **Número do logradouro.** O dicionário o declara como número decimal; na amostra, 97,7% dos valores preenchidos terminam em `.0` (por exemplo, `1000.0`). Remova o `.0` ao juntar com outras bases.
- **Pessoas e veículos.** Nem todo sinistro tem linhas em `pessoas` (981.184 dos 1.450.961 têm) nem em `veiculos` (969.834 têm); quem soma pessoas ou veículos deve partir das tabelas respectivas ou das colunas `qtd_*`.

## Exemplos

Sinistros fatais por região administrativa em 2024 (`ano` é a partição e `qtd_gravidade_fatal` é texto, nulo quando não há óbito):

```python
import polars as pl

s = pl.scan_parquet("lake/infosiga/sinistros/**/*.parquet", hive_partitioning=True)
fatais = (
    s.filter((pl.col("ano") == 2024) & (pl.col("tipo_registro") == "SINISTRO FATAL"))
    .group_by("regiao_administrativa")
    .agg(
        pl.len().alias("sinistros_fatais"),
        pl.col("qtd_gravidade_fatal").cast(pl.Int64).fill_null(0).sum().alias("obitos"),
    )
    .sort("sinistros_fatais", descending=True)
    .collect()
)
```

## Referências

- Painel Infosiga.SP (Detran-SP): https://infosiga.detran.sp.gov.br/
- Dicionários de dados oficiais (PDF, v1.8): https://infosiga.detran.sp.gov.br/painel/download/file/Infosiga_dicionario_dados.zip
- Período disponível no painel (JSON): https://infosiga.detran.sp.gov.br/painel/minMaxDates
